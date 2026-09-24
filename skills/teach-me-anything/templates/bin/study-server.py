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
import datetime
import http.server
import json
import os
import re
import socket
import sys
import threading

TERMINAL_PREFIX = "/terminal"
CHANGES_PATH = "/changes"
SUBMIT_PATH = "/submit"
SUBMIT_MAX = 256 * 1024
PREFS_PATH = "/preferences"
PREFS_FILE = "preferences.js"
PREFS_MAX = 16 * 1024
PREFS_KEY = re.compile(r"^[A-Za-z][A-Za-z0-9]{0,31}$")
# Kept word for word in step with templates/preferences.js.
PREFS_HEAD = """/* Learner preferences — the choices on preferences.html. Schema and what each
   setting does: formats/preferences.md. Everything after "window.PREFS =" is
   strict JSON: the server rewrites this file when the learner presses Save. */
window.PREFS = """
# The theme: style.css imports theme.css from the workspace folder, and a Save that
# picks one copies assets/themes/<name>.css there. Only a name with a file behind it.
THEME_FILE = "theme.css"
THEMES_DIR = os.path.join("assets", "themes")
THEME_NAME = re.compile(r"^[a-z][a-z0-9-]{0,31}$")
# Settings the tutor has nothing to act on (the console's look): saved, but left
# out of the line typed into the drawer.
PREFS_QUIET = ("theme",)
CHUNK = 65536

