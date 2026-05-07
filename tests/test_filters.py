from deal_scout.filters import passes_filters
from deal_scout.models import Deal


def test_blocks_pork_terms():
    deal = Deal(title="Pork tenderloin $3.99/lb", source="test", url="https://example.com")
    assert not passes_filters(deal, blocked_keywords=["pork", "bacon"])


def test_allows_non_pork_deal():
    deal = Deal(title="Cologne tester $15.15", source="test", url="https://example.com")
    assert passes_filters(deal, blocked_keywords=["pork", "bacon"], include_keywords=["cologne"])

