# O(n log n) — Recursión con un bucle interior (estilo merge sort)
def merge_sort(lista):
    if len(lista) <= 1:
        return lista
    medio = len(lista) // 2
    izquierda = merge_sort(lista[:medio])
    derecha = merge_sort(lista[medio:])
    resultado = []
    for elem in izquierda:
        resultado.append(elem)
    for elem in derecha:
        resultado.append(elem)
    return resultado
