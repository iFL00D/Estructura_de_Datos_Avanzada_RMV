'''
    Ejercicio Realizar una función recursiva para detectar palindromos
'''

def es_palindromo(cadena):
    #Convertimos a minusculas y quitamos espacios para que sea mas precisa la verificación
    cadena = cadena.lower().replace(" ", "")
    #Caso Base (parada de la recursion)
    if len(cadena) <= 1:
        return True
    #Paso para recursividad
    if cadena[0] == cadena[-1]:
        return es_palindromo(cadena[1:-1])
    else:
        return False

# Escribimos la palabra que queremos saber si es palindromo o no
palabra = input('Ingresa la palabra o frase para saber si es palindromo: ')

if es_palindromo(palabra):
    print(f"'{palabra}' SI es un palindromo.")
else:
    print(f"'{palabra}' NO es un palindromo.")