/*
 * ejemplo.java — Fichero de prueba para el analizador de Java.
 *
 * Contiene métodos con distintas complejidades:
 *   - sumaConstante()       → O(1)
 *   - busquedaLineal()      → O(n)
 *   - ordenarBurbuja()      → O(n²)
 *   - factorialRecursivo()  → O(n) recursivo
 */

public class ejemplo {

    /* Operación constante: no depende del tamaño de entrada */
    public static int sumaConstante(int a, int b) {
        return a + b;
    }

    /* Busca un elemento recorriendo el array una vez → O(n) */
    public static int busquedaLineal(int[] arr, int objetivo) {
        for (int i = 0; i < arr.length; i++) {
            if (arr[i] == objetivo) {
                return i;
            }
        }
        return -1;
    }

    /* Ordenamiento burbuja clásico → O(n²) */
    public static void ordenarBurbuja(int[] arr) {
        int n = arr.length;
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
    public static int factorialRecursivo(int n) {
        if (n <= 1) {
            return 1;
        }
        return n * factorialRecursivo(n - 1);
    }

    public static void main(String[] args) {
        int[] datos = {64, 34, 25, 12, 22, 11, 90};

        System.out.println("Factorial de 5: " + factorialRecursivo(5));

        ordenarBurbuja(datos);
        System.out.print("Array ordenado: ");
        for (int dato : datos) {
            System.out.print(dato + " ");
        }
        System.out.println();
    }
}
