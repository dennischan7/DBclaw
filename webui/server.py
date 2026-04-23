"""DBA SafeGuard WebUI — HTTP Server Entry Point.

基于 Python http.server，零依赖（除标准库外）。
启动方式:
    python server.py [--port 8787] [--host 0.0.0.0]

架构:
    server.py  →  dba_routes.py  →  dba_bridge.py  →  DBA Plugin modules
       ↓
    static/  +  templates/index.html
"""

from __future__ import annotations

import argparse
import json
import logging
import mimetypes
import os
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
from pathlib import Path
from urllib.parse import urlparse, parse_qs


class ThreadingHTTPServer(ThreadingMixIn, HTTPServer):
    """HTTP server that handles each request in a new thread.

    Critical for SSE — the long-lived /api/dba/events connection
    must not block other API requests.
    """
    daemon_threads = True

# ---------------------------------------------------------------------------
# Path Setup — ensure DBA plugin is importable
# ---------------------------------------------------------------------------

WEBUI_DIR = Path(__file__).parent.resolve()
PROJECT_ROOT = WEBUI_DIR.parent
PLUGIN_DIR = PROJECT_ROOT / ".hermes" / "plugins" / "dba-safeguard"

# Add plugin dir to sys.path so we can import plugin modules:
#   from engine.dba_loop import PipelineStage
# NOTE: Do NOT add PROJECT_ROOT — it has a tools/ package that shadows
# the plugin's tools/ (audit_logger, db_connector, etc.)
if str(PLUGIN_DIR) not in sys.path:
    sys.path.insert(0, str(PLUGIN_DIR))
if str(WEBUI_DIR) not in sys.path:
    sys.path.insert(0, str(WEBUI_DIR))

STATIC_DIR = WEBUI_DIR / "static"
TEMPLATES_DIR = WEBUI_DIR / "templates"

logger = logging.getLogger("dba_webui.server")

# ---------------------------------------------------------------------------
# Import routes (deferred to avoid circular imports at module level)
# ---------------------------------------------------------------------------


def _get_router():
    """Lazy import of dba_routes to allow plugin modules to initialize."""
    from dba_routes import handle_dba_request
    return handle_dba_request


# ---------------------------------------------------------------------------
# Request Handler
# ---------------------------------------------------------------------------

