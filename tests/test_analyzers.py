import unittest
from pathlib import Path

from analyzer import get_analyzer


class BaseTestAnalyzer(unittest.TestCase):
    def _run_file_test(self, filename: str, func_name: str, expected_complexity: str) -> None:
        path = Path("examples/tests") / filename
        self.assertTrue(path.is_file(), f"No se encontró el fichero de test: {path}")
        analyzer_info = get_analyzer(path.suffix.lower())
        self.assertIsNotNone(analyzer_info)
        if analyzer_info:
            analyzer, _ = analyzer_info
            source_code = path.read_text(encoding="utf-8")
            analysis_results = analyzer.estimate_complexity(source_code)
            result = next((r for r in analysis_results if r.function_name == func_name), None)
            self.assertIsNotNone(result, f"No se detectó la función '{func_name}' en {filename}")
            if result:
                self.assertEqual(result.complexity, expected_complexity)

    def _run_source_test(
        self,
        extension: str,
        source_code: str,
        expected_by_function: dict[str, str],
    ) -> None:
        analyzer_info = get_analyzer(extension)
        self.assertIsNotNone(analyzer_info, f"No hay analizador para {extension}")
        if analyzer_info:
            analyzer, _ = analyzer_info
            analysis_results = analyzer.estimate_complexity(source_code)
            by_name = {result.function_name: result for result in analysis_results}
            for func_name, expected_complexity in expected_by_function.items():
                self.assertIn(
                    func_name,
                    by_name,
                    f"No se detectó la función '{func_name}' para extensión {extension}",
                )
                self.assertEqual(by_name[func_name].complexity, expected_complexity)


class TestCAnalyzer(BaseTestAnalyzer):
    def test_constant(self) -> None:
        self._run_file_test("c_constant.c", "suma", "O(1)")

    def test_linear(self) -> None:
        self._run_file_test("c_linear.c", "buscar", "O(n)")

    def test_quadratic(self) -> None:
        self._run_file_test("c_quadratic.c", "burbuja", "O(n²)")

    def test_cubic(self) -> None:
        self._run_file_test("c_cubic.c", "multiplicar_matrices", "O(n³)")

    def test_recursive(self) -> None:
        self._run_file_test("c_recursive.c", "factorial", "O(n)")

    def test_rec_loop(self) -> None:
        self._run_file_test("c_rec_loop.c", "merge_sort", "O(n)")

    def test_mixed(self) -> None:
        self._run_file_test("c_mixed.c", "maximo", "O(1)")
        self._run_file_test("c_mixed.c", "sumar_array", "O(n)")
        self._run_file_test("c_mixed.c", "seleccion", "O(n²)")
        self._run_file_test("c_mixed.c", "fibonacci", "O(n)")

    def test_ignore(self) -> None:
        source = """
// bigO: ignore
void ignored_func() {
    for(int i=0; i<10; i++) {}
}
void normal_func() {
    for(int i=0; i<10; i++) {}
}
"""
        analyzer_info = get_analyzer(".c")
        if analyzer_info:
            analyzer, _ = analyzer_info
            results = analyzer.estimate_complexity(source)
            self.assertEqual(len(results), 1)
            self.assertEqual(results[0].function_name, "normal_func")


