from __future__ import annotations

from collections.abc import Iterable
from typing import Any

from .atom import fetch_atom
from .merchant_page import fetch_merchant_page
from .reddit import fetch_reddit


def fetch_source(source: dict[str, Any], *, user_agent: str) -> Iterable:
    source_type = source.get("type")
    if source_type == "atom":
        return fetch_atom(source, user_agent=user_agent)
    if source_type == "reddit":
        return fetch_reddit(source, user_agent=user_agent)
    if source_type == "merchant_page":
        return fetch_merchant_page(source, user_agent=user_agent)
    raise ValueError(f"Unsupported source type: {source_type}")

