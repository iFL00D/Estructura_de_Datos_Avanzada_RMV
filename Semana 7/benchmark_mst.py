import time
import random
import matplotlib
matplotlib.use('Agg') # Use non-interactive backend
import matplotlib.pyplot as plt
from mst import NetworkDesigner

def generate_random_graph(num_nodes, density=0.3):
    """
    Generates a random connected graph.
    density: probability of an edge between any two nodes.
    """
    g = NetworkDesigner(num_nodes)
    max_edges = num_nodes * (num_nodes - 1) // 2
    target_edges = int(max_edges * density)
    
    # Ensure connectivity by creating a spanning tree first
    nodes = list(range(num_nodes))
    random.shuffle(nodes)
    for i in range(num_nodes - 1):
        u, v = nodes[i], nodes[i+1]
        w = random.randint(1, 100)
        g.add_edge(u, v, w)
        
    # Add remaining random edges
    current_edges = num_nodes - 1
    while current_edges < target_edges:
        u = random.randint(0, num_nodes - 1)
        v = random.randint(0, num_nodes - 1)
        if u != v:
            w = random.randint(1, 100)
            g.add_edge(u, v, w)
            current_edges += 1
            
    return g

def benchmark():
    sizes = [10, 100, 1000]
    prim_times = []
    kruskal_times = []
    
    print(f"{'Nodes':<10} | {'Prim (s)':<15} | {'Kruskal (s)':<15}")
    print("-" * 45)
    
    for n in sizes:
        # Generate graph
        g = generate_random_graph(n, density=0.2) # 20% density
        
        # Benchmark Prim
        start_time = time.time()
        g.prim_mst()
        prim_time = time.time() - start_time
        prim_times.append(prim_time)
        
        # Benchmark Kruskal
        start_time = time.time()
        g.kruskal_mst()
        kruskal_time = time.time() - start_time
        kruskal_times.append(kruskal_time)
        
        print(f"{n:<10} | {prim_time:<15.6f} | {kruskal_time:<15.6f}")

    # Optional: Plotting (if environment supports it, otherwise just print)
    try:
        plt.figure(figsize=(10, 6))
        plt.plot(sizes, prim_times, label='Prim', marker='o')
        plt.plot(sizes, kruskal_times, label='Kruskal', marker='x')
        plt.xlabel('Number of Nodes')
        plt.ylabel('Execution Time (seconds)')
        plt.title('MST Algorithm Performance Comparison')
        plt.legend()
        plt.grid(True)
        plt.savefig('Semana_7/benchmark_plot.png')
        print("\nBenchmark plot saved to 'Semana_7/benchmark_plot.png'")
    except Exception as e:
        print(f"\nCould not generate plot: {e}")

if __name__ == "__main__":
    benchmark()