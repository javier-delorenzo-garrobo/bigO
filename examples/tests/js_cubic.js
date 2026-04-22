/* O(n³) — Bucles anidados triples */
const multiplicarMatrices = function(a, b, c, n) {
    for (let i = 0; i < n; i++) {
        for (let j = 0; j < n; j++) {
            c[i][j] = 0;
            for (let k = 0; k < n; k++) {
                c[i][j] += a[i][k] * b[k][j];
            }
        }
    }
};
