# ─────────────────────────────────────────────────────────────
# analyzer/java_analyzer.py
# Analizador de complejidad para código Java (.java).
#
# Funciona con regex y heurísticas sobre el texto fuente,
# de forma análoga al analizador de C. Las diferencias
# principales son los patrones de definición de función
# (métodos Java incluyen modificadores de acceso, anotaciones,
# etc.) y los bucles for-each.
# ─────────────────────────────────────────────────────────────

import re

from analyzer.base_analyzer import BaseAnalyzer, FunctionAnalysis


class JavaAnalyzer(BaseAnalyzer):
    """Analizador heurístico de complejidad para Java."""

    # Patrones que identifican el inicio de un bucle en Java
    _LOOP_PATTERNS: list[re.Pattern[str]] = [
        re.compile(r"\bfor\s*\("),       # for clásico y for-each
        re.compile(r"\bwhile\s*\("),
        re.compile(r"\bdo\s*\{"),
    ]

    # Patrón para métodos Java (public void foo(...) {)
    # Grupo 1 captura el nombre del método
    _METHOD_DEF_PATTERN: re.Pattern[str] = re.compile(
        r"(?:public|private|protected|static|final|abstract|synchronized|\s)+"
        r"(?!if|while|for|switch|catch\b)[\w<>\[\],\s]+?"       # Tipo de retorno (puede incluir genéricos)
        r"\b(?!(?:if|while|for|switch|catch)\b)([a-zA-Z_]\w*)\s*\("          # Nombre del método
        r"[^)]*\)\s*"            # Parámetros
        r"(?:throws\s+[\w,\s]+)?"  # Cláusula throws opcional
        r"\s*\{"                # Llave de apertura del cuerpo
    )

    def analyze(self, source_code: str) -> list[FunctionAnalysis]:
        """Analiza código Java usando regex para estimar métricas por función."""
        clean = self._strip_comments(source_code)
        source_lines = source_code.splitlines()
        line_starts = self._build_line_starts(clean)
        results = []

        for match in self._METHOD_DEF_PATTERN.finditer(clean):
            method_name = match.group(1)
            
            func_name_start = match.start(1)
            line_idx = self._line_index_from_pos(line_starts, func_name_start)
            preceding_line = source_lines[line_idx - 1] if line_idx > 0 else ""
            
            original_body = self._extract_body(source_code, match.end() - 1)
            
            if self._is_ignored(original_body, preceding_line):
                continue
            
            clean_body = self._extract_body(clean, match.end() - 1)
            max_depth = self._max_loop_depth(clean_body)
            is_recursive = self._detect_recursion_in_body(clean_body, method_name)
            
            results.append(FunctionAnalysis(
                name=method_name,
                max_depth=max_depth,
                is_recursive=is_recursive,
                body=clean_body
            ))

        return results
