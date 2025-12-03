import math

def floyd_warshall_fixed(n, edges):
    # Inicialización
    dist = [[math.inf] * n for _ in range(n)]
    for i in range(n):
        dist[i][i] = 0
        
    for u, v, w in edges:
        dist[u][v] = w
        
    # Algoritmo FW
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
                    
    # CORRECCIÓN: Detección de ciclos negativos
    # Si la distancia de un nodo a sí mismo es negativa, existe un ciclo negativo
    for i in range(n):
        if dist[i][i] < 0:
            raise ValueError("Ciclo negativo detectado")
    
    return dist

# Test Case
edges = [
    (0, 1, 2),
    (1, 2, -1),
    (2, 0, -4)
]
n = 3

try:
    result = floyd_warshall_fixed(n, edges)
    print("Resultado obtenido:")
    for row in result:
        print(row)
except ValueError as e:
    print(f"ÉXITO: {e}")