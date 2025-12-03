import unittest
from mst import NetworkDesigner

class TestMSTAlgorithms(unittest.TestCase):

    def setUp(self):
        pass

    def test_simple_triangle(self):
        """Case 1: Simple triangle"""
        g = NetworkDesigner(3)
        g.add_edge(0, 1, 10)
        g.add_edge(1, 2, 10)
        g.add_edge(0, 2, 5)
        
        # MST should be (0,2,5) and either (0,1,10) or (1,2,10) -> Total 15
        _, cost_prim = g.prim_mst()
        _, cost_kruskal = g.kruskal_mst()
        
        self.assertEqual(cost_prim, 15)
        self.assertEqual(cost_kruskal, 15)

    def test_disconnected_graph(self):
        """Case 2: Disconnected graph (Forest)"""
        g = NetworkDesigner(4)
        g.add_edge(0, 1, 5)
        g.add_edge(2, 3, 10)
        # No connection between {0,1} and {2,3}
        
        # Prim starting at 0 will only find edge (0,1) -> cost 5
        # Kruskal will find (0,1) and (2,3) -> cost 15
        # Note: Standard Prim only finds MST for the component of start_node.
        # Kruskal finds MSF (Minimum Spanning Forest).
        
        _, cost_prim = g.prim_mst(0)
        _, cost_kruskal = g.kruskal_mst()
        
        self.assertEqual(cost_prim, 5)
        self.assertEqual(cost_kruskal, 15)

    def test_linear_chain(self):
        """Case 3: Linear chain"""
        g = NetworkDesigner(4)
        g.add_edge(0, 1, 1)
        g.add_edge(1, 2, 2)
        g.add_edge(2, 3, 3)
        
        # MST is the graph itself -> cost 6
        _, cost_prim = g.prim_mst()
        _, cost_kruskal = g.kruskal_mst()
        
        self.assertEqual(cost_prim, 6)
        self.assertEqual(cost_kruskal, 6)

    def test_complete_graph_k4(self):
        """Case 4: Complete graph K4 with varying weights"""
        g = NetworkDesigner(4)
        # Edges: (0,1,1), (0,2,2), (0,3,3), (1,2,4), (1,3,5), (2,3,6)
        g.add_edge(0, 1, 1)
        g.add_edge(0, 2, 2)
        g.add_edge(0, 3, 3)
        g.add_edge(1, 2, 4)
        g.add_edge(1, 3, 5)
        g.add_edge(2, 3, 6)
        
        # MST should use edges (0,1,1), (0,2,2), (0,3,3) -> Total 6
        # Why? 1, 2, 3 are cheapest edges connecting 0 to others.
        # Let's trace:
        # Kruskal: (0,1,1) ok, (0,2,2) ok, (0,3,3) ok. Next is (1,2,4) cycle.
        
        _, cost_prim = g.prim_mst()
        _, cost_kruskal = g.kruskal_mst()
        
        self.assertEqual(cost_prim, 6)
        self.assertEqual(cost_kruskal, 6)

    def test_complex_graph(self):
        """Case 5: Larger complex graph"""
        g = NetworkDesigner(9)
        # Example from GeeksforGeeks or similar standard example
        # 0-1: 4, 0-7: 8
        # 1-2: 8, 1-7: 11
        # 2-3: 7, 2-8: 2, 2-5: 4
        # 3-4: 9, 3-5: 14
        # 4-5: 10
        # 5-6: 2
        # 6-7: 1, 6-8: 6
        # 7-8: 7
        
        edges = [
            (0, 1, 4), (0, 7, 8),
            (1, 2, 8), (1, 7, 11),
            (2, 3, 7), (2, 8, 2), (2, 5, 4),
            (3, 4, 9), (3, 5, 14),
            (4, 5, 10),
            (5, 6, 2),
            (6, 7, 1), (6, 8, 6),
            (7, 8, 7)
        ]
        
        for u, v, w in edges:
            g.add_edge(u, v, w)
            
        # Expected MST Cost: 37
        # Edges: (6,7,1), (2,8,2), (5,6,2), (0,1,4), (2,5,4), (2,3,7), (0,7,8), (3,4,9)
        # Sum: 1+2+2+4+4+7+8+9 = 37
        
        _, cost_prim = g.prim_mst()
        _, cost_kruskal = g.kruskal_mst()
        
        self.assertEqual(cost_prim, 37)
        self.assertEqual(cost_kruskal, 37)

if __name__ == '__main__':
    unittest.main()