class TestPythonAnalyzer(BaseTestAnalyzer):
    def test_constant(self) -> None:
        self._run_file_test("py_constant.py", "suma", "O(1)")

    def test_linear(self) -> None:
        self._run_file_test("py_linear.py", "buscar", "O(n)")

    def test_quadratic(self) -> None:
        self._run_file_test("py_quadratic.py", "burbuja", "O(n²)")

    def test_cubic(self) -> None:
        self._run_file_test("py_cubic.py", "multiplicar_matrices", "O(n³)")

    def test_recursive(self) -> None:
        self._run_file_test("py_recursive.py", "factorial", "O(n)")

    def test_rec_loop(self) -> None:
        self._run_file_test("py_rec_loop.py", "merge_sort", "O(n)")

    def test_mixed(self) -> None:
        self._run_file_test("py_mixed.py", "maximo", "O(1)")
        self._run_file_test("py_mixed.py", "sumar_lista", "O(n)")
        self._run_file_test("py_mixed.py", "seleccion", "O(n²)")
        self._run_file_test("py_mixed.py", "fibonacci", "O(n)")

    def test_ignore(self) -> None:
        source = """
# bigo: ignore
def ignored_func():
    for i in range(10): pass

def normal_func():
    # Esta debe ser analizada
    for i in range(10): pass
"""
        analyzer_info = get_analyzer(".py")
        if analyzer_info:
            analyzer, _ = analyzer_info
            results = analyzer.estimate_complexity(source)
            self.assertEqual(len(results), 1)
            self.assertEqual(results[0].function_name, "normal_func")


class TestJavaAnalyzer(BaseTestAnalyzer):
    def test_constant(self) -> None:
        self._run_file_test("java_constant.java", "suma", "O(1)")

    def test_linear(self) -> None:
        self._run_file_test("java_linear.java", "buscar", "O(n)")

    def test_quadratic(self) -> None:
        self._run_file_test("java_quadratic.java", "burbuja", "O(n²)")

    def test_cubic(self) -> None:
        self._run_file_test("java_cubic.java", "multiplicarMatrices", "O(n³)")

    def test_recursive(self) -> None:
        self._run_file_test("java_recursive.java", "factorial", "O(n)")

    def test_rec_loop(self) -> None:
        self._run_file_test("java_rec_loop.java", "mergeSort", "O(n)")

    def test_mixed(self) -> None:
        self._run_file_test("java_mixed.java", "maximo", "O(1)")
        self._run_file_test("java_mixed.java", "sumarArray", "O(n)")
        self._run_file_test("java_mixed.java", "seleccion", "O(n²)")
        self._run_file_test("java_mixed.java", "fibonacci", "O(n)")

    def test_ignore(self) -> None:
        source = """
public class Test {
    // bigo: ignore
    public void ignoredFunc() {
        for(int i=0; i<10; i++) {}
    }
    public void normalFunc() {
        for(int i=0; i<10; i++) {}
    }
}
"""
        analyzer_info = get_analyzer(".java")
        if analyzer_info:
            analyzer, _ = analyzer_info
            results = analyzer.estimate_complexity(source)
            self.assertEqual(len(results), 1)
            self.assertEqual(results[0].function_name, "normalFunc")


class TestJavaScriptAnalyzer(BaseTestAnalyzer):
    def test_constant(self) -> None:
        self._run_file_test("js_constant.js", "suma", "O(1)")

    def test_linear(self) -> None:
        self._run_file_test("js_linear.js", "buscar", "O(n)")

    def test_quadratic(self) -> None:
        self._run_file_test("js_quadratic.js", "burbuja", "O(n²)")

    def test_cubic(self) -> None:
        self._run_file_test("js_cubic.js", "multiplicarMatrices", "O(n³)")

    def test_recursive(self) -> None:
        self._run_file_test("js_recursive.js", "factorial", "O(n)")

    def test_rec_loop(self) -> None:
        self._run_file_test("js_rec_loop.js", "mergeSort", "O(n)")

    def test_mixed(self) -> None:
        self._run_file_test("js_mixed.js", "maximo", "O(1)")
        self._run_file_test("js_mixed.js", "sumarArray", "O(n)")
        self._run_file_test("js_mixed.js", "seleccion", "O(n²)")
        self._run_file_test("js_mixed.js", "fibonacci", "O(n)")

    def test_ignore(self) -> None:
        source = """
// bigO: ignore
function ignoredFunc() {
    for(let i=0; i<10; i++) {}
}
function normalFunc() {
    for(let i=0; i<10; i++) {}
}
"""
        analyzer_info = get_analyzer(".js")
        if analyzer_info:
            analyzer, _ = analyzer_info
            results = analyzer.estimate_complexity(source)
            self.assertEqual(len(results), 1)
            self.assertEqual(results[0].function_name, "normalFunc")


