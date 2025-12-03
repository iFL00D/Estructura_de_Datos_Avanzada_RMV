import pytest
import math
from optimization import WeightedGraph, RouteOptimizer

# --- Fixtures ---

@pytest.fixture
def simple_graph():
    """
    Creates a simple directed graph:
    A -> B (10)
    A -> C (5)
    B -> D (1)
    C -> B (3)
    C -> D (9)
    D -> E (2)
    """
    g = WeightedGraph(directed=True)
    # Manually populate adjacency list to avoid file dependency in unit tests
    g.adjacency_list = {
        'A': [('B', 10.0), ('C', 5.0)],
        'B': [('D', 1.0)],
        'C': [('B', 3.0), ('D', 9.0)],
        'D': [('E', 2.0)],
        'E': []
    }
    return g

@pytest.fixture
def negative_graph():
    """
    Graph with negative edges but no negative cycles.
    A -> B (5)
    B -> C (-2)
    C -> D (1)
    """
    g = WeightedGraph(directed=True)
    g.adjacency_list = {
        'A': [('B', 5.0)],
        'B': [('C', -2.0)],
        'C': [('D', 1.0)],
        'D': []
    }
    return g

@pytest.fixture
def negative_cycle_graph():
    """
    Graph with a negative cycle.
    A -> B (1)
    B -> C (-5)
    C -> A (2)
    """
    g = WeightedGraph(directed=True)
    g.adjacency_list = {
        'A': [('B', 1.0)],
        'B': [('C', -5.0)],
        'C': [('A', 2.0)]
    }
    return g

# --- Dijkstra Tests ---

def test_dijkstra_shortest_path(simple_graph):
    """Test 1: Standard shortest path calculation."""
    dist, parent = simple_graph.dijkstra('A')
    
    # Path A -> C -> B -> D -> E
    # Cost: 5 + 3 + 1 + 2 = 11
    assert dist['E'] == 11.0
    assert dist['B'] == 8.0  # A->C->B (5+3) is better than A->B (10)

def test_dijkstra_path_reconstruction(simple_graph):
    """Test 2: Verify path reconstruction."""
    dist, parent = simple_graph.dijkstra('A')
    path = simple_graph.reconstruct_path(parent, 'E')
    assert path == ['A', 'C', 'B', 'D', 'E']

def test_dijkstra_unreachable_node():
    """Test 3: Unreachable node should have infinity distance."""
    g = WeightedGraph(directed=True)
    g.adjacency_list = {
        'A': [('B', 1.0)],
        'C': []
    }
    dist, _ = g.dijkstra('A')
    assert dist['C'] == float('inf')

def test_dijkstra_start_node_not_in_graph():
    """Test 4: Error when start node doesn't exist."""
    g = WeightedGraph(directed=True)
    with pytest.raises(ValueError):
        g.dijkstra('Z')

def test_dijkstra_single_node():
    """Test 5: Graph with single node."""
    g = WeightedGraph(directed=True)
    g.adjacency_list = {'A': []}
    dist, _ = g.dijkstra('A')
    assert dist['A'] == 0

# --- Floyd-Warshall Tests ---

def test_fw_all_pairs(simple_graph):
    """Test 6: Standard all-pairs shortest path."""
    dist, next_node = simple_graph.floyd_warshall()
    
    # A -> E cost is 11
    assert dist['A']['E'] == 11.0
    # C -> D cost is 4 (C->B->D: 3+1) better than direct (9)
    assert dist['C']['D'] == 4.0

def test_fw_negative_weights(negative_graph):
    """Test 7: Handle negative weights correctly."""
    dist, _ = negative_graph.floyd_warshall()
    # A -> C: 5 + (-2) = 3
    assert dist['A']['C'] == 3.0

def test_fw_negative_cycle_detection(negative_cycle_graph):
    """Test 8: Detect negative cycles."""
    with pytest.raises(ValueError, match="Negative cycle detected"):
        negative_cycle_graph.floyd_warshall()

def test_fw_path_reconstruction(simple_graph):
    """Test 9: Reconstruct path from FW matrix."""
    _, next_node = simple_graph.floyd_warshall()
    path = simple_graph.reconstruct_path_fw(next_node, 'A', 'E')
    assert path == ['A', 'C', 'B', 'D', 'E']

def test_fw_disconnected_components():
    """Test 10: Disconnected components."""
    g = WeightedGraph(directed=True)
    g.adjacency_list = {
        'A': [('B', 1.0)],
        'C': [('D', 1.0)]
    }
    dist, _ = g.floyd_warshall()
    assert dist['A']['C'] == float('inf')

# --- RouteOptimizer Tests ---

def test_optimizer_traffic_simulation(simple_graph):
    """Test 11: Traffic simulation increases weights."""
    optimizer = RouteOptimizer(simple_graph)
    
    # Original path A->E cost 11
    path, cost = optimizer.get_optimal_route('A', 'E')
    assert cost == 11.0
    
    # Simulate 2x traffic globally
    optimizer.simulate_traffic(congestion_factor=2.0)
    
    # New cost should be 22
    path_traffic, cost_traffic = optimizer.get_optimal_route('A', 'E')
    assert cost_traffic == 22.0

def test_optimizer_localized_traffic(simple_graph):
    """Test 12: Localized traffic affects only specific nodes."""
    optimizer = RouteOptimizer(simple_graph)
    
    # Congest node B (affects edges entering/leaving B)
    # Edges affected: A->B, C->B, B->D
    optimizer.simulate_traffic(congestion_factor=10.0, affected_nodes=['B'])
    
    # Path A->C->B->D->E uses C->B and B->D, which are now expensive
    # C->B (3->30), B->D (1->10)
    # Alternative path A->C->D->E avoids B?
    # A->C (5), C->D (9), D->E (2) = 16
    # Old path cost: 5 + 30 + 10 + 2 = 47
    
    path, cost = optimizer.get_optimal_route('A', 'E')
    
    # Should choose A->C->D->E
    assert path == ['A', 'C', 'D', 'E']
    assert cost == 16.0

if __name__ == "__main__":
    pytest.main([__file__, "-v"])