# ─────────────────────────────────────────────────────────────
# ejemplo.py — Fichero de prueba para el analizador de Python.
#
# Contiene funciones con distintas complejidades para
# verificar que el analizador las detecta correctamente:
#   - constante_ejemplo()    → O(1)
#   - busqueda_lineal()      → O(n)
#   - burbuja()              → O(n²)
#   - factorial_recursivo()  → O(n) recursivo
# ─────────────────────────────────────────────────────────────


def constante_ejemplo(x: int) -> int:
    """Operación constante: no depende del tamaño de la entrada."""
    return x * 2 + 1


def busqueda_lineal(lista: list[int], objetivo: int) -> int:
    """Busca un elemento recorriendo la lista una vez → O(n)."""
    for i in range(len(lista)):
        if lista[i] == objetivo:
            return i
    return -1


def burbuja(lista: list[int]) -> list[int]:
    """Ordenamiento burbuja clásico → O(n²)."""
    n = len(lista)
    for i in range(n):
        for j in range(0, n - i - 1):
            if lista[j] > lista[j + 1]:
                lista[j], lista[j + 1] = lista[j + 1], lista[j]
    return lista


def factorial_recursivo(n: int) -> int:
    """Calcula el factorial recursivamente → O(n) recursivo."""
    if n <= 1:
        return 1
    return n * factorial_recursivo(n - 1)


if __name__ == "__main__":
    datos = [64, 34, 25, 12, 22, 11, 90]
    print("Original:", datos)
    print("Ordenado:", burbuja(datos.copy()))
    print("Factorial de 5:", factorial_recursivo(5))
