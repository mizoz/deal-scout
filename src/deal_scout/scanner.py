from __future__ import annotations

from typing import Any

from .filters import contains_any, passes_filters
from .models import Deal
from .scoring import score_deal
from .sources import fetch_source


def scan(config: dict[str, Any], *, extra_includes: list[str] | None = None) -> list[Deal]:
    user_agent = config.get("user_agent", "deal-scout/0.1")
    blocked = config.get("blocked_keywords", [])
    priority = config.get("priority_keywords", {})
    minimum_score = float(config.get("minimum_score", 0))
    deals: list[Deal] = []

    for source in config.get("sources", []):
        source_includes = list(source.get("include_keywords", []))
        source_blocked = list(blocked) + list(source.get("blocked_keywords", []))

        try:
            source_deals = list(fetch_source(source, user_agent=user_agent))
        except Exception as exc:
            deals.append(
                Deal(
                    title=f"Source failed: {source.get('name', source.get('url', 'unknown'))}",
                    source="deal-scout",
                    url=source.get("url", ""),
                    summary=str(exc),
                    tags=["error"],
                    score=-1,
                )
            )
            continue

        for deal in source_deals:
            if not passes_filters(deal, blocked_keywords=source_blocked, include_keywords=source_includes):
                continue
            include_text = " ".join([deal.title, deal.summary, deal.source])
            if extra_includes and not contains_any(include_text, extra_includes):
                continue
            score_deal(deal, priority)
            if deal.score >= minimum_score:
                deals.append(deal)

    ranked = sorted(deals, key=lambda item: item.score, reverse=True)
    max_per_url = config.get("max_per_url")
    if not max_per_url:
        return ranked

    capped: list[Deal] = []
    counts: dict[str, int] = {}
    for deal in ranked:
        key = deal.url or deal.title
        counts[key] = counts.get(key, 0)
        if counts[key] >= int(max_per_url):
            continue
        counts[key] += 1
        capped.append(deal)
    return capped
