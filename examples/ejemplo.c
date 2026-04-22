/*
 * ejemplo.c — Fichero de prueba para el analizador de C.
 *
 * Contiene funciones con distintas complejidades:
 *   - suma_constante()       → O(1)
 *   - busqueda_lineal()      → O(n)
 *   - ordenar_burbuja()      → O(n²)
 *   - factorial_recursivo()  → O(n) recursivo
 */

#include <stdio.h>

/* Operación constante: no depende del tamaño de entrada */
int suma_constante(int a, int b) {
    return a + b;
}

/* Busca un elemento recorriendo el array una vez → O(n) */
int busqueda_lineal(int arr[], int n, int objetivo) {
    for (int i = 0; i < n; i++) {
        if (arr[i] == objetivo) {
            return i;
        }
    }
    return -1;
}

/* Ordenamiento burbuja clásico → O(n²) */
void ordenar_burbuja(int arr[], int n) {
    for (int i = 0; i < n - 1; i++) {
        for (int j = 0; j < n - i - 1; j++) {
            if (arr[j] > arr[j + 1]) {
                int temp = arr[j];
                arr[j] = arr[j + 1];
                arr[j + 1] = temp;
            }
        }
    }
}

/* Factorial recursivo → O(n) recursivo */
int factorial_recursivo(int n) {
    if (n <= 1) {
        return 1;
    }
    return n * factorial_recursivo(n - 1);
}

int main() {
    int datos[] = {64, 34, 25, 12, 22, 11, 90};
    int n = sizeof(datos) / sizeof(datos[0]);

    printf("Factorial de 5: %d\n", factorial_recursivo(5));

    ordenar_burbuja(datos, n);
    printf("Array ordenado: ");
    for (int i = 0; i < n; i++) {
        printf("%d ", datos[i]);
    }
    printf("\n");

    return 0;
}
