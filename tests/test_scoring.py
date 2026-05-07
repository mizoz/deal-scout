from deal_scout.models import Deal
from deal_scout.scoring import score_deal


def test_fragrance_and_deep_discount_score_high():
    deal = Deal(
        title="Men cologne tester $15.15 70% off",
        source="test",
        url="https://example.com",
        price=15.15,
        discount_percent=70,
    )
    score = score_deal(deal, {"cologne": 30, "tester": 10})
    assert score >= 120

