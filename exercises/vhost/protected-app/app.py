#!/usr/bin/env python3
"""Dependency-free protected-project web application example.

The production application receives identity only from the governed RCC proxy.
Local demonstration mode is deliberately restricted to loopback and synthetic
headers. The example exposes curated records, never arbitrary filesystem paths.
"""
from __future__ import annotations

import html
import ipaddress
import json
import os
import re
import sqlite3
from pathlib import Path
from urllib.parse import unquote
from wsgiref.simple_server import make_server

UID_RE = re.compile(r"^[a-z][a-z0-9._-]{0,63}$")
GROUP_RE = re.compile(r"^[a-z][a-z0-9._-]{0,127}$")
FILE_ID_RE = re.compile(r"^[a-f0-9]{32}$")


def required(name: str, default: str | None = None) -> str:
    value = os.environ.get(name, default or "").strip()
    if not value:
        raise RuntimeError(f"Missing required environment variable {name}")
    return value


def networks(raw: str):
    result = tuple(ipaddress.ip_network(item.strip(), strict=True) for item in raw.split(",") if item.strip())
    if not result:
        raise RuntimeError("RCC_TRUSTED_PROXY_CIDRS is empty")
    return result


EXPECTED_HOST = required("RCC_EXPECTED_HOST", "example.invalid").lower().rstrip(".")
TRUSTED = networks(required("RCC_TRUSTED_PROXY_CIDRS", "127.0.0.0/8,::1/128"))
REQUIRED_GROUP = required("RCC_REQUIRED_GROUP", "project_demo").lower()
DATABASE = Path(required("RCC_DATABASE", str(Path(__file__).with_name("demo.sqlite3"))))
DEMO_MODE = os.environ.get("RCC_DEMO_MODE", "0") == "1"

if not GROUP_RE.fullmatch(REQUIRED_GROUP):
    raise RuntimeError("Invalid project group")


def response(start_response, status: str, body: bytes, content_type="text/html; charset=utf-8", headers=None):
    base = [
        ("Content-Type", content_type),
        ("Content-Length", str(len(body))),
        ("Cache-Control", "no-store"),
        ("Content-Security-Policy", "default-src 'none'; style-src 'self'; img-src 'self'; form-action 'none'; frame-ancestors 'none'; base-uri 'none'"),
        ("Referrer-Policy", "no-referrer"),
        ("X-Content-Type-Options", "nosniff"),
        ("X-Frame-Options", "DENY"),
    ]
    start_response(status, base + (headers or []))
    return [body]


def error(start_response, code: int, message: str):
    body = f"<h1>{code}</h1><p>{html.escape(message)}</p>".encode()
    return response(start_response, f"{code} Error", body)


def trusted_source(environ) -> bool:
    try:
        address = ipaddress.ip_address(environ.get("REMOTE_ADDR", ""))
    except ValueError:
        return False
    return any(address in network for network in TRUSTED)


def identity(environ):
    uid = environ.get("HTTP_REMOTE_USER", "").strip().lower()
    groups = {x.strip().lower() for x in environ.get("HTTP_REMOTE_GROUPS", "").split(",") if x.strip()}
    if DEMO_MODE and trusted_source(environ):
        uid = uid or "demo-user"
        groups = groups or {REQUIRED_GROUP}
    if not UID_RE.fullmatch(uid):
        return None, "Authenticated RCC identity is missing"
    if not groups or any(not GROUP_RE.fullmatch(x) for x in groups):
        return None, "Invalid project-group identity"
    if REQUIRED_GROUP not in groups:
        return None, "Your account is not authorized for this project"
    return {"uid": uid, "groups": sorted(groups)}, None


def db():
    if not DATABASE.exists():
        raise RuntimeError("Demo database is missing; run init_demo_data.py")
    con = sqlite3.connect(f"file:{DATABASE.resolve()}?mode=ro", uri=True)
    con.row_factory = sqlite3.Row
    return con


def application(environ, start_response):
    method = environ.get("REQUEST_METHOD", "GET")
    if method not in {"GET", "HEAD"}:
        return error(start_response, 405, "Only GET and HEAD are allowed")
    if not trusted_source(environ):
        return error(start_response, 403, "Direct backend access is prohibited")
    host = environ.get("HTTP_HOST", "").split(":", 1)[0].lower().rstrip(".")
    if not DEMO_MODE and host != EXPECTED_HOST:
        return error(start_response, 400, "Unexpected Host header")
    if not DEMO_MODE and environ.get("HTTP_X_FORWARDED_PROTO", "").lower() != "https":
        return error(start_response, 400, "HTTPS proxy context is required")
    user, problem = identity(environ)
    if problem:
        return error(start_response, 403, problem)

    path = unquote(environ.get("PATH_INFO", "/"))
    if path == "/healthz":
        body = json.dumps({"status": "ok", "user": user["uid"]}, sort_keys=True).encode()
        return response(start_response, "200 OK", body, "application/json")
    if path == "/":
        with db() as con:
            rows = con.execute("SELECT title, summary FROM records ORDER BY title LIMIT 100").fetchall()
        items = "".join(f"<li><strong>{html.escape(r['title'])}</strong>: {html.escape(r['summary'])}</li>" for r in rows)
        body = (f"<!doctype html><title>Protected project example</title><h1>Project records</h1>"
                f"<p>Signed in as <strong>{html.escape(user['uid'])}</strong>.</p><ul>{items}</ul>").encode()
        return response(start_response, "200 OK", body)
    match = re.fullmatch(r"/files/([a-f0-9]{32})", path)
    if match:
        with db() as con:
            row = con.execute("SELECT content, download_name FROM files WHERE id=?", (match.group(1),)).fetchone()
        if row is None:
            return error(start_response, 404, "Not found")
        body = bytes(row["content"])
        safe = re.sub(r"[^A-Za-z0-9._-]", "_", row["download_name"])
        return response(start_response, "200 OK", body, "application/octet-stream", [("Content-Disposition", f'attachment; filename="{safe}"')])
    return error(start_response, 404, "Not found")


if __name__ == "__main__":
    if not DEMO_MODE:
        raise SystemExit("Set RCC_DEMO_MODE=1 for loopback-only local demonstration")
    with make_server("127.0.0.1", 8080, application) as server:
        print("Local demo: http://127.0.0.1:8080/ (Ctrl-C to stop)")
        server.serve_forever()
