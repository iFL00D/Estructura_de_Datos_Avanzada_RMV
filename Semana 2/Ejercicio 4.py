# Codigo roto
# def fibonacci_dp_roto(n):
#     dp = [0] * n  # Error 1: ?
#     dp[1] = 1
#     for i in range(2, n):  # Error 2: ?
#         dp[i] = dp[i-1] + dp[i-2]
#     return dp[n]  # Error 3: ?

#Correción de codigo
def fibonacci_dp_arreglado(n):
    if n == 0: return 0
    if n == 1: return 1

    dp = [0] * (n+1)

    dp[0] = 0
    dp[1] = 1

    for i in range(2, n+1):
        dp[i] = dp[i-1] + dp[i-2]
    
    return dp[n]

