from typing import Optional, List
import bisect

class CloudFileStorage:
    def __init__(self):
        self.fileStore={}  # { file_path: content } for L1, { file_path: {"content":..., "expires_at":...} } for L2

    # ─── LEVEL 1: Basic File Operations ──────────────────────────────────────
    def upload(self, file_path: str, content: str) -> bool:
        """
        Inputs:  file_path (str) — full path of the file e.g. "/dir/file.txt"
                 content   (str) — the file's text content
        Output:  bool — True if file was newly created,
                        False if file already existed and was overwritten.
        Does:    Stores the file at the given path with the given content.
                 If file already exists, overwrites it.
        """
        if file_path not in self.fileStore:
            self.fileStore[file_path]=content
            return True
        else:
            self.fileStore[file_path]=content
            return False

    def get(self, file_path: str) -> Optional[str]:
        """
        Input:   file_path (str) — full path of the file
        Output:  str — content of the file, or None if file doesn't exist.
        Does:    Retrieves the content of a file at the given path.
        """
        if file_path in self.fileStore:
             return self.fileStore[file_path] 
        else:
            return None

    def delete(self, file_path: str) -> bool:
        """
        Input:   file_path (str) — full path of the file
        Output:  bool — True if file existed and was deleted, False otherwise.
        Does:    Removes the file at the given path from storage.
        """
        if file_path in self.fileStore:
            del self.fileStore[file_path]
            return True
        return False

    def list_files(self, directory: str) -> List[str]:
        """
        Input:   directory (str) — a directory prefix e.g. "/dir/"
        Output:  List[str] — sorted list of all file paths that live directly
                 under this directory. Returns [] if none exist.
        Does:    Lists all files in a given directory (non-recursive).
        Example: files at "/a/b.txt", "/a/c.txt", "/a/sub/d.txt"
                 list_files("/a/") -> ["/a/b.txt", "/a/c.txt"]  (not /a/sub/)
        """
        list_files=[]
        for file_path in self.fileStore.keys():
            if file_path.startswith(directory):
                if '/' not in file_path[len(directory):]:
                    list_files.append(file_path)
        return sorted(list_files)


    # ─── LEVEL 2: TTL / Auto-Expiry ──────────────────────────────────────────
    def upload_with_ttl(self, file_path: str, content: str,
                        ttl: int, current_time: int) -> bool:
        """
        Inputs:  file_path    (str) — full path of the file
                 content      (str) — the file's text content
                 ttl          (int) — seconds until file expires
                 current_time (int) — current timestamp in seconds
        Output:  bool — True if newly created, False if overwritten.
        Does:    Same as upload but file auto-expires after `ttl` seconds.
                 After expiry, get/list treat it as if it doesn't exist.
        """
        existed = file_path in self.fileStore
        self.fileStore[file_path] = {"content": content, "expires_at": current_time + ttl}
        return not existed

    def get_active(self, file_path: str, current_time: int) -> Optional[str]:
        """
        Inputs:  file_path    (str)
                 current_time (int) — current timestamp in seconds
        Output:  str — content if file exists AND has not expired, else None.
        Does:    Retrieves file only if it is still alive at current_time.
        """
        if file_path not in self.fileStore:
            return None
        if current_time >= self.fileStore[file_path]["expires_at"]:  # expired
            return None
        return self.fileStore[file_path]["content"]
        

    # ─── LEVEL 3: File Versioning / Point-in-time ────────────────────────────
    def upload_versioned(self, file_path: str, content: str,
                         timestamp: int) -> int:
        """
        Inputs:  file_path (str) — full path of the file
                 content   (str) — the file's text content
                 timestamp (int) — time this upload occurred
        Output:  int — the version number assigned to this upload (1-indexed,
                 increments per file independently).
        Does:    Stores a new version of the file tagged with timestamp.
                 Older versions are preserved and queryable.
        """
        if file_path not in self.fileStore:
            self.fileStore[file_path] = []                              # init empty list for this file
        self.fileStore[file_path].append({"content": content, "timestamp": timestamp})
        return len(self.fileStore[file_path])                           # version = length (1-indexed)
            
    def get_version(self, file_path: str, version: int) -> Optional[str]:
        """
        Inputs:  file_path (str)
                 version   (int) — 1-indexed version number
        Output:  str — content of that specific version, or None if version
                 doesn't exist.
        Does:    Retrieves a specific historical version of a file.
        """
        if file_path not in self.fileStore:
            return None
        if version < 1 or version > len(self.fileStore[file_path]):
            return None
        return self.fileStore[file_path][version - 1]["content"]

    def get_at_time(self, file_path: str, timestamp: int) -> Optional[str]:
        """
        Inputs:  file_path (str)
                 timestamp (int) — point-in-time to query
        Output:  str — content of the latest version whose upload timestamp
                 is <= the given timestamp. None if no such version exists.
        Does:    Point-in-time read — reconstructs what the file looked like
                 at a specific moment.
        Example: upload_versioned("/f.txt","v1",10), ("f.txt","v2",20)
                 get_at_time("/f.txt", 15) -> "v1"
                 get_at_time("/f.txt", 25) -> "v2"
        """
        if file_path not in self.fileStore:
            return None
        timestamps = [v["timestamp"] for v in self.fileStore[file_path]]
        idx = bisect.bisect_right(timestamps, timestamp) - 1  # latest version <= timestamp
        if idx < 0:
            return None
        return self.fileStore[file_path][idx]["content"]

    # ─── LEVEL 4: Deletion + Rollback ────────────────────────────────────────
    def delete_versioned(self, file_path: str, timestamp: int) -> bool:
        """
        Inputs:  file_path (str)
                 timestamp (int) — time this deletion occurred
        Output:  bool — True if file existed at that timestamp, False otherwise.
        Does:    Inserts a tombstone at `timestamp`. Queries at or after this
                 timestamp return None. Queries before it still work.
                 File can be re-uploaded after deletion with a later timestamp.
        """
        pass

    def rollback(self, file_path: str, timestamp: int) -> bool:
        """
        Inputs:  file_path (str)
                 timestamp (int) — point-in-time to roll back to
        Output:  bool — True if rollback succeeded, False if no version existed
                 at that timestamp.
        Does:    Restores the file to whatever state it was in at `timestamp`.
                 Creates a new version with current time = latest + 1.
                 Effectively undoes all changes after `timestamp`.
        """
        pass

    def list_versions(self, file_path: str) -> List[tuple]:
        """
        Input:   file_path (str)
        Output:  List of (version, timestamp, content_or_"DELETED") tuples
                 sorted ascending by version number. Returns [] if file
                 never existed.
        Does:    Returns the full audit history of a file including deletions,
                 for compliance/debugging purposes.
        """
        pass
