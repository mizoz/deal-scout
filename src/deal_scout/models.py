from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass(slots=True)
class Deal:
    title: str
    source: str
    url: str
    price: float | None = None
    original_price: float | None = None
    discount_percent: float | None = None
    summary: str = ""
    published_at: datetime | None = None
    tags: list[str] = field(default_factory=list)
    score: float = 0

    @property
    def searchable_text(self) -> str:
        return " ".join([self.title, self.summary, self.source, " ".join(self.tags)])

    def to_dict(self) -> dict[str, Any]:
        return {
            "title": self.title,
            "source": self.source,
            "url": self.url,
            "price": self.price,
            "original_price": self.original_price,
            "discount_percent": self.discount_percent,
            "summary": self.summary,
            "published_at": self.published_at.isoformat() if self.published_at else None,
            "tags": self.tags,
            "score": round(self.score, 2),
        }