# What the console renders, and so what counts as "new content" landing.
CONTENT_EXT = (".html", ".js", ".css")
SKIP_DIRS = {"bin", "node_modules"}

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
    # Files this server wrote itself, path → mtime. The page that caused the write
    # has already redrawn the console, so they are not "new content" for the badge.
    self_written = {}

    # ---- routing ---------------------------------------------------------
    def _is_terminal(self):
        p = self.path
        return p == TERMINAL_PREFIX or p.startswith(TERMINAL_PREFIX + "/") \
            or p.startswith(TERMINAL_PREFIX + "?")

    def do_GET(self):
        if self._is_terminal():
            return self.relay()
        if self.path.split("?", 1)[0] == CHANGES_PATH:
            return self.changes()
        if self._no_theme():
            return self.empty_theme()
        return super().do_GET()

    # ---- new content -----------------------------------------------------
    def changes(self):
        """The newest page in the workspace, so the console can show a badge
        when the tutor writes one. Polled; the workspace is small enough that
        a walk per poll costs nothing worth an inotify dependency."""
        stamp, latest = 0, ""
        for base, dirs, files in os.walk(self.directory):
            dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith(".")]
            for name in files:
                if not name.endswith(CONTENT_EXT):
                    continue
                full = os.path.join(base, name)
                try:
                    mtime = os.stat(full).st_mtime_ns
                except OSError:
                    continue
                if self.self_written.get(full) == mtime:
                    continue
                if mtime > stamp:
                    stamp = mtime
                    latest = os.path.relpath(os.path.join(base, name), self.directory)
        body = json.dumps({"stamp": stamp, "latest": latest}).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_HEAD(self):
        if self._is_terminal():
            return self.relay()
        if self._no_theme():
            return self.empty_theme()
        return super().do_HEAD()

    # ---- the theme -------------------------------------------------------
    def _no_theme(self):
        return self.path.split("?", 1)[0] == "/" + THEME_FILE and \
            not os.path.exists(os.path.join(self.directory, THEME_FILE))

    def empty_theme(self):
        """Every page imports theme.css; until a theme is picked there is none.
        An empty stylesheet means the defaults, and no 404 line in the terminal."""
        self.send_response(200)
        self.send_header("Content-Type", "text/css; charset=utf-8")
        self.send_header("Content-Length", "0")
        self.end_headers()

    def do_POST(self):
        # ttyd asks for a token over POST; the others are a page's answers and
        # the preferences page's Save.
        if self._is_terminal():
            return self.relay()
        if self.path.split("?", 1)[0] == SUBMIT_PATH:
            return self.submit()
        if self.path.split("?", 1)[0] == PREFS_PATH:
            return self.preferences()
        self.send_error(405, "nothing here accepts POST")

    # ---- submissions -----------------------------------------------------
    def submit(self):
        """A page's answers (assets/submit.js) → submissions/<date>-<kind>.md, and
        the one-line note the console then types into the tutor's drawer. Same
        Origin rule as the terminal: only this console may write here."""
        origin = self.headers.get("Origin", "")
        if origin and origin not in self.allowed_origins:
            self.send_error(403, "wrong origin")
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if not 0 < length <= SUBMIT_MAX:
                raise ValueError("size")
            data = json.loads(self.rfile.read(length).decode("utf-8"))
            items = data["items"]
            if not isinstance(items, list):
                raise ValueError("items")
        except (ValueError, KeyError, TypeError):
            self.send_error(400, "bad submission")
            return

        kind = re.sub(r"[^a-z0-9-]+", "-", str(data.get("kind", "page")).lower()).strip("-") or "page"
        page = str(data.get("page", ""))
        when = datetime.datetime.now()
        outcome = lambda it: str(it.get("outcome", "open"))
        right = sum(1 for it in items if outcome(it) == "right")
        missed = [it for it in items if outcome(it) == "missed"]
        open_ = sum(1 for it in items if outcome(it) == "open")
        written = sum(1 for it in items if it.get("type") in ("short", "challenge") and it.get("answer"))
        missed_topics = []
        for it in missed:
            t = str(it.get("topic") or ("Q" + str(it.get("n", "?"))))
            if t not in missed_topics:
                missed_topics.append(t)

        lines = ["# %s — %s" % (kind, when.strftime("%Y-%m-%d %H:%M")), "",
                 "page: %s" % page,
                 "%d right · %d missed · %d unanswered · %d written" %
                 (right, len(missed), open_, written), ""]
        for it in items:
            # Questions carry their own numbering ("1. …"); only number the unnumbered.
            question = str(it.get("question", ""))
            head = "## " + (question if re.match(r"\d", question) else "%s. %s" % (it.get("n", "?"), question))
            if it.get("topic"):
                head += "   [%s]" % it["topic"]
            lines += [head + " — " + outcome(it)]
            if it.get("type") == "choice":
                picked = it.get("picked") or []
                lines += ["picked: " + (" → ".join(map(str, picked)) if picked else "(nothing)"),
                          "correct: " + str(it.get("correct", ""))]
            else:
                answer = str(it.get("answer", "")).strip()
                lines += ["answer:"] + (["> " + l for l in answer.splitlines()] if answer else ["> (nothing written)"])
                if it.get("model"):
                    lines += ["model: " + str(it["model"])]
            lines += [""]

        sub_dir = os.path.join(self.directory, "submissions")
        os.makedirs(sub_dir, exist_ok=True)
        stem = when.strftime("%Y-%m-%d-%H%M") + "-" + kind
        name, n = stem + ".md", 2
        while os.path.exists(os.path.join(sub_dir, name)):
            name, n = "%s-%d.md" % (stem, n), n + 1
        with open(os.path.join(sub_dir, name), "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        rel = "submissions/" + name

        summary = "%d right, %d missed" % (right, len(missed))
        if missed_topics:
            summary += " (" + ", ".join(missed_topics) + ")"
        if open_:
            summary += ", %d unanswered" % open_
        if written:
            summary += ", %d written answer%s to grade" % (written, "" if written == 1 else "s")
        line = "[console] I submitted %s: %s. Full answers: %s" % (page or kind, summary, rel)

        body = json.dumps({"path": rel, "line": line}).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    # ---- preferences -----------------------------------------------------
    def preferences(self):
        """preferences.html's Save → preferences.js, merged onto what is there,
        and the one-line note naming what changed. The file is loaded as a script
        by the console, so only flat keys and plain values get in — never markup
        or code, whatever the request carries."""
        origin = self.headers.get("Origin", "")
        if origin and origin not in self.allowed_origins:
            self.send_error(403, "wrong origin")
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if not 0 < length <= PREFS_MAX:
                raise ValueError("size")
            incoming = json.loads(self.rfile.read(length).decode("utf-8"))
            if not isinstance(incoming, dict) or len(incoming) > 40:
                raise ValueError("shape")
            for key, value in incoming.items():
                if not PREFS_KEY.match(key):
                    raise ValueError("key")
                if isinstance(value, bool) or value is None:
                    continue
                if isinstance(value, (int, float)):
                    if value != value or abs(value) > 1e6:
                        raise ValueError("number")
                    continue
                if not isinstance(value, str) or len(value) > 200 \
                        or any(ord(c) < 32 for c in value):
                    raise ValueError("value")
            theme_src = None
            if "theme" in incoming:
                name = incoming["theme"]
                if not isinstance(name, str) or not THEME_NAME.match(name):
                    raise ValueError("theme")
                theme_src = os.path.join(self.directory, THEMES_DIR, name + ".css")
                if not os.path.isfile(theme_src):
                    raise ValueError("theme")
        except (ValueError, TypeError, UnicodeDecodeError):
            self.send_error(400, "bad preferences")
            return

        path = os.path.join(self.directory, PREFS_FILE)
        old = {}
        try:
            with open(path, encoding="utf-8") as f:
                text = f.read()
            # Anchored to a line start: the header comment names "window.PREFS =" too.
            start = re.search(r"^window\.PREFS\s*=", text, re.M)
            old = json.loads(text[start.end():].strip().rstrip(";").strip())
            if not isinstance(old, dict):
                old = {}
        except (OSError, AttributeError, ValueError):
            old = {}   # missing, or hand-edited past JSON: the save still lands

        new = dict(old)
        new.update(incoming)
        shown = lambda v: v if isinstance(v, str) and v else json.dumps(v, ensure_ascii=False)
        changed = [(k, "%s %s → %s" % (k, shown(old[k]) if k in old else "(unset)", shown(v)))
                   for k, v in incoming.items() if k not in old or old[k] != v]
        told = [text for k, text in changed if k not in PREFS_QUIET]
        with open(path, "w", encoding="utf-8") as f:
            f.write(PREFS_HEAD + json.dumps(new, indent=2, ensure_ascii=False) + ";\n")
        try:
            StudyHandler.self_written[path] = os.stat(path).st_mtime_ns
        except OSError:
            pass
        if theme_src:
            theme = os.path.join(self.directory, THEME_FILE)
            with open(theme_src, "rb") as src, open(theme, "wb") as dst:
                dst.write(src.read())
            try:
                StudyHandler.self_written[theme] = os.stat(theme).st_mtime_ns
            except OSError:
                pass

        line = ("[console] I saved my preferences: %s. Now in %s." % (", ".join(told), PREFS_FILE)
                if told else None)
        body = json.dumps({"path": PREFS_FILE, "line": line,
                           "changed": [text for k, text in changed]},
                          ensure_ascii=False).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

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

        # Replay the request upstream with Host rewritten. ttyd runs with
        # `-b /terminal`, so the path is forwarded unchanged.
        upgrade = "upgrade" in (self.headers.get("Connection") or "").lower()
        dropped = {"host", "keep-alive"} if upgrade else {"host", "keep-alive", "connection"}
        head = [f"{self.command} {self.path} HTTP/1.1"]
        for key, value in self.headers.items():
            if key.lower() in dropped:
                continue
            head.append(f"{key}: {value}")
        head.append("Host: 127.0.0.1")
        if not upgrade:
            head.append("Connection: close")
        request = ("\r\n".join(head) + "\r\n\r\n").encode("latin-1")

        # Either way this client connection is finished afterwards.
        self.close_connection = True
        try:
            upstream.sendall(request)
            length = int(self.headers.get("Content-Length") or 0)
            if length:
                upstream.sendall(self.rfile.read(length))
            if upgrade:
                self.tunnel(upstream)
            else:
                self.forward_one_response(upstream)
        except OSError:
            pass
        finally:
            upstream.close()

    def tunnel(self, upstream):
        """A WebSocket: after the 101 the connection is ttyd's for good, so bytes
        are pumped both ways until either side hangs up."""
        down = threading.Thread(
            target=_pump_socket, args=(upstream, self.connection), daemon=True
        )
        down.start()
        _pump_reader(self.rfile, upstream)
        down.join(timeout=5)

    def forward_one_response(self, upstream):
        """A plain request: relay exactly ONE response, then hang up.

        This must not be a raw two-way pipe. Browsers keep connections alive and
        reuse them, so a pipe left open after `GET /terminal/` would carry the
        browser's *next* request — a lesson, the stylesheet — straight to ttyd,
        which knows nothing about it and answers with its own bare "404". That
        was a real bug: refresh the console and the lesson came back as 404.
        So the response is marked `Connection: close` and the socket is shut,
        which makes the browser open a fresh connection that gets routed again.
        """
        upstream.settimeout(15)
        buf = b""
        while b"\r\n\r\n" not in buf:
            chunk = upstream.recv(CHUNK)
            if not chunk:
                break
            buf += chunk
        head, sep, body = buf.partition(b"\r\n\r\n")
        if not sep:
            self.send_error(502, "the tutor terminal sent no response")
            return

        lines = head.split(b"\r\n")
        length = None
        kept = [lines[0]]
        for line in lines[1:]:
            name = line.split(b":", 1)[0].strip().lower()
            if name in (b"connection", b"keep-alive"):
                continue
            if name == b"content-length":
                try:
                    length = int(line.split(b":", 1)[1])
                except ValueError:
                    pass
            kept.append(line)
        kept.append(b"Connection: close")
        self.connection.sendall(b"\r\n".join(kept) + b"\r\n\r\n")

        status = lines[0].split(b" ", 2)[1:2]
        if self.command == "HEAD" or status in ([b"204"], [b"304"]):
            return  # these carry a Content-Length but never a body

        # With a Content-Length, stop there; without one, the body runs to EOF,
        # which `Connection: close` upstream guarantees will come.
        sent = 0
        while True:
            if body:
                self.connection.sendall(body)
                sent += len(body)
            if length is not None and sent >= length:
                break
            body = upstream.recv(CHUNK)
            if not body:
                break

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
        # reviews.js, preferences.js and theme.css are data that gets rewritten,
        # not assets: never cached either.
        tail = self.path.split("?", 1)[0].rsplit("/", 1)[-1]
        is_page = tail == "" or tail.endswith(".html") or "." not in tail \
            or tail in ("reviews.js", PREFS_FILE, THEME_FILE)
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
