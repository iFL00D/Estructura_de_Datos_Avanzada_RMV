# Visualización de Floyd-Warshall

## 1. Diagrama del Grafo (Mermaid)

```mermaid
graph LR
    0((0))
    1((1))
    2((2))
    3((3))

    0 -->|4| 1
    0 -->|11| 2
    1 -->|2| 2
    2 -->|6| 0
    2 -->|7| 3
    3 -->|2| 1

    style 0 fill:#f9f,stroke:#333,stroke-width:2px
    style 1 fill:#bbf,stroke:#333,stroke-width:2px
    style 2 fill:#bfb,stroke:#333,stroke-width:2px
    style 3 fill:#fbb,stroke:#333,stroke-width:2px
```

## 2. Ejecución Paso a Paso (Tabla HTML)

Esta tabla muestra la matriz de distancias $D^{(k)}$ después de considerar cada nodo $k$ como intermedio.

<style>
    table { border-collapse: collapse; width: 100%; font-family: monospace; }
    th, td { border: 1px solid #ddd; padding: 8px; text-align: center; }
    th { background-color: #f2f2f2; }
    .highlight { background-color: #ffffcc; font-weight: bold; }
    .header-row { background-color: #e0e0e0; font-weight: bold; }
</style>

<table>
    <tr class="header-row">
        <th>k (Pivote)</th>
        <th>Matriz de Distancias Resultante</th>
        <th>Cambios Significativos</th>
    </tr>
    <tr>
        <td><strong>Inicial (k=-1)</strong></td>
        <td>
            <table>
                <tr><td>0</td><td>4</td><td>11</td><td>∞</td></tr>
                <tr><td>∞</td><td>0</td><td>2</td><td>∞</td></tr>
                <tr><td>6</td><td>∞</td><td>0</td><td>7</td></tr>
                <tr><td>∞</td><td>2</td><td>∞</td><td>0</td></tr>
            </table>
        </td>
        <td>Configuración inicial basada en pesos directos.</td>
    </tr>
    <tr>
        <td><strong>k=0</strong><br>(Usando nodo 0)</td>
        <td>
            <table>
                <tr><td>0</td><td>4</td><td>11</td><td>∞</td></tr>
                <tr><td>∞</td><td>0</td><td>2</td><td>∞</td></tr>
                <tr><td>6</td><td class="highlight">10</td><td>0</td><td>7</td></tr>
                <tr><td>∞</td><td>2</td><td>∞</td><td>0</td></tr>
            </table>
        </td>
        <td>
            2->1 mejorado: 2->0->1 (6+4=10) < ∞
        </td>
    </tr>
    <tr>
        <td><strong>k=1</strong><br>(Usando nodo 1)</td>
        <td>
            <table>
                <tr><td>0</td><td>4</td><td class="highlight">6</td><td>∞</td></tr>
                <tr><td>∞</td><td>0</td><td>2</td><td>∞</td></tr>
                <tr><td>6</td><td>10</td><td>0</td><td>7</td></tr>
                <tr><td>∞</td><td>2</td><td class="highlight">4</td><td>0</td></tr>
            </table>
        </td>
        <td>
            0->2 mejorado: 0->1->2 (4+2=6) < 11<br>
            3->2 mejorado: 3->1->2 (2+2=4) < ∞
        </td>
    </tr>
    <tr>
        <td><strong>k=2</strong><br>(Usando nodo 2)</td>
        <td>
            <table>
                <tr><td>0</td><td>4</td><td>6</td><td class="highlight">13</td></tr>
                <tr><td><td class="highlight">8</td><td>0</td><td>2</td><td class="highlight">9</td></tr>
                <tr><td>6</td><td>10</td><td>0</td><td>7</td></tr>
                <tr><td><td class="highlight">10</td><td>2</td><td>4</td><td class="highlight">11</td></tr>
            </table>
        </td>
        <td>
            0->3: 0->2->3 (6+7=13)<br>
            1->0: 1->2->0 (2+6=8)<br>
            1->3: 1->2->3 (2+7=9)<br>
            3->0: 3->2->0 (4+6=10)<br>
            3->3: 3->2->3 (4+7=11) (Ciclo positivo)
        </td>
    </tr>
    <tr>
        <td><strong>k=3</strong><br>(Usando nodo 3)</td>
        <td>
            <table>
                <tr><td>0</td><td>4</td><td>6</td><td>13</td></tr>
                <tr><td>8</td><td>0</td><td>2</td><td>9</td></tr>
                <tr><td>6</td><td><td class="highlight">9</td><td>0</td><td>7</td></tr>
                <tr><td>10</td><td>2</td><td>4</td><td>11</td></tr>
            </table>
        </td>
        <td>
            2->1 mejorado: 2->3->1 (7+2=9) < 10
        </td>
    </tr>
</table>

## Sugerencias de Estilo

-   **Celdas Modificadas:** Usar un color de fondo suave (ej. amarillo claro `#ffffcc`) para resaltar los valores que cambiaron en la iteración actual.
-   **Infinito:** Representar `math.inf` como `∞` para legibilidad.
-   **Diagonal:** Mantener la diagonal en gris claro o negrita para referencia visual rápida (debe ser siempre 0 si no hay ciclos negativos).
