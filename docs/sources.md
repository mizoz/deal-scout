# Sources

Deal Scout ships with conservative source adapters. They are designed to pull a
small number of public pages or feeds and avoid heavy scraping.

## Current Adapters

| Adapter | Best For | Notes |
| --- | --- | --- |
| `atom` | Forums and sites with feeds | Used for RedFlagDeals Hot Deals |
| `reddit` | Local searches and subreddits | Uses public JSON endpoints |
| `merchant_page` | Simple product grids | Can follow product pages for variants |

## Adding a Source

Add a source block to a config file:

```yaml
- name: My Local Liquidator
  type: merchant_page
  url: https://example.com/deals
  tags: [local, liquidation]
  include_keywords: [clearance, liquidation, "$1"]
```

Then inspect it:

```bash
deal-scout sources --config configs/calgary.yaml
deal-scout scan --config configs/calgary.yaml --limit 10
```

## Adding a New Adapter

1. Create `src/deal_scout/sources/<name>.py`.
2. Return a list of `Deal` objects.
3. Register it in `src/deal_scout/sources/__init__.py`.
4. Add tests for parsing and filtering.
5. Document the source type here.

## Polite Use

Keep scan frequency human-scale. Deal Scout is intended for personal weekly or
daily checks, not aggressive crawling.

