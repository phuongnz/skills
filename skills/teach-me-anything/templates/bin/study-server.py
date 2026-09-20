#!/usr/bin/env python3
"""Serve the learning workspace, and relay the tutor terminal from a UNIX socket.

Why this exists rather than "just open index.html": the console embeds the tutor
terminal in an iframe, and browsers treat a different port as a different origin.
Serving the pages and the terminal from ONE origin keeps the iframe simple and,
more importantly, lets us close the door behind it:

  * ttyd listens on a UNIX socket, not a TCP port. Nothing in the browser can
    reach it directly and nothing on the network can see it at all.
  * This server is the only thing that can talk to that socket, and it refuses
    any /terminal request carrying someone else's Origin — which is what stops
    another page you have open from quietly opening a shell on this machine.

Everything binds to 127.0.0.1. Stdlib only.
"""

import argparse
import http.server
import os
import socket
import sys
import threading

TERMINAL_PREFIX = "/terminal"
CHUNK = 65536

DOWN_PAGE = """<!doctype html>
<meta charset="utf-8">
<title>tutor terminal not running</title>
<style>
  body { margin: 0; background: #1c1a17; color: #c9c2b6;
         font: 14px/1.7 -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
         padding: 1.5rem 1.6rem; }
  strong { color: #e8e2d8; }
  code { background: #2a251f; color: #e8e2d8; padding: .12em .45em; border-radius: 4px;
         font-family: "SF Mono", Menlo, monospace; font-size: .92em; }
  p { max-width: 42rem; }
</style>
<p><strong>The tutor terminal is not running.</strong></p>
<p>The workspace is still being served, but nothing is listening on the terminal
socket. The launcher restarts it automatically; if this stays up, stop the session
with Ctrl-C and run <code>bin/study</code> again.</p>
<p>Reload this pane once it is back.</p>
"""


def _pump_reader(src, dst):
    """Relay a buffered reader (the client side) into a socket."""
    try:
        while True:
            chunk = src.read1(CHUNK)
            if not chunk:
                break
            dst.sendall(chunk)
    except OSError:
        pass
    finally:
        try:
            dst.shutdown(socket.SHUT_WR)
        except OSError:
            pass


def _pump_socket(src, dst):
    """Relay a socket (the ttyd side) into another socket."""
    try:
        while True:
            chunk = src.recv(CHUNK)
            if not chunk:
                break
            dst.sendall(chunk)
    except OSError:
        pass
    finally:
        try:
            dst.shutdown(socket.SHUT_WR)
        except OSError:
            pass


class StudyHandler(http.server.SimpleHTTPRequestHandler):
    # HTTP/1.1 is required: a WebSocket upgrade cannot happen over HTTP/1.0.
    protocol_version = "HTTP/1.1"
    socket_path = None
    allowed_origins = ()

    # ---- routing ---------------------------------------------------------
    def _is_terminal(self):
        p = self.path
        return p == TERMINAL_PREFIX or p.startswith(TERMINAL_PREFIX + "/") \
            or p.startswith(TERMINAL_PREFIX + "?")

    def do_GET(self):
        if self._is_terminal():
            return self.relay()
        return super().do_GET()

    def do_HEAD(self):
        if self._is_terminal():
            return self.relay()
        return super().do_HEAD()

    def do_POST(self):
        # ttyd asks for a token over POST; nothing else here accepts one.
        if self._is_terminal():
            return self.relay()
        self.send_error(405, "nothing here accepts POST")

    # ---- the terminal relay ----------------------------------------------
    def relay(self):
        origin = self.headers.get("Origin")
        if origin is not None and origin not in self.allowed_origins:
            self.log_error("refused cross-origin terminal request from %s", origin)
            self.send_error(403, "cross-origin request to the tutor terminal refused")
            return

        if not self.socket_path or not os.path.exists(self.socket_path):
            self.terminal_down()
            return

        try:
            upstream = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            upstream.connect(self.socket_path)
        except OSError as exc:
            self.log_error("cannot reach ttyd on %s: %s", self.socket_path, exc)
            self.terminal_down()
            return

        # Replay the request upstream verbatim, with Host rewritten. ttyd runs
        # with `-b /terminal`, so the path is forwarded unchanged.
        head = [f"{self.command} {self.path} HTTP/1.1"]
        for key, value in self.headers.items():
            if key.lower() == "host":
                continue
            head.append(f"{key}: {value}")
        head.append("Host: 127.0.0.1")
        request = ("\r\n".join(head) + "\r\n\r\n").encode("latin-1")

        self.close_connection = True
        client = self.connection
        try:
            upstream.sendall(request)
            length = int(self.headers.get("Content-Length") or 0)
            if length:
                upstream.sendall(self.rfile.read(length))

            down = threading.Thread(
                target=_pump_socket, args=(upstream, client), daemon=True
            )
            down.start()
            _pump_reader(self.rfile, upstream)
            down.join(timeout=5)
        except OSError:
            pass
        finally:
            upstream.close()

    def terminal_down(self):
        """Explain the outage in the drawer rather than showing a bare 502."""
        if self.command != "GET" or self.path.rstrip("/").endswith("/ws"):
            self.send_error(503, "the tutor terminal is not running")
            return
        body = DOWN_PAGE.encode("utf-8")
        self.send_response(503)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    # ---- niceties --------------------------------------------------------
    def end_headers(self):
        # Pages are edited live, so they are never cached. Assets are stable and
        # get a short TTL on purpose: a no-store stylesheet has to be re-fetched
        # on every page load, so a restart of this server at the wrong moment
        # leaves a lesson rendering unstyled with no cached copy to fall back on.
        tail = self.path.split("?", 1)[0].rsplit("/", 1)[-1]
        is_page = tail == "" or tail.endswith(".html") or "." not in tail
        self.send_header("Cache-Control", "no-store" if is_page else "max-age=60")
        super().end_headers()

    def log_message(self, fmt, *args):
        # Quiet on success — this shares a terminal with the launcher.
        status = args[1] if len(args) > 1 else ""
        if str(status).startswith(("4", "5")):
            sys.stderr.write("  %s\n" % (fmt % args))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True, help="workspace directory to serve")
    parser.add_argument("--port", type=int, default=8800)
    parser.add_argument("--socket", required=True, help="ttyd UNIX socket path")
    args = parser.parse_args()

    StudyHandler.socket_path = args.socket
    StudyHandler.allowed_origins = (
        f"http://127.0.0.1:{args.port}",
        f"http://localhost:{args.port}",
    )

    def handler(*a, **kw):
        return StudyHandler(*a, directory=args.root, **kw)

    server = http.server.ThreadingHTTPServer(("127.0.0.1", args.port), handler)
    server.daemon_threads = True
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
