import heapq

class GraphMST:
    def __init__(self, vertices):
        self.V = vertices
        self.edges = []  # Para Kruskal: (u, v, w)
        self.adj = {i: [] for i in range(vertices)}  # Para Prim

    def add_edge(self, u, v, w):
        self.edges.append((u, v, w))
        self.adj[u].append((v, w))
        self.adj[v].append((u, w))

    # --- ALGORITMO DE PRIM ---
    def prim_mst(self, start_node=0):
        visited = [False] * self.V
        pq = []

        visited[start_node] = True
        for neighbor, weight in self.adj[start_node]:
            heapq.heappush(pq, (weight, start_node, neighbor))

        mst_edges = []
        mst_cost = 0

        while pq:
            weight, u, v = heapq.heappop(pq)
            if visited[v]:
                continue

            visited[v] = True
            mst_edges.append((u, v, weight))
            mst_cost += weight

            for next_node, next_weight in self.adj[v]:
                if not visited[next_node]:
                    heapq.heappush(pq, (next_weight, v, next_node))

        return mst_edges, mst_cost

    # --- UNION-FIND OPTIMIZADO ---
    class DSU:
        def __init__(self, n):
            self.parent = list(range(n))
            self.rank = [0] * n

        def find(self, i):
            if self.parent[i] != i:
                self.parent[i] = self.find(self.parent[i])
            return self.parent[i]

        def union(self, i, j):
            root_i = self.find(i)
            root_j = self.find(j)

            if root_i != root_j:
                if self.rank[root_i] < self.rank[root_j]:
                    self.parent[root_i] = root_j
                elif self.rank[root_i] > self.rank[root_j]:
                    self.parent[root_j] = root_i
                else:
                    self.parent[root_j] = root_i
                    self.rank[root_i] += 1
                return True
            return False

    # --- ALGORITMO DE KRUSKAL ---
    def kruskal_mst(self):
        mst_cost = 0
        mst_edges = []
        dsu = self.DSU(self.V)

        sorted_edges = sorted(self.edges, key=lambda item: item[2])

        for u, v, w in sorted_edges:
            if dsu.union(u, v):
                mst_edges.append((u, v, w))
                mst_cost += w

        return mst_edges, mst_cost

# Prueba rápida
if __name__ == "__main__":
    g = GraphMST(4)
    g.add_edge(0, 1, 10)
    g.add_edge(0, 2, 6)
    g.add_edge(0, 3, 5)
    g.add_edge(1, 3, 15)
    g.add_edge(2, 3, 4)

    edges_p, cost_p = g.prim_mst()
    print("MST Prim:", edges_p, "Costo:", cost_p)

    edges_k, cost_k = g.kruskal_mst()
    print("MST Kruskal:", edges_k, "Costo:", cost_k)