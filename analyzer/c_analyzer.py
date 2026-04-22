# ─────────────────────────────────────────────────────────────
# analyzer/c_analyzer.py
# Analizador de complejidad para código C (.c / .h).
#
# Al no disponer de un parser AST estándar en Python para C,
# se utilizan expresiones regulares y heurísticas sobre el
# texto fuente. Es menos preciso que el análisis AST de
# Python, pero suficiente para la mayoría de casos habituales.
# ─────────────────────────────────────────────────────────────

import re

from analyzer.base_analyzer import BaseAnalyzer, FunctionAnalysis


class CAnalyzer(BaseAnalyzer):
    """Analizador heurístico de complejidad para C."""

    # Patrones que identifican el inicio de un bucle en C
    _LOOP_PATTERNS: list[re.Pattern[str]] = [
        re.compile(r"\bfor\s*\("),
        re.compile(r"\bwhile\s*\("),
        re.compile(r"\bdo\s*\{"),
    ]

    # Patrón para extraer definiciones de funciones en C
    # Captura el nombre de la función (grupo 1)
    # Excluye palabras clave de control para no dar falsos positivos.
    _FUNC_DEF_PATTERN: re.Pattern[str] = re.compile(
        r"(?:^|\n)\s*"
        r"(?!if|while|for|switch|return|sizeof\b)[\w\s\*]+?"
        r"\b(?!(?:if|while|for|switch|return|sizeof)\b)([a-zA-Z_]\w*)\s*\("
        r"[^)]*\)\s*\{"
    )

    def analyze(self, source_code: str) -> list[FunctionAnalysis]:
        """Analiza código C usando regex para estimar métricas por función."""
        clean = self._strip_comments(source_code)
        source_lines = source_code.splitlines()
        results = []

        for match in self._FUNC_DEF_PATTERN.finditer(clean):
            func_name = match.group(1)
            
            func_name_start = match.start(1)
            line_idx = clean[:func_name_start].count("\n")
            preceding_line = source_lines[line_idx - 1] if line_idx > 0 else ""
            
            original_body = self._extract_body(source_code, match.end() - 1)
            
            if self._is_ignored(original_body, preceding_line):
                continue
                
            clean_body = self._extract_body(clean, match.end() - 1)
            
            # Analizamos métricas SÓLO dentro del cuerpo limpio
            max_depth = self._max_loop_depth(clean_body)
            is_recursive = self._detect_recursion_in_body(clean_body, func_name)
            
            results.append(FunctionAnalysis(
                name=func_name,
                max_depth=max_depth,
                is_recursive=is_recursive,
                body=clean_body
            ))

        return results
