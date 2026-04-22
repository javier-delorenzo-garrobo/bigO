# ─────────────────────────────────────────────────────────────
# analyzer/python_analyzer.py
# Analizador de complejidad para código Python.
#
# Usa el módulo estándar `ast` para construir el AST real
# del fichero, lo que permite un análisis preciso de la
# estructura de bucles y llamadas recursivas sin depender
# de regex frágiles.
# ─────────────────────────────────────────────────────────────

import ast

from analyzer.base_analyzer import BaseAnalyzer, FunctionAnalysis


class PythonAnalyzer(BaseAnalyzer):
    """Analizador de complejidad para Python basado en AST."""

    def analyze(self, source_code: str) -> list[FunctionAnalysis]:
        """Parsea el AST del código Python y extrae métricas por función."""
        try:
            tree = ast.parse(source_code)
        except SyntaxError:
            return []

        source_lines = source_code.splitlines()
        results = []
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                preceding_line_idx = node.lineno - 2
                preceding_line = source_lines[preceding_line_idx] if 0 <= preceding_line_idx < len(source_lines) else ""
                
                end_lineno = getattr(node, "end_lineno", len(source_lines))
                body_lines = source_lines[node.lineno:end_lineno]
                body_text = "\n".join(body_lines)
                
                if self._is_ignored(body_text, preceding_line):
                    continue
                
                max_depth = self._max_loop_depth(node)
                is_recursive = self._detect_recursion(node)
                results.append(FunctionAnalysis(
                    name=node.name,
                    max_depth=max_depth,
                    is_recursive=is_recursive
                ))

        # Si no hay funciones, analizamos a nivel global
        if not results:
            max_depth = self._max_loop_depth(tree)
            is_recursive = False # Sin funciones no hay recursión (normalmente)
            results.append(FunctionAnalysis(
                name="Global",
                max_depth=max_depth,
                is_recursive=is_recursive
            ))

        return results

    # ── Profundidad de bucles ────────────────────────────────

    def _max_loop_depth(self, node: ast.AST, current_depth: int = 0) -> int:
        """Calcula recursivamente la profundidad máxima de bucles anidados."""
        max_found = current_depth

        for child in ast.iter_child_nodes(node):
            if isinstance(child, (ast.For, ast.While, ast.AsyncFor)):
                depth = self._max_loop_depth(child, current_depth + 1)
                max_found = max(max_found, depth)
            # Evitamos descender dentro de funciones internas si empezamos desde un módulo
            # pero como analizamos nodo por nodo, si este nodo no es bucle, seguimos.
            # Cuidado: no queremos contar bucles de funciones internas como propios
            # de la función externa. AST iter_child_nodes entrará en funciones internas.
            elif isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            else:
                depth = self._max_loop_depth(child, current_depth)
                max_found = max(max_found, depth)

        return max_found

    # ── Detección de recursividad ────────────────────────────

    def _detect_recursion(self, func_node: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
        """Comprueba si la función dada se llama a sí misma."""
        func_name = func_node.name
        for inner in ast.walk(func_node):
            if isinstance(inner, ast.Call):
                if isinstance(inner.func, ast.Name) and inner.func.id == func_name:
                    return True
                if isinstance(inner.func, ast.Attribute) and inner.func.attr == func_name:
                    return True
        return False
