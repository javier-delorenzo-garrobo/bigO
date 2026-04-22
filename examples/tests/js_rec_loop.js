/* O(n log n) — Recursión con un bucle interior (estilo merge sort) */
const mergeSort = (arr, inicio, fin) => {
    if (inicio >= fin) {
        return;
    }
    let medio = Math.floor((inicio + fin) / 2);
    mergeSort(arr, inicio, medio);
    mergeSort(arr, medio + 1, fin);
    for (let i = inicio; i <= fin; i++) {
        arr[i] = arr[i]; // placeholder merge
    }
};
