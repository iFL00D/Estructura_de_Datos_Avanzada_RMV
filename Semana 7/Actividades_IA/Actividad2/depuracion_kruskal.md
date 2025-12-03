# Actividad 2: Depuración de implementación de Kruskal

## 1. Código del Estudiante (Con Error)

```python
class GraphMST:
    def __init__(self, vertices):
        self.V = vertices
        self.edges = []

    def add_edge(self, u, v, w):
        self.edges.append((u, v, w))

    def find(self, parent, i):
        if parent[i] == i:
            return i
        return self.find(parent, parent[i])

    def union(self, parent, rank, x, y):
        xroot = self.find(parent, x)
        yroot = self.find(parent, y)

        if rank[xroot] < rank[yroot]:
            parent[xroot] = yroot
        elif rank[xroot] > rank[yroot]:
            parent[yroot] = xroot
        else:
            parent[yroot] = xroot
            rank[xroot] += 1

    def kruskal_mst(self):
        result = []
        i = 0
        e = 0

        # ERROR: ¡Falta ordenar las aristas por peso!
        # self.edges = sorted(self.edges, key=lambda item: item[2])

        parent = []
        rank = []

        for node in range(self.V):
            parent.append(node)
            rank.append(0)

        while e < self.V - 1 and i < len(self.edges):
            u, v, w = self.edges[i]
            i = i + 1

            x = self.find(parent, u)
            y = self.find(parent, v)

            if x != y:
                e = e + 1
                result.append((u, v, w))
                self.union(parent, rank, x, y)

        cost = sum([w for u, v, w in result])
        return result, cost
```

### Grafo de Prueba

```python
g = GraphMST(4)
# Orden de inserción no ordenado por peso
g.add_edge(0, 1, 10)
g.add_edge(0, 2, 6)
g.add_edge(0, 3, 5)
g.add_edge(1, 3, 15)
g.add_edge(2, 3, 4)

# Resultado Esperado (MST Real):
# Aristas: (2,3,4), (0,3,5), (0,2,6) -> NO, (0,2) crea ciclo 0-3-2-0.
# Mejor: (2,3,4), (0,3,5). Falta conectar 1.
# (0,1,10) vs (1,3,15). (0,1) es mejor.
# MST: (2,3,4), (0,3,5), (0,1,10). Costo = 19.

# Resultado Obtenido con el código (sin ordenar):
# 1. (0,1,10) -> Aceptada.
# 2. (0,2,6)  -> Aceptada.
# 3. (0,3,5)  -> Aceptada. (0-1, 0-2, 0-3). Conectado.
# Costo = 10 + 6 + 5 = 21.
# ¡Incorrecto! (21 > 19)
```

---

## Respuesta de la IA

### 1. Identificación del Error

El error específico es que **las aristas no se están ordenando por peso** antes de iterar sobre ellas. La línea `self.edges = sorted(self.edges, key=lambda item: item[2])` está comentada o ausente.

### 2. Explicación del Comportamiento

El algoritmo de Kruskal es un algoritmo **voraz (greedy)**. Su premisa fundamental es intentar añadir siempre la arista **más barata disponible** que no forme un ciclo.

-   Si no ordenas las aristas, el algoritmo simplemente toma las primeras aristas que encuentra en la lista (el orden de inserción) y las añade si no forman ciclos.
-   Esto produce un **Árbol Generador** (es válido, conecta todo y no tiene ciclos), pero **no garantiza que sea Mínimo**. Simplemente es "el primer árbol que encontramos".
-   En el ejemplo, el algoritmo tomó la arista (0,1) con peso 10 porque apareció primero, bloqueando la posibilidad de usar caminos más baratos que podrían haber conectado el nodo 1 indirectamente (aunque en este caso específico la lógica es más compleja, el principio es que se toman decisiones subóptimas prematuramente).

### 3. Código Corregido

```python
    def kruskal_mst(self):
        result = []
        i = 0
        e = 0

        # CORRECCIÓN: Ordenar las aristas por peso (el tercer elemento de la tupla)
        # Esto es crucial para garantizar la propiedad 'greedy' del algoritmo.
        self.edges = sorted(self.edges, key=lambda item: item[2])

        parent = []
        rank = []

        for node in range(self.V):
            parent.append(node)
            rank.append(0)

        while e < self.V - 1 and i < len(self.edges):
            u, v, w = self.edges[i]
            i = i + 1

            x = self.find(parent, u)
            y = self.find(parent, v)

            if x != y:
                e = e + 1
                result.append((u, v, w))
                self.union(parent, rank, x, y)

        cost = sum([w for u, v, w in result])
        return result, cost
```

### 4. Casos de Prueba Adicionales

Estos casos ayudarían a detectar si el ordenamiento falta, poniendo aristas caras al principio de la definición del grafo.

1.  **Triángulo Simple Inverso:**

    -   `add_edge(0, 1, 100)` (Cara, agregada primero)
    -   `add_edge(1, 2, 1)`
    -   `add_edge(0, 2, 1)`
    -   _Sin ordenar:_ Toma (0,1,100) y (1,2,1). Costo 101.
    -   _Correcto:_ Toma (1,2,1) y (0,2,1). Costo 2.

2.  **Línea vs Puente:**

    -   Nodos 0, 1, 2, 3.
    -   `add_edge(0, 3, 10)` (Puente directo caro)
    -   `add_edge(0, 1, 1)`
    -   `add_edge(1, 2, 1)`
    -   `add_edge(2, 3, 1)`
    -   _Sin ordenar:_ Toma (0,3,10), (0,1,1), (1,2,1). Costo 12.
    -   _Correcto:_ (0,1), (1,2), (2,3). Costo 3.

3.  **Grafo Estrella Desordenado:**
    -   Centro 0. Hojas 1, 2, 3.
    -   `add_edge(1, 2, 10)` (Arista externa cara)
    -   `add_edge(2, 3, 10)` (Arista externa cara)
    -   `add_edge(0, 1, 2)`
    -   `add_edge(0, 2, 2)`
    -   `add_edge(0, 3, 2)`
    -   _Sin ordenar:_ Podría tomar (1,2) y (2,3) antes que las conexiones al centro si se agregan primero.
