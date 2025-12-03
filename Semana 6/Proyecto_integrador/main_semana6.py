import time
import os
from optimization import WeightedGraph, RouteOptimizer

def print_header(title):
    print(f"\n{'='*60}")
    print(f" {title}")
    print(f"{'='*60}")

def analyze_centrality(graph: WeightedGraph):
    """
    Calculates average travel time from each node to all others using Floyd-Warshall.
    Identifies 'central' stations (lowest average travel time).
    """
    print_header("1. Centrality Analysis (Floyd-Warshall)")
    
    try:
        start_time = time.time()
        dist_matrix, _ = graph.floyd_warshall()
        fw_time = time.time() - start_time
        
        print(f"Floyd-Warshall computed in {fw_time:.4f} seconds.")
        
        avg_times = {}
        nodes = sorted(dist_matrix.keys())
        
        for u in nodes:
            total_dist = 0
            count = 0
            for v in nodes:
                d = dist_matrix[u][v]
                if d != float('inf') and u != v:
                    total_dist += d
                    count += 1
            
            if count > 0:
                avg_times[u] = total_dist / count
            else:
                avg_times[u] = float('inf')
                
        # Sort by average time
        sorted_stations = sorted(avg_times.items(), key=lambda x: x[1])
        
        print("\nTop 5 Most Central Stations (Lowest Avg Travel Time):")
        print(f"{'Station':<15} | {'Avg Time':<10}")
        print("-" * 30)
        for station, avg in sorted_stations[:5]:
            print(f"{station:<15} | {avg:.2f}")
            
        return dist_matrix
        
    except ValueError as e:
        print(f"Error: {e}")
        return None

def compare_algorithms(graph: WeightedGraph, start_node: str):
    """
    Compares Dijkstra vs Floyd-Warshall performance for single-source queries.
    """
    print_header("2. Algorithm Comparison: Dijkstra vs Floyd-Warshall")
    
    # Dijkstra
    start_time = time.time()
    dijkstra_dist, _ = graph.dijkstra(start_node)
    dijkstra_time = time.time() - start_time
    
    # Floyd-Warshall (already computed, but let's measure full re-compute for fairness in this context
    # or just use the lookup time if we assume pre-computation)
    # Here we measure computation time.
    start_time = time.time()
    fw_dist_matrix, _ = graph.floyd_warshall()
    fw_time = time.time() - start_time
    
    print(f"Source Node: {start_node}")
    print(f"Dijkstra Time:       {dijkstra_time:.6f} sec")
    print(f"Floyd-Warshall Time: {fw_time:.6f} sec")
    
    if dijkstra_time < fw_time:
        print(f"-> Dijkstra was {fw_time/dijkstra_time:.1f}x faster for single-source.")
    else:
        print(f"-> Floyd-Warshall was faster (unexpected for single execution).")

def run_traffic_simulation(graph: WeightedGraph, start: str, end: str):
    """
    Simulates traffic and compares routes.
    """
    print_header("3. Traffic Simulation Case Study")
    
    optimizer = RouteOptimizer(graph)
    
    # Baseline
    path_base, cost_base = optimizer.get_optimal_route(start, end)
    print(f"Baseline Route ({start} -> {end}):")
    print(f"  Path: {' -> '.join(path_base)}")
    print(f"  Time: {cost_base:.2f} min")
    
    # Simulation: Peak Hour (Global +20%)
    print("\n[Scenario 1] Peak Hour (Global Traffic +20%)")
    optimizer.simulate_traffic(congestion_factor=1.2)
    path_peak, cost_peak = optimizer.get_optimal_route(start, end)
    print(f"  Path: {' -> '.join(path_peak)}")
    print(f"  Time: {cost_peak:.2f} min (+{(cost_peak - cost_base):.2f})")
    
    # Reset
    optimizer.reset_traffic()
    
    # Simulation: Accident at specific node (if path has intermediate nodes)
    if len(path_base) > 2:
        accident_node = path_base[1] # Pick a node in the middle
        print(f"\n[Scenario 2] Accident at {accident_node} (Congestion x5)")
        optimizer.simulate_traffic(congestion_factor=5.0, affected_nodes=[accident_node])
        
        path_accident, cost_accident = optimizer.get_optimal_route(start, end)
        print(f"  Path: {' -> '.join(path_accident)}")
        print(f"  Time: {cost_accident:.2f} min")
        
        if path_accident != path_base:
            print("  -> Route changed to avoid congestion!")
        else:
            print("  -> Route stayed same (alternative was still slower).")

def main():
    # Load Graph
    # Assuming we are in 'Proyecto_integrador' or parent. 
    # The file paths in analysis.py are relative.
    # Let's try to locate the files.
    
    base_path = "Proyecto_integrador" if os.path.exists("Proyecto_integrador") else "."
    file_path = os.path.join(base_path, "edges_directed.txt")
    
    if not os.path.exists(file_path):
        # Fallback for specific structure
        file_path = "edges_directed.txt"
        
    print(f"Loading graph from {file_path}...")
    
    graph = WeightedGraph(directed=True)
    graph.load_from_file(file_path)
    
    if not graph.adjacency_list:
        print("Error: Graph not loaded or empty.")
        return

    # 1. Centrality
    analyze_centrality(graph)
    
    # Pick start/end nodes for demos (first and last sorted)
    nodes = sorted(list(graph.adjacency_list.keys()))
    if len(nodes) < 2:
        print("Not enough nodes for simulation.")
        return
        
    start_node = nodes[0]
    end_node = nodes[-1]
    
    # 2. Comparison
    compare_algorithms(graph, start_node)
    
    # 3. Traffic Sim
    run_traffic_simulation(graph, start_node, end_node)

if __name__ == "__main__":
    main()