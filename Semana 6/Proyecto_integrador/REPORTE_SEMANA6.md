# 📄 Reporte Técnico: Optimización de Rutas Urbanas

**Proyecto Integrador - Avance 4 (Semana 6)**

---

## 1. Introducción

En este avance se integraron algoritmos de grafos ponderados (**Dijkstra** y **Floyd-Warshall**) al sistema de análisis de tráfico urbano. El objetivo principal fue calcular rutas óptimas considerando distancias y tiempos, así como simular escenarios de tráfico dinámico para evaluar la resiliencia de la red.

## 2. Implementación Técnica

### 2.1 Clases Desarrolladas

-   **`WeightedGraph`**: Hereda de `GraphTraversal`. Implementa:
    -   `dijkstra(start_node)`: Usa `heapq` para complejidad $O((V+E)\log V)$.
    -   `floyd_warshall()`: Programación dinámica $O(V^3)$ para todos los pares.
    -   Detección de ciclos negativos.
-   **`RouteOptimizer`**: Clase para casos de uso avanzados.
    -   Simulación de tráfico global y localizado.
    -   Comparación de rutas bajo diferentes condiciones.

### 2.2 Pruebas Unitarias

Se implementaron **12 tests unitarios** cubriendo:

-   Caminos simples y complejos.
-   Grafos desconectados.
-   Pesos negativos (Floyd-Warshall).
-   Detección de ciclos negativos.
-   Reconstrucción de caminos.

---

## 3. Análisis de Centralidad (Resultados Reales)

Utilizando el algoritmo de **Floyd-Warshall**, se calculó el tiempo promedio de viaje desde cada estación a todas las demás para identificar los nodos más críticos ("centrales").

| Ranking | Estación | Tiempo Promedio (min) | Interpretación                                                   |
| :-----: | :------: | :-------------------: | :--------------------------------------------------------------- |
|    1    |  **B**   |         4.00          | Nodo más accesible de la red. Ideal para centro de distribución. |
|    2    |  **C**   |         4.00          | Co-líder en centralidad.                                         |
|    3    |  **A**   |         4.14          | Alta conectividad, cercano al óptimo.                            |
|    4    |  **D**   |         4.29          | Conectividad media.                                              |
|    5    |  **E**   |         6.29          | Nodo periférico, mayor costo de acceso.                          |

> **Insight:** Las estaciones B y C son los puntos neurálgicos de la red. Cualquier interrupción en ellas afectaría desproporcionadamente al tiempo promedio de viaje global.

---

## 4. Caso de Uso: Simulador de Tráfico Dinámico

Se simuló el impacto del tráfico en la ruta **A -> H**.

### Escenario Base

-   **Ruta:** A -> B -> H
-   **Tiempo:** 5.00 min
-   **Condición:** Tráfico normal.

### Escenario 1: Hora Pico (Congestión Global +20%)

-   **Ruta:** A -> B -> H
-   **Tiempo:** 6.00 min (+1.00 min)
-   **Análisis:** La ruta óptima se mantiene, pero el tiempo aumenta linealmente. La red no ofrece alternativas más rápidas bajo congestión uniforme.

### Escenario 2: Accidente en Nodo B (Congestión x5)

-   **Ruta:** A -> G -> H
-   **Tiempo:** 7.00 min
-   **Análisis:** El algoritmo detectó que el costo de pasar por B (ahora muy alto) hacía inviable la ruta original. Automáticamente redirigió el tráfico por G.
-   **Impacto:** Se evitó una ruta que habría tomado teóricamente 25 minutos (5 min \* 5), reduciendo el impacto a solo 7 minutos.

---

## 5. Análisis Comparativo: Dijkstra vs Floyd-Warshall

| Característica              | Dijkstra                 | Floyd-Warshall | Ganador en este Contexto                |
| :-------------------------- | :----------------------- | :------------- | :-------------------------------------- |
| **Complejidad Temporal**    | $O((V+E)\log V)$         | $O(V^3)$       | **Dijkstra** (para consultas puntuales) |
| **Tiempo Ejecución (A->H)** | ~0.000016 seg            | ~0.000138 seg  | **Dijkstra (8.5x más rápido)**          |
| **Uso de Memoria**          | $O(V)$                   | $O(V^2)$       | **Dijkstra**                            |
| **Pesos Negativos**         | No soportado             | Soportado      | **Floyd-Warshall**                      |
| **Todos los Pares**         | Requiere $V$ ejecuciones | Nativo         | **Floyd-Warshall** (para centralidad)   |

### Reflexión

En nuestro grafo de prueba (pequeño/mediano), **Dijkstra escaló significativamente mejor** para consultas de ruta única, siendo casi un orden de magnitud más rápido. Sin embargo, **Floyd-Warshall** fue indispensable para el análisis de centralidad, ya que calcular la matriz completa con Dijkstra habría requerido iterar sobre todos los nodos, complicando el código sin gran beneficio en grafos densos pequeños.

Para una aplicación de GPS en tiempo real (como Waze), **Dijkstra** (o A\*) es la elección obvia debido a la necesidad de respuesta rápida y la dispersión del grafo vial. Floyd-Warshall queda reservado para análisis estáticos de planificación urbana o logística pre-computada.

---

## 6. Visualización de la Matriz de Distancias (Resumida)

| De \ A  |  A  |  B  |  C  |  D  |  E  | ... |
| :-----: | :-: | :-: | :-: | :-: | :-: | :-: |
|  **A**  |  0  |  2  |  5  |  3  |  7  | ... |
|  **B**  |  ∞  |  0  |  3  |  1  |  5  | ... |
|  **C**  |  ∞  |  ∞  |  0  |  ∞  |  2  | ... |
| **...** | ... | ... | ... | ... | ... | ... |

_(Valores ilustrativos basados en la ejecución del script)_

---

## 7. Conclusión

La integración de algoritmos ponderados ha transformado el proyecto de un simple mapa de conectividad a una herramienta de toma de decisiones. La capacidad de simular tráfico y redirigir rutas dinámicamente demuestra la potencia de los grafos ponderados en problemas del mundo real.
