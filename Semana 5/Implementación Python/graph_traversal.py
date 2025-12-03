"""
Módulo de algoritmos de exploración y búsqueda en grafos.
Incluye implementaciones de BFS, DFS y aplicaciones avanzadas.

Autor: Curso Estructuras de Datos Avanzadas
Fecha: 2025
"""

from collections import deque, defaultdict
from enum import Enum
from typing import List, Dict, Set, Optional, Tuple


class NodeState(Enum):
    """Estados de nodo para detección de ciclos en grafos dirigidos."""
    NOT_VISITED = 0
    IN_PROGRESS = 1
    COMPLETED = 2


class GraphTraversal:
    """
    Clase que implementa algoritmos de exploración y búsqueda en grafos.
    Soporta grafos dirigidos y no dirigidos.
    """
    
    def __init__(self, directed: bool = False):
        """
        Inicializa el grafo.
        
        Args:
            directed: True si el grafo es dirigido, False en caso contrario.
        """
        # Usamos defaultdict, pero nos aseguraremos de registrar todos los nodos
        self.adjacency_list: Dict[int, List[int]] = defaultdict(list)
        self.directed = directed
        self._nodes: Set[int] = set() # Set auxiliar para rastrear existencia real de nodos

    def _register_node(self, node: int) -> None:
        """Registra un nodo para asegurar que exista en el grafo."""
        self._nodes.add(node)
        # Asegura que el nodo tenga una entrada en el dict, aunque sea lista vacía
        if node not in self.adjacency_list:
            self.adjacency_list[node] = []

    def _validate_node(self, node: int) -> None:
        """Valida si un nodo existe en el grafo."""
        if node not in self._nodes:
            raise ValueError(f"El nodo {node} no existe en el grafo.")

    def add_edge(self, u: int, v: int) -> None:
        """
        Agrega una arista al grafo. Corregido para registrar ambos nodos.
        
        Args:
            u: Nodo origen
            v: Nodo destino
        """
        self._register_node(u)
        self._register_node(v)
        
        self.adjacency_list[u].append(v)
        
        if not self.directed:
            self.adjacency_list[v].append(u)
    
    # ========================================
    # BÚSQUEDA EN AMPLITUD (BFS)
    # ========================================
    
    def bfs(self, start: int) -> List[int]:
        self._validate_node(start) # Validación estandarizada
        
        visited: Set[int] = {start}
        result: List[int] = []
        queue = deque([start])
        
        while queue:
            current = queue.popleft()
            result.append(current)
            
            for neighbor in self.adjacency_list[current]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        
        return result
    
    def bfs_distances(self, start: int) -> Dict[int, int]:
        self._validate_node(start) # Corregido: Validación agregada
        
        distances: Dict[int, int] = {start: 0}
        queue = deque([start])
        
        while queue:
            current = queue.popleft()
            
            for neighbor in self.adjacency_list[current]:
                if neighbor not in distances:
                    distances[neighbor] = distances[current] + 1
                    queue.append(neighbor)
        
        return distances
    
    def bfs_shortest_path(self, start: int, end: int) -> Optional[List[int]]:
        self._validate_node(start) # Corregido: Validación agregada
        self._validate_node(end)   # Corregido: Validación agregada
        
        parent: Dict[int, Optional[int]] = {start: None}
        visited: Set[int] = {start}
        queue = deque([start])
        
        found = False
        
        while queue and not found:
            current = queue.popleft()
            
            if current == end:
                found = True
                break
            
            for neighbor in self.adjacency_list[current]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    parent[neighbor] = current
                    queue.append(neighbor)
        
        if not found:
            return None
        
        # Reconstruir camino
        path: List[int] = []
        node: Optional[int] = end
        while node is not None:
            path.append(node)
            node = parent[node]
        
        path.reverse()
        return path
    
    def bfs_levels(self, start: int) -> Dict[int, List[int]]:
        self._validate_node(start) # Corregido: Validación agregada
        
        levels: Dict[int, List[int]] = defaultdict(list)
        visited: Set[int] = {start}
        queue = deque([(start, 0)])
        
        while queue:
            current, level = queue.popleft()
            levels[level].append(current)
            
            for neighbor in self.adjacency_list[current]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, level + 1))
        
        return dict(levels)
    
    # ========================================
    # BÚSQUEDA EN PROFUNDIDAD (DFS)
    # ========================================
    
    def dfs_recursive(self, start: int) -> List[int]:
        self._validate_node(start)
        
        visited: Set[int] = set()
        result: List[int] = []
        
        def dfs_helper(node: int) -> None:
            visited.add(node)
            result.append(node)
            
            for neighbor in self.adjacency_list[node]:
                if neighbor not in visited:
                    dfs_helper(neighbor)
        
        dfs_helper(start)
        return result
    
    def dfs_iterative(self, start: int) -> List[int]:
        self._validate_node(start)
        
        visited: Set[int] = set()
        result: List[int] = []
        stack = [start]
        
        while stack:
            current = stack.pop()
            
            if current in visited:
                continue
            
            visited.add(current)
            result.append(current)
            
            # Apilar vecinos en orden inverso para preservar orden izquierda-derecha al desapilar
            neighbors = list(self.adjacency_list[current])
            neighbors.reverse()
            
            for neighbor in neighbors:
                if neighbor not in visited:
                    stack.append(neighbor)
        
        return result
    
    # ========================================
    # APLICACIONES AVANZADAS
    # ========================================
    
    def has_cycle_directed(self) -> bool:
        if not self.directed:
            raise ValueError("Este método requiere un grafo dirigido")
        
        # Corregido: Iteramos sobre self._nodes para asegurar cobertura total
        state: Dict[int, NodeState] = {
            node: NodeState.NOT_VISITED 
            for node in self._nodes
        }
        
        def dfs_cycle(node: int) -> bool:
            state[node] = NodeState.IN_PROGRESS
            
            for neighbor in self.adjacency_list[node]:
                neighbor_state = state.get(neighbor, NodeState.NOT_VISITED)
                
                if neighbor_state == NodeState.IN_PROGRESS:
                    return True
                
                if neighbor_state == NodeState.NOT_VISITED:
                    if dfs_cycle(neighbor):
                        return True
            
            state[node] = NodeState.COMPLETED
            return False
        
        for node in self._nodes:
            if state[node] == NodeState.NOT_VISITED:
                if dfs_cycle(node):
                    return True
        
        return False
    
    def topological_sort(self) -> Optional[List[int]]:
        if not self.directed:
            raise ValueError("Ordenamiento topológico requiere grafo dirigido")
        
        if self.has_cycle_directed():
            return None
        
        visited: Set[int] = set()
        stack: List[int] = []
        
        def dfs_topo(node: int) -> None:
            visited.add(node)
            
            for neighbor in self.adjacency_list[node]:
                if neighbor not in visited:
                    dfs_topo(neighbor)
            
            stack.append(node)
        
        # Corregido: Iterar sobre self._nodes asegura que procesamos nodos desconectados
        for node in self._nodes:
            if node not in visited:
                dfs_topo(node)
        
        stack.reverse()
        return stack
    
    def find_connected_components(self) -> List[List[int]]:
        if self.directed:
            raise ValueError("Este método requiere un grafo no dirigido")
        
        visited: Set[int] = set()
        components: List[List[int]] = []
        
        def dfs_component(node: int, component: List[int]) -> None:
            visited.add(node)
            component.append(node)
            
            for neighbor in self.adjacency_list[node]:
                if neighbor not in visited:
                    dfs_component(neighbor, component)
        
        # Corregido: Uso de self._nodes
        for node in self._nodes:
            if node not in visited:
                component: List[int] = []
                dfs_component(node, component)
                components.append(component)
        
        return components
    
    def has_cycle_undirected(self) -> bool:
        if self.directed:
            raise ValueError("Este método requiere un grafo no dirigido")
        
        visited: Set[int] = set()
        
        def dfs_cycle(node: int, parent: Optional[int]) -> bool:
            visited.add(node)
            
            for neighbor in self.adjacency_list[node]:
                if neighbor not in visited:
                    if dfs_cycle(neighbor, node):
                        return True
                elif neighbor != parent:
                    return True
            
            return False
        
        # Corregido: Uso de self._nodes
        for node in self._nodes:
            if node not in visited:
                if dfs_cycle(node, None):
                    return True
        
        return False


# ========================================
# PROGRAMA DE DEMOSTRACIÓN
# ========================================

def main():
    print("=== DEMOSTRACIÓN BFS Y DFS CORREGIDA ===\n")
    
    # Crear grafo no dirigido
    graph = GraphTraversal(directed=False)
    edges = [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (5, 7)]
    for u, v in edges:
        graph.add_edge(u, v)
    
    # Prueba de validación
    try:
        graph.bfs(99)
    except ValueError as e:
        print(f"Validación correcta detectada: {e}")
    print()

    # BFS
    print("--- BFS desde nodo 1 ---")
    print(f"Orden: {graph.bfs(1)}")
    
    # DFS
    print("--- DFS Iterativo desde nodo 1 ---")
    print(f"Orden: {graph.dfs_iterative(1)}")
    
    # Componentes conectadas
    print("\n--- Componentes Conectadas ---")
    disconnected = GraphTraversal(directed=False)
    disconnected.add_edge(1, 2)
    disconnected.add_edge(4, 5)
    # Ahora 1, 2, 4, 5 son nodos válidos.
    
    comps = disconnected.find_connected_components()
    print(f"Componentes encontradas: {comps}")

if __name__ == "__main__":
    main()