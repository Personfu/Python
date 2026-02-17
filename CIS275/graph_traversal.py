# ============================================================
# Graph Traversal — Complete Implementation
# CIS 275 — Data Structures | Preston Furulie
# ============================================================
# Covers: adjacency list/matrix representations, BFS, DFS
# (iterative & recursive), shortest path (Dijkstra's),
# topological sort, cycle detection, connected components,
# and practical applications.
# ============================================================

from collections import deque, defaultdict
import heapq


class Graph:
    """Graph using adjacency list representation.
    Supports both directed and undirected, weighted and unweighted."""

    def __init__(self, directed=False):
        self.adj = defaultdict(list)   # {node: [(neighbor, weight), ...]}
        self.directed = directed
        self._nodes = set()

    def add_edge(self, u, v, weight=1):
        """Add an edge from u to v with optional weight."""
        self.adj[u].append((v, weight))
        self._nodes.add(u)
        self._nodes.add(v)
        if not self.directed:
            self.adj[v].append((u, weight))

    def get_neighbors(self, node):
        """Get all neighbors of a node."""
        return [(n, w) for n, w in self.adj[node]]

    def get_nodes(self):
        """Get all nodes in the graph."""
        return self._nodes

    # ── BFS (Breadth-First Search) ──────────────────────────

    def bfs(self, start):
        """BFS: Explore all neighbors at current depth before going deeper.
        Uses a queue (FIFO). Guarantees shortest path in unweighted graphs.

        Time:  O(V + E) where V = vertices, E = edges
        Space: O(V) for the visited set and queue
        """
        visited = set()
        queue = deque([start])
        visited.add(start)
        order = []

        while queue:
            node = queue.popleft()
            order.append(node)
            for neighbor, _ in self.adj[node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)

        return order

    def bfs_shortest_path(self, start, end):
        """Find shortest path (fewest edges) using BFS.
        Tracks parent pointers to reconstruct the path."""
        if start == end:
            return [start]

        visited = {start}
        queue = deque([(start, [start])])

        while queue:
            node, path = queue.popleft()
            for neighbor, _ in self.adj[node]:
                if neighbor == end:
                    return path + [neighbor]
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))

        return []  # no path exists

    def bfs_level_order(self, start):
        """BFS with level tracking — returns nodes grouped by distance."""
        visited = {start}
        queue = deque([start])
        levels = []

        while queue:
            level_size = len(queue)
            current_level = []
            for _ in range(level_size):
                node = queue.popleft()
                current_level.append(node)
                for neighbor, _ in self.adj[node]:
                    if neighbor not in visited:
                        visited.add(neighbor)
                        queue.append(neighbor)
            levels.append(current_level)

        return levels

    # ── DFS (Depth-First Search) ────────────────────────────

    def dfs_recursive(self, start, visited=None):
        """DFS (recursive): Go as deep as possible before backtracking.
        Uses the call stack implicitly.

        Time:  O(V + E)
        Space: O(V) for visited set + O(V) recursion stack
        """
        if visited is None:
            visited = set()
        visited.add(start)
        order = [start]

        for neighbor, _ in self.adj[start]:
            if neighbor not in visited:
                order.extend(self.dfs_recursive(neighbor, visited))

        return order

    def dfs_iterative(self, start):
        """DFS (iterative): Uses an explicit stack instead of recursion.
        Avoids stack overflow for very deep graphs."""
        visited = set()
        stack = [start]
        order = []

        while stack:
            node = stack.pop()
            if node not in visited:
                visited.add(node)
                order.append(node)
                # Add neighbors in reverse order so leftmost is processed first
                for neighbor, _ in reversed(self.adj[node]):
                    if neighbor not in visited:
                        stack.append(neighbor)

        return order

    def dfs_paths(self, start, end, path=None):
        """Find ALL paths between start and end using DFS backtracking."""
        if path is None:
            path = []
        path = path + [start]

        if start == end:
            return [path]

        paths = []
        for neighbor, _ in self.adj[start]:
            if neighbor not in path:  # avoid cycles
                new_paths = self.dfs_paths(neighbor, end, path)
                paths.extend(new_paths)

        return paths

    # ── Dijkstra's Shortest Path (Weighted) ─────────────────

    def dijkstra(self, start):
        """Dijkstra's algorithm: Find shortest weighted path from start
        to all other nodes. Uses a min-heap (priority queue).

        Time:  O((V + E) log V) with a binary heap
        Space: O(V)
        Requirement: No negative edge weights
        """
        distances = {node: float('inf') for node in self._nodes}
        distances[start] = 0
        previous = {node: None for node in self._nodes}
        heap = [(0, start)]  # (distance, node)
        visited = set()

        while heap:
            dist, node = heapq.heappop(heap)

            if node in visited:
                continue
            visited.add(node)

            for neighbor, weight in self.adj[node]:
                new_dist = dist + weight
                if new_dist < distances[neighbor]:
                    distances[neighbor] = new_dist
                    previous[neighbor] = node
                    heapq.heappush(heap, (new_dist, neighbor))

        return distances, previous

    def shortest_weighted_path(self, start, end):
        """Get the shortest weighted path and its total distance."""
        distances, previous = self.dijkstra(start)
        path = []
        node = end
        while node is not None:
            path.append(node)
            node = previous[node]
        path.reverse()
        if path[0] != start:
            return [], float('inf')
        return path, distances[end]

    # ── Cycle Detection ─────────────────────────────────────

    def has_cycle(self):
        """Detect if the graph contains a cycle.
        For directed: uses DFS with three states (white/gray/black).
        For undirected: uses DFS tracking parent."""
        if self.directed:
            return self._has_cycle_directed()
        return self._has_cycle_undirected()

    def _has_cycle_directed(self):
        WHITE, GRAY, BLACK = 0, 1, 2
        color = {node: WHITE for node in self._nodes}

        def dfs(node):
            color[node] = GRAY
            for neighbor, _ in self.adj[node]:
                if color[neighbor] == GRAY:
                    return True  # back edge = cycle
                if color[neighbor] == WHITE and dfs(neighbor):
                    return True
            color[node] = BLACK
            return False

        for node in self._nodes:
            if color[node] == WHITE:
                if dfs(node):
                    return True
        return False

    def _has_cycle_undirected(self):
        visited = set()

        def dfs(node, parent):
            visited.add(node)
            for neighbor, _ in self.adj[node]:
                if neighbor not in visited:
                    if dfs(neighbor, node):
                        return True
                elif neighbor != parent:
                    return True
            return False

        for node in self._nodes:
            if node not in visited:
                if dfs(node, None):
                    return True
        return False

    # ── Topological Sort (DAG only) ─────────────────────────

    def topological_sort(self):
        """Topological sort using Kahn's algorithm (BFS-based).
        Only valid for directed acyclic graphs (DAGs).

        Returns: ordered list where for every edge u→v, u appears before v.
        Use case: task scheduling, build dependencies, course prerequisites.
        """
        if not self.directed:
            raise ValueError("Topological sort requires a directed graph")

        in_degree = defaultdict(int)
        for node in self._nodes:
            if node not in in_degree:
                in_degree[node] = 0
            for neighbor, _ in self.adj[node]:
                in_degree[neighbor] += 1

        queue = deque([node for node in self._nodes if in_degree[node] == 0])
        result = []

        while queue:
            node = queue.popleft()
            result.append(node)
            for neighbor, _ in self.adj[node]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

        if len(result) != len(self._nodes):
            raise ValueError("Graph has a cycle — topological sort impossible")
        return result

    # ── Connected Components ────────────────────────────────

    def connected_components(self):
        """Find all connected components in an undirected graph.
        Returns a list of sets, each set being a component."""
        visited = set()
        components = []

        for node in self._nodes:
            if node not in visited:
                component = set()
                queue = deque([node])
                while queue:
                    n = queue.popleft()
                    if n not in visited:
                        visited.add(n)
                        component.add(n)
                        for neighbor, _ in self.adj[n]:
                            queue.append(neighbor)
                components.append(component)

        return components

    def __str__(self):
        kind = "Directed" if self.directed else "Undirected"
        lines = [f"{kind} Graph ({len(self._nodes)} nodes):"]
        for node in sorted(self._nodes):
            neighbors = [(n, w) for n, w in self.adj[node]]
            lines.append(f"  {node} → {neighbors}")
        return "\n".join(lines)


