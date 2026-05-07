from __future__ import annotations

import argparse
from pathlib import Path

from .config import load_config
from .output import render_json, render_markdown, render_sources, render_table
from .scanner import scan


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="deal-scout",
        description="Scan configured local and online deal sources, then rank the strongest finds.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    scan_parser = subparsers.add_parser("scan", help="scan configured deal sources")
    scan_parser.add_argument("--config", default="configs/calgary.yaml", help="YAML config path")
    scan_parser.add_argument("--format", choices=["table", "markdown", "json"], default="table")
    scan_parser.add_argument("--limit", type=int, default=None)
    scan_parser.add_argument("--include", action="append", default=[], help="extra keyword to require")
    scan_parser.add_argument("--min-score", type=float, default=None, help="override config minimum_score")
    scan_parser.add_argument("--output", help="write output to a file")

    sources_parser = subparsers.add_parser("sources", help="list configured sources")
    sources_parser.add_argument("--config", default="configs/calgary.yaml", help="YAML config path")

    doctor_parser = subparsers.add_parser("doctor", help="validate config and environment")
    doctor_parser.add_argument("--config", default="configs/calgary.yaml", help="YAML config path")

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "scan":
        config = load_config(args.config)
        if args.min_score is not None:
            config["minimum_score"] = args.min_score
        limit = args.limit if args.limit is not None else int(config.get("limit", 25))
        deals = scan(config, extra_includes=args.include)[:limit]
        if args.format == "json":
            rendered = render_json(deals)
        elif args.format == "markdown":
            title = f"{config.get('location', config.get('profile', 'Deal'))} Deal Scout"
            rendered = render_markdown(deals, title=title)
        else:
            rendered = render_table(deals)

        if args.output:
            Path(args.output).write_text(rendered, encoding="utf-8")
        else:
            print(rendered)
        return 0

    if args.command == "sources":
        config = load_config(args.config)
        print(render_sources(config))
        return 0

    if args.command == "doctor":
        config = load_config(args.config)
        sources = config.get("sources", [])
        blocked = config.get("blocked_keywords", [])
        priority = config.get("priority_keywords", {})
        print("Deal Scout doctor")
        print(f"Config: {Path(args.config).resolve()}")
        print(f"Profile: {config.get('profile', 'unnamed')}")
        print(f"Sources: {len(sources)}")
        print(f"Blocked keywords: {len(blocked)}")
        print(f"Priority boosts: {len(priority)}")
        print("Status: OK")
        return 0

    parser.error(f"Unhandled command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
