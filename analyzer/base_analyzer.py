# ─────────────────────────────────────────────────────────────
# analyzer/base_analyzer.py
# Clase base abstracta para todos los analizadores de
# complejidad algorítmica (patrón Estrategia).
#
# Define la interfaz común y la lógica de estimación
# compartida: cualquier analizador concreto solo necesita
# implementar `analyze()` para extraer métricas del código.
# ─────────────────────────────────────────────────────────────

import re
from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class FunctionAnalysis:
    """Métricas brutas extraídas de una función individual."""
    name: str
    max_depth: int
    is_recursive: bool
    body: str = ""


@dataclass
class AnalysisResult:
    """Resultado del análisis de complejidad. Puede representar
    una única función o el resumen global de un fichero.
    """
    max_depth: int
    is_recursive: bool
    complexity: str
    explanation: str
    function_name: str = "Global"
    warning: str = ""


# Mapa de exponente → superíndice Unicode para formatear la complejidad
_SUPERSCRIPTS: dict[int, str] = {
    0: "⁰", 1: "¹", 2: "²", 3: "³", 4: "⁴",
    5: "⁵", 6: "⁶", 7: "⁷", 8: "⁸", 9: "⁹",
}


def _superscript(n: int) -> str:
    """Convierte un entero positivo a su representación en superíndice Unicode."""
    return "".join(_SUPERSCRIPTS[int(d)] for d in str(n))


class BaseAnalyzer(ABC):
    """Interfaz común de los analizadores (patrón Estrategia)."""

    @abstractmethod
    def analyze(self, source_code: str) -> list[FunctionAnalysis]:
        """Analiza el código fuente y devuelve las métricas por función.

        Args:
            source_code: Contenido íntegro del fichero a analizar.

        Returns:
            Lista de FunctionAnalysis, uno por cada función detectada.
        """
        ...

    def estimate_complexity(self, source_code: str) -> list[AnalysisResult]:
        """Ejecuta el análisis y aplica las reglas de estimación
        a cada función detectada en el código fuente.
        """
        functions_metrics = self.analyze(source_code)

        if not functions_metrics:
            functions_metrics.append(FunctionAnalysis(name="Global", max_depth=0, is_recursive=False))

        results = []

        for func in functions_metrics:
            result = self._estimate_single(func.max_depth, func.is_recursive)
            result.function_name = func.name
            if func.body and self._has_braceless_loops(func.body):
                result.warning = "Posible bucle sin llaves — la profundidad puede estar subestimada."
            results.append(result)

        return results

    def _estimate_single(self, max_depth: int, is_recursive: bool) -> AnalysisResult:
        """Reglas de estimación (por orden de prioridad)."""
        if is_recursive and max_depth > 0:
            sup = _superscript(max_depth)
            complexity = f"O(n{sup})" if max_depth > 1 else "O(n)"
            explanation = (
                f"{max_depth} nivel{'es' if max_depth > 1 else ''} de bucle anidado "
                f"con recursividad — la complejidad real puede ser mayor dependiendo "
                f"del tipo de recursión"
            )
        elif is_recursive:
            complexity = "O(n)"
            explanation = "recursividad sin bucles (estimación lineal)"
        elif max_depth == 0:
            complexity = "O(1)"
            explanation = "sin bucles ni recursividad"
        elif max_depth == 1:
            complexity = "O(n)"
            explanation = "un nivel de bucle"
        else:
            sup = _superscript(max_depth)
            complexity = f"O(n{sup})"
            explanation = f"{max_depth} niveles de bucle anidados"

        return AnalysisResult(
            max_depth=max_depth,
            is_recursive=is_recursive,
            complexity=complexity,
            explanation=explanation,
        )

    # ── Métodos compartidos para analizadores basados en texto ──

    @staticmethod
    def _strip_comments(source: str) -> str:
        """Elimina comentarios de bloque (/* ... */) y de línea (// ...).
        Preserva la longitud exacta y las líneas para no romper los índices.
        """
        def repl_block(m: re.Match[str]) -> str:
            return "".join("\n" if c == "\n" else " " for c in m.group(0))
        def repl_line(m: re.Match[str]) -> str:
            return " " * len(m.group(0))
            
        source = re.sub(r"/\*.*?\*/", repl_block, source, flags=re.DOTALL)
        source = re.sub(r"//.*", repl_line, source)
        return source

    def _max_loop_depth(self, source: str) -> int:
        """Estima la profundidad máxima de bucles anidados en un bloque."""
        max_depth = 0
        current_depth = 0
        brace_is_loop: list[bool] = []
        loop_patterns = getattr(self, "_LOOP_PATTERNS", [])

        for line in source.splitlines():
            stripped = line.strip()
            is_loop_line = any(p.search(stripped) for p in loop_patterns)
            opens = stripped.count("{")
            closes = stripped.count("}")

            for _ in range(opens):
                if is_loop_line:
                    current_depth += 1
                    brace_is_loop.append(True)
                    is_loop_line = False
                else:
                    brace_is_loop.append(False)
                max_depth = max(max_depth, current_depth)

            for _ in range(closes):
                if brace_is_loop and brace_is_loop.pop():
                    current_depth -= 1

        return max_depth

    def _detect_recursion_in_body(self, body: str, func_name: str) -> bool:
        """Comprueba si el cuerpo contiene una llamada a su propio nombre."""
        call_pattern = re.compile(rf"(?:\bthis\s*\.\s*)?\b{re.escape(func_name)}\s*\(")
        return bool(call_pattern.search(body))

    @staticmethod
    def _extract_body(source: str, brace_pos: int) -> str:
        """Extrae el texto entre llaves balanceadas a partir de `brace_pos`."""
        depth = 0
        start = brace_pos
        for i in range(brace_pos, len(source)):
            if source[i] == "{":
                depth += 1
            elif source[i] == "}":
                depth -= 1
                if depth == 0:
                    return source[start + 1 : i]
        return source[start:]

    @staticmethod
    def _has_braceless_loops(source: str) -> bool:
        """Heurística para detectar bucles sin llaves."""
        lines = source.splitlines()
        for i, line in enumerate(lines):
            stripped = line.strip()
            if re.search(r"\b(for|while|do)\b", stripped):
                if not stripped.endswith("{"):
                    # Comprobar la siguiente línea no vacía
                    for j in range(i + 1, len(lines)):
                        next_stripped = lines[j].strip()
                        if next_stripped:
                            if not next_stripped.startswith("{"):
                                return True
                            break
        return False

    @staticmethod
    def _is_ignored(body: str, preceding_line: str) -> bool:
        """Devuelve True si alguna de las dos líneas contiene el comentario de ignore."""
        pattern = re.compile(r"(#|//)\s*bigo:\s*ignore", re.IGNORECASE)
        if pattern.search(preceding_line):
            return True
        
        for line in body.splitlines():
            stripped = line.strip()
            if stripped:
                if pattern.search(stripped):
                    return True
                break
        return False
