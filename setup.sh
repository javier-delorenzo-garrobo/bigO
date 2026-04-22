#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────
# setup.sh — Script de configuración automática del proyecto
# Crea toda la estructura de directorios y ficheros necesarios.
# Uso: bash setup.sh
# ─────────────────────────────────────────────────────────────

set -euo pipefail

# Directorio raíz del proyecto (donde vive este script)
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "🔧 Creando estructura del proyecto en: $PROJECT_DIR"

# Crear directorios
mkdir -p "$PROJECT_DIR/analyzer"
mkdir -p "$PROJECT_DIR/examples"

# Crear ficheros vacíos si no existen (no sobreescribe los existentes)
touch "$PROJECT_DIR/main.py"
touch "$PROJECT_DIR/requirements.txt"
touch "$PROJECT_DIR/README.md"
touch "$PROJECT_DIR/analyzer/__init__.py"
touch "$PROJECT_DIR/analyzer/base_analyzer.py"
touch "$PROJECT_DIR/analyzer/python_analyzer.py"
touch "$PROJECT_DIR/analyzer/c_analyzer.py"
touch "$PROJECT_DIR/analyzer/java_analyzer.py"
touch "$PROJECT_DIR/analyzer/js_analyzer.py"
touch "$PROJECT_DIR/examples/ejemplo.py"
touch "$PROJECT_DIR/examples/ejemplo.c"
touch "$PROJECT_DIR/examples/ejemplo.java"
touch "$PROJECT_DIR/examples/ejemplo.js"

echo ""
echo "✅ Estructura creada correctamente:"
echo ""
# Mostrar el árbol del proyecto (usa 'find' por si 'tree' no está instalado)
if command -v tree &> /dev/null; then
    tree "$PROJECT_DIR" --charset utf-8
else
    find "$PROJECT_DIR" -not -path '*/__pycache__/*' -not -name '__pycache__' \
        | sed "s|$PROJECT_DIR/||" | sort
fi

echo ""
echo "🚀 Ahora ejecuta: python main.py examples/ejemplo.py"
