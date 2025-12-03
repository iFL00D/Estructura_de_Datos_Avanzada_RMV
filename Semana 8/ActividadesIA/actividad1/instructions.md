# Predicción y verificación de rotaciones AVL

**Enfoque activo:** Tú predices, la IA verifica.

Voy a proponerte una secuencia de inserciones en un AVL y MI PREDICCIÓN de qué rotación ocurrirá. Verifica si mi predicción es correcta.

**Secuencia:** [30, 20, 25]

**MI PREDICCIÓN:**

-   Después de insertar 30: árbol con solo la raíz 30
-   Después de insertar 20: 30 tiene hijo izquierdo 20, FB(30)=+1
-   Después de insertar 25:
    -   25 va a la derecha de 20
    -   FB(30) = +2 (desbalanceado)
    -   FB(20) = -1 (hijo va a la derecha)
    -   Esto es caso LR, necesita rotación doble

¿Es correcta mi predicción? Si hay errores, explícame dónde me equivoqué paso a paso.
