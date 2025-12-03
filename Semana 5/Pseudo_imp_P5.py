#|==================================================================================================================================|
#|  Este código cubre: Modelado (1), Detección de Ciclos (2), Ordenamiento Topológico (3), Paralelismo (4) y Semestres Mínimos (5). |
#|==================================================================================================================================|
from collections import deque, defaultdict

class SistemaMallaCurricular:
    def __init__(self):
        # 1. Modelado del Grafo
        self.grafo = defaultdict(list)
        self.in_degree = defaultdict(int)
        self.materias = set()

    def agregar_materia(self, materia, requisitos=[]):
        """Agrega nodo y aristas al grafo."""
        self.materias.add(materia)
        if materia not in self.in_degree:
            self.in_degree[materia] = 0
            
        for req in requisitos:
            self.grafo[req].append(materia)
            self.in_degree[materia] += 1
            self.materias.add(req)
            if req not in self.in_degree:
                self.in_degree[req] = 0

    def generar_plan_estudios(self):
        """
        Funcionalidades 2, 3, 4 y 5:
        - Detecta ciclos
        - Genera Topo Sort
        - Agrupa por semestres (paralelismo)
        """
        # Cola para algoritmo de Kahn (materias con 0 requisitos pendientes)
        cola = deque([m for m in self.in_degree if self.in_degree[m] == 0])
        
        plan_por_semestre = []
        materias_ordenadas = []
        
        while cola:
            # Nivel actual (Semestre actual)
            # Todo lo que está en la cola en este momento se puede cursar en paralelo
            semestre_actual = []
            
            # Procesamos todos los nodos de este nivel (BFS por capas)
            for _ in range(len(cola)):
                materia_actual = cola.popleft()
                semestre_actual.append(materia_actual)
                materias_ordenadas.append(materia_actual)
                
                # Reducir in-degree de los vecinos
                for vecino in self.grafo[materia_actual]:
                    self.in_degree[vecino] -= 1
                    if self.in_degree[vecino] == 0:
                        cola.append(vecino)
            
            plan_por_semestre.append(semestre_actual)

        # 2. Detección de configuración inválida (Ciclos)
        if len(materias_ordenadas) != len(self.in_degree):
            raise ValueError("¡Error Crítico! Se detectó una dependencia circular (Ciclo). El plan de estudios es imposible.")

        return plan_por_semestre