#!/usr/bin/env python3
# ─────────────────────────────────────────────────────────────
# main.py — Punto de entrada CLI del analizador de complejidad.
#
# Recibe un fichero de código fuente como argumento, detecta
# el lenguaje por extensión, delega al analizador adecuado
# y muestra el resultado formateado en la terminal.
# ─────────────────────────────────────────────────────────────

import sys
from pathlib import Path
from typing import TYPE_CHECKING

from analyzer import get_analyzer, supported_extensions

if TYPE_CHECKING:
    from analyzer.base_analyzer import AnalysisResult


def print_result(filepath: str, language: str, results: list["AnalysisResult"]) -> None:
    """Imprime el resultado del análisis con formato alineado y legible.

    Usa caracteres Unicode (─) para la línea decorativa y alinea
    las etiquetas con un ancho fijo para que el output sea limpio
    independientemente de la longitud de los valores.
    """
    title = "Analizador de Complejidad Algorítmica"
    separator = "─" * len(title)

    print()
    print(f"  {title}")
    print(f"  {separator}")
    print(f"  {'Archivo':<12}: {filepath}")
    print(f"  {'Lenguaje':<12}: {language}")
    print()

    for result in results:
        recursive_str = "Sí" if result.is_recursive else "No"
        depth_str = (
            f"{result.max_depth} nivel{'es' if result.max_depth != 1 else ''}"
        )
        print(f"  [{result.function_name}]")
        print(f"  {'Anidamiento':<12}: {depth_str}")
        print(f"  {'Recursivo':<12}: {recursive_str}")
        print(f"  {'Complejidad':<12}: {result.complexity} — {result.explanation}")
        if result.warning:
            print(f"  {'Aviso':<12}: {result.warning}")
        print()


def main() -> int:
    """Función principal: parsea argumentos, ejecuta el análisis y muestra resultados."""

    # --- Validación de argumentos ---
    if len(sys.argv) != 2:
        print(f"Uso: python {sys.argv[0]} <fichero_fuente>")
        print(f"Extensiones soportadas: {', '.join(supported_extensions())}")
        return 1

    filepath = sys.argv[1]
    path = Path(filepath)

    # --- Verificar que el fichero existe ---
    if not path.is_file():
        print(f"Error: no se encontró el fichero '{filepath}'")
        return 1

    # --- Detectar lenguaje por extensión ---
    extension = path.suffix.lower()
    result = get_analyzer(extension)

    if result is None:
        print(f"Error: extensión '{extension}' no soportada.")
        print(f"Extensiones soportadas: {', '.join(supported_extensions())}")
        return 1

    analyzer, language = result

    # --- Leer el fichero y analizar ---
    try:
        source_code = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        # Fallback para ficheros con codificación distinta
        source_code = path.read_text(encoding="latin-1")

    analysis_results = analyzer.estimate_complexity(source_code)

    # --- Mostrar resultado ---
    print_result(filepath, language, analysis_results)

    return 0


if __name__ == "__main__":
    sys.exit(main())
