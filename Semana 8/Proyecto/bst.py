class NodoBST:
    def __init__(self, palabra, linea, columna):
        self.palabra = palabra
        self.posiciones = [(linea, columna)]  # Lista de tuplas (linea, columna)
        self.izquierdo = None
        self.derecho = None

class BST:
    """
    Árbol Binario de Búsqueda para indexación de texto.
    Almacena palabras y sus posiciones (línea, columna).
    """
    
    def __init__(self):
        self.raiz = None
    
    def insertar(self, palabra, linea, columna):
        """Inserta una palabra o agrega una nueva posición si ya existe."""
        if not self.raiz:
            self.raiz = NodoBST(palabra, linea, columna)
        else:
            self._insertar_recursivo(self.raiz, palabra, linea, columna)
    
    def _insertar_recursivo(self, nodo, palabra, linea, columna):
        if palabra < nodo.palabra:
            if nodo.izquierdo is None:
                nodo.izquierdo = NodoBST(palabra, linea, columna)
            else:
                self._insertar_recursivo(nodo.izquierdo, palabra, linea, columna)
        elif palabra > nodo.palabra:
            if nodo.derecho is None:
                nodo.derecho = NodoBST(palabra, linea, columna)
            else:
                self._insertar_recursivo(nodo.derecho, palabra, linea, columna)
        else:
            # La palabra ya existe, agregamos la nueva posición
            nodo.posiciones.append((linea, columna))
    
    def buscar(self, palabra):
        """Busca una palabra y retorna sus posiciones o None."""
        return self._buscar_recursivo(self.raiz, palabra)
    
    def _buscar_recursivo(self, nodo, palabra):
        if nodo is None:
            return None
        if palabra == nodo.palabra:
            return nodo.posiciones
        elif palabra < nodo.palabra:
            return self._buscar_recursivo(nodo.izquierdo, palabra)
        else:
            return self._buscar_recursivo(nodo.derecho, palabra)
    
    def eliminar(self, palabra):
        """Elimina una palabra del índice."""
        self.raiz = self._eliminar_recursivo(self.raiz, palabra)
    
    def _eliminar_recursivo(self, nodo, palabra):
        if nodo is None:
            return None
        
        if palabra < nodo.palabra:
            nodo.izquierdo = self._eliminar_recursivo(nodo.izquierdo, palabra)
        elif palabra > nodo.palabra:
            nodo.derecho = self._eliminar_recursivo(nodo.derecho, palabra)
        else:
            # Caso 1: Hoja
            if nodo.izquierdo is None and nodo.derecho is None:
                return None
            
            # Caso 2: Un hijo
            if nodo.izquierdo is None:
                return nodo.derecho
            if nodo.derecho is None:
                return nodo.izquierdo
            
            # Caso 3: Dos hijos
            sucesor = self._encontrar_minimo(nodo.derecho)
            nodo.palabra = sucesor.palabra
            nodo.posiciones = sucesor.posiciones # Copiamos también las posiciones
            nodo.derecho = self._eliminar_recursivo(nodo.derecho, sucesor.palabra)
        
        return nodo
    
    def _encontrar_minimo(self, nodo):
        actual = nodo
        while actual.izquierdo is not None:
            actual = actual.izquierdo
        return actual
    
    def inorden(self):
        """Retorna una lista de tuplas (palabra, posiciones) ordenada."""
        resultado = []
        self._inorden_recursivo(self.raiz, resultado)
        return resultado
    
    def _inorden_recursivo(self, nodo, resultado):
        if nodo:
            self._inorden_recursivo(nodo.izquierdo, resultado)
            resultado.append((nodo.palabra, nodo.posiciones))
            self._inorden_recursivo(nodo.derecho, resultado)

if __name__ == "__main__":
    # Pruebas básicas
    bst = BST()
    bst.insertar("hola", 1, 1)
    bst.insertar("mundo", 1, 2)
    bst.insertar("hola", 2, 1) # Repetida
    
    print("Búsqueda 'hola':", bst.buscar("hola"))
    print("Inorden:", bst.inorden())
    
    bst.eliminar("hola")
    print("Después de eliminar 'hola':", bst.inorden())