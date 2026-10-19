#!/usr/bin/env python3
"""Proxy local para OpenCode Go (el «Worker» de andar por casa).

Por qué hace falta: opencode.ai no manda la cabecera Access-Control-Allow-Origin,
así que la app (una página estática en GitHub Pages) no puede llamarlo desde el
navegador: el navegador corta la petición antes de enviarla. Este programa escucha
en tu propio PC, reenvía la petición a OpenCode y añade las cabeceras CORS que
faltan. Tu clave se queda aquí, no en el navegador.

Uso (PowerShell):

    $env:OC_KEY = "oc_sk_..."
    python tools/go-proxy.py

Y en la app: Proveedor «DeepSeek / OpenAI / OpenRouter»,
Endpoint Base = http://127.0.0.1:8787
Modelo = deepseek-v4.1-flash
API Key = «local» (cualquier texto: la clave real está en OC_KEY)

Mientras el proceso esté abierto, la app funciona. Al cerrarlo, deja de funcionar.
"""
import json
import os
import sys
import urllib.error
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

DESTINO = os.environ.get(
    "TARGET_URL", "https://opencode.ai/inference/go/openai/v1/chat/completions")
CLAVE = os.environ.get("OC_KEY", "")
PUERTO = int(os.environ.get("PORT", "8787"))
CORS = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Headers": "authorization, content-type, x-opencode-session",
    "Access-Control-Allow-Methods": "POST, OPTIONS",
    "Access-Control-Max-Age": "86400",
}


class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def _cors(self):
        for clave, valor in CORS.items():
            self.send_header(clave, valor)

    def _responder(self, estado, datos, tipo="application/json"):
        self.send_response(estado)
        self._cors()
        self.send_header("Content-Type", tipo)
        self.send_header("Content-Length", str(len(datos)))
        self.end_headers()
        self.wfile.write(datos)

    def _json(self, estado, obj):
        self._responder(estado, json.dumps(obj).encode("utf-8"))

    def do_OPTIONS(self):
        self._responder(204, b"")

    def do_POST(self):
        if not CLAVE:
            self._json(500, {"error": {"message": "Falta OC_KEY en el entorno"}})
            return
        largo = int(self.headers.get("Content-Length") or 0)
        cuerpo = self.rfile.read(largo) if largo else b""
        peticion = urllib.request.Request(
            DESTINO, data=cuerpo, method="POST",
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer " + CLAVE,
                # OpenCode Go pide identificar al cliente y una sesión estable.
                "User-Agent": "b2-quiz-proxy-local/1.0",
                "x-opencode-session": self.headers.get("x-opencode-session") or "b2-local",
            })
        try:
            with urllib.request.urlopen(peticion, timeout=900) as resp:
                datos = resp.read()
                estado = resp.status
                tipo = resp.headers.get("content-type", "application/json")
        except urllib.error.HTTPError as exc:
            datos = exc.read()
            estado = exc.code
            tipo = exc.headers.get("content-type", "application/json")
        except Exception as exc:  # red, timeout, DNS…
            self._json(502, {"error": {"message": f"{type(exc).__name__}: {exc}"}})
            return
        self._responder(estado, datos, tipo)

    def log_message(self, fmt, *args):
        sys.stderr.write("proxy: " + (fmt % args) + "\n")


if __name__ == "__main__":
    if not CLAVE:
        print("Falta OC_KEY:   $env:OC_KEY = \"oc_sk_...\"", file=sys.stderr)
        sys.exit(1)
    print(f"proxy en http://127.0.0.1:{PUERTO}  ->  {DESTINO}", file=sys.stderr)
    ThreadingHTTPServer(("127.0.0.1", PUERTO), Handler).serve_forever()
