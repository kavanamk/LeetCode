# LRU Cache — Doubly Linked List + HashMap
# lru -> a b c d <- mru
# IDEA:
#   - HashMap: key → node (O(1) lookup)
#   - DLL: tracks order (MRU at tail, LRU at head)
#   - On get/put → move node to tail (most recently used)
#   - On eviction → remove from head (least recently used)
#
#  [head] ↔ [LRU] ↔ ... ↔ [MRU] ↔ [tail]
#    (dummy)                         (dummy)

class Node:
    def __init__(self, key, val):
        self.key = key
        self.val = val
        self.prev = None
        self.next = None

class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {}          # key → node

        # dummy head and tail — avoids edge cases on insert/delete
        self.head = Node(0, 0)  # LRU end
        self.tail = Node(0, 0)  # MRU end
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node: Node) -> None:
        # TODO 1: unlink node from DLL
        # node.prev ↔ node ↔ node.next  →  node.prev ↔ node.next
        prev=node.prev
        nxt=node.next
        prev.next=nxt
        nxt.prev=prev
        del self.cache[node.key]

    def _insert_tail(self, node: Node) -> None:
        # TODO 2: insert node right before tail (mark as MRU)
        # ... ↔ tail.prev ↔ tail  →  ... ↔ tail.prev ↔ node ↔ tail
        prev=self.tail.prev
        prev.next=node
        node.prev=prev
        self.tail.prev=node
        node.next=self.tail

    def get(self, key: int) -> int:
        # TODO 3: if key exists:
        #   - move its node to tail (it was just used)
        #   - return val
        # else return -1
        if key not in self.cache:
            return -1
        node = self.cache[key]      # O(1) lookup
        self._remove(node)
        self._insert_tail(node)
        return node.val



    def put(self, key: int, value: int) -> None:
        # TODO 4: if key exists → update val, move to tail
        # TODO 5: if new key:
        #   - create node, add to cache + insert at tail
        #   - if over capacity → evict head.next (LRU)
        #     remember to remove from cache dict too!
        
        if key in self.cache:                          # key exists → update
            self.cache[key].val = value
            self._remove(self.cache[key])
            self._insert_tail(self.cache[key])
        else:
            if len(self.cache) >= self.capacity:       # evict LRU
                lru = self.head.next
                self._remove(lru)
                del self.cache[lru.key]
            node = Node(key, value)                    # insert new
            self.cache[key] = node
            self._insert_tail(node)

        

