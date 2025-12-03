import heapq

class DSU:
    """
    Disjoint Set Union (Union-Find) with Path Compression and Union by Rank.
    Optimized for Kruskal's algorithm.
    """
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, i):
        if self.parent[i] != i:
            self.parent[i] = self.find(self.parent[i])  # Path compression
        return self.parent[i]

    def union(self, i, j):
        root_i = self.find(i)
        root_j = self.find(j)

        if root_i != root_j:
            # Union by rank
            if self.rank[root_i] < self.rank[root_j]:
                self.parent[root_i] = root_j
            elif self.rank[root_i] > self.rank[root_j]:
                self.parent[root_j] = root_i
            else:
                self.parent[root_j] = root_i
                self.rank[root_i] += 1
            return True
        return False

class NetworkDesigner:
    """
    Class to design networks using MST algorithms (Prim and Kruskal).
    """
    def __init__(self, vertices):
        self.V = vertices
        self.edges = []  # List of (u, v, w) for Kruskal
        self.adj = {i: [] for i in range(vertices)}  # Adjacency list for Prim

    def add_edge(self, u, v, w):
        """
        Adds an undirected edge to the graph.
        """
        self.edges.append((u, v, w))
        self.adj[u].append((v, w))
        self.adj[v].append((u, w))

    def prim_mst(self, start_node=0):
        """
        Implements Prim's algorithm to find the MST.
        Returns: (mst_edges, total_cost)
        """
        if self.V == 0:
            return [], 0

        visited = [False] * self.V
        pq = []  # Priority queue: (weight, u, v)
        
        # Start from start_node
        # We push initial edges from start_node
        visited[start_node] = True
        for neighbor, weight in self.adj[start_node]:
            heapq.heappush(pq, (weight, start_node, neighbor))

        mst_edges = []
        mst_cost = 0
        nodes_in_mst = 1

        while pq:
            weight, u, v = heapq.heappop(pq)

            if visited[v]:
                continue

            visited[v] = True
            mst_edges.append((u, v, weight))
            mst_cost += weight
            nodes_in_mst += 1

            for next_node, next_weight in self.adj[v]:
                if not visited[next_node]:
                    heapq.heappush(pq, (next_weight, v, next_node))
        
        # Check if graph is connected (for MST purposes)
        # If nodes_in_mst < self.V, it's a Minimum Spanning Forest, but we return what we found for the component.
        return mst_edges, mst_cost

    def kruskal_mst(self):
        """
        Implements Kruskal's algorithm to find the MST.
        Returns: (mst_edges, total_cost)
        """
        mst_cost = 0
        mst_edges = []
        dsu = DSU(self.V)

        # Sort edges by weight
        sorted_edges = sorted(self.edges, key=lambda item: item[2])

        for u, v, w in sorted_edges:
            if dsu.union(u, v):
                mst_edges.append((u, v, w))
                mst_cost += w

        return mst_edges, mst_cost

    def get_total_connection_cost(self):
        """
        Calculates the cost if all edges were used (fully connected based on available edges).
        """
        return sum(w for u, v, w in self.edges)