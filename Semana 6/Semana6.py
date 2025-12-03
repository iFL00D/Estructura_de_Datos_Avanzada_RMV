import heapq
import math
from collections import defaultdict
from typing import Dict, List, Tuple

class WeightedGraph:
    def __init__(self, n: int):
        self.n = n
        self.adj = {i: [] for i in range(n)}
    
    def add_edge(self, u: int, v: int, w: float):
        self.adj[u].append((v, w))
        # Para no dirigido: self.adj[v].append((u, w))
    
    # Dijkstra
    def dijkstra(self, src: int) -> Tuple[List[float], List[int]]:
        dist = [math.inf] * self.n
        parent = [-1] * self.n
        dist[src] = 0
        pq = [(0, src)]  # (dist, node)
        visited = [False] * self.n
        
        while pq:
            cost, u = heapq.heappop(pq)
            if visited[u]: continue
            visited[u] = True
            
            for v, w in self.adj[u]:
                if dist[u] + w < dist[v]:
                    dist[v] = dist[u] + w
                    parent[v] = u
                    heapq.heappush(pq, (dist[v], v))
        
        return dist, parent
    
    # Floyd-Warshall
    def floyd_warshall(self) -> List[List[float]]:
        if self.n == 0:
            raise ValueError("El grafo está vacío")
            
        dist = [[math.inf] * self.n for _ in range(self.n)]
        for i in range(self.n):
            dist[i][i] = 0
        
        for u in range(self.n):
            for v, w in self.adj[u]:
                dist[u][v] = w
        
        for k in range(self.n):
            for i in range(self.n):
                for j in range(self.n):
                    if dist[i][k] + dist[k][j] < dist[i][j]:
                        dist[i][j] = dist[i][k] + dist[k][j]
        
        # Detectar ciclos negativos
        for i in range(self.n):
            if dist[i][i] < 0:
                raise ValueError("Ciclo negativo detectado")
        
        return dist

# Ejemplo de uso
g = WeightedGraph(6)
g.add_edge(0,1,10); g.add_edge(0,2,5)
g.add_edge(1,3,3); g.add_edge(2,3,2); g.add_edge(2,4,8)
g.add_edge(3,4,4); g.add_edge(1,5,15); g.add_edge(4,5,7)

dist, parent = g.dijkstra(0)
print(f"Dist a F: {dist[5]}")  # 18

fw = g.floyd_warshall()
print(f"FW dist 0-5: {fw[0][5]}")  # 18

