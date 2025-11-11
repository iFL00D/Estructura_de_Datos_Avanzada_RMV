'''
    Serie Fibonacci recursivo y iterativo
'''

def fibonacci_recursivo(n):
    #Caso base
    if(n <= 1):
        return n
    else:
        return fibonacci_recursivo(n-1) + fibonacci_recursivo(n-2)
    
def fibonacci_iterativa(n):
    #Caso base
    if(n <= 1):
        return n
    #Declaracion de variables
    a, b = 0, 1
    #Paso iterativo
    for _ in range(n - 1):
        a, b = b, a + b
    #Devuelta de b
    return b

print("Serie Fibonacci recursivo: ")
for i in range(20):
    print(fibonacci_recursivo(i), end=" ")

print("")

print("Serie Fibonacci Iterativo: ")
for i in range(10):
    print(fibonacci_iterativa(i), end=" ")