from collections import defaultdict
from typing import Dict, List, Tuple
import os

def load_graph(file_path: str, is_directed: bool = True) -> Dict[str, List[Tuple[str, float]]]:
    """
    Carga un grafo desde un archivo de texto con manejo robusto de errores.
    
    Args:
        file_path: Ruta al archivo de aristas
        is_directed: True para grafo dirigido, False para no dirigido
    
    Returns:
        Diccionario con lista de adyacencia
    """
    adjacency_list = defaultdict(list)
    
    if not os.path.exists(file_path):
        print(f"❌ Error: El archivo '{file_path}' no existe.")
        return adjacency_list
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line_num, line in enumerate(file, 1):
                line = line.strip()
                
                # Ignorar líneas vacías y comentarios
                if not line or line.startswith('#'):
                    continue
                
                parts = line.split()
                if len(parts) < 2:
                    print(f"⚠️  Línea {line_num}: '{line}' ignorada (faltan vértices)")
                    continue
                
                from_vertex, to_vertex = parts[0], parts[1]
                
                # Procesar peso con validación
                try:
                    weight = float(parts[2]) if len(parts) > 2 else 1.0
                except (ValueError, IndexError):
                    print(f"⚠️  Línea {line_num}: peso inválido, usando 1.0")
                    weight = 1.0
                
                # Agregar arista
                adjacency_list[from_vertex].append((to_vertex, weight))
                
                # Si es no dirigido, agregar arista inversa
                if not is_directed:
                    adjacency_list[to_vertex].append((from_vertex, weight))
                    
    except FileNotFoundError:
        print(f"❌ Error: No se encontró el archivo '{file_path}'")
    except Exception as e:
        print(f"❌ Error inesperado al leer '{file_path}': {e}")
    
    return dict(adjacency_list)

def get_neighbors(graph: Dict[str, List[Tuple[str, float]]], vertex: str) -> List[Tuple[str, float]]:
    """Obtiene la lista de vecinos de un vértice."""
    return graph.get(vertex, [])

def has_edge(graph: Dict[str, List[Tuple[str, float]]], from_vertex: str, to_vertex: str) -> bool:
    """
    CORREGIDO: Verifica si existe una arista de from_vertex a to_vertex.
    Sintaxis corregida para desempaquetado de tuplas.
    """
    neighbors = graph.get(from_vertex, [])
    return any(neighbor == to_vertex for neighbor, _ in neighbors)

def get_out_degree(graph: Dict[str, List[Tuple[str, float]]], vertex: str) -> int:
    """Calcula el grado de salida de un vértice."""
    return len(graph.get(vertex, []))

def get_in_degree(graph: Dict[str, List[Tuple[str, float]]], vertex: str) -> int:
    """Calcula el grado de entrada de un vértice."""
    in_degree = 0
    for neighbors in graph.values():
        in_degree += sum(1 for neighbor, _ in neighbors if neighbor == vertex)
    return in_degree

def analyze_graph(graph: Dict[str, List[Tuple[str, float]]], graph_type: str):
    """Analiza y muestra estadísticas detalladas del grafo."""
    print(f"\n{'='*50}")
    print(f"🔍 Análisis del Grafo {graph_type}")
    print(f"{'='*50}")
    
    if not graph:
        print("⚠️  El grafo está vacío")
        return
    
    vertices = sorted(graph.keys())
    total_edges = sum(len(neighbors) for neighbors in graph.values())
    
    print(f"📊 Estadísticas generales:")
    print(f"   • Vértices: {len(vertices)}")
    print(f"   • Aristas: {total_edges}")
    
    # Calcular densidad (para grafos dirigidos)
    max_possible_edges = len(vertices) * (len(vertices) - 1)
    if max_possible_edges > 0:
        density = total_edges / max_possible_edges
        print(f"   • Densidad: {density:.3f}")
    
    print(f"\n🔍 Detalles por vértice:")
    for vertex in vertices:
        out_deg = get_out_degree(graph, vertex)
        in_deg = get_in_degree(graph, vertex)
        neighbors = get_neighbors(graph, vertex)
        
        neighbor_str = ", ".join([f"{neighbor}({weight:.1f}km)" for neighbor, weight in neighbors])
        
        print(f"   {vertex}: Out-degree={out_deg}, In-degree={in_deg}")
        print(f"      └─ Vecinos: [{neighbor_str}]")

def find_most_connected_vertex(graph: Dict[str, List[Tuple[str, float]]]) -> str:
    """Encuentra el vértice con mayor grado total (entrada + salida)."""
    if not graph:
        return ""
    
    max_degree = 0
    most_connected = ""
    
    for vertex in graph.keys():
        total_degree = get_out_degree(graph, vertex) + get_in_degree(graph, vertex)
        if total_degree > max_degree:
            max_degree = total_degree
            most_connected = vertex
    
    return most_connected



#Hakimi algoritmo 
from typing import List