class TestDiverseCodeBank(BaseTestAnalyzer):
    def test_python_snippets_bank(self) -> None:
        cases = [
            (
                "python_global_without_functions",
                """
for i in range(5):
    print(i)
""",
                {"Global": "O(n)"},
            ),
            (
                "python_nested_function_not_counted_in_outer",
                """
def outer(nums):
    for _ in nums:
        pass

    def inner(m):
        for i in m:
            for j in m:
                pass

    return len(nums)
""",
                {"outer": "O(n)", "inner": "O(n²)"},
            ),
            (
                "python_recursion_with_loop",
                """
def process(n):
    for _ in range(n):
        pass
    if n <= 1:
        return 1
    return process(n - 1)
""",
                {"process": "O(n)"},
            ),
        ]

        for case_name, source_code, expected in cases:
            with self.subTest(case=case_name):
                self._run_source_test(".py", source_code, expected)

    def test_c_snippets_bank(self) -> None:
        cases = [
            (
                "c_functions_with_different_orders",
                """
int constant() {
    return 1;
}

int linear(int n) {
    for (int i = 0; i < n; i++) {
    }
    return n;
}

int quadratic(int n) {
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
        }
    }
    return n;
}
""",
                {"constant": "O(1)", "linear": "O(n)", "quadratic": "O(n²)"},
            ),
            (
                "c_recursion_plus_loop",
                """
int walk(int n) {
    for (int i = 0; i < n; i++) {
    }
    if (n <= 0) {
        return 0;
    }
    return walk(n - 1);
}
""",
                {"walk": "O(n)"},
            ),
        ]

        for case_name, source_code, expected in cases:
            with self.subTest(case=case_name):
                self._run_source_test(".c", source_code, expected)

    def test_java_snippets_bank(self) -> None:
        cases = [
            (
                "java_class_methods_varied",
                """
public class Sample {
    public int base(int a) {
        return a;
    }

    public int linear(int n) {
        for (int i = 0; i < n; i++) {
        }
        return n;
    }

    public int cubic(int n) {
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                for (int k = 0; k < n; k++) {
                }
            }
        }
        return n;
    }
}
""",
                {"base": "O(1)", "linear": "O(n)", "cubic": "O(n³)"},
            ),
            (
                "java_recursive_with_loop",
                """
public class Rec {
    public int go(int n) {
        for (int i = 0; i < n; i++) {
        }
        if (n <= 1) {
            return 1;
        }
        return go(n - 1);
    }
}
""",
                {"go": "O(n)"},
            ),
        ]

        for case_name, source_code, expected in cases:
            with self.subTest(case=case_name):
                self._run_source_test(".java", source_code, expected)

    def test_js_snippets_bank(self) -> None:
        cases = [
            (
                "js_function_and_arrow",
                """
function constant() {
    return 1;
}

const linear = (n) => {
    for (let i = 0; i < n; i++) {
    }
    return n;
};

const square = function(n) {
    for (let i = 0; i < n; i++) {
        for (let j = 0; j < n; j++) {
        }
    }
    return n;
};
""",
                {"constant": "O(1)", "linear": "O(n)", "square": "O(n²)"},
            ),
            (
                "js_recursion_plus_loop",
                """
function walk(n) {
    for (let i = 0; i < n; i++) {
    }
    if (n <= 1) {
        return 1;
    }
    return walk(n - 1);
}
""",
                {"walk": "O(n)"},
            ),
        ]

        for case_name, source_code, expected in cases:
            with self.subTest(case=case_name):
                self._run_source_test(".js", source_code, expected)


if __name__ == "__main__":
    unittest.main(verbosity=2)
