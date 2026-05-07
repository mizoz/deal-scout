from deal_scout.models import Deal
from deal_scout.output import render_sources, render_table


def test_render_table_has_core_columns():
    table = render_table(
        [
            Deal(
                title="Cologne tester $15",
                source="PerfumeOnline",
                url="https://example.com",
                price=15,
                discount_percent=80,
                score=123,
            )
        ]
    )
    assert "Score" in table
    assert "Cologne tester" in table
    assert "$15" in table


def test_render_sources_lists_source_names():
    table = render_sources(
        {
            "sources": [
                {
                    "name": "RedFlagDeals",
                    "type": "atom",
                    "tags": ["canada"],
                    "url": "https://example.com/feed",
                }
            ]
        }
    )
    assert "RedFlagDeals" in table
    assert "atom" in table
