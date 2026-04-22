# Archivo con varias funciones de distinta complejidad

# O(1)
def maximo(a, b):
    return a if a > b else b

# O(n)
def sumar_lista(lista):
    total = 0
    for elem in lista:
        total += elem
    return total

# O(n²)
def seleccion(lista):
    n = len(lista)
    for i in range(n - 1):
        min_idx = i
        for j in range(i + 1, n):
            if lista[j] < lista[min_idx]:
                min_idx = j
        lista[i], lista[min_idx] = lista[min_idx], lista[i]
    return lista

# O(n) recursivo
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)
