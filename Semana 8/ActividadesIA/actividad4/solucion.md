# Solución: Comparación de estructuras para indexación

**Escenario Definido:**

-   **Registros:** 1,000,000 (1 millón)
-   **Operaciones:** Búsquedas puntuales y **rangos** frecuentes.
-   **Almacenamiento:** Disco Duro (HDD) - _Esto es clave: el acceso aleatorio es lento._
-   **Bloque de disco:** 4 KB (4096 bytes)

## 1. Comparativa General

| Estructura  | Tipo    | Optimizado para        | Búsqueda Puntual | Búsqueda Rango |
| :---------- | :------ | :--------------------- | :--------------: | :------------: |
| **BST**     | Memoria | Nada (puede degenerar) |  O(n) peor caso  |     Pobre      |
| **AVL**     | Memoria | Balanceo estricto      |     O(log n)     |    Regular     |
| **B-Tree**  | Disco   | Minimizar I/O          |    O(log_m n)    |     Bueno      |
| **B+ Tree** | Disco   | Rangos + I/O           |    O(log_m n)    | **Excelente**  |

## 2. Cálculos Detallados

Asumiremos:

-   Tamaño de clave (ID): 8 bytes
-   Tamaño de puntero: 8 bytes
-   Tamaño de registro (data): 128 bytes (solo para referencia, en B+ solo hojas tienen data)

### A. BST y AVL (Estructuras de Memoria)

Estas estructuras almacenan un nodo por "bloque" lógico de memoria. En disco, cada nodo podría estar en un bloque diferente disperso.

-   **Altura AVL:** $1.44 \times \log_2(1,000,000) \approx 1.44 \times 20 \approx \mathbf{29}$ niveles.
-   **Accesos a disco:** En el peor caso (nodos dispersos en HDD), cada salto de nivel es una lectura de disco (seek time ~10ms).
    -   29 accesos $\times$ 10ms = **290 ms** por búsqueda.
    -   _Inviable para bases de datos reales._

### B. Árbol B+ (Estructura de Disco)

Calculamos el **Orden (m)** (número máximo de hijos) que cabe en un bloque de 4KB.

-   Nodo interno: contiene claves y punteros.
-   $m \times Puntero + (m-1) \times Clave \le 4096$
-   $m \times 8 + (m-1) \times 8 \le 4096$
-   $16m - 8 \le 4096 \Rightarrow 16m \le 4104 \Rightarrow m \le 256$
-   **Orden m ≈ 256**

**Altura del B+ Tree:**

-   Fórmula: $\log_{\lceil m/2 \rceil} (N)$
-   Base del logaritmo (factor de ramificación promedio): $256 / 2 = 128$ (asumiendo nodos al 50% de llenado, pesimista).
-   Altura = $\log_{128}(1,000,000) \approx \mathbf{3}$ niveles.

**Accesos a disco:**

-   3 accesos $\times$ 10ms = **30 ms** (10 veces más rápido que AVL).
-   _Nota:_ Normalmente los niveles superiores (raíz y nivel 1) se guardan en RAM (caché), reduciendo a **1 acceso físico real**.

## 3. Análisis de Ventajas/Desventajas

### BST / AVL

-   **Ventajas:** Simples de implementar. Excelentes si todo cabe en RAM.
-   **Desventajas:** Pésimo rendimiento en disco (muchos saltos aleatorios). No optimizados para bloques de 4KB.
-   **Rangos:** Requieren recorrido inorden (subir y bajar por el árbol), lo cual genera mucho "thrashing" de disco.

### B-Tree

-   **Ventajas:** Reduce altura drásticamente.
-   **Desventajas:** Los datos están en todos los nodos. Para rangos, aún hay que saltar entre subárboles.

### B+ Tree

-   **Ventajas:**
    -   **Altura mínima:** Menos accesos a disco.
    -   **Hojas enlazadas:** Para consultas de rango (ej. `ID > 500 AND ID < 1000`), encuentras el 500 y luego lees secuencialmente las hojas enlazadas. El HDD es muy rápido en lectura secuencial.
    -   **Densidad:** Al no tener datos en nodos internos, caben más claves, aumentando el factor de ramificación.

## 4. Recomendación Final

**Estructura Óptima: Árbol B+**

**Justificación:**

1.  **Minimización de I/O:** Con 1 millón de registros, pasamos de ~29 accesos (AVL) a solo ~3 accesos (B+). En un HDD, esto es la diferencia entre un sistema usable y uno colapsado.
2.  **Eficiencia en Rangos:** El requisito de "búsquedas por rango" descarta al B-Tree estándar y favorece fuertemente al B+, ya que su lista enlazada de hojas permite extraer rangos a velocidad de lectura secuencial del disco.
3.  **Uso de Bloques:** Aprovecha perfectamente los bloques de 4KB, leyendo cientos de claves en una sola operación de hardware.
