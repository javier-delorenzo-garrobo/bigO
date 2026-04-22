# 🚀 bigO

Herramienta de línea de comandos y web que analiza código fuente y estima su **complejidad algorítmica en notación Big-O**.

Soporta **Python**, **C**, **Java** y **JavaScript**, detectando automáticamente el lenguaje por la extensión del fichero.

---

## ✨ Características

- **Detección automática del lenguaje** por extensión del fichero (`.py`, `.c`, `.h`, `.java`, `.js`)
- **Análisis AST real** para Python mediante el módulo estándar `ast`
- **Análisis heurístico** con regex para C, Java y JavaScript
- **Detección de recursividad** (funciones que se llaman a sí mismas)
- **Estimación de complejidad** basada en profundidad de bucles anidados
- **Sin dependencias externas**: funciona solo con la biblioteca estándar de Python 3.10+
- **Arquitectura extensible** con patrón Estrategia: añadir un nuevo lenguaje no requiere modificar los existentes

---

## 📦 Instalación

```bash
# Clonar el repositorio
git clone https://github.com/tu-usuario/bigO.git
cd bigO

# (Opcional) Crear la estructura de carpetas desde cero
bash setup.sh

# No hay dependencias externas que instalar
```

> **Requisito:** Python 3.10 o superior.

---

## 🚀 Uso

### CLI

```bash
python main.py <fichero_fuente>
```

### Ejemplos

```bash
# Analizar un fichero Python
python main.py examples/ejemplo.py

# Analizar un fichero C
python main.py examples/ejemplo.c

# Analizar un fichero Java
python main.py examples/ejemplo.java

# Analizar un fichero JavaScript
python main.py examples/ejemplo.js
```

### Salida de ejemplo

Al ejecutar `python main.py examples/ejemplo.py`:

```
  Analizador de Complejidad Algorítmica
  ──────────────────────────────────────
  Archivo     : examples/ejemplo.py
  Lenguaje    : Python
  Anidamiento : 2 niveles
  Recursivo   : Sí
  Complejidad : O(n log n) o peor (n² × recursión) — recursividad detectada junto con 2 niveles de bucle anidado
```

### Web (Docker Compose)

Puedes arrancar la interfaz web utilizando Docker de forma rápida y limpia:

```bash
docker compose up -d
```

Luego abre `http://localhost:8080` en tu navegador. Para más detalles, consulta el fichero [USAGE.md](USAGE.md).

---

## 📐 Reglas de estimación

La complejidad se estima según estas reglas, en orden de prioridad:

| Condición                     | Complejidad estimada      |
|-------------------------------|---------------------------|
| Recursividad + bucles         | O(n log n) o peor         |
| Solo recursividad             | O(n)                      |
| 0 niveles de bucle            | O(1)                      |
| 1 nivel de bucle              | O(n)                      |
| 2 niveles de bucle anidados   | O(n²)                     |
| 3 niveles de bucle anidados   | O(n³)                     |
| N niveles de bucle anidados   | O(nᴺ)                     |

> **Nota:** estas son estimaciones heurísticas. La herramienta analiza la estructura estática del código, no su comportamiento en tiempo de ejecución.

---

## 🏗️ Arquitectura

El proyecto sigue el **patrón Estrategia** (Strategy Pattern), donde cada analizador de lenguaje implementa la misma interfaz pero con su propia lógica de parsing:

```
bigO/
├── main.py                  # Punto de entrada CLI
├── requirements.txt         # Dependencias (ninguna)
├── README.md                # Este fichero
├── setup.sh                 # Script de creación de estructura
├── analyzer/
│   ├── __init__.py          # Factoría de analizadores (registro de extensiones)
│   ├── base_analyzer.py     # Clase abstracta + lógica de estimación compartida
│   ├── python_analyzer.py   # Análisis AST con módulo `ast`
│   ├── c_analyzer.py        # Análisis heurístico con regex
│   ├── java_analyzer.py     # Análisis heurístico con regex
│   └── js_analyzer.py       # Análisis heurístico con regex
└── examples/
    ├── ejemplo.py            # Ejemplo Python (O(1), O(n), O(n²), recursivo)
    ├── ejemplo.c             # Ejemplo C
    ├── ejemplo.java          # Ejemplo Java
    └── ejemplo.js            # Ejemplo JavaScript
```

### Diagrama de clases

```
          ┌──────────────────────┐
          │   BaseAnalyzer (ABC) │
          ├──────────────────────┤
          │ + analyze()          │  ← abstracto: cada lenguaje lo implementa
          │ + estimate_complexity│  ← compartido: reglas de estimación
          └──────────┬───────────┘
                     │
       ┌─────────────┼──────────────┬──────────────┐
       │             │              │              │
┌──────┴──────┐ ┌────┴─────┐ ┌─────┴─────┐ ┌─────┴──────┐
│   Python    │ │    C     │ │   Java    │ │ JavaScript │
│  Analyzer   │ │ Analyzer │ │ Analyzer  │ │  Analyzer  │
├─────────────┤ ├──────────┤ ├───────────┤ ├────────────┤
│ usa ast     │ │ usa regex│ │ usa regex │ │ usa regex  │
└─────────────┘ └──────────┘ └───────────┘ └────────────┘
```

### Principios de diseño

- **Abierto a extensión, cerrado a modificación (OCP):** para añadir un nuevo lenguaje, se crea un nuevo fichero en `analyzer/` que herede de `BaseAnalyzer` y se registra en `__init__.py`. No se tocan los demás analizadores.
- **Responsabilidad única (SRP):** cada analizador solo conoce la sintaxis de su lenguaje. La lógica de estimación vive en la clase base.
- **Inversión de dependencias (DIP):** `main.py` depende de la abstracción (`BaseAnalyzer`), no de las implementaciones concretas.

---

## 🔧 Cómo añadir un nuevo lenguaje

1. Crea `analyzer/nuevo_analyzer.py` heredando de `BaseAnalyzer`
2. Implementa el método `analyze(source_code) → (max_depth, is_recursive)`
3. Registra la extensión en `analyzer/__init__.py`:

```python
from analyzer.nuevo_analyzer import NuevoAnalyzer

_REGISTRY[".ext"] = (NuevoAnalyzer, "NuevoLenguaje")
```

¡Listo! No hace falta tocar nada más.

---

## 📄 Licencia

MIT License. Libre para uso personal y académico.

## Limitaciones conocidas

1. Bucles sin llaves → profundidad subestimada (se emite aviso).
2. Recursión mutua → no se detecta.
3. Arrow functions JS de una línea sin bloque (x => x*2) → no se analizan.
4. Constructores Java → pueden generar falsos positivos en la detección de métodos.
