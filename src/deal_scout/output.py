from __future__ import annotations

import json
from datetime import datetime

from .models import Deal


def render_json(deals: list[Deal]) -> str:
    return json.dumps([deal.to_dict() for deal in deals], indent=2, ensure_ascii=False)


def render_markdown(deals: list[Deal], *, title: str = "Deal Scout Digest") -> str:
    lines = [f"# {title}", "", f"Generated: {datetime.now().isoformat(timespec='seconds')}", ""]
    if not deals:
        lines.append("No deals matched the filters.")
        return "\n".join(lines)

    for idx, deal in enumerate(deals, start=1):
        bits = []
        if deal.price is not None:
            bits.append(f"${deal.price:g}")
        if deal.discount_percent is not None:
            bits.append(f"{deal.discount_percent:g}% off")
        if deal.score:
            bits.append(f"score {deal.score:.0f}")
        suffix = f" ({', '.join(bits)})" if bits else ""
        lines.append(f"{idx}. [{deal.title}]({deal.url}){suffix}")
        lines.append(f"   Source: {deal.source}")
        if deal.summary:
            summary = " ".join(deal.summary.split())
            if len(summary) > 220:
                summary = summary[:217].rstrip() + "..."
            lines.append(f"   Notes: {summary}")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def render_table(deals: list[Deal]) -> str:
    headers = ["#", "Score", "Deal", "Price", "Discount", "Source"]
    rows: list[list[str]] = []

    for idx, deal in enumerate(deals, start=1):
        title = " ".join(deal.title.split())
        if len(title) > 58:
            title = title[:55].rstrip() + "..."
        rows.append(
            [
                str(idx),
                f"{deal.score:.0f}",
                title,
                f"${deal.price:g}" if deal.price is not None else "",
                f"{deal.discount_percent:g}%" if deal.discount_percent is not None else "",
                deal.source,
            ]
        )

    widths = [
        max(len(headers[col]), *(len(row[col]) for row in rows)) if rows else len(headers[col])
        for col in range(len(headers))
    ]

    def fmt(row: list[str]) -> str:
        return "  ".join(value.ljust(widths[idx]) for idx, value in enumerate(row)).rstrip()

    lines = [fmt(headers), fmt(["-" * width for width in widths])]
    lines.extend(fmt(row) for row in rows)
    if not rows:
        lines.append("No deals matched the filters.")
    return "\n".join(lines)


def render_sources(config: dict) -> str:
    headers = ["#", "Name", "Type", "Tags", "URL"]
    rows: list[list[str]] = []
    for idx, source in enumerate(config.get("sources", []), start=1):
        rows.append(
            [
                str(idx),
                source.get("name", ""),
                source.get("type", ""),
                ", ".join(source.get("tags", [])),
                source.get("url", ""),
            ]
        )

    widths = [
        min(46, max(len(headers[col]), *(len(row[col]) for row in rows))) if rows else len(headers[col])
        for col in range(len(headers))
    ]

    def trim(value: str, width: int) -> str:
        return value if len(value) <= width else value[: width - 3].rstrip() + "..."

    def fmt(row: list[str]) -> str:
        return "  ".join(trim(value, widths[idx]).ljust(widths[idx]) for idx, value in enumerate(row)).rstrip()

    lines = [fmt(headers), fmt(["-" * width for width in widths])]
    lines.extend(fmt(row) for row in rows)
    return "\n".join(lines)
