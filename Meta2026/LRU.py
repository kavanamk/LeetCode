class DLLNode:
    def __init__(self, key, val):
        self.key = key
        self.val = val
        self.prev = None
        self.next = None

class LRUCache:

    # ─── LEVEL 1 ─────────────────────────────────────────────────────────────
   
    def __init__(self, capacity: int):
        """
        Input:   capacity (int) — max number of key-value pairs the cache holds
        Does:    Initializes the cache with a fixed capacity.
        """
        self.capacity=capacity
        self.cacleDLL = None

    def get(self, key: int) -> int:
        """
        Input:   key (int)
        Output:  int — the value associated with key, or -1 if key not in cache.
        Does:    Retrieves a value from the cache.
                 Marks key as most recently used.
        """
        pass

    def put(self, key: int, value: int) -> None:
        """
        Inputs:  key (int), value (int)
        Output:  None
        Does:    Inserts or updates key with value.
                 Marks key as most recently used.
                 If cache is at capacity and key is new, evicts the
                 least recently used key before inserting.
        """
        node=DLLNode()

    # ─── LEVEL 2 ─────────────────────────────────────────────────────────────
    def get_lru_key(self) -> int:
        """
        Input:   None
        Output:  int — the key that would be evicted next (least recently used).
                 Returns -1 if cache is empty.
        Does:    Returns the least recently used key without evicting it.
        """
        pass

    def get_mru_key(self) -> int:
        """
        Input:   None
        Output:  int — the most recently used key.
                 Returns -1 if cache is empty.
        Does:    Returns the most recently used key without modifying the cache.
        """
        pass

    # ─── LEVEL 3 ─────────────────────────────────────────────────────────────
    def get_top_k(self, k: int) -> list:
        """
        Input:   k (int)
        Output:  List[int] — the k most recently used keys, ordered from
                 most recent to least recent.
        Does:    Returns the k keys that were accessed or inserted most
                 recently. Returns fewer than k if cache has fewer entries.
        """
        pass
