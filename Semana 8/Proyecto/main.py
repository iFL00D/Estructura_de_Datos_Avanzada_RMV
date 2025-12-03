import time
import os
import sys
from bst import BST
from avl import AVL
from huffman import Huffman

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def cargar_archivo(ruta):
    try:
        with open(ruta, 'r', encoding='utf-8') as f:
            contenido = f.readlines()
        return contenido
    except FileNotFoundError:
        print(f"Error: El archivo '{ruta}' no existe.")
        return None

def procesar_texto(lineas):
    palabras_procesadas = []
    for num_linea, linea in enumerate(lineas, 1):
        # Limpieza básica: quitar signos de puntuación y convertir a minúsculas
        palabras = linea.lower().replace('.', '').replace(',', '').replace('?', '').replace('!', '').split()
        for num_col, palabra in enumerate(palabras, 1):
            palabras_procesadas.append((palabra, num_linea, num_col))
    return palabras_procesadas

def construir_indices(palabras_procesadas):
    bst = BST()
    avl = AVL()
    
    print("\nConstruyendo índices...")
    
    # Medir tiempo BST
    inicio = time.time()
    for palabra, linea, col in palabras_procesadas:
        bst.insertar(palabra, linea, col)
    fin = time.time()
    tiempo_bst = (fin - inicio) * 1000
    print(f"Tiempo construcción BST: {tiempo_bst:.4f} ms")
    
    # Medir tiempo AVL
    inicio = time.time()
    for palabra, linea, col in palabras_procesadas:
        avl.insertar(palabra, linea, col)
    fin = time.time()
    tiempo_avl = (fin - inicio) * 1000
    print(f"Tiempo construcción AVL: {tiempo_avl:.4f} ms")
    
    return bst, avl, tiempo_bst, tiempo_avl

def buscar_palabra(arbol, nombre_arbol):
    palabra = input(f"\nIngrese palabra a buscar en {nombre_arbol}: ").lower()
    inicio = time.time()
    resultados = arbol.buscar(palabra)
    fin = time.time()
    
    tiempo = (fin - inicio) * 1000
    
    if resultados:
        print(f"Encontrada en {len(resultados)} posiciones:")
        # Mostrar solo las primeras 10 ocurrencias para no saturar
        for i, (linea, col) in enumerate(resultados):
            if i >= 10:
                print(f"... y {len(resultados) - 10} más.")
                break
            print(f"  - Línea {linea}, Columna {col}")
    else:
        print("Palabra no encontrada.")
    
    print(f"Tiempo de búsqueda: {tiempo:.6f} ms")

def menu_principal():
    bst = None
    avl = None
    ruta_archivo = "test_data.txt" # Por defecto
    huffman = Huffman()
    
    while True:
        print("\n=== PROYECTO FINAL: ESTRUCTURAS DE DATOS ===")
        print(f"Archivo actual: {ruta_archivo}")
        print("1. Cargar archivo y construir índices (BST vs AVL)")
        print("2. Buscar palabra en BST")
        print("3. Buscar palabra en AVL")
        print("4. Comprimir archivo (Huffman)")
        print("5. Descomprimir archivo (Huffman)")
        print("6. Cambiar archivo de entrada")
        print("7. Salir")
        
        opcion = input("\nSeleccione una opción: ")
        
        if opcion == '1':
            contenido = cargar_archivo(ruta_archivo)
            if contenido:
                datos = procesar_texto(contenido)
                bst, avl, t_bst, t_avl = construir_indices(datos)
                print(f"\nComparativa:")
                if t_bst < t_avl:
                    print(f"BST fue {t_avl/t_bst:.2f}x más rápido en construcción.")
                else:
                    print(f"AVL fue {t_bst/t_avl:.2f}x más rápido en construcción.")
        
        elif opcion == '2':
            if bst:
                buscar_palabra(bst, "BST")
            else:
                print("Primero debe cargar el archivo (Opción 1).")
        
        elif opcion == '3':
            if avl:
                buscar_palabra(avl, "AVL")
            else:
                print("Primero debe cargar el archivo (Opción 1).")
        
        elif opcion == '4':
            if os.path.exists(ruta_archivo):
                salida = ruta_archivo.split('.')[0] + ".huff"
                inicio = time.time()
                huffman.comprimir_archivo(ruta_archivo, salida)
                fin = time.time()
                print(f"Tiempo de compresión: {(fin-inicio)*1000:.4f} ms")
            else:
                print("El archivo no existe.")
        
        elif opcion == '5':
            entrada = input("Ingrese nombre del archivo .huff: ")
            if os.path.exists(entrada):
                salida = entrada.split('.')[0] + "_decomp.txt"
                inicio = time.time()
                huffman.descomprimir_archivo(entrada, salida)
                fin = time.time()
                print(f"Tiempo de descompresión: {(fin-inicio)*1000:.4f} ms")
            else:
                print("El archivo no existe.")
        
        elif opcion == '6':
            nueva_ruta = input("Ingrese ruta del archivo: ")
            if os.path.exists(nueva_ruta):
                ruta_archivo = nueva_ruta
                bst = None
                avl = None
                print("Archivo cambiado. Recuerde construir los índices nuevamente.")
            else:
                print("Archivo no encontrado.")
        
        elif opcion == '7':
            print("Saliendo...")
            break
        
        else:
            print("Opción no válida.")

if __name__ == "__main__":
    # Asegurarse de estar en el directorio correcto si se ejecuta desde fuera
    # os.chdir(os.path.dirname(os.path.abspath(__file__)))
    menu_principal()