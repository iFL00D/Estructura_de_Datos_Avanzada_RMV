import math
from optimization import WeightedGraph, RouteOptimizer

def run_tests():
    print("Running manual tests...")
    
    # Setup Simple Graph
    g = WeightedGraph(directed=True)
    g.adjacency_list = {
        'A': [('B', 10.0), ('C', 5.0)],
        'B': [('D', 1.0)],
        'C': [('B', 3.0), ('D', 9.0)],
        'D': [('E', 2.0)],
        'E': []
    }
    
    # Test 1: Dijkstra Shortest Path
    print("Test 1: Dijkstra Shortest Path...", end="")
    dist, parent = g.dijkstra('A')
    assert dist['E'] == 11.0, f"Expected 11.0, got {dist['E']}"
    assert dist['B'] == 8.0, f"Expected 8.0, got {dist['B']}"
    print("PASS")
    
    # Test 2: Dijkstra Path Reconstruction
    print("Test 2: Dijkstra Path Reconstruction...", end="")
    path = g.reconstruct_path(parent, 'E')
    assert path == ['A', 'C', 'B', 'D', 'E'], f"Got {path}"
    print("PASS")
    
    # Test 3: Floyd-Warshall All Pairs
    print("Test 3: Floyd-Warshall All Pairs...", end="")
    dist_fw, next_node = g.floyd_warshall()
    assert dist_fw['A']['E'] == 11.0, f"Expected 11.0, got {dist_fw['A']['E']}"
    assert dist_fw['C']['D'] == 4.0, f"Expected 4.0, got {dist_fw['C']['D']}"
    print("PASS")
    
    # Test 4: FW Path Reconstruction
    print("Test 4: FW Path Reconstruction...", end="")
    path_fw = g.reconstruct_path_fw(next_node, 'A', 'E')
    assert path_fw == ['A', 'C', 'B', 'D', 'E'], f"Got {path_fw}"
    print("PASS")
    
    # Test 5: Negative Weights (No Cycle)
    print("Test 5: Negative Weights (No Cycle)...", end="")
    neg_g = WeightedGraph(directed=True)
    neg_g.adjacency_list = {
        'A': [('B', 5.0)],
        'B': [('C', -2.0)],
        'C': [('D', 1.0)],
        'D': []
    }
    dist_neg, _ = neg_g.floyd_warshall()
    assert dist_neg['A']['C'] == 3.0, f"Expected 3.0, got {dist_neg['A']['C']}"
    print("PASS")
    
    # Test 6: Negative Cycle Detection
    print("Test 6: Negative Cycle Detection...", end="")
    cycle_g = WeightedGraph(directed=True)
    cycle_g.adjacency_list = {
        'A': [('B', 1.0)],
        'B': [('C', -5.0)],
        'C': [('A', 2.0)]
    }
    try:
        cycle_g.floyd_warshall()
        print("FAIL (No exception raised)")
    except ValueError as e:
        assert str(e) == "Negative cycle detected"
        print("PASS")
        
    # Test 7: Route Optimizer Traffic
    print("Test 7: Route Optimizer Traffic...", end="")
    optimizer = RouteOptimizer(g)
    optimizer.simulate_traffic(congestion_factor=2.0)
    path_traffic, cost_traffic = optimizer.get_optimal_route('A', 'E')
    assert cost_traffic == 22.0, f"Expected 22.0, got {cost_traffic}"
    print("PASS")
    
    print("\nAll manual tests passed successfully!")

if __name__ == "__main__":
    run_tests()