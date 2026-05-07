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