# ── Demonstrations ──────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 60)
    print("  GRAPH TRAVERSAL — CIS 275 | Preston Furulie")
    print("=" * 60)

    # --- Unweighted undirected graph ---
    print("\n--- Unweighted Undirected Graph ---")
    g = Graph(directed=False)
    edges = [("A", "B"), ("A", "C"), ("B", "D"), ("B", "E"),
             ("C", "F"), ("E", "F"), ("D", "G")]
    for u, v in edges:
        g.add_edge(u, v)

    print(f"\n  BFS from A:    {g.bfs('A')}")
    print(f"  DFS from A:    {g.dfs_recursive('A')}")
    print(f"  DFS iterative: {g.dfs_iterative('A')}")
    print(f"  BFS levels:    {g.bfs_level_order('A')}")
    print(f"  Path A→G:      {g.bfs_shortest_path('A', 'G')}")
    print(f"  All paths A→F: {g.dfs_paths('A', 'F')}")
    print(f"  Has cycle:     {g.has_cycle()}")
    print(f"  Components:    {g.connected_components()}")

    # --- Weighted directed graph (Dijkstra's) ---
    print("\n--- Weighted Directed Graph (Dijkstra) ---")
    wg = Graph(directed=True)
    wg.add_edge("A", "B", 4)
    wg.add_edge("A", "C", 2)
    wg.add_edge("B", "D", 3)
    wg.add_edge("B", "E", 1)
    wg.add_edge("C", "B", 1)
    wg.add_edge("C", "D", 5)
    wg.add_edge("D", "E", 2)
    wg.add_edge("E", "F", 3)
    wg.add_edge("D", "F", 6)

    distances, _ = wg.dijkstra("A")
    print(f"\n  Shortest distances from A:")
    for node in sorted(distances):
        print(f"    A → {node}: {distances[node]}")

    path, dist = wg.shortest_weighted_path("A", "F")
    print(f"\n  Shortest path A→F: {' → '.join(path)} (distance: {dist})")

    # --- Topological sort (DAG) ---
    print("\n--- Topological Sort (Course Prerequisites) ---")
    dag = Graph(directed=True)
    dag.add_edge("CIS 120", "CIS 133")
    dag.add_edge("CIS 133", "CIS 195")
    dag.add_edge("CIS 133", "CIS 233")
    dag.add_edge("CIS 133", "CIS 275")
    dag.add_edge("CIS 195", "CIS 425")
    dag.add_edge("CIS 233", "CIS 425")
    dag.add_edge("CIS 275", "CIS 425")
    dag.add_edge("CIS 275", "CIS 350")
    dag.add_edge("CIS 350", "CIS 410")
    dag.add_edge("CIS 410", "CIS 425")

    order = dag.topological_sort()
    print(f"  Course order: {' → '.join(order)}")
    print(f"  Has cycle:    {dag.has_cycle()}")
