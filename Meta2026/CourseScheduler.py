from collections import defaultdict

class CourseScheduler:
    def __init__(self):
        self.parent={}
        self.courseGraph=defaultdict(list)

    # ─── LEVEL 1 ─────────────────────────────────────────────────────────────
    def add_course(self, course: int) -> None:
        """
        Input:   course (int) — a course ID
        Output:  None
        Does:    Registers a course in the system.
                 Adding the same course twice has no effect.
        """
        self.parent[course]=course
        self.courseGraph[course]=[]

    def find(self,x):
        if self.parent[x]==x:
            return x
        self.find(parent[x])
    
    def union(self,x,y):
        xRoot=self.find(x)
        yRoot = self.find(y)
        #cycle
        if xRoot==yRoot:
            return True
        self.parent[xRoot]=yRoot

    def add_prerequisite(self, course: int, prereq: int) -> None:
        """
        Inputs:  course (int) — the course you want to take
                 prereq (int) — must be completed before `course`
        Output:  None
        Does:    Records that `prereq` must be taken before `course`.
                 Both courses are added to the system if not already present.
        """
        self.courseGraph[course].append(prereq)
        self.union(course,prereq)
        

    # ─── LEVEL 2 ─────────────────────────────────────────────────────────────
    def can_finish(self) -> bool:
        """
        Input:   None
        Output:  bool — True if all courses can be completed, False otherwise.
        Does:    Determines whether it is possible to finish all registered
                 courses given their prerequisites.
                 Returns False if there is a circular dependency
                 (e.g. A requires B and B requires A).
        """
        visited = set()    # fully processed — safe, no cycle through here
        visiting = set()   # on current DFS path — cycle if we see this again
        def dfs(node):
            for neigh in self.courseGraph[node]:
                if neigh in visiting:          # back edge = cycle
                    return False
                if neigh not in visited:       # unvisited — explore it
                    visiting.add(neigh)
                    visited.add(neigh)
                    if not dfs(neigh):         # propagate False up
                        return False
            visiting.remove(node)              # done with this node, remove from path
            return True

        for course in self.courseGraph:
            if course not in visited:          # skip already fully processed nodes
                visiting.add(course)
                visited.add(course)
                if not dfs(course):
                    return False
        return True

    # ─── LEVEL 3 ─────────────────────────────────────────────────────────────
    def find_order(self) -> list:
        """
        Input:   None
        Output:  List[int] — a valid order to take all courses such that every
                 prerequisite is completed before the course that needs it.
                 Returns [] if no valid order exists (circular dependency).
        Does:    Returns one valid topological ordering of all courses.
                 If multiple valid orderings exist, return any one of them.
        """
        if not self.can_finish():
             return []
        visited=set()
        stack =[]

        def dfs(node):
            visited.add(node)
            for neigh in self.courseGraph[node]:
                if neigh not in visited:
                    dfs(neigh)
            stack.append(node)

        for course in self.courseGraph.keys():
            if course not in visited:
                dfs(course)
        return list(reversed(stack))

    # ─── LEVEL 4 ─────────────────────────────────────────────────────────────
    def min_semesters(self) -> int:
        """
        Input:   None
        Output:  int — minimum number of semesters to complete all courses.
                 Returns -1 if it is impossible (circular dependency).
        Does:    Each semester you can take any number of courses, as long as
                 all their prerequisites were completed in a prior semester.
                 Returns the fewest semesters needed to finish everything.
        Example: A->B->C (chain) requires 3 semesters.
                 A->C, B->C (A and B have no deps) requires 2 semesters.
        """
        if not self.can_finish():
            return -1

        # count how many prereqs each course has
        inDegree = {course: 0 for course in self.courseGraph}
        for course in self.courseGraph:
            for prereq in self.courseGraph[course]:
                inDegree[course] += 1  # course depends on prereq

        # start with courses that have no prerequisites
        from collections import deque
        q = deque([c for c in inDegree if inDegree[c] == 0])
        semesters = 0

        while q:
            # all courses in q can be taken this semester simultaneously
            for _ in range(len(q)):
                course = q.popleft()
                for prereq in self.courseGraph[course]:
                    inDegree[prereq] -= 1      # unblock prereq's dependents
                    if inDegree[prereq] == 0:
                        q.append(prereq)
            semesters += 1                     # one full semester done

        return semesters

