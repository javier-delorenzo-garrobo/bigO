/* O(n log n) — Recursión con un bucle interior (estilo merge sort) */
void merge_sort(int arr[], int inicio, int fin) {
    if (inicio >= fin) {
        return;
    }
    int medio = (inicio + fin) / 2;
    merge_sort(arr, inicio, medio);
    merge_sort(arr, medio + 1, fin);
    for (int i = inicio; i <= fin; i++) {
        arr[i] = arr[i]; /* placeholder merge */
    }
}
