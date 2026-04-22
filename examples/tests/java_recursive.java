public class java_recursive {
    /* O(n) — Recursión simple sin bucles */
    public static int factorial(int n) {
        if (n <= 1) {
            return 1;
        }
        return n * factorial(n - 1);
    }
}
