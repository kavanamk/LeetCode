from collections import defaultdict
from collections import Counter
import heapq

class TrieNode:
    def __init__(self):
        self.children={}
        self.isWord=False
        
class SearchAutocomplete:
    def __init__(self):
        self.queryCounter=Counter()
        self.root=TrieNode()

    # ─── LEVEL 1 ─────────────────────────────────────────────────────────────
    def add_query(self, query: str) -> None:
        """
        Input:   query (str) — a search query, lowercase, no spaces
        Output:  None
        Does:    Records that this query was searched once.
                 Calling multiple times increments its search count.
        """
        self.queryCounter[query]+=1
        node = self.root
        for letter in word:
            if letter not in node.children:
                node.children[letter]=TrieNode
            node=node.children.get(letter)
        node.isWord=True


    def get_count(self, query: str) -> int:
        """
        Input:   query (str)
        Output:  int — number of times query has been searched. 0 if never.
        Does:    Returns the total search count for an exact query.
        """
        return self.queryCounter[query]

    # ─── LEVEL 2 ─────────────────────────────────────────────────────────────
    def search(self, prefix: str) -> list:
        """
        Input:   prefix (str) — a string prefix
        Output:  List[str] — all queries that start with prefix,
                 sorted alphabetically. Returns [] if none found.
        Does:    Returns every stored query that begins with the given prefix.
        """
        res=[]
        def findPrefixNode(prefix):
            node=self.root
            for letter in prefix:
                if letter not in node.children:
                    return None
                node=node.children.get(letter)
            return node
        
        def findSuffix(node,curWord):
            if node.isWord:
                res.append(curWord)
            for letter, child in node.children.items():
                findSuffix(child,curWord+letter)
        
        startNode= findPrefixNode(prefix)
        if not startNode:
            return []
        findSuffix(startNode,prefix)
        return sorted(res)


        

    # ─── LEVEL 3 ─────────────────────────────────────────────────────────────
    def top_k_search(self, prefix: str, k: int) -> list:
        """
        Inputs:  prefix (str), k (int)
        Output:  List[str] — top k queries starting with prefix,
                 sorted descending by search count.
                 Ties broken alphabetically (ascending).
                 Returns fewer than k if not enough matches exist.
        Does:    Returns the k most frequently searched queries
                 that begin with the given prefix.
        """
        res=[]
        heap=[]
        startsWithPrefixList=self.search(prefix)
        for query in startsWithPrefixList:
            queryCount= self.queryCounter[query]
            heapq.heappush(heap,(-queryCount,query) )
        
        for _ in range(k):
            queryCount,query = heapq.heappop(heap)
            res.append(query)

        return res

    # ─── LEVEL 4 ─────────────────────────────────────────────────────────────
    def fuzzy_search(self, prefix: str, k: int, max_typos: int) -> list:
        """
        Inputs:  prefix (str), k (int), max_typos (int)
        Output:  List[str] — top k queries whose prefix (same length as input)
                 is within max_typos character substitutions of the input prefix,
                 sorted descending by search count. Ties broken alphabetically.
        Does:    Tolerates typos in the prefix — a query matches if you can
                 transform the input prefix into the query's first len(prefix)
                 characters by changing at most max_typos letters.
        Example: prefix="serch", max_typos=1 matches "search..." (1 substitution)
        """
        pass
