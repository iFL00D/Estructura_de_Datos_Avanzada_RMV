import heapq
import os
import pickle
from collections import Counter

class NodoHuffman:
    def __init__(self, caracter, frecuencia):
        self.caracter = caracter
        self.frecuencia = frecuencia
        self.izquierdo = None
        self.derecho = None

    def __lt__(self, otro):
        return self.frecuencia < otro.frecuencia
    
    def es_hoja(self):
        return self.izquierdo is None and self.derecho is None

class Huffman:
    def __init__(self):
        self.raiz = None
        self.codigos = {}
        self.codigos_inversos = {}

    def construir_arbol(self, texto):
        frecuencias = Counter(texto)
        if not frecuencias:
            return

        heap = [NodoHuffman(char, freq) for char, freq in frecuencias.items()]
        heapq.heapify(heap)

        while len(heap) > 1:
            izq = heapq.heappop(heap)
            der = heapq.heappop(heap)
            padre = NodoHuffman(None, izq.frecuencia + der.frecuencia)
            padre.izquierdo = izq
            padre.derecho = der
            heapq.heappush(heap, padre)

        self.raiz = heap[0]
        self._generar_codigos(self.raiz, "")

    def _generar_codigos(self, nodo, codigo_actual):
        if not nodo:
            return
        if nodo.es_hoja():
            self.codigos[nodo.caracter] = codigo_actual
            self.codigos_inversos[codigo_actual] = nodo.caracter
            return
        self._generar_codigos(nodo.izquierdo, codigo_actual + "0")
        self._generar_codigos(nodo.derecho, codigo_actual + "1")

    def comprimir_archivo(self, ruta_entrada, ruta_salida):
        """
        Comprime un archivo de texto usando Huffman.
        Guarda el árbol (frecuencias) y los bits comprimidos.
        """
        try:
            with open(ruta_entrada, 'r', encoding='utf-8') as f:
                texto = f.read()
            
            if not texto:
                print("El archivo está vacío.")
                return

            self.construir_arbol(texto)
            bits_codificados = "".join(self.codigos[c] for c in texto)
            
            # Padding para completar byte
            padding = 8 - (len(bits_codificados) % 8)
            bits_codificados += "0" * padding
            
            # Convertir bits a bytes
            b = bytearray()
            for i in range(0, len(bits_codificados), 8):
                byte = bits_codificados[i:i+8]
                b.append(int(byte, 2))
            
            # Guardar archivo comprimido
            # Estructura: [padding (1 byte)] [longitud tabla freq (4 bytes)] [tabla freq (pickle)] [datos comprimidos]
            with open(ruta_salida, 'wb') as f:
                # Guardamos la tabla de frecuencias para reconstruir el árbol
                frecuencias = Counter(texto)
                tabla_bytes = pickle.dumps(frecuencias)
                
                f.write(bytes([padding]))
                f.write(len(tabla_bytes).to_bytes(4, byteorder='big'))
                f.write(tabla_bytes)
                f.write(b)
            
            print(f"Archivo comprimido guardado en: {ruta_salida}")
            self._mostrar_estadisticas(ruta_entrada, ruta_salida)
            
        except Exception as e:
            print(f"Error al comprimir: {e}")

    def descomprimir_archivo(self, ruta_entrada, ruta_salida):
        """
        Descomprime un archivo .huff recuperando el texto original.
        """
        try:
            with open(ruta_entrada, 'rb') as f:
                padding = int.from_bytes(f.read(1), byteorder='big')
                len_tabla = int.from_bytes(f.read(4), byteorder='big')
                tabla_bytes = f.read(len_tabla)
                datos_comprimidos = f.read()
            
            # Reconstruir árbol
            frecuencias = pickle.loads(tabla_bytes)
            # Reconstruimos el árbol usando las frecuencias guardadas
            # Nota: Esto no es lo más eficiente pero es simple y funciona para el proyecto
            # Una optimización sería guardar la estructura del árbol o códigos canónicos
            heap = [NodoHuffman(char, freq) for char, freq in frecuencias.items()]
            heapq.heapify(heap)
            while len(heap) > 1:
                izq = heapq.heappop(heap)
                der = heapq.heappop(heap)
                padre = NodoHuffman(None, izq.frecuencia + der.frecuencia)
                padre.izquierdo = izq
                padre.derecho = der
                heapq.heappush(heap, padre)
            self.raiz = heap[0]
            
            # Convertir bytes a bits
            bits = ""
            for byte in datos_comprimidos:
                bits += f"{byte:08b}"
            
            # Quitar padding
            if padding > 0:
                bits = bits[:-padding]
            
            # Decodificar
            texto_decodificado = []
            nodo_actual = self.raiz
            for bit in bits:
                if bit == '0':
                    nodo_actual = nodo_actual.izquierdo
                else:
                    nodo_actual = nodo_actual.derecho
                
                if nodo_actual.es_hoja():
                    texto_decodificado.append(nodo_actual.caracter)
                    nodo_actual = self.raiz
            
            with open(ruta_salida, 'w', encoding='utf-8') as f:
                f.write("".join(texto_decodificado))
            
            print(f"Archivo descomprimido guardado en: {ruta_salida}")
            
        except Exception as e:
            print(f"Error al descomprimir: {e}")

    def _mostrar_estadisticas(self, original, comprimido):
        size_orig = os.path.getsize(original)
        size_comp = os.path.getsize(comprimido)
        ahorro = (1 - size_comp/size_orig) * 100
        print(f"\nEstadísticas:")
        print(f"Original: {size_orig} bytes")
        print(f"Comprimido: {size_comp} bytes")
        print(f"Ahorro: {ahorro:.2f}%")

if __name__ == "__main__":
    # Prueba simple
    h = Huffman()
    # Crear archivo temporal
    with open("temp.txt", "w") as f:
        f.write("ABRACADABRA " * 100)
    
    h.comprimir_archivo("temp.txt", "temp.huff")
    h.descomprimir_archivo("temp.huff", "temp_out.txt")
    
    # Limpieza
    # os.remove("temp.txt")
    # os.remove("temp.huff")
    # os.remove("temp_out.txt")