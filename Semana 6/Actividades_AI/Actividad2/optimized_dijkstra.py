import heapq
import math
from typing import Dict, List, Tuple, Any, Optional

class OptimizedGraph:
    def __init__(self):
        # Optimización sugerida por IA: Uso de diccionario para soportar cualquier tipo de nodo (str, int)
        self.adj: Dict[Any, List[Tuple[Any, float]]] = {}
    
    def add_edge(self, u: Any, v: Any, w: float, directed: bool = True):
        if u not in self.adj: self.adj[u] = []
        if v not in self.adj: self.adj[v] = []
        
        self.adj[u].append((v, w))
        if not directed:
            self.adj[v].append((u, w))
            
    def dijkstra(self, start_node: Any) -> Tuple[Dict[Any, float], Dict[Any, Any]]:
        # Optimización sugerida por IA: Validación de nodo inicial
        if start_node not in self.adj:
            raise ValueError(f"El nodo {start_node} no existe en el grafo")

        # Inicialización flexible
        dist = {node: math.inf for node in self.adj}
        parent = {node: None for node in self.adj}
        dist[start_node] = 0
        
        pq = [(0, start_node)]
        
        while pq:
            current_dist, u = heapq.heappop(pq)
            
            # Optimización sugerida por IA: Lazy deletion check
            # Si encontramos un camino más corto a 'u' antes de sacar este elemento, lo ignoramos
            if current_dist > dist[u]:
                continue
            
            for v, weight in self.adj[u]:
                if dist[u] + weight < dist[v]:
                    dist[v] = dist[u] + weight
                    parent[v] = u
                    heapq.heappush(pq, (dist[v], v))
                    
        return dist, parent

    def get_path(self, parent: Dict[Any, Any], target: Any) -> List[Any]:
        # Funcionalidad adicional: Reconstrucción de camino
        path = []
        curr = target
        while curr is not None:
            path.append(curr)
            curr = parent.get(curr)
        return path[::-1]

# Ejemplo de uso
if __name__ == "__main__":
    g = OptimizedGraph()
    g.add_edge('A', 'B', 4)
    g.add_edge('A', 'C', 2)
    g.add_edge('C', 'B', 1)
    g.add_edge('B', 'D', 5)
    
    dist, parent = g.dijkstra('A')
    print(f"Distancias desde A: {dist}")
    print(f"Camino a D: {g.get_path(parent, 'D')}")