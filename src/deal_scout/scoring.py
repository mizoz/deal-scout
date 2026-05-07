from __future__ import annotations

from .models import Deal


def score_deal(deal: Deal, priority_keywords: dict[str, int | float]) -> float:
    score = 0.0
    text = deal.searchable_text.casefold()

    if deal.discount_percent:
        score += min(deal.discount_percent, 100)

    if deal.price is not None:
        if deal.price <= 1:
            score += 35
        elif deal.price <= 5:
            score += 25
        elif deal.price <= 20:
            score += 14
        elif deal.price <= 50:
            score += 6

    for keyword, boost in priority_keywords.items():
        if keyword.casefold() in text:
            score += float(boost)

    if deal.original_price and deal.price and deal.original_price > deal.price:
        savings = deal.original_price - deal.price
        if savings >= 100:
            score += 20
        elif savings >= 50:
            score += 12
        elif savings >= 20:
            score += 6

    deal.score = score
    return score

