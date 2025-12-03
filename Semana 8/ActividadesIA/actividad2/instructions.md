# Depuración de implementación de eliminación BST

[INSTRUCCIONES: Pega tu código de BST con el método eliminar y un caso de prueba que falla]

Tengo esta implementación de eliminación en BST:

```python
# [PEGAR TU CÓDIGO AQUÍ]
```

Caso de prueba:

```python
bst = BST()
for v in [50, 30, 70, 20, 40, 60, 80]:
    bst.insertar(v)
bst.eliminar(70)  # Nodo con dos hijos
print(bst.inorden())  # Esperado: [20, 30, 40, 50, 60, 80]
                      # Obtenido: [resultado incorrecto o error]
```

Tareas:

1. Identifica si el error está en el manejo de alguno de los 3 casos
2. Muestra la ejecución paso a paso para mi caso de prueba
3. Corrige el código con comentarios explicativos
4. Dame 3 casos de prueba adicionales que cubran cada caso de eliminación
