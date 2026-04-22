public class java_linear {
    /* O(n) — Un solo bucle */
    public static int buscar(int[] arr, int x) {
        for (int i = 0; i < arr.length; i++) {
            if (arr[i] == x) {
                return i;
            }
        }
        return -1;
    }
}
