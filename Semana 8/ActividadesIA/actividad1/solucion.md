# Solución: Predicción y verificación de rotaciones AVL

## Análisis de tu predicción

**¡Tu predicción es CORRECTA en todos los puntos!** Has identificado perfectamente el caso de desbalance y la rotación necesaria.

A continuación, desgloso la verificación paso a paso para confirmar tu razonamiento:

### Paso 1: Insertar 30

-   **Árbol:** Raíz `30`.
-   **Factores de Balance (FB):**
    -   `30`: 0
-   **Estado:** Balanceado.

### Paso 2: Insertar 20

-   `20 < 30`, se inserta a la izquierda.
-   **Árbol:**
    ```mermaid
    graph TD
        30 --> 20
    ```
-   **Factores de Balance:**
    -   `20`: 0 (hoja)
    -   `30`: Altura(izq) - Altura(der) = 1 - 0 = **+1**
-   **Estado:** Balanceado (|FB| ≤ 1).

### Paso 3: Insertar 25

-   `25 < 30` (izquierda)
-   `25 > 20` (derecha) -> Se inserta como hijo derecho de 20.
-   **Árbol (antes de rotar):**
    ```mermaid
    graph TD
        30 --> 20
        20 --> null1[null]
        20 --> 25
        style 30 fill:#e74c3c
        style 20 fill:#f39c12
    ```
-   **Cálculo de FB:**
    -   `25`: 0
    -   `20`: Altura(izq) - Altura(der) = 0 - 1 = **-1**
    -   `30`: Altura(izq) - Altura(der) = 2 - 0 = **+2** (¡Desbalanceado!)

### Diagnóstico

1. **Nodo desbalanceado:** `30` (FB = +2).
2. **Hijo en la dirección del desbalance:** `20` (Hijo izquierdo).
3. **FB del hijo:** `20` tiene FB = -1.
4. **Conclusión:** Como los signos son opuestos (+2 en padre, -1 en hijo), es un caso **LR (Izquierda-Derecha)**.
5. **Solución:** Requiere una **Rotación Doble** (primero izquierda sobre el hijo, luego derecha sobre el padre).

### Ejecución de la Rotación Doble (LR)

**Fase 1: Rotación Simple Izquierda sobre 20**

-   El 25 sube a ocupar el lugar del 20.
-   El 20 baja a ser hijo izquierdo del 25.
-   **Árbol intermedio:**
    ```mermaid
    graph TD
        30 --> 25
        25 --> 20
    ```

**Fase 2: Rotación Simple Derecha sobre 30**

-   El 25 sube a la raíz.
-   El 30 baja a ser hijo derecho del 25.
-   **Árbol final:**
    ```mermaid
    graph TD
        25 --> 20
        25 --> 30
        style 25 fill:#27ae60
    ```

### Resultado Final

-   Raíz: 25
-   Hijos: 20 (izq), 30 (der)
-   Todos los nodos tienen FB = 0.
-   El árbol está perfectamente balanceado.

¡Excelente análisis! Has comprendido bien la lógica de detección de casos en AVL.
