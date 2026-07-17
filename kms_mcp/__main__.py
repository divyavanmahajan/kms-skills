"""CLI: `python3 -m kms_mcp [serve|index|search]`.

  serve            run the MCP server on stdio (default; used by .mcp.json)
  serve --http     run as a streamable-HTTP server for remote agents
  index            (re)build the Kuzu graph + embeddings in .kms-index/
  search "query"   quick semantic search from the terminal (debugging)
"""

import argparse
import json
import sys


def main() -> None:
    parser = argparse.ArgumentParser(prog="kms_mcp", description=__doc__)
    sub = parser.add_subparsers(dest="command")

    serve = sub.add_parser("serve", help="run the MCP server (default)")
    serve.add_argument("--http", action="store_true",
                       help="streamable HTTP transport instead of stdio")
    serve.add_argument("--host", default="127.0.0.1")
    serve.add_argument("--port", type=int, default=8471)

    sub.add_parser("index", help="rebuild the index")

    search = sub.add_parser("search", help="semantic search (debugging)")
    search.add_argument("query")
    search.add_argument("--limit", type=int, default=10)

    args = parser.parse_args()
    command = args.command or "serve"

    if command == "index":
        from .indexer import build_index
        build_index()
        return

    if command == "search":
        from .server import STATE
        STATE.ensure()
        hits = STATE.index.search(args.query, limit=args.limit)
        print(json.dumps([vars(h) for h in hits], indent=2))
        return

    from .server import mcp
    if getattr(args, "http", False):
        mcp.settings.host = args.host
        mcp.settings.port = args.port
        mcp.settings.stateless_http = True
        print(f"KMS MCP server on http://{args.host}:{args.port}/mcp",
              file=sys.stderr)
        mcp.run(transport="streamable-http")
    else:
        mcp.run()


if __name__ == "__main__":
    main()
