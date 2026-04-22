#!/usr/bin/env python3
# ─────────────────────────────────────────────────────────────
# server.py — Servidor HTTP para la interfaz web.
#
# Sirve los ficheros estáticos de web/ y expone un endpoint
# POST /api/analyze que recibe código fuente + extensión y
# devuelve el resultado del análisis en JSON.
#
# Usa únicamente la biblioteca estándar de Python (sin Flask,
# sin dependencias externas).
#
# Uso: python3 server.py [--port 8080]
# ─────────────────────────────────────────────────────────────

import argparse
import json
import sys
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path

# Importamos la factoría de analizadores del proyecto existente
from analyzer import get_analyzer, supported_extensions


class AnalyzerHandler(SimpleHTTPRequestHandler):
    """Handler HTTP que sirve ficheros estáticos y procesa peticiones de análisis.

    - GET /*        → Sirve ficheros estáticos desde la carpeta web/
    - POST /api/analyze → Analiza código fuente y devuelve JSON
    """

    # Directorio desde el que servir ficheros estáticos
    _web_dir: str = str(Path(__file__).parent / "web")

    def translate_path(self, path: str) -> str:
        """Redirige las peticiones de ficheros estáticos a la carpeta web/.

        Sobreescribimos este método para que el servidor sirva
        desde web/ en lugar del directorio de trabajo actual.
        """
        # Si la ruta es /api/*, no la traducimos (se maneja en do_POST)
        if path.startswith("/api/"):
            return path

        # Para la raíz, servir index.html
        if path == "/":
            path = "/index.html"

        # Construir la ruta completa dentro de web/
        return str(Path(self._web_dir) / path.lstrip("/"))

    def do_POST(self) -> None:
        """Maneja peticiones POST al endpoint /api/analyze."""
        if self.path != "/api/analyze":
            self._send_json_error(404, "Endpoint no encontrado")
            return

        try:
            # Leer el cuerpo de la petición
            content_length = int(self.headers.get("Content-Length", 0))
            raw_body = self.rfile.read(content_length)
            body = json.loads(raw_body.decode("utf-8"))

            code = body.get("code", "")
            extension = body.get("language", "")

            # Validaciones
            if not code.strip():
                self._send_json_error(400, "El código fuente está vacío")
                return

            if not extension.startswith("."):
                extension = f".{extension}"

            # Obtener el analizador adecuado
            result = get_analyzer(extension)
            if result is None:
                self._send_json_error(
                    400,
                    f"Extensión '{extension}' no soportada. "
                    f"Usa: {', '.join(supported_extensions())}"
                )
                return

            analyzer, language = result

            # Ejecutar el análisis
            analysis_list = analyzer.estimate_complexity(code)
            
            functions = []
            for analysis in analysis_list:
                functions.append({
                    "name": analysis.function_name,
                    "max_depth": analysis.max_depth,
                    "is_recursive": analysis.is_recursive,
                    "complexity": analysis.complexity,
                    "explanation": analysis.explanation,
                    "warning": analysis.warning,
                })

            # Responder con JSON
            self._send_json(200, {
                "success": True,
                "language": language,
                "functions": functions,
            })

        except json.JSONDecodeError:
            self._send_json_error(400, "JSON inválido en el cuerpo de la petición")
        except SyntaxError as e:
            # Error de sintaxis al parsear código Python con ast
            self._send_json_error(422, f"Error de sintaxis en el código: {e}")
        except Exception as e:
            self._send_json_error(500, f"Error interno: {e}")

    def _send_json(self, status: int, data: dict) -> None:
        """Envía una respuesta JSON con el código de estado indicado."""
        response = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(response)))
        # Permitir peticiones desde cualquier origen (desarrollo local)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(response)

    def _send_json_error(self, status: int, message: str) -> None:
        """Envía una respuesta de error en formato JSON."""
        self._send_json(status, {"success": False, "error": message})

    def do_OPTIONS(self) -> None:
        """Maneja preflight CORS para peticiones desde el navegador."""
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def log_message(self, format: str, *args: object) -> None:
        """Formatea los logs del servidor para que sean más legibles."""
        # Coloreamos el método HTTP para mayor claridad
        sys.stderr.write(f"  [{self.log_date_time_string()}] {format % args}\n")


def main() -> None:
    """Arranca el servidor HTTP."""
    parser = argparse.ArgumentParser(
        description="Servidor web para el analizador de complejidad"
    )
    parser.add_argument(
        "--port", "-p",
        type=int,
        default=8080,
        help="Puerto del servidor (por defecto: 8080)"
    )
    args = parser.parse_args()

    server = HTTPServer(("", args.port), AnalyzerHandler)

    print()
    print("  🌐 Analizador de Complejidad — Interfaz Web")
    print("  ──────────────────────────────────────────────")
    print(f"  Servidor activo en: http://localhost:{args.port}")
    print("  Pulsa Ctrl+C para detener")
    print()

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n  ⏹  Servidor detenido.")
        server.server_close()


if __name__ == "__main__":
    main()
