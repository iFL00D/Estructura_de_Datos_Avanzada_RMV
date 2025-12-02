using System;
using System.Collections.Generic;
using System.Linq;

// La clase contenedora GraphValidator debe ser única
// y no puede cerrarse y reabrirse con métodos estáticos fuera.
public static class GraphValidator
{
    /// <summary>
    /// Valida si una secuencia es gráfica usando Havel-Hakimi.
    /// </summary>
    public static bool IsGraphicalSequence(List<int> degrees)
    {
        // 1. Caso base: una secuencia vacía es gráfica (representa un grafo sin nodos)
        if (degrees.Count == 0) return true;
        
        // Crear copia para no modificar la original
        var seq = new List<int>(degrees);
        
        // Bucle principal de Havel-Hakimi
        while (true)
        {
            // Ordenar no creciente: ESTE PASO ES CRUCIAL y DEBE IR AL INICIO DEL BUCLE
            // O inmediatamente después de modificar la secuencia.
            seq.Sort((a, b) => b.CompareTo(a));
            
            // 2. Simplificación: Eliminar ceros
            // Este paso es importante para la eficiencia y para determinar 
            // la condición de parada real del algoritmo.
            seq.RemoveAll(d => d == 0);

            if (seq.Count == 0) return true; // Si solo quedan ceros o estaba vacía
            
            // 3. Revisión inicial de condiciones
            // a) Suma par (solo es necesario verificar al principio, pero la verificación
            // de la paridad en cada paso no introduce error, aunque es redundante).
            // b) Máximo grado: el primer elemento (el mayor) no puede ser mayor o igual
            // que el número de nodos restantes (el tamaño de la secuencia - 1, o el tamaño total). 
            // El algoritmo de Havel-Hakimi implícitamente maneja esto, pero una
            // verificación temprana es buena.
            
            // ⚠️ La verificación de 'suma par' solo se necesita una vez al principio.
            // Para simplificar el algoritmo iterativo de Havel-Hakimi, nos centramos en la reducción.

            int d1 = seq[0];
            
            // 4. Chequeo de consistencia: el grado mayor d1 no puede ser mayor que el número de nodos restantes.
            // Si d1 es mayor que el resto de los elementos (seq.Count - 1), la secuencia es NO gráfica.
            // OJO: d1 debe ser aplicado a los siguientes d1 elementos.
            if (d1 > seq.Count - 1) return false;

            // 5. El paso Havel-Hakimi: Quitar d1 y restar 1 a los siguientes d1 elementos.
            seq.RemoveAt(0);
            
            for (int i = 0; i < d1; i++)
            {
                // Revisar si el índice es válido (debería estar cubierto por la verificación d1 > seq.Count - 1)
                if (i >= seq.Count) 
                {
                    // Esto indica un problema lógico, pero es una buena verificación de seguridad.
                    return false; 
                }
                
                seq[i]--;
                
                // 6. Chequeo de consistencia: No puede haber grados negativos.
                if (seq[i] < 0) return false;
            }
            
            // En este punto, no es estrictamente necesario imprimir, pero ayuda al debugging.
            // Console.WriteLine($"Paso: [{string.Join(", ", seq)}]");
            seq.Sort((a, b) => b.CompareTo(a));
            Console.WriteLine($"Paso: [{string.Join(", ", seq)}]");
        }
    }
    
    // ---
    
    // ⚠️ ATENCIÓN: Los siguientes métodos requieren la definición de una clase `Graph<T>`
    // que NO está incluida en tu código. Asumiendo que existe, no se modifican.

    /// <summary>
    /// Verifica consistencia: suma grados par para grafo no dirigido.
    /// </summary>
    public static bool ValidateConsistency(Graph<string> graph)
    {
        // El método .Vertices() y .OutDegree(v) se asumen existentes en 'Graph<string>'.
        int totalDegree = graph.Vertices().Sum(v => graph.OutDegree(v));
        // En grafo no dirigido, suma de grados = 2 * |aristas|, debe ser par
        return totalDegree % 2 == 0;
    }

    /// <summary>
    /// Extrae secuencia de grados de un grafo (útil para conectar con Semana 3).
    /// </summary>
    public static List<int> ExtractDegreeSequence(Graph<string> graph)
    {
        var degrees = graph.Vertices()
                          .Select(v => graph.OutDegree(v))
                          .OrderByDescending(d => d)
                          .ToList();
        return degrees;
    }
}

// ⚠️ Se necesita una definición de 'Graph<T>' para que el código compile. 
// Añado una definición mínima para evitar un error de compilación.
public class Graph<T>
{
    public IEnumerable<T> Vertices() => Enumerable.Empty<T>();
    public int OutDegree(T vertex) => 0;
}


// ---

class Program
{
    static void Main()
    {
        // 🟢 Secuencia gráfica
        var seq1 = new List<int> {3,3,1,1,1,1};
        Console.WriteLine($"Secuencia: [{string.Join(", ", seq1)}]");
        Console.WriteLine($"¿Es Grafica? {GraphValidator.IsGraphicalSequence(seq1)}");
    }
}