import unittest
import math
from optimized_dijkstra import OptimizedGraph

class TestOptimizedDijkstra(unittest.TestCase):
    def setUp(self):
        self.g = OptimizedGraph()

    def test_basic_path(self):
        # Grafo simple
        # A -> B (4)
        # A -> C (2) -> B (1) = 3
        self.g.add_edge('A', 'B', 4)
        self.g.add_edge('A', 'C', 2)
        self.g.add_edge('C', 'B', 1)
        
        dist, parent = self.g.dijkstra('A')
        self.assertEqual(dist['B'], 3)
        self.assertEqual(self.g.get_path(parent, 'B'), ['A', 'C', 'B'])

    def test_disconnected_graph(self):
        self.g.add_edge('A', 'B', 1)
        self.g.add_edge('C', 'D', 1)
        
        dist, _ = self.g.dijkstra('A')
        self.assertEqual(dist['A'], 0)
        self.assertEqual(dist['B'], 1)
        self.assertEqual(dist['C'], math.inf)
        self.assertEqual(dist['D'], math.inf)

    def test_non_existent_start_node(self):
        with self.assertRaises(ValueError):
            self.g.dijkstra('Z')

    def test_mixed_node_types(self):
        # Probar flexibilidad de tipos (int y str)
        self.g.add_edge(1, 'Two', 5.5)
        dist, parent = self.g.dijkstra(1)
        self.assertEqual(dist['Two'], 5.5)
        self.assertEqual(self.g.get_path(parent, 'Two'), [1, 'Two'])

if __name__ == '__main__':
    unittest.main()