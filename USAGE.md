# 📖 Guía de Uso — bigO

Guía completa para utilizar la herramienta de análisis de complejidad algorítmica desde la línea de comandos y su interfaz web interactiva.

---

## Tabla de contenidos

1. [Requisitos previos](#-requisitos-previos)
2. [Instalación](#-instalación)
3. [Uso básico CLI](#-uso-básico-cli)
4. [Interfaz Web y Docker](#-interfaz-web-y-docker)
5. [Lenguajes soportados](#-lenguajes-soportados)
6. [Ejemplos prácticos](#-ejemplos-prácticos)
7. [Interpretación de resultados](#-interpretación-de-resultados)
8. [Reglas de estimación](#-reglas-de-estimación)
9. [Manejo de errores](#-manejo-de-errores)
10. [Añadir soporte para un nuevo lenguaje](#-añadir-soporte-para-un-nuevo-lenguaje)
11. [Limitaciones conocidas](#-limitaciones-conocidas)
12. [Preguntas frecuentes](#-preguntas-frecuentes)

---

## 🔧 Requisitos previos

| Requisito | Versión mínima |
|-----------|---------------|
| Python    | 3.10+         |
| Sistema operativo | Linux, macOS, Windows |

> **Nota:** No se requiere ninguna dependencia externa. El proyecto funciona únicamente con la biblioteca estándar de Python, incluyendo el servidor web y los tests.

Para verificar tu versión de Python:

```bash
python3 --version
```

---

## 📦 Instalación

### Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/bigO.git
cd bigO
```

---

## 🚀 Uso básico CLI

El analizador evalúa el código **función por función**, extrayendo las métricas de anidamiento y recursividad de cada bloque individualmente.

### Sintaxis

```bash
python3 main.py <ruta_al_fichero_fuente>
```

### Ejemplo rápido

```bash
python3 main.py examples/ejemplo.py
```

Salida:

```text
  Analizador de Complejidad Algorítmica
  ─────────────────────────────────────
  Archivo     : examples/ejemplo.py
  Lenguaje    : Python

  [constante_ejemplo]
  Anidamiento : 0 niveles
  Recursivo   : No
  Complejidad : O(1) — sin bucles ni recursividad

  [busqueda_lineal]
  Anidamiento : 1 nivel
  Recursivo   : No
  Complejidad : O(n) — un nivel de bucle
...
```

---

## 🌐 Interfaz Web y Docker

La herramienta cuenta con una moderna y fluida interfaz web sin dependencias, impulsada por un servidor de la biblioteca estándar de Python. 

Existen dos formas principales de arrancar el servidor web: usando Python directamente o mediante Docker.

### Método 1: Arrancar con Python local

```bash
python3 server.py
```

Opcionalmente, puedes especificar un puerto:

```bash
python3 server.py --port 8080
```

### Método 2: Despliegue con Docker Compose (Recomendado)

La aplicación incluye los archivos `Dockerfile` y `docker-compose.yml` para un despliegue aislado, seguro y sin ensuciar tu entorno local.

```bash
# Arranca la aplicación en segundo plano
docker compose up -d

# Para detener la aplicación
docker compose down
```

### Acceder a la interfaz

Tras iniciar el servidor por cualquiera de los métodos, abre tu navegador en:
👉 `http://localhost:8080`

La interfaz soporta arrastrar y soltar (Drag & Drop), selección de lenguaje y presenta los resultados de cada función en tarjetas dinámicas.

---

## 🌐 Lenguajes soportados

| Lenguaje   | Extensiones | Método de análisis |
|------------|-------------|--------------------|
| Python     | `.py`       | AST real (módulo `ast`) — el más preciso |
| C          | `.c`, `.h`  | Regex + heurísticas aisladas por bloque |
| Java       | `.java`     | Regex + heurísticas aisladas por bloque |
| JavaScript | `.js`       | Regex + heurísticas aisladas por bloque |

### ¿Qué método usa cada uno?

- **Python:** Construye el Árbol de Sintaxis Abstracta (AST) real del fichero. Analiza las métricas de bucles y llamadas a funciones visitando nodos `FunctionDef` individualmente, por lo que es inmune a falsos positivos.
- **C, Java, JavaScript:** Usan expresiones regulares refinadas con lookaheads negativos para extraer bloques de funciones o métodos, ignorando estructuras de control (como `if` o `while` confundidos como funciones). Posteriormente analizan los bucles dentro del bloque aislado.

---

## 💡 Ejemplos prácticos

### Analizar un fichero Python

```bash
python3 main.py examples/ejemplo.py
```

```text
  Analizador de Complejidad Algorítmica
  ─────────────────────────────────────
  Archivo     : examples/ejemplo.py
  Lenguaje    : Python

  [factorial_recursivo]
  Anidamiento : 0 niveles
  Recursivo   : Sí
  Complejidad : O(n) — recursividad sin bucles (estimación lineal)
```

### Analizar cualquier fichero de tu proyecto

```bash
# Analizar un fichero de tu propio proyecto
python3 main.py /ruta/a/tu/script.c

# Analizar un script JavaScript de un proyecto Node
python3 main.py mi_app/utils.js
```

---

## 📊 Interpretación de resultados

La salida del analizador para cada función muestra cinco campos:

| Campo        | Significado |
|--------------|-------------|
| **[nombre]**    | Nombre de la función o método analizado. |
| **Anidamiento** | Profundidad máxima de bucles anidados encontrados dentro del cuerpo de la función. |
| **Recursivo**   | `Sí` si la función contiene llamadas a sí misma dentro de su bloque. |
| **Complejidad** | Estimación Big-O algorítmica para esa función. |

### Ejemplos de interpretación

| Anidamiento | Recursivo | Complejidad | Significado |
|:-----------:|:---------:|:-----------:|-------------|
| 0 niveles   | No        | O(1)        | Código constante, sin bucles ni recursión |
| 1 nivel     | No        | O(n)        | Un solo bucle recorriendo la entrada |
| 2 niveles   | No        | O(n²)       | Bucle dentro de bucle (ej: bubble sort) |
| 3 niveles   | No        | O(n³)       | Triple anidamiento (ej: multiplicación de matrices) |
| 0 niveles   | Sí        | O(n)        | Recursión sin bucles (ej: factorial) |
| 2 niveles   | Sí        | O(n log n) o peor | Recursión + bucles anidados |

---

## 📐 Reglas de estimación

La herramienta aplica estas reglas **en orden de prioridad** para cada función (la primera que coincida gana):

```
┌─────┬──────────────────────────────────┬───────────────────────────┐
│  #  │ Condición                        │ Complejidad estimada      │
├─────┼──────────────────────────────────┼───────────────────────────┤
│  1  │ Recursividad + bucles            │ O(n log n) o peor         │
│  2  │ Solo recursividad (sin bucles)   │ O(n)                      │
│  3  │ 0 niveles de bucle               │ O(1)                      │
│  4  │ 1 nivel de bucle                 │ O(n)                      │
│  5  │ 2 niveles de bucle anidados      │ O(n²)                     │
│  6  │ 3 niveles de bucle anidados      │ O(n³)                     │
│  7  │ N niveles de bucle anidados      │ O(nᴺ)                     │
└─────┴──────────────────────────────────┴───────────────────────────┘
```

> **Importante:** Estas son estimaciones **estáticas heurísticas** basadas en la estructura de bloque del código. La complejidad real puede variar dependiendo de las condiciones de los bucles.

---

## ⚠️ Manejo de errores

### Sin argumentos

```bash
python3 main.py
```

```
Uso: python main.py <fichero_fuente>
Extensiones soportadas: .py, .c, .h, .java, .js
```

### Fichero inexistente

```bash
python3 main.py noexiste.txt
```

```
Error: no se encontró el fichero 'noexiste.txt'
```

---

## 🔌 Añadir soporte para un nuevo lenguaje

El proyecto usa el **patrón Estrategia**, lo que permite añadir lenguajes sin modificar el motor central.

### Paso 1: Crear el analizador

Crea un fichero `analyzer/nuevo_analyzer.py`:

```python
import re
from analyzer.base_analyzer import BaseAnalyzer, FunctionAnalysis

class NuevoAnalyzer(BaseAnalyzer):
    """Analizador para el lenguaje Nuevo."""

    def analyze(self, source_code: str) -> list[FunctionAnalysis]:
        """Implementa la lógica de análisis específica para extraer funciones.

        Debe devolver una lista de objetos FunctionAnalysis.
        """
        results = []
        # Implementar la extracción y parseo por función aquí
        results.append(FunctionAnalysis(
            name="mi_funcion",
            max_depth=1,
            is_recursive=False
        ))
        return results
```

### Paso 2: Registrar la extensión

Añade la extensión en `analyzer/__init__.py`:

```python
from analyzer.nuevo_analyzer import NuevoAnalyzer

# Dentro del diccionario _REGISTRY:
_REGISTRY[".ext"] = (NuevoAnalyzer, "NuevoLenguaje")
```

¡Y la arquitectura se encargará automáticamente de mapearlo tanto en CLI como en Web!

---

## 🔒 Limitaciones conocidas

### Generales

- **Análisis estático:** La herramienta examina la estructura del código, no su ejecución. No puede determinar si un bucle itera `n` veces o un número fijo o fraccional (`O(log n)`).
- **Recursividad mutua:** No detecta recursividad indirecta (función A llama a B, que llama a A).

### Específicas de C/Java/JavaScript (análisis por regex)

- **Bucles sin llaves:** En estos momentos se buscan llaves `{ }` balanceadas o palabras clave. Los bucles for muy compactos sin corchetes no son analizados tan estrictamente como el AST de Python.
- **Macros en C:** Las macros del preprocesador que ocultan bucles no se detectan.

### Específicas de Python (análisis AST)

- **List comprehensions:** Las comprensiones de lista con bucles implícitos se soportan limitadamente según la estrategia de nodos.
- **`map`/`filter`:** Las funciones de orden superior nativas no se detectan como una iteración en sí mismas.

---

## ❓ Preguntas frecuentes

### ¿Puedo analizar ficheros en subdirectorios?

Sí, basta con indicar la ruta relativa o absoluta en CLI o arrastrar el archivo a la web.

```bash
python3 main.py src/utils/helpers.py
```

### ¿Qué pasa si mi fichero tiene errores de sintaxis?

- **Python:** El módulo `ast` lanzará un error de parsing y lo abortará con advertencia.
- **C/Java/JS:** Al usar regex, el análisis es más tolerante y simplemente procesará el archivo en busca de patrones conocidos a pesar de los errores léxicos.

### ¿Hay tests unitarios?

**¡Sí!** Contamos con un robusto banco de 28 pruebas que cubren 7 escenarios de complejidad (`O(1)` a recursiones mixtas) en los 4 lenguajes, testeando a nivel de bloque de función.

Puedes ejecutarlos así:

```bash
PYTHONPATH=. python3 -m unittest tests/test_analyzers.py -v
```

---

## 📎 Referencia rápida

```bash
# Uso CLI
python3 main.py <fichero>

# Iniciar Interfaz Web
python3 server.py

# Ejecutar Batería de Pruebas
PYTHONPATH=. python3 -m unittest tests/test_analyzers.py -v
```
