from __future__ import annotations

import sys


def main() -> None:
    try:
        from markitdown_mcp.__main__ import main as mcp_main
    except ImportError as exc:
        print(
            "PageMint connector requires markitdown-mcp. Install with "
            "`pip install markitdown-mcp` or `pip install pagemint-offline[connectors]`.",
            file=sys.stderr,
        )
        raise SystemExit(1) from exc

    mcp_main()


if __name__ == "__main__":
    main()
