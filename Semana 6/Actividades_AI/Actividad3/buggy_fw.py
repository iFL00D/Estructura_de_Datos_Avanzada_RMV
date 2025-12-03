import math

def floyd_warshall_buggy(n, edges):
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
                    
    # BUG: Falta la detección de ciclos negativos
    # Debería verificar si dist[i][i] < 0
    
    return dist

# Test Case del Prompt
# 0->1:2, 1->2:-1, 2->0:-4
# Ciclo: 0->1->2->0 = 2 + (-1) + (-4) = -3 (Ciclo Negativo)
edges = [
    (0, 1, 2),
    (1, 2, -1),
    (2, 0, -4)
]
n = 3

try:
    result = floyd_warshall_buggy(n, edges)
    print("Resultado obtenido (dist matrix):")
    for row in result:
        print(row)
    print(f"Distancia 0->0: {result[0][0]}")
    if result[0][0] < 0:
        print("¡ERROR! Se calculó una distancia negativa de un nodo a sí mismo, pero no se lanzó excepción.")
except ValueError as e:
    print(f"Excepción capturada correctamente: {e}")