def is_graphical_sequence(degrees: List[int]) -> bool:
    """
    Valida secuencia gráfica con Havel-Hakimi.
    Complejidad: O(n² log n) por reordenamiento en cada iteración.
    """
    if not degrees:
        return True
    
    # Crear copia para no modificar original
    seq = sorted(degrees, reverse=True)
    
    # Verificar suma par y máx grado
    total_sum = sum(seq)
    if total_sum % 2 != 0 or seq[0] >= len(seq):
        return False
    
    while seq:
        d1 = seq.pop(0)
        
        if d1 == 0:
            return True
        
        if d1 > len(seq):
            return False
        
        # Restar 1 de los siguientes d1
        for i in range(d1):
            seq[i] -= 1
            if seq[i] < 0:
                return False
        
        # CRÍTICO: Reordenar después de modificar
        seq.sort(reverse=True)
    
    return True

def validate_consistency(graph) -> bool:
    """
    Verifica consistencia: suma de grados debe ser par en grafo no dirigido.
    Nota: Para grafos grandes, optimiza usando in_degree() directamente.
    """
    # vertices = list(graph.adj.keys())
    # total_degree = sum(len(graph.adj[v]) for v in vertices)
    # # En grafo no dirigido, suma de grados = 2 * |aristas|
    # return total_degree % 2 == 0

     # Suma la longitud de cada lista de vecinos (que es el grado de cada vértice)
    total_degree = sum(len(neighbors) for neighbors in graph.values())
    
    # En cualquier grafo, la suma de los grados siempre debe ser par.
    return total_degree % 2 == 0

def extract_degree_sequence(graph) -> List[int]:
    """
    Extrae secuencia de grados del grafo de Semana 3.
    Útil para validar el mapa urbano como secuencia gráfica.
    
    Enlace directo con proyecto: usa esta función para extraer grados
    de tu mapa urbano y validar con is_graphical_sequence().
    """
    # degrees = sorted([len(graph.adj[v]) for v in graph.adj.keys()], reverse=True)

    # return degrees

     # Obtiene la longitud (grado) de cada lista de vecinos en el diccionario
    degrees = [len(neighbors) for neighbors in graph.values()]
    
    # Devuelve la lista ordenada en modo descendente
    return sorted(degrees, reverse=True)


def adjMatrix(graph: Dict[str, List[Tuple[str, float]]]) -> List[List[int]]:
    """Convierte lista de adyacencia a matriz de adyacencia."""
    vertices = sorted(graph.keys())
    index_map = {vertex: idx for idx, vertex in enumerate(vertices)}
    size = len(vertices)
    
    # Inicializar matriz con ceros
    matrix = [[0]*size for _ in range(size)]
    
    for from_vertex, neighbors in graph.items():
        from_idx = index_map[from_vertex]
        for to_vertex, _ in neighbors:
            to_idx = index_map[to_vertex]
            matrix[from_idx][to_idx] = 1  # Usar 1 para indicar arista
    
    return matrix, index_map

def verify_consistency(
    graph: Dict[str, List[Tuple[str, float]]], 
    matrix: List[List[int]], 
    index_map: Dict[str, int]
) -> List[str]:
    """
    Compara la lista de adyacencia y la matriz para encontrar inconsistencias.
    
    Returns:
        Una lista de mensajes de error. Si está vacía, todo es consistente.
    """
    inconsistencies = []
    
    # Invertir el mapa para facilitar la búsqueda (índice -> nombre de vértice)
    vertex_map = {idx: vertex for vertex, idx in index_map.items()}
    
    # 1. Verificación: Lista -> Matriz
    # Cada arista en la lista debe ser un '1' en la matriz.
    for from_vertex, neighbors in graph.items():
        for to_vertex, _ in neighbors:
            if from_vertex in index_map and to_vertex in index_map:
                from_idx = index_map[from_vertex]
                to_idx = index_map[to_vertex]
                if matrix[from_idx][to_idx] == 0:
                    error_msg = f"❌ Inconsistencia: Arista {from_vertex}→{to_vertex} existe en la lista pero no en la matriz."
                    inconsistencies.append(error_msg)

    # 2. Verificación: Matriz -> Lista
    # Cada '1' en la matriz debe corresponder a una arista en la lista.
    for from_idx, row in enumerate(matrix):
        for to_idx, value in enumerate(row):
            if value == 1:
                from_vertex = vertex_map[from_idx]
                to_vertex = vertex_map[to_idx]
                # Usamos tu función has_edge para verificar
                if not has_edge(graph, from_vertex, to_vertex):
                    error_msg = f"❌ Inconsistencia: Arista {from_vertex}→{to_vertex} existe en la matriz pero no en la lista."
                    inconsistencies.append(error_msg)
                    
    return inconsistencies

