from collections import deque

def bfs(grafo, nodo_inicio):
    # Conjunto para llevar registro de nodos visitados y evitar ciclos
    visitados = set()
    
    # Cola para gestionar los nodos pendientes de explorar (FIFO)
    cola = deque([nodo_inicio])
    
    # Marcamos el inicio como visitado
    visitados.add(nodo_inicio)
    
    print(f"Iniciando recorrido BFS desde: {nodo_inicio}")
    
    while cola:
        # Sacamos el primer elemento de la cola (el más antiguo)
        nodo_actual = cola.popleft()
        print(f" -> Visitando: {nodo_actual}")
        
        # Exploramos los vecinos del nodo actual
        for vecino in grafo[nodo_actual]:
            if vecino not in visitados:
                visitados.add(vecino)
                cola.append(vecino)

# --- Bloque de Prueba ---

if __name__ == "__main__":
    # Representación del grafo usando lista de adyacencia (Diccionario)
    mi_grafo = {
        'A': ['B', 'C'],
        'B': ['D', 'E'],
        'C': ['F'],
        'D': [],
        'E': ['F'],
        'F': []
    }

    # Ejecutamos el algoritmo
    bfs(mi_grafo, 'A')