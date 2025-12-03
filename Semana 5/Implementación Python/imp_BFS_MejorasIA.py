from collections import deque
from typing import Dict, List, Optional, Any

# Optimización sugerida por IA: [Claridad] Agregamos Type Hints para saber qué datos entran y salen
def bfs_mejorado(grafo: Dict[str, List[str]], nodo_inicio: str) -> Dict[str, int]:
    """
    Realiza BFS y devuelve un diccionario con las distancias desde el inicio.
    """
    
    # Optimización sugerida por IA: [Robustez] Validar que el nodo de inicio exista para evitar crashes
    if nodo_inicio not in grafo:
        print(f"Error: El nodo '{nodo_inicio}' no existe en el grafo.")
        return {}

    # Optimización sugerida por IA: [Extensibilidad] Guardamos distancias para darle más utilidad al algoritmo
    # Esto también sirve como conjunto de 'visitados' (si está en el dict, ya fue visitado)
    distancias = {nodo_inicio: 0}
    
    cola = deque([nodo_inicio])
    
    print(f"Iniciando recorrido BFS mejorado desde: {nodo_inicio}")
    
    while cola:
        nodo_actual = cola.popleft()
        
        # Optimización sugerida por IA: [Robustez] Usamos .get() por si un nodo hoja no está definido como clave
        vecinos = grafo.get(nodo_actual, [])
        
        for vecino in vecinos:
            if vecino not in distancias:
                # Optimización sugerida por IA: [Eficiencia] Marcamos visitado y calculamos distancia en un solo paso
                distancias[vecino] = distancias[nodo_actual] + 1
                cola.append(vecino)
                
    return distancias

# --- Bloque de Prueba (Validación) ---

if __name__ == "__main__":
    # Grafo de prueba
    mi_grafo = {
        'A': ['B', 'C'],
        'B': ['D', 'E'],
        'C': ['F'],
        'D': [],
        'E': ['F'],
        'F': []
    }

    print("--- Test 1: Grafo Normal ---")
    resultados = bfs_mejorado(mi_grafo, 'A')
    print("Distancias calculadas:", resultados)
    # Verificación: A es 0, B es 1, F debería ser 2 (camino A->C->F)
    
    print("\n--- Test 2: Caso Límite (Nodo Inexistente) ---")
    bfs_mejorado(mi_grafo, 'Z')