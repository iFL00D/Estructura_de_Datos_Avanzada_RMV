# Solución: Diseño de esquema de compresión Huffman

**Contexto Asumido:**

-   **Idioma:** Español
-   **Tipo:** Texto literario (ej. novela clásica como Don Quijote)
-   **Tamaño aproximado:** 10 KB (~10,000 caracteres)

## 1. Estimación de Frecuencias (Español Literario)

Basado en estadísticas estándar del idioma español, las frecuencias relativas aproximadas son:

| Carácter    | Frecuencia (%) | Apariciones (en 10k) |
| :---------- | :------------: | :------------------: |
| **Espacio** |     16.0%      |         1600         |
| **E**       |     13.0%      |         1300         |
| **A**       |     12.0%      |         1200         |
| **O**       |      9.0%      |         900          |
| **S**       |      7.5%      |         750          |
| **N**       |      7.0%      |         700          |
| **R**       |      6.5%      |         650          |
| **I**       |      6.0%      |         600          |
| **L**       |      5.5%      |         550          |
| **D**       |      5.0%      |         500          |
| **Otros**   |     12.5%      |         1250         |

_(Nota: "Otros" agrupa T, C, U, M, P, B, G, V, Y, Q, H, F, Z, J, Ñ, X, K, W y signos de puntuación)_

## 2. Construcción del Árbol de Huffman (Simplificado)

Para ilustrar el proceso, usaremos los 5 símbolos más frecuentes + un grupo "Resto".

**Cola de Prioridad Inicial:**

1. Resto: 1250
2. D: 500
3. L: 550
4. I: 600
5. R: 650
6. N: 700
7. S: 750
8. O: 900
9. A: 1200
10. E: 1300
11. Espacio: 1600

**Pasos de Combinación (Resumidos):**

1. Combinar (D, L) -> Nodo(1050)
2. Combinar (I, R) -> Nodo(1250)
3. Combinar (Resto, Nodo_DL) -> Nodo(2300)
4. Combinar (N, S) -> Nodo(1450)
5. Combinar (O, A) -> Nodo(2100)
6. Combinar (Nodo_IR, E) -> Nodo(2550)
7. Combinar (Nodo_NS, Espacio) -> Nodo(3050)
8. Combinar (Nodo_OA, Nodo_RestoDL) -> Nodo(4400)
9. Combinar (Nodo_IRE, Nodo_NSEspacio) -> Nodo(5600)
10. Combinar (Nodo_OARestoDL, Nodo_IRENSEspacio) -> **Raíz(10000)**

## 3. Tabla de Códigos Resultante (Estimada)

Los caracteres más frecuentes obtienen códigos más cortos.

| Carácter    | Código Huffman (Ejemplo) | Longitud (bits) | ASCII (bits) |
| :---------- | :----------------------- | :-------------: | :----------: |
| **Espacio** | `00`                     |        2        |      8       |
| **E**       | `01`                     |        2        |      8       |
| **A**       | `100`                    |        3        |      8       |
| **O**       | `101`                    |        3        |      8       |
| **S**       | `1100`                   |        4        |      8       |
| **N**       | `1101`                   |        4        |      8       |
| **R**       | `1110`                   |        4        |      8       |
| **I**       | `1111`                   |        4        |      8       |
| **L**       | `10010`                  |        5        |      8       |
| **D**       | `10011`                  |        5        |      8       |
| ...         | ...                      |       ...       |     ...      |

## 4. Cálculo de Compresión Teórica

**Tamaño Original (ASCII):**
10,000 caracteres \* 8 bits/char = **80,000 bits**

**Tamaño Comprimido (Huffman):**
Calculamos la longitud promedio ponderada (L):
$L = \sum (Frecuencia_i \times Longitud_i)$

-   Espacio (16%): $0.16 \times 2 = 0.32$
-   E (13%): $0.13 \times 2 = 0.26$
-   A (12%): $0.12 \times 3 = 0.36$
-   O (9%): $0.09 \times 3 = 0.27$
-   S (7.5%): $0.075 \times 4 = 0.30$
-   N (7%): $0.07 \times 4 = 0.28$
-   R (6.5%): $0.065 \times 4 = 0.26$
-   I (6%): $0.06 \times 4 = 0.24$
-   Resto (~23%): Promedio ~5 bits = $0.23 \times 5 = 1.15$

**Longitud promedio total:** ~3.44 bits/carácter

**Total bits Huffman:** 10,000 \* 3.44 = **34,400 bits**

**Ahorro:**
$(80,000 - 34,400) / 80,000 = 0.57$ -> **57% de compresión**

## 5. Almacenamiento del Árbol

Para que el receptor pueda descomprimir, el árbol debe ir incluido en el archivo. Métodos comunes:

1.  **Tabla de Frecuencias:** Guardar al inicio del archivo una lista de `(carácter, frecuencia)`. El descompresor reconstruye el árbol idéntico antes de leer los datos.

    -   _Ventaja:_ Simple.
    -   _Desventaja:_ Ocupa espacio extra (ej. 256 enteros = 1KB).

2.  **Árbol Serializado:** Recorrer el árbol en Preorden escribiendo un bit `0` para nodos internos y `1` + `carácter` para hojas.

    -   _Ventaja:_ Muy compacto.

3.  **Códigos Canónicos:** Solo se guardan las longitudes de los códigos para cada carácter. El árbol se reconstruye de forma determinista.

## Pregunta Adicional: ¿Qué pasa si las frecuencias reales difieren?

Si usamos un árbol pre-calculado (basado en estadísticas generales del español) para comprimir un texto atípico (ej. un poema lipograma sin la letra 'e' o un log de servidor con muchos números):

1.  **Pérdida de eficiencia:** Los caracteres frecuentes en _ese_ texto específico podrían tener códigos largos en nuestro árbol genérico.
2.  **Posible expansión:** En casos extremos, el archivo "comprimido" podría pesar más que el original si los símbolos más comunes reciben códigos de >8 bits.

**Solución:** Huffman es **adaptativo** por naturaleza. Lo ideal es siempre calcular las frecuencias **del archivo específico** que se va a comprimir, no usar tablas genéricas, a menos que se quiera evitar la primera pasada de lectura.
