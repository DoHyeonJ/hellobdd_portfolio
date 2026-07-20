#!/usr/bin/env python3
"""로컬에서 포트폴리오 정적 사이트를 띄웁니다."""

from __future__ import annotations

import argparse
import functools
import http.server
import os
import socket
import socketserver
import webbrowser

ROOT = os.path.dirname(os.path.abspath(__file__))
DEFAULT_PORT = 5500
DEFAULT_HOST = "127.0.0.1"


class ReusableTCPServer(socketserver.TCPServer):
    allow_reuse_address = True


def port_in_use(host: str, port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(0.3)
        return sock.connect_ex((host, port)) == 0


def find_free_port(host: str, start: int, tries: int = 20) -> int:
    for port in range(start, start + tries):
        if not port_in_use(host, port):
            return port
    raise OSError(f"No free port found from {start} to {start + tries - 1}")


def main() -> None:
    parser = argparse.ArgumentParser(description="HELLOBDD portfolio local server")
    parser.add_argument("-p", "--port", type=int, default=DEFAULT_PORT)
    parser.add_argument("--host", default=DEFAULT_HOST)
    parser.add_argument("--no-open", action="store_true", help="브라우저 자동 실행 안 함")
    args = parser.parse_args()

    os.chdir(ROOT)
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=ROOT)

    port = args.port
    if port_in_use(args.host, port):
        port = find_free_port(args.host, args.port + 1)
        print(f"Port {args.port} is busy → using {port}")

    with ReusableTCPServer((args.host, port), handler) as httpd:
        url = f"http://{args.host}:{port}/index.html"
        print(f"Serving {ROOT}")
        print(f"Open {url}")
        print("Ctrl+C to stop")
        if not args.no_open:
            webbrowser.open(url)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nStopped.")


if __name__ == "__main__":
    main()
