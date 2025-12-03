import heapq
import math
import copy
from typing import Dict, List, Tuple, Any

class TransportNetwork:
    def __init__(self):
        self.adj = {}
        self.stations = set()

    def add_connection(self, u: str, v: str, time: float):
        if u not in self.adj: self.adj[u] = []
        if v not in self.adj: self.adj[v] = []
        self.adj[u].append((v, time))
        self.adj[v].append((u, time)) # Bidireccional
        self.stations.add(u)
        self.stations.add(v)

    def dijkstra(self, start: str) -> Dict[str, float]:
        dist = {node: math.inf for node in self.stations}
        dist[start] = 0
        pq = [(0, start)]
        
        while pq:
            d, u = heapq.heappop(pq)
            if d > dist[u]: continue
            
            for v, w in self.adj.get(u, []):
                if dist[u] + w < dist[v]:
                    dist[v] = dist[u] + w
                    heapq.heappush(pq, (dist[v], v))
        return dist

    def floyd_warshall(self) -> Dict[str, Dict[str, float]]:
        nodes = sorted(list(self.stations))
        dist = {u: {v: math.inf for v in nodes} for u in nodes}
        
        for u in nodes:
            dist[u][u] = 0
            for v, w in self.adj.get(u, []):
                dist[u][v] = min(dist[u][v], w) # Handle multiple edges
                
        for k in nodes:
            for i in nodes:
                for j in nodes:
                    if dist[i][k] + dist[k][j] < dist[i][j]:
                        dist[i][j] = dist[i][k] + dist[k][j]
        return dist

    def get_bottlenecks(self, top_n=3):
        # Centralidad de cercanía (Closeness Centrality) inversa
        # Menor promedio de distancia = Más central
        fw_matrix = self.floyd_warshall()
        avg_times = []
        
        for u in fw_matrix:
            total_dist = sum(d for d in fw_matrix[u].values() if d != math.inf)
            count = len([d for d in fw_matrix[u].values() if d != math.inf]) - 1 # Exclude self
            if count > 0:
                avg = total_dist / count
                avg_times.append((u, avg))
        
        return sorted(avg_times, key=lambda x: x[1])[:top_n]

    def simulate_closure(self, closed_station: str):
        print(f"\n--- Simulando cierre de estación: {closed_station} ---")
        original_adj = copy.deepcopy(self.adj)
        
        # Eliminar estación
        if closed_station in self.adj:
            del self.adj[closed_station]
        for u in self.adj:
            self.adj[u] = [(v, w) for v, w in self.adj[u] if v != closed_station]
            
        # Recalcular métricas
        try:
            new_bottlenecks = self.get_bottlenecks(1)
            if new_bottlenecks:
                print(f"Nueva estación más crítica: {new_bottlenecks[0][0]} (Avg time: {new_bottlenecks[0][1]:.2f})")
            else:
                print("La red quedó desconectada o vacía.")
        except Exception as e:
            print(f"Error en simulación: {e}")
            
        # Restaurar
        self.adj = original_adj

# Datos Reales (Aproximados) CDMX - Línea 1 y transbordos
network = TransportNetwork()
network.add_connection("Observatorio", "Tacubaya", 4)
network.add_connection("Tacubaya", "Juanacatlan", 3)
network.add_connection("Juanacatlan", "Chapultepec", 3)
network.add_connection("Chapultepec", "Sevilla", 2)
network.add_connection("Sevilla", "Insurgentes", 3)
network.add_connection("Insurgentes", "Cuauhtemoc", 2)
network.add_connection("Cuauhtemoc", "Balderas", 2)
network.add_connection("Balderas", "Salto del Agua", 2)
network.add_connection("Salto del Agua", "Isabel la Catolica", 2)
network.add_connection("Isabel la Catolica", "Pino Suarez", 2)

# Transbordos ficticios para hacer la red más interesante
network.add_connection("Tacubaya", "Balderas", 15) # Línea express ficticia
network.add_connection("Observatorio", "Pino Suarez", 25) # Bus directo

print("1. Calculando Tiempos desde Observatorio (Dijkstra)")
dists = network.dijkstra("Observatorio")
for st, time in dists.items():
    print(f"  -> {st}: {time} min")

print("\n2. Identificando Bottlenecks (Floyd-Warshall)")
bottlenecks = network.get_bottlenecks()
print("Estaciones más centrales (menor tiempo promedio a todas las demás):")
for st, avg in bottlenecks:
    print(f"  {st}: {avg:.2f} min")

print("\n3. Simulación de Impacto")
network.simulate_closure("Balderas")

print("\n4. Recomendación")
print("Basado en los bottlenecks, conectar 'Observatorio' con 'Insurgentes' reduciría la carga en la línea principal.")