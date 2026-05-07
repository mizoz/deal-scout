from deal_scout.models import Deal
from deal_scout.scanner import scan


def test_extra_includes_are_required(monkeypatch):
    def fake_fetch_source(source, *, user_agent):
        return [
            Deal(title="Cheap cologne", source="test", url="https://example.com/1"),
            Deal(title="Cheap monitor", source="test", url="https://example.com/2"),
        ]

    monkeypatch.setattr("deal_scout.scanner.fetch_source", fake_fetch_source)
    results = scan(
        {
            "user_agent": "test",
            "minimum_score": 0,
            "priority_keywords": {"cheap": 1},
            "sources": [{"name": "test", "type": "atom", "url": "https://example.com"}],
        },
        extra_includes=["cologne"],
    )

    assert [deal.title for deal in results] == ["Cheap cologne"]


def test_extra_includes_do_not_match_source_tags_only(monkeypatch):
    def fake_fetch_source(source, *, user_agent):
        return [
            Deal(
                title="Women perfume tester",
                source="test",
                url="https://example.com/1",
                tags=["cologne"],
            )
        ]

    monkeypatch.setattr("deal_scout.scanner.fetch_source", fake_fetch_source)
    results = scan(
        {
            "user_agent": "test",
            "minimum_score": 0,
            "priority_keywords": {},
            "sources": [{"name": "test", "type": "atom", "url": "https://example.com"}],
        },
        extra_includes=["cologne"],
    )

    assert results == []
