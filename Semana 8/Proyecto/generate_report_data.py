import time
import os
import sys
from bst import BST
from avl import AVL
from huffman import Huffman

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
        palabras = linea.lower().replace('.', '').replace(',', '').replace('?', '').replace('!', '').replace(';', '').replace(':', '').replace('"', '').replace('(', '').replace(')', '').split()
        for num_col, palabra in enumerate(palabras, 1):
            palabras_procesadas.append((palabra, num_linea, num_col))
    return palabras_procesadas

def medir_construccion(palabras_procesadas):
    bst = BST()
    avl = AVL()
    
    # Medir tiempo BST
    inicio = time.time()
    for palabra, linea, col in palabras_procesadas:
        bst.insertar(palabra, linea, col)
    fin = time.time()
    tiempo_bst = (fin - inicio) * 1000
    
    # Medir tiempo AVL
    inicio = time.time()
    for palabra, linea, col in palabras_procesadas:
        avl.insertar(palabra, linea, col)
    fin = time.time()
    tiempo_avl = (fin - inicio) * 1000
    
    return bst, avl, tiempo_bst, tiempo_avl

def medir_busqueda(arbol, palabra):
    inicio = time.time()
    arbol.buscar(palabra)
    fin = time.time()
    return (fin - inicio) * 1000

def medir_huffman(ruta_entrada):
    huffman = Huffman()
    ruta_salida = ruta_entrada.split('.')[0] + ".huff"
    
    # Comprimir
    huffman.comprimir_archivo(ruta_entrada, ruta_salida)
    
    # Obtener estadísticas
    size_orig = os.path.getsize(ruta_entrada)
    size_comp = os.path.getsize(ruta_salida)
    ahorro = (1 - size_comp/size_orig) * 100
    
    # Limpiar archivo generado
    if os.path.exists(ruta_salida):
        os.remove(ruta_salida)
        
    return size_orig, size_comp, ahorro

def main():
    ruta_archivo = "test_data.txt"
    
    if not os.path.exists(ruta_archivo):
        print(f"Error: No se encuentra {ruta_archivo}")
        return

    print("=== GENERANDO DATOS PARA EL REPORTE ===")
    
    # 1. Carga y Procesamiento
    contenido = cargar_archivo(ruta_archivo)
    datos = procesar_texto(contenido)
    
    # 2. Construcción
    bst, avl, t_bst, t_avl = medir_construccion(datos)
    
    print("\n--- Tiempos de Construcción ---")
    print(f"BST: {t_bst:.4f} ms")
    print(f"AVL: {t_avl:.4f} ms")
    
    # 3. Búsqueda
    palabras_prueba = ["quijote", "caballero", "molinos"] # Palabras que probablemente estén o no
    # Ajustamos a palabras que seguro están en el texto del Quijote proporcionado
    palabras_prueba = ["hidalgo", "caballero", "dulcinea"] 
    
    print("\n--- Tiempos de Búsqueda ---")
    print(f"{'Palabra':<15} | {'BST (ms)':<10} | {'AVL (ms)':<10}")
    print("-" * 45)
    
    for p in palabras_prueba:
        t_b = medir_busqueda(bst, p)
        t_a = medir_busqueda(avl, p)
        print(f"{p:<15} | {t_b:.6f}   | {t_a:.6f}")

    # 4. Huffman
    size_orig, size_comp, ahorro = medir_huffman(ruta_archivo)
    
    print("\n--- Compresión Huffman ---")
    print(f"Original: {size_orig} bytes")
    print(f"Comprimido: {size_comp} bytes")
    print(f"Ahorro: {ahorro:.2f}%")

if __name__ == "__main__":
    main()