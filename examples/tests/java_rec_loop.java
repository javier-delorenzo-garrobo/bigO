public class java_rec_loop {
    /* O(n log n) — Recursión con un bucle interior (estilo merge sort) */
    public static void mergeSort(int[] arr, int inicio, int fin) {
        if (inicio >= fin) {
            return;
        }
        int medio = (inicio + fin) / 2;
        mergeSort(arr, inicio, medio);
        mergeSort(arr, medio + 1, fin);
        for (int i = inicio; i <= fin; i++) {
            arr[i] = arr[i]; // placeholder merge
        }
    }
}
