# ─────────────────────────────────────────────────────────────
# analyzer/__init__.py
# Paquete de analizadores de complejidad algorítmica.
#
# Expone una factoría centralizada para obtener el analizador
# correcto según la extensión del fichero, sin que el código
# cliente tenga que conocer las clases concretas.
# ─────────────────────────────────────────────────────────────

from analyzer.python_analyzer import PythonAnalyzer
from analyzer.c_analyzer import CAnalyzer
from analyzer.java_analyzer import JavaAnalyzer
from analyzer.js_analyzer import JavaScriptAnalyzer
from analyzer.base_analyzer import BaseAnalyzer

# Mapeo extensión → (clase analizadora, nombre legible del lenguaje).
# Para añadir un nuevo lenguaje basta con importar su analizador
# y agregar una entrada aquí; no hay que tocar nada más.
_REGISTRY: dict[str, tuple[type[BaseAnalyzer], str]] = {
    ".py":   (PythonAnalyzer,     "Python"),
    ".c":    (CAnalyzer,          "C"),
    ".h":    (CAnalyzer,          "C (header)"),
    ".java": (JavaAnalyzer,       "Java"),
    ".js":   (JavaScriptAnalyzer, "JavaScript"),
}


def get_analyzer(extension: str) -> tuple[BaseAnalyzer, str] | None:
    """Devuelve una instancia del analizador y el nombre del lenguaje,
    o None si la extensión no está soportada."""
    entry = _REGISTRY.get(extension)
    if entry is None:
        return None
    analyzer_cls, language = entry
    return analyzer_cls(), language


def supported_extensions() -> list[str]:
    """Lista de extensiones soportadas (para mensajes de error)."""
    return list(_REGISTRY.keys())
