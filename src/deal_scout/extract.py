from __future__ import annotations

import re

MONEY_RE = re.compile(
    r"(?<![\w])(?:(?:CA\$|CAD\s*)?\$\s*|CAD\s+)([0-9][0-9,]*(?:\.[0-9]{1,2})?)",
    re.I,
)
CENTS_RE = re.compile(r"(?<![\w])([1-9][0-9]?)\s*cents?\b", re.I)
PERCENT_RE = re.compile(
    r"(?:"
    r"(?P<pct_after>[0-9]{1,3}(?:\.[0-9]+)?)\s*%\s*(?:off|save|discount|savings)"
    r"|"
    r"(?:save|saves|saving|discount)\s*(?P<pct_before>[0-9]{1,3}(?:\.[0-9]+)?)\s*%"
    r")",
    re.I,
)
SAVE_RE = re.compile(r"(?:save|saves|saving|discount)\s*(?:CA\$|CAD\s*)?\$?\s*([0-9][0-9,]*(?:\.[0-9]{1,2})?)", re.I)


def extract_money_values(text: str) -> list[float]:
    values: list[float] = []
    for match in MONEY_RE.finditer(text):
        raw = match.group(1).replace(",", "")
        try:
            values.append(float(raw))
        except ValueError:
            continue
    for match in CENTS_RE.finditer(text):
        try:
            values.append(float(match.group(1)) / 100)
        except ValueError:
            continue
    return values


def extract_percent(text: str) -> float | None:
    matches = []
    for match in PERCENT_RE.finditer(text):
        value = float(match.group("pct_after") or match.group("pct_before"))
        if 0 < value <= 100:
            matches.append(value)
    return max(matches) if matches else None


def extract_save_amount(text: str) -> float | None:
    values = []
    for match in SAVE_RE.finditer(text):
        try:
            values.append(float(match.group(1).replace(",", "")))
        except ValueError:
            continue
    return max(values) if values else None


def infer_prices(text: str) -> tuple[float | None, float | None, float | None]:
    """Infer current price, original price, and discount from deal text."""
    money_values = extract_money_values(text)
    percent = extract_percent(text)

    current = None
    original = None

    if money_values:
        current = min(money_values)
        original = max(money_values) if len(money_values) > 1 and max(money_values) != current else None

    if percent is None and current and original and original > current:
        percent = round((original - current) / original * 100, 2)

    save_amount = extract_save_amount(text)
    if original is None and current and save_amount:
        original = current + save_amount
        if percent is None and original > 0:
            percent = round(save_amount / original * 100, 2)

    return current, original, percent
