def es_secuencia_grafica(grados):
    """Implementación Pythonic de Havel-Hakimi"""
    # Validación inicial: Suma par (built-in sum)
    if sum(grados) % 2 != 0:
        return False
    
    # Trabajamos con una copia para no alterar el original
    copia = grados[:]
    
    while copia:
        # 1. Ordenar descendente (argumento nombrado)
        copia.sort(reverse=True)
        
        # 2. Extraer cabeza (si es 0, terminamos porque está ordenado)
        if copia[0] == 0:
            return True
            
        n = copia.pop(0) # Extrae y retorna el primero
        
        # 3. Verificar longitud
        if n > len(copia):
            return False
            
        # 4. Restar 1 (Pythonic loop)
        for i in range(n):
            copia[i] -= 1
            if copia[i] < 0:
                return False
                
    return True

# Ejecución (Main guard)
if __name__ == "__main__":
    # Dataset Urbano CDMX
    dataset_cdmx = [5, 5, 5, 4, 4, 4, 4, 4, 4, 4, 4, 4, 3, 3, 3, 3, 3, 3, 3, 2, 2, 2, 2, 2, 2]
    
    print(f"Procesando dataset de {len(dataset_cdmx)} zonas...")
    resultado = es_secuencia_grafica(dataset_cdmx)
    
    print("VALIDO: Es una secuencia gráfica." if resultado else "INVALIDO: No se puede formar el grafo.")