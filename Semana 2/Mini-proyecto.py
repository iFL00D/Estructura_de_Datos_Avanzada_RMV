def suma_maxima_memo(nums):
    memo = {}
    
    def resolver(i):
        # Casos Base
        if i < 0: return 0
        
        # ¿Ya lo calculé?
        if i in memo: return memo[i]
        
        # DECISIÓN CLAVE:
        # Opción A: Tomar el número actual 'nums[i]' 
        #           (No puedo tomar el anterior i-1, salto a i-2)
        tomar = nums[i] + resolver(i - 2)
        
        # Opción B: No tomar el actual
        #           (Me quedo con el mejor resultado hasta i-1)
        saltar = resolver(i - 1)
        
        # Guardamos el máximo de las dos opciones
        memo[i] = max(tomar, saltar)
        return memo[i]

    # Iniciamos desde el último elemento del array
    return resolver(len(nums) - 1)

def suma_maxima_tabla(nums):
    n = len(nums)
    
    # Manejo de casos borde (arrays vacíos o muy cortos)
    if n == 0: return 0
    if n == 1: return nums[0]
    
    # 1. Crear tabla
    dp = [0] * n
    
    # 2. Casos base manuales
    dp[0] = nums[0]
    # En la posición 1, la mejor opción es el mayor entre el 0 y el 1
    dp[1] = max(nums[0], nums[1])
    
    # 3. Llenar tabla iterativamente
    for i in range(2, n):
        # La fórmula es idéntica a la versión recursiva:
        tomar = nums[i] + dp[i-2]
        saltar = dp[i-1]
        
        dp[i] = max(tomar, saltar)
        
    return dp[n-1]

# Prueba memo
nums = [2, 7, 9, 3, 1]
print(f"Resultado Memo: {suma_maxima_memo(nums)}") # Debería ser 2 + 9 + 1 = 12

# Prueba tabla
print(f"Resultado Tabla: {suma_maxima_tabla(nums)}")