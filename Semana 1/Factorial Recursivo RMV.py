'''
    Fatorial recursivo y no recursivo
'''

def factorial(numero):
    if(numero <= 1):
        return 1
    
    return numero * factorial(numero - 1)

def FactorialIterativo(num):
    resultado = 1
    
    for i in range(2, num + 1):
        resultado *= i

    return resultado

n = 10
resultado = factorial(n)
resultadoIterativo = FactorialIterativo(n)
print("El factorial de ",n," es: ",resultado)
print("El factorial de ",n," es: ", resultadoIterativo)