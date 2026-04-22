/*
 * ejemplo.js — Fichero de prueba para el analizador de JavaScript.
 *
 * Contiene funciones con distintas complejidades:
 *   - sumaConstante()       → O(1)
 *   - busquedaLineal()      → O(n)
 *   - ordenarBurbuja()      → O(n²)
 *   - factorialRecursivo()  → O(n) recursivo
 */

/* Operación constante: no depende del tamaño de entrada */
function sumaConstante(a, b) {
    return a + b;
}

/* Busca un elemento recorriendo el array una vez → O(n) */
function busquedaLineal(arr, objetivo) {
    for (let i = 0; i < arr.length; i++) {
        if (arr[i] === objetivo) {
            return i;
        }
    }
    return -1;
}

/* Ordenamiento burbuja clásico → O(n²) */
function ordenarBurbuja(arr) {
    const n = arr.length;
    for (let i = 0; i < n - 1; i++) {
        for (let j = 0; j < n - i - 1; j++) {
            if (arr[j] > arr[j + 1]) {
                const temp = arr[j];
                arr[j] = arr[j + 1];
                arr[j + 1] = temp;
            }
        }
    }
    return arr;
}

/* Factorial recursivo → O(n) recursivo */
function factorialRecursivo(n) {
    if (n <= 1) {
        return 1;
    }
    return n * factorialRecursivo(n - 1);
}

// --- Ejecución de prueba ---
const datos = [64, 34, 25, 12, 22, 11, 90];
console.log("Factorial de 5:", factorialRecursivo(5));
console.log("Array ordenado:", ordenarBurbuja([...datos]));
