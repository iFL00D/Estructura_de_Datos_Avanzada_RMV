using System;
using System.Collections.Generic;
using System.Linq;

public class GraphValidator
{
    public static bool EsSecuenciaGrafica(List<int> grados)
    {
        // Validación inicial: Suma debe ser par
        if (grados.Sum() % 2 != 0) return false;

        List<int> copia = new List<int>(grados);

        while (copia.Count > 0)
        {
            // 1. Ordenar descendente (Mayor a menor)
            copia.Sort((a, b) => b.CompareTo(a));

            // 2. Extraer el nodo con mayor grado (cabeza)
            int N = copia[0];
            copia.RemoveAt(0);

            // Caso base: Si N es 0, hemos terminado (resto son ceros)
            if (N == 0) return true;

            // 3. Verificar si hay suficientes nodos restantes
            if (N > copia.Count) return false;

            // 4. Restar 1 a los siguientes N nodos
            for (int i = 0; i < N; i++)
            {
                copia[i]--;
                // Si algún grado se vuelve negativo, imposible
                if (copia[i] < 0) return false;
            }
        }
        return true;
    }

    public static void Main()
    {
        // Dataset Urbano CDMX (Del paso anterior)
        List<int> datasetCDMX = new List<int> { 5, 5, 5, 4, 4, 4, 4, 4, 4, 4, 4, 4, 3, 3, 3, 3, 3, 3, 3, 2, 2, 2, 2, 2, 2 };
        
        Console.WriteLine($"Procesando dataset de {datasetCDMX.Count} zonas...");
        bool resultado = EsSecuenciaGrafica(datasetCDMX);
        
        Console.WriteLine(resultado ? "VALIDO: Es una secuencia gráfica." : "INVALIDO: No se puede formar el grafo.");
    }
}