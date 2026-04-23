# ─────────────────────────────────────────────────────────────
# analyzer/js_analyzer.py
# Analizador de complejidad para código JavaScript (.js).
#
# Usa regex y heurísticas, al igual que los analizadores de
# C y Java. Las particularidades de JS son:
#   - Funciones declaradas con `function`, arrow functions,
#     y métodos de objeto.
#   - Bucles for...of y for...in además de los clásicos.
# ─────────────────────────────────────────────────────────────

import re

from analyzer.base_analyzer import BaseAnalyzer, FunctionAnalysis


class JavaScriptAnalyzer(BaseAnalyzer):
    """Analizador heurístico de complejidad para JavaScript."""

    # Patrones que identifican el inicio de un bucle en JS
    _LOOP_PATTERNS: list[re.Pattern[str]] = [
        re.compile(r"\bfor\s*\("),       # for clásico, for...in, for...of
        re.compile(r"\bwhile\s*\("),
        re.compile(r"\bdo\s*\{"),
    ]

    # Patrones para definiciones de funciones en JavaScript
    # Captura el nombre en grupo 1
    _FUNC_PATTERNS: list[re.Pattern[str]] = [
        # function foo(...) {
        re.compile(r"\bfunction\s+(\w+)\s*\([^)]*\)\s*\{"),
        # const foo = (...) => {   o   const foo = function(...) {
        re.compile(r"(?:const|let|var)\s+(\w+)\s*=\s*(?:function\s*)?\([^)]*\)\s*=>\s*\{"),
        re.compile(r"(?:const|let|var)\s+(\w+)\s*=\s*function\s*\([^)]*\)\s*\{"),
    ]

    def analyze(self, source_code: str) -> list[FunctionAnalysis]:
        """Analiza código JavaScript usando regex para estimar métricas por función."""
        clean = self._strip_comments(source_code)
        source_lines = source_code.splitlines()
        line_starts = self._build_line_starts(clean)
        results = []

        for pattern in self._FUNC_PATTERNS:
            for match in pattern.finditer(clean):
                func_name = match.group(1)
                
                func_name_start = match.start(1)
                line_idx = self._line_index_from_pos(line_starts, func_name_start)
                preceding_line = source_lines[line_idx - 1] if line_idx > 0 else ""
                
                original_body = self._extract_body(source_code, match.end() - 1)
                
                if self._is_ignored(original_body, preceding_line):
                    continue
                
                clean_body = self._extract_body(clean, match.end() - 1)
                max_depth = self._max_loop_depth(clean_body)
                is_recursive = self._detect_recursion_in_body(clean_body, func_name)
                
                results.append(FunctionAnalysis(
                    name=func_name,
                    max_depth=max_depth,
                    is_recursive=is_recursive,
                    body=clean_body
                ))

        return results
