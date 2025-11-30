# Codigo DP
def min_monedas(n, monedas=[1,3,4]):
    # Casos base
    if n == 0: return 0
    if n < 0: return float('inf') #Imposible

    # 1. Crear tabla DP
    # Llenamos con infinito porque queremos buscar el MÍNIMO.
    # Cualquier número será menor que infinito.
    dp = [float('inf')] * (n+1)
    dp[0] = 0 # 0 monedas para formar 0

    # 2. Llenar tabla
    # Vamos desde 1 hasta n calculando el óptimo para cada número
    for i in range(1, n+1):
        for moneda in monedas:
            if i >= moneda:
                # --- Tu codigo aqui ---
                # Comparamos el valor que ya tenemos (dp[i])
                # con la opción de usar esta moneda:
                # (Solución para el resto 'i - moneda') + 1 moneda actual
                dp[i] = min(dp[i], dp[i - moneda] + 1)
    
    return dp[n] if dp[n] != float('inf') else -1

