from __future__ import annotations

from bs4 import BeautifulSoup

from ..extract import extract_money_values, infer_prices
from ..models import Deal
from .http import fetch_text


def _candidate_blocks(soup: BeautifulSoup) -> list:
    selectors = [
        "article",
        ".product",
        ".card",
        ".grid__item",
        ".product-item",
        ".featured-product",
        "li",
    ]
    blocks = []
    seen: set[int] = set()
    for selector in selectors:
        for block in soup.select(selector):
            ident = id(block)
            if ident not in seen:
                seen.add(ident)
                blocks.append(block)
    return blocks


def _absolute_url(base_url: str, href: str | None) -> str:
    if not href:
        return base_url
    if href.startswith("http://") or href.startswith("https://"):
        return href
    if href.startswith("/"):
        root = base_url.split("/", 3)[:3]
        return "/".join(root) + href
    return base_url.rstrip("/") + "/" + href


def _product_links(soup: BeautifulSoup, base_url: str, max_links: int) -> list[str]:
    links: list[str] = []
    seen: set[str] = set()
    for anchor in soup.find_all("a", href=True):
        href = anchor["href"]
        if "/products/" not in href:
            continue
        url = _absolute_url(base_url, href.split("?", 1)[0])
        if url in seen:
            continue
        seen.add(url)
        links.append(url)
        if len(links) >= max_links:
            break
    return links


def _product_links_from_blocks(
    soup: BeautifulSoup,
    base_url: str,
    max_links: int,
    include_keywords: list[str],
) -> list[str]:
    links: list[str] = []
    seen: set[str] = set()
    for block in _candidate_blocks(soup):
        text = " ".join(block.get_text(" ", strip=True).split()).casefold()
        if include_keywords and not any(keyword in text for keyword in include_keywords):
            continue
        if "$" not in text and "cents" not in text:
            continue
        anchor = block.find("a", href=True)
        if not anchor or "/products/" not in anchor["href"]:
            continue
        url = _absolute_url(base_url, anchor["href"].split("?", 1)[0])
        if url in seen:
            continue
        seen.add(url)
        links.append(url)
        if len(links) >= max_links:
            break
    return links


def _product_title(soup: BeautifulSoup, url: str) -> str:
    for node in soup.find_all("h1"):
        text = " ".join(node.get_text(" ", strip=True).split())
        if text:
            return text
    for attr in ({"property": "og:title"}, {"name": "twitter:title"}):
        node = soup.find("meta", attrs=attr)
        content = (node.get("content") or "").strip() if node else ""
        if content:
            return content
    if soup.title and soup.title.string:
        text = " ".join(soup.title.string.split())
        if text:
            return text.split("–", 1)[0].strip()
    return url.rsplit("/", 1)[-1].replace("-", " ").title()


def _parse_product_detail(source: dict, url: str, html: str) -> list[Deal]:
    soup = BeautifulSoup(html, "html.parser")
    title = _product_title(soup, url)
    tags = list(source.get("tags", []))
    strings = list(soup.stripped_strings)
    deals: list[Deal] = []
    seen: set[tuple[str, float]] = set()

    for index, value in enumerate(strings[:-1]):
        variant = value.strip()
        price_text = strings[index + 1].strip()
        if not variant.endswith("-"):
            continue
        prices = extract_money_values(price_text)
        if not prices:
            continue
        variant = variant[:-1].strip()
        if not variant or "sold out" in variant.casefold():
            continue
        price = prices[0]
        key = (variant.casefold(), price)
        if key in seen:
            continue
        seen.add(key)
        deal_title = f"{title} - {variant}"
        summary = f"{deal_title} - {price_text}"
        current, original, percent = infer_prices(summary)
        deals.append(
            Deal(
                title=deal_title,
                source=source["name"],
                url=url,
                price=current or price,
                original_price=original,
                discount_percent=percent,
                summary=summary,
                tags=tags,
            )
        )

    return deals


def fetch_merchant_page(source: dict, *, user_agent: str) -> list[Deal]:
    html = fetch_text(source["url"], user_agent=user_agent)
    soup = BeautifulSoup(html, "html.parser")
    tags = list(source.get("tags", []))
    include_keywords = [kw.casefold() for kw in source.get("include_keywords", [])]
    deals: list[Deal] = []

    if source.get("follow_product_pages"):
        max_links = int(source.get("max_links", 20))
        links = _product_links_from_blocks(soup, source["url"], max_links, include_keywords)
        if not links:
            links = _product_links(soup, source["url"], max_links)
        for url in links:
            try:
                detail_html = fetch_text(url, user_agent=user_agent)
            except Exception:
                continue
            deals.extend(_parse_product_detail(source, url, detail_html))
        if deals:
            return deals

    for block in _candidate_blocks(soup):
        text = " ".join(block.get_text(" ", strip=True).split())
        if len(text) < 12:
            continue
        if include_keywords and not any(keyword in text.casefold() for keyword in include_keywords):
            continue

        price, original, percent = infer_prices(text)
        if price is None and percent is None and "$" not in text:
            continue

        title = text
        if len(title) > 140:
            title = title[:137].rstrip() + "..."

        link = block.find("a", href=True)
        url = _absolute_url(source["url"], link["href"] if link else None)

        deals.append(
            Deal(
                title=title,
                source=source["name"],
                url=url,
                price=price,
                original_price=original,
                discount_percent=percent,
                summary=text,
                tags=tags,
            )
        )

    return deals