# Programa principal
def main():
    """Función principal para análisis de grafos."""
    print("🌍 === Análisis de Mapas de Tráfico - Proyecto Semana 3 ===")
    
    # Analizar grafo no dirigido
    undirected_graph = load_graph("edges_undirected.txt", is_directed=False)
    analyze_graph(undirected_graph, "No Dirigido")
    
    # Analizar grafo dirigido
    directed_graph = load_graph("edges_directed.txt", is_directed=True)
    analyze_graph(directed_graph, "Dirigido")
    
    # Pruebas de conectividad
    print(f"\n{'='*50}")
    print("🔗 Pruebas de Conectividad")
    print(f"{'='*50}")
    
    if directed_graph:
        print(f"¿A→G dirigido? {has_edge(directed_graph, 'A', 'G')} (esperado: True)")
        print(f"¿G→A dirigido? {has_edge(directed_graph, 'G', 'A')} (esperado: False)")
        
        if 'A' in directed_graph:
            print(f"Grado de salida de A: {get_out_degree(directed_graph, 'A')}")
            print(f"Grado de entrada de A: {get_in_degree(directed_graph, 'A')}")
        
        # Análisis adicional
        most_connected = find_most_connected_vertex(directed_graph)
        if most_connected:
            print(f"Vértice más conectado: {most_connected}")
    
    print("\n🎉 ¡Análisis completado exitosamente!")






    #Implementación Hakimi
    print("=== Pruebas de Havel-Hakimi ===\n")
    
    # Caso válido
    seq_valid = [4, 3, 3, 2, 2, 2, 1, 1]
    print(f"Caso 1: {seq_valid}")
    print(f"Resultado: {'✓ Gráfica' if is_graphical_sequence(seq_valid) else '✖ No Gráfica'}\n")
    seq_valid = [3, 2, 2, 1]
    print(f"Caso 2: {seq_valid}")
    print(f"Resultado: {'✓ Gráfica' if is_graphical_sequence(seq_valid) else '✖ No Gráfica'}\n")
    seq_valid= [4, 3, 3, 2, 2, 2]
    print(f"Caso 3: {seq_valid}")
    print(f"Resultado: {'✓ Gráfica' if is_graphical_sequence(seq_valid) else '✖ No Gráfica'}\n")
    seq_valid = [0, 0, 0, 0]	
    print(f"Caso 4: {seq_valid}")
    print(f"Resultado: {'✓ Gráfica' if is_graphical_sequence(seq_valid) else '✖ No Gráfica'}\n")
    seq_valid = [3, 3, 3, 3]
    print(f"Caso 5: {seq_valid}")
    print(f"Resultado: {'✓ Gráfica' if is_graphical_sequence(seq_valid) else '✖ No Gráfica'}\n")

    # Caso NO válido (corregido)
    seq_invalid = [3, 3, 3, 1]
    print(f"Caso 1: {seq_invalid}")
    print(f"Resultado: {'✓ Gráfica' if is_graphical_sequence(seq_invalid) else '✖ No Gráfica'}\n")
    seq_invalid =[5, 5, 4, 3, 2, 1]
    print(f"Caso 2: {seq_invalid}")
    print(f"Resultado: {'✓ Gráfica' if is_graphical_sequence(seq_invalid) else '✖ No Gráfica'}\n")
    seq_invalid = [3, 2, 1]	
    print(f"Caso 3: {seq_invalid}")
    print(f"Resultado: {'✓ Gráfica' if is_graphical_sequence(seq_invalid) else '✖ No Gráfica'}\n")
    seq_invalid = [6, 1, 1, 1, 1, 1, 1]	
    print(f"Caso 4: {seq_invalid}")
    print(f"Resultado: {'✓ Gráfica' if is_graphical_sequence(seq_invalid) else '✖ No Gráfica'}\n")
    seq_invalid = [5, 3, 2, 2, 1]	
    print(f"Caso 4: {seq_invalid}")
    print(f"Resultado: {'✓ Gráfica' if is_graphical_sequence(seq_invalid) else '✖ No Gráfica'}\n")


    # Conectar con Semana 3 (requiere tu código de Semana 3)
    # Ejemplo de extracción de secuencia:
    # from grafo import load_graph
    graph = load_graph("edges_undirected.txt", is_directed=False)
    extracted_seq = extract_degree_sequence(graph)
    print(f"Secuencia del mapa urbano: {extracted_seq}")
    print(f"¿Es gráfica? {is_graphical_sequence(extracted_seq)}")
    print(f"¿Consistente? {validate_consistency(graph)}")

    #matriz de adjacencia
    print("\n=== Matriz de Adyacencia ===")
    abc = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    matrix,index_map = adjMatrix(directed_graph)
    for letra in abc[:len(matrix)]:
        print("\t", letra, end=" ")
    print()
    for fila in matrix:
        print(abc[matrix.index(fila)], end=" ")
        for valor in fila:
            print("\t", valor, end=" ")
        print()


    print("\n" + "="*50)
    print("Verificación de Consistencia: Lista vs. Matriz")
    print("="*50)

    if directed_graph:
        inconsistencies = verify_consistency(directed_graph, matrix, index_map)
        if not inconsistencies:
            print("¡Éxito! La lista de adyacencia y la matriz son consistentes.")
        else:
            print("Se encontraron las siguientes inconsistencias:")
            for error in inconsistencies:
                print(f"   • {error}")
    else:
        print("No se puede verificar la consistencia porque el grafo está vacío.")




if __name__ == "__main__":
    main()
