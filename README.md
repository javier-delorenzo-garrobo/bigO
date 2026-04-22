# 🚀 bigO

Herramienta de línea de comandos y web que analiza código fuente y estima su **complejidad algorítmica en notación Big-O**.

Soporta **Python**, **C**, **Java** y **JavaScript**, detectando automáticamente el lenguaje por la extensión del fichero.

---

## ✨ Características

- **Detección automática del lenguaje** por extensión del fichero (`.py`, `.c`, `.h`, `.java`, `.js`)
- **Análisis AST real** para Python mediante el módulo estándar `ast`
- **Análisis heurístico** con regex para C, Java y JavaScript
- **Directiva de ignorado**: permite excluir funciones individuales del análisis añadiendo el comentario `// bigO: ignore` o `# bigo: ignore` justo antes de su definición.
- **Detección de recursividad** (funciones que se llaman a sí mismas)
- **Estimación de complejidad** basada en profundidad de bucles anidados
- **Sistema de alertas heurísticas**: detecta y advierte sobre constructos que pueden mermar la precisión (como bucles anidados sin llaves `{}`, que pueden subestimar la complejidad).
- **Dashboard Web interactivo**: interfaz premium y responsiva en formato *dashboard* de una sola pantalla para visualizar las métricas rápidamente.
- **Sin dependencias externas**: tanto el CLI como el servidor HTTP y los tests funcionan solo con la biblioteca estándar de Python 3.10+
- **Arquitectura extensible** con patrón Estrategia: añadir un nuevo lenguaje no requiere modificar los existentes.

---

## 📦 Instalación y Uso

### CLI (Línea de Comandos)

```bash
# Clonar el repositorio
git clone https://github.com/tu-usuario/bigO.git
cd bigO

# Analizar un fichero
python main.py examples/ejemplo.py
python main.py examples/ejemplo.c
```

**Salida de ejemplo:**
```text
  Analizador de Complejidad Algorítmica
  ──────────────────────────────────────
  Archivo     : examples/ejemplo.py
  Lenguaje    : Python

  [merge_sort]
  Anidamiento : 1 nivel
  Recursivo   : Sí
  Complejidad : O(n) — 1 nivel de bucle anidado con recursividad — la complejidad real puede ser mayor dependiendo del tipo de recursión
```

### Web Dashboard (Docker)

Puedes arrancar la interfaz web utilizando Docker de forma rápida y limpia. Esta versión incluye un panel interactivo premium.

```bash
docker compose up -d --build
```

Luego abre `http://localhost:8080` en tu navegador. Para más detalles, consulta el fichero [USAGE.md](USAGE.md).

---

## 🛠️ Directiva `ignore`

Si deseas que el analizador ignore una función concreta para que no aparezca en los reportes, añade un comentario con el texto `bigo: ignore` (indistinto a mayúsculas o minúsculas) en la línea inmediatamente superior a la definición de la función:

```python
# bigo: ignore
def mi_funcion_excluida():
    for i in range(100):
        pass
```

```c
// bigO: ignore
void ignored_func() {
    for(int i=0; i<10; i++) {}
}
```

---

## 📐 Reglas de estimación

La complejidad se estima según estas reglas, en orden de prioridad:

| Condición                     | Complejidad estimada      |
|-------------------------------|---------------------------|
| Recursividad + bucles         | `O(n)` (con advertencia)  |
| Solo recursividad             | `O(n)`                    |
| 0 niveles de bucle            | `O(1)`                    |
| 1 nivel de bucle              | `O(n)`                    |
| 2 niveles de bucle anidados   | `O(n²)`                   |
| 3 niveles de bucle anidados   | `O(n³)`                   |
| N niveles de bucle anidados   | `O(nᴺ)`                   |

> **Nota:** estas son estimaciones estáticas y estructurales. La herramienta cuenta anidamientos y detecta auto-llamadas, no simula el comportamiento en tiempo de ejecución.

---

## 🏗️ Arquitectura y Tests

El proyecto sigue el **patrón Estrategia** (Strategy Pattern), donde cada analizador de lenguaje implementa la misma interfaz pero con su propia lógica de parsing. 

Para ejecutar la batería de pruebas (organizadas dinámicamente por lenguaje), ejecuta:
```bash
python3 -m unittest tests/test_analyzers.py
```

### Principios de diseño

- **Abierto a extensión, cerrado a modificación (OCP):** para añadir un nuevo lenguaje, se crea un nuevo fichero en `analyzer/` que herede de `BaseAnalyzer` y se registra en `__init__.py`.
- **Responsabilidad única (SRP):** cada analizador solo conoce la sintaxis de su lenguaje. La lógica de estimación vive en la clase base.
- **Inversión de dependencias (DIP):** `main.py` y `server.py` dependen de abstracciones, no de clases concretas.

---

## ⚠️ Limitaciones conocidas y Análisis Heurístico

Este proyecto utiliza **análisis AST** riguroso para Python, pero depende de **heurísticas basadas en expresiones regulares** para C, Java y JavaScript. Esto implica ciertas limitaciones intrínsecas con las que el usuario debe contar:

1. **Bucles sin llaves (`{}`) en C/Java/JS**: Las sentencias `for`/`while` sin llaves en estos lenguajes provocan que el analizador heurístico subestime la profundidad de anidamiento. La herramienta detectará esta estructura y emitirá una advertencia (`warning`) en la interfaz y consola alertando de la posible subestimación.
2. **Recursión mutua**: Actualmente, solo se detecta recursividad directa (una función que se llama explícitamente a sí misma).
3. **Arrow functions en JS**: Funciones de flecha sin bloque (ej. `x => x * 2`) en una sola línea no son capturadas por el motor de análisis.
4. **Firmas complejas**: Algunos constructores en Java o macros muy complejas en C pueden generar falsos positivos (funciones detectadas que no lo son).

---

## 📄 Licencia

MIT License. Libre para uso personal y académico.