class DBARequestHandler(BaseHTTPRequestHandler):
    """HTTP request handler for DBA SafeGuard WebUI."""

    server_version = "DBA-SafeGuard-WebUI/1.0"

    def log_message(self, format, *args):
        """Override to use cleaner logging format."""
        sys.stderr.write(
            f"[WebUI] {self.address_string()} - {format % args}\n"
        )

    # --- Static file serving ---

    def _serve_static(self, path: str) -> bool:
        """Serve static files from static/ directory. Returns True if handled."""
        if not path.startswith("/static/"):
            return False

        rel = path[len("/static/"):]
        # Security: prevent directory traversal
        file_path = (STATIC_DIR / rel).resolve()
        if not str(file_path).startswith(str(STATIC_DIR)):
            self.send_error(403, "Forbidden")
            return True

        if not file_path.is_file():
            self.send_error(404, "Not Found")
            return True

        content_type, _ = mimetypes.guess_type(str(file_path))
        if content_type is None:
            content_type = "application/octet-stream"

        # JavaScript modules need correct MIME type
        if file_path.suffix == ".js":
            content_type = "application/javascript"

        data = file_path.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()
        self.wfile.write(data)
        return True

    def _serve_index(self) -> None:
        """Serve the main index.html page."""
        index_path = TEMPLATES_DIR / "index.html"
        if not index_path.is_file():
            self.send_error(500, "index.html not found")
            return

        data = index_path.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    # --- JSON helpers ---

    def send_json(self, data: dict, status: int = 200) -> None:
        """Send a JSON response."""
        from auth_middleware import flush_pending_headers
        body = json.dumps(data, ensure_ascii=False, default=str).encode("utf-8")
        self.send_response(status)
        flush_pending_headers(self)  # Set-Cookie, CSRF etc.
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def read_json_body(self) -> dict:
        """Read and parse JSON request body."""
        content_length = int(self.headers.get("Content-Length", 0))
        if content_length == 0:
            return {}
        raw = self.rfile.read(content_length)
        try:
            return json.loads(raw)
        except (json.JSONDecodeError, UnicodeDecodeError):
            return {}

    def send_csv(self, csv_data: str, filename: str) -> None:
        """Send CSV file as download."""
        body = csv_data.encode("utf-8-sig")  # BOM for Excel compatibility
        self.send_response(200)
        self.send_header("Content-Type", "text/csv; charset=utf-8")
        self.send_header("Content-Disposition", f'attachment; filename="{filename}"')
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def send_sse_headers(self) -> None:
        """Send SSE response headers (keep connection open)."""
        from auth_middleware import flush_pending_headers
        self.send_response(200)
        flush_pending_headers(self)
        self.send_header("Content-Type", "text/event-stream")
        self.send_header("Cache-Control", "no-cache")
        self.send_header("Connection", "keep-alive")
        self.send_header("X-Accel-Buffering", "no")
        self.end_headers()

    def send_sse_event(self, event: str, data: dict) -> None:
        """Send a single SSE event."""
        payload = json.dumps(data, ensure_ascii=False, default=str)
        msg = f"event: {event}\ndata: {payload}\n\n"
        self.wfile.write(msg.encode("utf-8"))
        self.wfile.flush()

    # --- HTTP method handlers ---

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path

        # Static files
        if self._serve_static(path):
            return

        # API routes
        if path.startswith("/api/dba/"):
            try:
                router = _get_router()
                router(self, "GET", path, {}, parse_qs(parsed.query))
            except Exception as e:
                logger.error("Unhandled API GET error on %s: %s", path, e, exc_info=True)
                self.send_json({"error": f"Internal server error: {str(e)}"}, status=500)
            return

        # Default: serve index.html (SPA-style)
        self._serve_index()

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path.startswith("/api/dba/"):
            try:
                body = self.read_json_body()
                router = _get_router()
                router(self, "POST", path, body, parse_qs(parsed.query))
            except Exception as e:
                logger.error("Unhandled API POST error on %s: %s", path, e, exc_info=True)
                self.send_json({"error": f"Internal server error: {str(e)}"}, status=500)
            return

        self.send_error(404, "Not Found")

    def do_PUT(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path.startswith("/api/dba/"):
            try:
                body = self.read_json_body()
                router = _get_router()
                router(self, "PUT", path, body, parse_qs(parsed.query))
            except Exception as e:
                logger.error("Unhandled API PUT error on %s: %s", path, e, exc_info=True)
                self.send_json({"error": f"Internal server error: {str(e)}"}, status=500)
            return

        self.send_error(404, "Not Found")

    def do_DELETE(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path.startswith("/api/dba/"):
            try:
                body = self.read_json_body()
                router = _get_router()
                router(self, "DELETE", path, body, parse_qs(parsed.query))
            except Exception as e:
                logger.error("Unhandled API DELETE error on %s: %s", path, e, exc_info=True)
                self.send_json({"error": f"Internal server error: {str(e)}"}, status=500)
            return

        self.send_error(404, "Not Found")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="DBA SafeGuard WebUI Server")
    parser.add_argument("--host", default="127.0.0.1", help="Bind host (default: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=8787, help="Bind port (default: 8787)")
    args = parser.parse_args()

    server = ThreadingHTTPServer((args.host, args.port), DBARequestHandler)
    print(f"\n  DBA SafeGuard WebUI")
    print(f"  http://{args.host}:{args.port}")
    print(f"  Plugin: {PLUGIN_DIR}")
    print(f"  Press Ctrl+C to stop\n")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down...")
        server.shutdown()


if __name__ == "__main__":
    main()
