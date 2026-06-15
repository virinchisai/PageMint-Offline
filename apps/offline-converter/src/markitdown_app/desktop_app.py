from __future__ import annotations

import socket
import threading
import time
import webbrowser

from waitress import serve

from markitdown_app.server import create_app


def find_port(start: int = 8765, attempts: int = 20) -> int:
    for port in range(start, start + attempts):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            try:
                sock.bind(("127.0.0.1", port))
            except OSError:
                continue
            return port
    raise RuntimeError("No available local port found for PageMint Offline.")


def main() -> None:
    port = find_port()
    url = f"http://127.0.0.1:{port}"
    app = create_app()

    thread = threading.Thread(
        target=lambda: serve(app, host="127.0.0.1", port=port),
        daemon=True,
    )
    thread.start()
    time.sleep(1)
    webbrowser.open(url)

    try:
        while thread.is_alive():
            thread.join(timeout=1)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
