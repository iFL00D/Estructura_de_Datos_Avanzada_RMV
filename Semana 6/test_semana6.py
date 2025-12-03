import pytest
import math
from Semana6 import WeightedGraph

def test_dijkstra_simple():
    # Case 1: Grafo ponderado simple
    g = WeightedGraph(4)
    g.add_edge(0, 1, 10)
    g.add_edge(0, 2, 5)
    g.add_edge(2, 3, 2)
    g.add_edge(1, 3, 3)
    
    dist, _ = g.dijkstra(0)
    assert dist[3] == 7
    assert math.isinf(dist[3]) == False

def test_dijkstra_zero_weight():
    # Case 2: Grafo con pesos cero
    g = WeightedGraph(3)
    g.add_edge(0, 1, 0)
    g.add_edge(1, 2, 5)
    
    dist, _ = g.dijkstra(0)
    assert dist[2] == 5

def test_dijkstra_disconnected():
    # Case 3: Grafo desconectado
    g = WeightedGraph(3)
    g.add_edge(0, 1, 10)
    
    dist, _ = g.dijkstra(0)
    assert math.isinf(dist[2])

def test_dijkstra_single_node():
    # Case 4: Nodo único
    g = WeightedGraph(1)
    
    dist, _ = g.dijkstra(0)
    assert dist[0] == 0

def test_dijkstra_multiple_paths():
    # Case 5: Camino más corto con múltiples opciones
    # Note: The table in HTML had conflicting math (4+1=5, not 3). 
    # We use the input values provided and assert the correct mathematical result (5).
    g = WeightedGraph(4)
    g.add_edge(0, 1, 4)
    g.add_edge(0, 2, 2)
    g.add_edge(1, 3, 1)
    g.add_edge(2, 3, 3)
    
    dist, _ = g.dijkstra(0)
    assert dist[3] == 5

def test_floyd_warshall_simple():
    # Case 6: Grafo denso pequeño
    g = WeightedGraph(3)
    g.add_edge(0, 1, 4)
    g.add_edge(1, 2, 2)
    g.add_edge(2, 0, 3)
    
    fw = g.floyd_warshall()
    assert fw[0][2] == 6  # 0-1-2 (4+2=6)

def test_floyd_warshall_negative_no_cycle():
    # Case 7: Con pesos negativos (sin ciclo)
    g = WeightedGraph(3)
    g.add_edge(0, 1, 2)
    g.add_edge(1, 2, -1)
    
    fw = g.floyd_warshall()
    assert fw[0][2] == 1

def test_floyd_warshall_negative_cycle():
    # Case 8: Ciclo negativo detectado
    g = WeightedGraph(2)
    g.add_edge(0, 1, -2)
    g.add_edge(1, 0, -1)
    
    with pytest.raises(ValueError):
        g.floyd_warshall()

def test_floyd_warshall_complete_graph():
    # Case 9: Grafo completo (3 nodos, todas aristas)
    g = WeightedGraph(3)
    # 0<->1, 1<->2, 2<->0
    g.add_edge(0, 1, 1)
    g.add_edge(1, 0, 1)
    g.add_edge(1, 2, 1)
    g.add_edge(2, 1, 1)
    g.add_edge(2, 0, 1)
    g.add_edge(0, 2, 1)
    
    fw = g.floyd_warshall()
    # Direct edges are all 1, so shortest path between any pair is 1
    assert fw[0][1] == 1
    assert fw[0][2] == 1
    assert fw[1][2] == 1

def test_floyd_warshall_disconnected():
    # Case 10: Desconectado
    g = WeightedGraph(3)
    g.add_edge(0, 1, 10)
    
    fw = g.floyd_warshall()
    assert math.isinf(fw[0][2])

# Edge cases
def test_dijkstra_non_existent_src():
    g = WeightedGraph(1)
    with pytest.raises(IndexError):
        g.dijkstra(1)

def test_floyd_warshall_empty():
    g = WeightedGraph(0)
    with pytest.raises(ValueError):
        g.floyd_warshall()

if __name__ == "__main__":
    pytest.main([__file__, "-v"])