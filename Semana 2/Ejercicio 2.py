def formas_ingenuo(n):
    # Casos base
    if n <= 0: return 1
    if n == 1: return 1

    # Tu código aquí - ¿Cómo se relaciona n con n-1 y n-2?
    # La lógica recursiva:
    # Opción A: Damos un paso de 1 -> nos falta resolver para (n-1)
    # Opción B: Damos un paso de 2 -> nos falta resolver para (n-2)
    return formas_ingenuo(n-1) + formas_ingenuo(n-2)

def formas_memo(n, memo={}):
    # 1. Casos base (igual que antes)
    if n <= 0: return 1
    if n == 1: return 1

    # 2. ¿Ya lo calculé antes? (Memoization)
    if n in memo:
        return memo[n]
    
    # 3. Calcularlo y guardarlo
    # IMPORTANTE: Pasamos 'memo' a las llamadas recursivas
    resultado = formas_memo(n-1, memo) + formas_memo(n-2, memo)

    # Guardamos el resultado en la "libreta" antes de retornarlo
    memo[n] = resultado

    return resultado

def formas_tabla(n):
    # Caso rápido: si n es 0 o 1, la respuesta es 1.
    if n <= 1: return 1

    # 1. Crear tabla (Array)
    # Creamos una lista llena de ceros del tamaño necesario (n+1 huecos)
    dp = [0] * (n+1)

    # 2. Casos base (Llenamos los primeros valores manuales)
    dp[0] = 1 # Formas de llegar a 0
    dp[1] = 1 # Formas de llegar a 1

    # 3. Llenar tabla iterativamente
    # Empezamos desde el 2 hasta n
    for i in range(2, n+1):
        # Tu código aquí:
        # El valor actual es la suma de los dos valores que ya calculamos antes
        dp[i] = dp[i-1] + dp[i-2]
    
    return dp[n]

