from __future__ import annotations

import argparse
from pathlib import Path

from .config import load_config
from .output import render_json, render_markdown
from .scanner import scan


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="deal-scout")
    subparsers = parser.add_subparsers(dest="command", required=True)

    scan_parser = subparsers.add_parser("scan", help="scan configured deal sources")
    scan_parser.add_argument("--config", default="configs/calgary.yaml", help="YAML config path")
    scan_parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    scan_parser.add_argument("--limit", type=int, default=None)
    scan_parser.add_argument("--include", action="append", default=[], help="extra keyword to require")
    scan_parser.add_argument("--output", help="write output to a file")

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "scan":
        config = load_config(args.config)
        limit = args.limit if args.limit is not None else int(config.get("limit", 25))
        deals = scan(config, extra_includes=args.include)[:limit]
        if args.format == "json":
            rendered = render_json(deals)
        else:
            title = f"{config.get('location', config.get('profile', 'Deal'))} Deal Scout"
            rendered = render_markdown(deals, title=title)

        if args.output:
            Path(args.output).write_text(rendered, encoding="utf-8")
        else:
            print(rendered)
        return 0

    parser.error(f"Unhandled command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())

