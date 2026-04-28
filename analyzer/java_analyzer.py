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

from analyzer.base_analyzer import BaseAnalyzer


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

    def analyze(self, source_code: str):
        """Analiza código Java usando regex para estimar métricas por función."""
        return self._analyze_with_patterns(source_code, [self._METHOD_DEF_PATTERN])
