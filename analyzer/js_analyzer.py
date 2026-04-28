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

from analyzer.base_analyzer import BaseAnalyzer


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

    def analyze(self, source_code: str):
        """Analiza código JavaScript usando regex para estimar métricas por función."""
        return self._analyze_with_patterns(source_code, self._FUNC_PATTERNS)
