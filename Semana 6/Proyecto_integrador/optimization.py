import heapq
import math
import copy
from typing import Dict, List, Tuple, Optional, Any, Set

# Try to import from local analysis.py, handling both package and script execution contexts
try:
    from analysis import GraphTraversal
except ImportError:
    # Fallback for when running from parent directory
    from Proyecto_integrador.analysis import GraphTraversal

class WeightedGraph(GraphTraversal):
    """
    Extends GraphTraversal to include weighted graph algorithms:
    - Dijkstra (Single-Source Shortest Path)
    - Floyd-Warshall (All-Pairs Shortest Path)
    """

    def dijkstra(self, start_node: str) -> Tuple[Dict[str, float], Dict[str, Optional[str]]]:
        """
        Implements Dijkstra's algorithm using a priority queue.
        Returns:
            - dist: Dictionary {node: min_distance}
            - parent: Dictionary {node: parent_node} for path reconstruction
        """
        # Ensure start node exists in the graph (either as a key or a value in adjacency list)
        all_nodes = set(self.adjacency_list.keys())
        for neighbors in self.adjacency_list.values():
            for v, _ in neighbors:
                all_nodes.add(v)
                
        if start_node not in all_nodes:
            raise ValueError(f"Start node '{start_node}' not found in graph.")

        # Initialization
        dist: Dict[str, float] = {node: float('inf') for node in all_nodes}
        parent: Dict[str, Optional[str]] = {node: None for node in all_nodes}
        dist[start_node] = 0
        
        # Priority Queue: (distance, node)
        pq = [(0, start_node)]
        
        while pq:
            current_dist, u = heapq.heappop(pq)
            
            # Optimization: If we found a shorter path to u before, skip
            if current_dist > dist[u]:
                continue
            
            # Explore neighbors
            # Use .get() because u might be a sink node not in adjacency_list keys
            for v, weight in self.adjacency_list.get(u, []):
                if dist[u] + weight < dist[v]:
                    dist[v] = dist[u] + weight
                    parent[v] = u
                    heapq.heappush(pq, (dist[v], v))
                    
        return dist, parent

    def reconstruct_path(self, parent: Dict[str, Optional[str]], end_node: str) -> List[str]:
        """Reconstructs the path from start_node to end_node using the parent map."""
        path = []
        current = end_node
        
        # If end_node is not in parent map (unreachable or invalid), return empty
        if current not in parent:
            return []
            
        while current is not None:
            path.append(current)
            current = parent[current]
            
        return path[::-1] # Reverse to get start -> end

    def floyd_warshall(self) -> Tuple[Dict[str, Dict[str, float]], Dict[str, Dict[str, Optional[str]]]]:
        """
        Implements Floyd-Warshall algorithm for all-pairs shortest paths.
        Returns:
            - dist: Dict of Dicts {u: {v: distance}}
            - next_node: Dict of Dicts {u: {v: next_node}} for path reconstruction
        """
        # Collect all unique nodes
        nodes = set(self.adjacency_list.keys())
        for neighbors in self.adjacency_list.values():
            for v, _ in neighbors:
                nodes.add(v)
        sorted_nodes = sorted(list(nodes))
        
        # Initialize distances and next_node pointers
        dist = {u: {v: float('inf') for v in sorted_nodes} for u in sorted_nodes}
        next_node = {u: {v: None for v in sorted_nodes} for u in sorted_nodes}
        
        for u in sorted_nodes:
            dist[u][u] = 0
            
        for u in self.adjacency_list:
            for v, w in self.adjacency_list[u]:
                # Handle multiple edges: keep the one with min weight
                if w < dist[u][v]:
                    dist[u][v] = w
                    next_node[u][v] = v 
                
        # Main loop
        for k in sorted_nodes:
            for i in sorted_nodes:
                for j in sorted_nodes:
                    if dist[i][k] == float('inf') or dist[k][j] == float('inf'):
                        continue
                    if dist[i][k] + dist[k][j] < dist[i][j]:
                        dist[i][j] = dist[i][k] + dist[k][j]
                        next_node[i][j] = next_node[i][k]
        
        # Negative cycle detection
        for i in sorted_nodes:
            if dist[i][i] < 0:
                raise ValueError("Negative cycle detected")
                
        return dist, next_node

    def reconstruct_path_fw(self, next_node: Dict[str, Dict[str, Optional[str]]], start: str, end: str) -> List[str]:
        """Reconstructs path from Floyd-Warshall next_node matrix."""
        if start not in next_node or end not in next_node[start] or next_node[start][end] is None:
            return []
        
        path = [start]
        current = start
        while current != end:
            current = next_node[current][end]
            if current is None: 
                return []
            path.append(current)
            # Cycle prevention
            if len(path) > len(next_node): 
                return [] 
                
        return path

class RouteOptimizer:
    """
    Case of Use: Traffic Simulator and Route Optimization.
    """
    def __init__(self, graph: WeightedGraph):
        self.original_graph = graph
        # Create a working copy for simulation
        self.current_graph = copy.deepcopy(graph)

    def reset_traffic(self):
        """Resets weights to original values."""
        self.current_graph = copy.deepcopy(self.original_graph)

    def simulate_traffic(self, congestion_factor: float = 1.2, affected_nodes: List[str] = None):
        """
        Increases weights of edges connected to affected_nodes by congestion_factor.
        """
        if affected_nodes is None:
            # Global traffic
            for u in self.current_graph.adjacency_list:
                new_neighbors = []
                for v, w in self.current_graph.adjacency_list[u]:
                    new_neighbors.append((v, w * congestion_factor))
                self.current_graph.adjacency_list[u] = new_neighbors
        else:
            # Localized traffic
            affected_set = set(affected_nodes)
            for u in self.current_graph.adjacency_list:
                new_neighbors = []
                for v, w in self.current_graph.adjacency_list[u]:
                    # If edge enters or leaves an affected node
                    if u in affected_set or v in affected_set:
                        new_neighbors.append((v, w * congestion_factor))
                    else:
                        new_neighbors.append((v, w))
                self.current_graph.adjacency_list[u] = new_neighbors

    def get_optimal_route(self, start: str, end: str, algorithm: str = 'dijkstra') -> Tuple[List[str], float]:
        """
        Finds optimal route using specified algorithm.
        """
        if algorithm.lower() == 'dijkstra':
            dist, parent = self.current_graph.dijkstra(start)
            if dist[end] == float('inf'):
                return [], float('inf')
            path = self.current_graph.reconstruct_path(parent, end)
            return path, dist[end]
        elif algorithm.lower() == 'fw':
            dist_matrix, next_node = self.current_graph.floyd_warshall()
            if dist_matrix[start][end] == float('inf'):
                return [], float('inf')
            path = self.current_graph.reconstruct_path_fw(next_node, start, end)
            return path, dist_matrix[start][end]
        else:
            raise ValueError("Unknown algorithm. Use 'dijkstra' or 'fw'.")