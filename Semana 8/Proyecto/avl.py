class NodoAVL:
    def __init__(self, palabra, linea, columna):
        self.palabra = palabra
        self.posiciones = [(linea, columna)]
        self.izquierdo = None
        self.derecho = None
        self.altura = 1

class AVL:
    """
    Árbol AVL para indexación de texto balanceada.
    Almacena palabras y sus posiciones (línea, columna).
    """
    
    def __init__(self):
        self.raiz = None
    
    def altura(self, nodo):
        return nodo.altura if nodo else 0
    
    def factor_balance(self, nodo):
        if not nodo:
            return 0
        return self.altura(nodo.izquierdo) - self.altura(nodo.derecho)
    
    def actualizar_altura(self, nodo):
        nodo.altura = 1 + max(self.altura(nodo.izquierdo), self.altura(nodo.derecho))
    
    def rotacion_derecha(self, z):
        y = z.izquierdo
        T3 = y.derecho
        
        y.derecho = z
        z.izquierdo = T3
        
        self.actualizar_altura(z)
        self.actualizar_altura(y)
        
        return y
    
    def rotacion_izquierda(self, z):
        y = z.derecho
        T2 = y.izquierdo
        
        y.izquierdo = z
        z.derecho = T2
        
        self.actualizar_altura(z)
        self.actualizar_altura(y)
        
        return y
    
    def insertar(self, palabra, linea, columna):
        self.raiz = self._insertar_recursivo(self.raiz, palabra, linea, columna)
    
    def _insertar_recursivo(self, nodo, palabra, linea, columna):
        if not nodo:
            return NodoAVL(palabra, linea, columna)
        
        if palabra < nodo.palabra:
            nodo.izquierdo = self._insertar_recursivo(nodo.izquierdo, palabra, linea, columna)
        elif palabra > nodo.palabra:
            nodo.derecho = self._insertar_recursivo(nodo.derecho, palabra, linea, columna)
        else:
            nodo.posiciones.append((linea, columna))
            return nodo
        
        self.actualizar_altura(nodo)
        fb = self.factor_balance(nodo)
        
        # Casos de rotación
        # LL
        if fb > 1 and palabra < nodo.izquierdo.palabra:
            return self.rotacion_derecha(nodo)
        # RR
        if fb < -1 and palabra > nodo.derecho.palabra:
            return self.rotacion_izquierda(nodo)
        # LR
        if fb > 1 and palabra > nodo.izquierdo.palabra:
            nodo.izquierdo = self.rotacion_izquierda(nodo.izquierdo)
            return self.rotacion_derecha(nodo)
        # RL
        if fb < -1 and palabra < nodo.derecho.palabra:
            nodo.derecho = self.rotacion_derecha(nodo.derecho)
            return self.rotacion_izquierda(nodo)
        
        return nodo

    def buscar(self, palabra):
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
        self.raiz = self._eliminar_recursivo(self.raiz, palabra)

    def _eliminar_recursivo(self, nodo, palabra):
        if not nodo:
            return None
        
        if palabra < nodo.palabra:
            nodo.izquierdo = self._eliminar_recursivo(nodo.izquierdo, palabra)
        elif palabra > nodo.palabra:
            nodo.derecho = self._eliminar_recursivo(nodo.derecho, palabra)
        else:
            if not nodo.izquierdo or not nodo.derecho:
                temp = nodo.izquierdo if nodo.izquierdo else nodo.derecho
                if not temp:
                    temp = None
                    nodo = None
                else:
                    nodo = temp
            else:
                temp = self._encontrar_minimo(nodo.derecho)
                nodo.palabra = temp.palabra
                nodo.posiciones = temp.posiciones
                nodo.derecho = self._eliminar_recursivo(nodo.derecho, temp.palabra)
        
        if not nodo:
            return None
        
        self.actualizar_altura(nodo)
        fb = self.factor_balance(nodo)
        
        # Balanceo tras eliminación
        if fb > 1 and self.factor_balance(nodo.izquierdo) >= 0:
            return self.rotacion_derecha(nodo)
        if fb > 1 and self.factor_balance(nodo.izquierdo) < 0:
            nodo.izquierdo = self.rotacion_izquierda(nodo.izquierdo)
            return self.rotacion_derecha(nodo)
        if fb < -1 and self.factor_balance(nodo.derecho) <= 0:
            return self.rotacion_izquierda(nodo)
        if fb < -1 and self.factor_balance(nodo.derecho) > 0:
            nodo.derecho = self.rotacion_derecha(nodo.derecho)
            return self.rotacion_izquierda(nodo)
            
        return nodo

    def _encontrar_minimo(self, nodo):
        actual = nodo
        while actual.izquierdo:
            actual = actual.izquierdo
        return actual

    def inorden(self):
        resultado = []
        self._inorden_recursivo(self.raiz, resultado)
        return resultado
    
    def _inorden_recursivo(self, nodo, resultado):
        if nodo:
            self._inorden_recursivo(nodo.izquierdo, resultado)
            resultado.append((nodo.palabra, nodo.posiciones))
            self._inorden_recursivo(nodo.derecho, resultado)

if __name__ == "__main__":
    avl = AVL()
    palabras = ["perro", "gato", "casa", "arbol", "zorro", "perro"]
    for i, p in enumerate(palabras):
        avl.insertar(p, 1, i+1)
    
    print("Inorden:", avl.inorden())
    print("Raíz:", avl.raiz.palabra) # Debería estar balanceado