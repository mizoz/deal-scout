# Deal Scout

Deal Scout is a small, shareable deal scanner for local and online bargain hunting.
It is built for fast weekly scans: pull configured sources, extract prices and
discounts, remove blocked items, score the strongest deals, and print a clean
Markdown or JSON digest.

The first profile is tuned for Calgary and Canada-wide online deals, with:

- RedFlagDeals Hot Deals via the public Atom feed
- Reddit JSON feeds for local deal posts
- merchant pages such as PerfumeOnline clearance/product pages
- personal filters, including a default no-pork block list
- priority keywords for fragrance/cologne, 90% off, liquidation, clearance, and
  cheap essentials

## Existing Projects Checked

There are useful projects, but none matched this exact workflow:

- `Kiizon/flippscrape`: Flipp grocery flyer scraping by postal code.
- `MauriceZ/rfdwatch`: tiny RedFlagDeals keyword watcher.
- `jez500/pricebuddy`: full self-hosted product price tracker with alerts.

Deal Scout keeps the scope smaller: weekly scouting and shareable digests with
local/personal filters.

## Quick Start

```bash
cd /home/az/deal-scout
python3 -m venv .venv
. .venv/bin/activate
pip install -e ".[dev]"
deal-scout scan --config configs/calgary.yaml --format markdown
```

You can also run without installing:

```bash
PYTHONPATH=src python3 -m deal_scout.cli scan --config configs/calgary.yaml
```

## Examples

Only show the strongest 12 deals:

```bash
deal-scout scan --config configs/calgary.yaml --limit 12
```

Save JSON for a web app or automation:

```bash
deal-scout scan --config configs/calgary.yaml --format json > deals.json
```

Search harder for fragrance/cologne:

```bash
deal-scout scan --config configs/calgary.yaml --include cologne --include fragrance
```

## Config

The Calgary profile lives in `configs/calgary.yaml`.

Important sections:

- `blocked_keywords`: terms removed from results. Pork terms are blocked there.
- `priority_keywords`: words that boost score.
- `sources`: feed and page definitions.
- `minimum_score`: cuts low-quality noise.

## Notes

This is a polite scanner. Keep source counts low, respect robots/terms for every
site you add, and do not run it as a high-frequency scraper.

