
from collections import defaultdict

class FriendRecommender:
    def __init__(self):
        self.friendGraph=defaultdict(set)

    # ─── LEVEL 1 ─────────────────────────────────────────────────────────────
    def add_friendship(self, user_a: int, user_b: int) -> None:
        """
        Inputs:  user_a, user_b (int) — two user IDs
        Output:  None
        Does:    Records a bidirectional friendship between user_a and user_b.
                 Calling this twice with the same pair has no effect.
        """
        self.friendGraph[user_a].add(user_b)
        self.friendGraph[user_b].add(user_a)


    def mutual_friends(self, user_a: int, user_b: int) -> list:
        """
        Inputs:  user_a, user_b (int) — two user IDs
        Output:  List[int] — sorted list of user IDs who are friends with BOTH
                 user_a and user_b. Returns [] if either user doesn't exist.
        Does:    Finds the common friends between two users.
        
        """
        if user_a not in self.friendGraph or user_b not in self.friendGraph:
            return []
        return list(self.friendGraph[user_a].intersection(self.friendGraph[user_b]))
    

    # ─── LEVEL 2 ─────────────────────────────────────────────────────────────
    def top_k_recommendations(self, user_id: int, k: int) -> list:
        """
        Inputs:  user_id (int) — the user to generate recommendations for
                 k       (int) — number of recommendations to return
        Output:  List[int] — up to k user IDs who are NOT already friends with
                 user_id, sorted descending by number of mutual friends with
                 user_id. Ties broken by ascending user ID.
                 Excludes user_id themselves.
        Does:    Recommends strangers who share the most mutual friends —
                 classic "People You May Know".
        """
        heap=[]
        #list of strangers
        # calculate mutual friends -> (friend_count, user_id)
        #store it in heap and
        strangerList=list(set([x for x in self.friendGraph.keys()]).difference(set(self.friendGraph[user_id]))) - {user_id}

        for stanger_id in strangerList:
            numOfMutuals= len(self.mutual_friends(user_id,stanger_id))
            heapq.heappush(heap,(-numOfMutuals,stanger_id))
        
        # return top k elements
        reccommendations=[]
        for _ in range(k):
            numOfmutuals, rec_id =heapq.heappop(heap)
            reccommendations.append(rec_id)
        
        return reccommendations

    # ─── LEVEL 3 ─────────────────────────────────────────────────────────────
    def friends_within_degrees(self, user_id: int, n: int) -> list:
        """
        Inputs:  user_id (int) — the starting user
                 n       (int) — max degrees of separation
        Output:  List[int] — sorted list of all user IDs reachable from
                 user_id within n hops. Excludes user_id themselves.
        Does:    1st degree = direct friends, 2nd degree = friends of friends,
                 etc. Uses BFS to explore the social graph up to depth n.
                 Each user appears at most once (shortest path degree).
        Example: n=1 → same as direct friends
                 n=2 → friends + friends-of-friends (not already friends)
        """
        res=[]
        def bfs(user_id,n):
            visited=set([user_id])
            q=deque([user_id])
            level=0
            while q and level<n:
                size=len(q)
                for _ in range(len(q)):
                    node=q.popleft()
                    
                    for neighbor in self.friendGraph[node]:
                        if neighbor not in visited:
                            q.append(neighbor)
                            visited.add(node)
                level+=1
        return sorted(bfs(user_id, n) - {user_id})
                        



    # ─── LEVEL 4 ─────────────────────────────────────────────────────────────
    def shortest_path(self, user_a: int, user_b: int) -> list:
        """
        Inputs:  user_a, user_b (int) — two user IDs
        Output:  List[int] — the shortest chain of user IDs connecting
                 user_a to user_b, inclusive of both endpoints.
                 Returns [] if no path exists or either user doesn't exist.
        Does:    Finds the shortest friendship path between two users (BFS).
                 If multiple paths of equal length exist, any valid one is fine.
        Example: user_a=1, user_b=4, path: 1→2→3→4
                 returns [1, 2, 3, 4]
        """
        if user_a not in self.friendGraph or user_b not in self.friendGraph:
            return []

        def bfs(user_a, user_b):
            # parent replaces visited — if node is in parent, it's been seen
            # user_a has no parent (it's the start)
            parent = {user_a: None}
            q = deque([user_a])
            while q:
                for _ in range(len(q)):
                    node = q.popleft()
                    if node == user_b:
                        # reached target — reconstruct path by walking parent back
                        path = []
                        curr = user_b
                        while curr is not None:
                            path.append(curr)
                            curr = parent[curr]
                        return path[::-1]  # reverse to get user_a → user_b
                    for neigh in self.friendGraph[node]:
                        if neigh not in parent:
                            parent[neigh] = node  # came from node
                            q.append(neigh)
            return []  # no path found

        return bfs(user_a, user_b)
                        
        
