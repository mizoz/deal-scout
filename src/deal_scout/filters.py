from __future__ import annotations

from collections.abc import Iterable

from .models import Deal


def contains_any(text: str, keywords: Iterable[str]) -> bool:
    folded = text.casefold()
    return any(keyword.casefold() in folded for keyword in keywords)


def passes_filters(
    deal: Deal,
    *,
    blocked_keywords: Iterable[str] = (),
    include_keywords: Iterable[str] = (),
) -> bool:
    text = deal.searchable_text
    if contains_any(text, blocked_keywords):
        return False
    include = list(include_keywords)
    if include and not contains_any(text, include):
        return False
    return True

