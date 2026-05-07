from __future__ import annotations

from datetime import datetime
from html import unescape
import re
import xml.etree.ElementTree as ET

from ..extract import infer_prices
from ..models import Deal
from .http import fetch_text

ATOM_NS = {"atom": "http://www.w3.org/2005/Atom"}
TAG_RE = re.compile(r"<[^>]+>")


def _text(node: ET.Element | None) -> str:
    if node is None or node.text is None:
        return ""
    return unescape(node.text).strip()


def _clean_html(value: str) -> str:
    return unescape(TAG_RE.sub(" ", value)).strip()


def _parse_date(value: str) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def fetch_atom(source: dict, *, user_agent: str) -> list[Deal]:
    xml_text = fetch_text(source["url"], user_agent=user_agent)
    root = ET.fromstring(xml_text)
    deals: list[Deal] = []
    tags = list(source.get("tags", []))

    for entry in root.findall("atom:entry", ATOM_NS):
        title = _text(entry.find("atom:title", ATOM_NS))
        content = _clean_html(_text(entry.find("atom:content", ATOM_NS)))
        link = ""
        link_node = entry.find("atom:link", ATOM_NS)
        if link_node is not None:
            link = link_node.attrib.get("href", "")
        published = _parse_date(_text(entry.find("atom:published", ATOM_NS)))
        price, original, percent = infer_prices(" ".join([title, content]))
        deals.append(
            Deal(
                title=title,
                source=source["name"],
                url=link or source["url"],
                price=price,
                original_price=original,
                discount_percent=percent,
                summary=content,
                published_at=published,
                tags=tags,
            )
        )
    return deals

