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

from analyzer.base_analyzer import BaseAnalyzer


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

    def analyze(self, source_code: str):
        """Analiza código C usando regex para estimar métricas por función."""
        return self._analyze_with_patterns(source_code, [self._FUNC_DEF_PATTERN])
