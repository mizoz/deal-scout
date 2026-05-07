from __future__ import annotations

from datetime import datetime, timezone

from ..extract import infer_prices
from ..models import Deal
from .http import fetch_json


def fetch_reddit(source: dict, *, user_agent: str) -> list[Deal]:
    payload = fetch_json(source["url"], user_agent=user_agent)
    tags = list(source.get("tags", []))
    deals: list[Deal] = []

    for child in payload.get("data", {}).get("children", []):
        item = child.get("data", {})
        title = item.get("title") or ""
        summary = item.get("selftext") or ""
        permalink = item.get("permalink") or ""
        url = "https://www.reddit.com" + permalink if permalink.startswith("/") else item.get("url") or source["url"]
        created = item.get("created_utc")
        published = datetime.fromtimestamp(created, tz=timezone.utc) if created else None
        price, original, percent = infer_prices(" ".join([title, summary]))
        deals.append(
            Deal(
                title=title,
                source=source["name"],
                url=url,
                price=price,
                original_price=original,
                discount_percent=percent,
                summary=summary,
                published_at=published,
                tags=tags,
            )
        )
    return deals

