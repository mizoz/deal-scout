# Configuration

Deal Scout profiles are YAML files. A profile controls sources, filters,
scoring, output size, and the user agent sent to websites.

## Minimal Profile

```yaml
profile: calgary
location: Calgary, AB
currency: CAD
limit: 25
minimum_score: 18
max_per_url: 3

blocked_keywords:
  - pork
  - bacon

priority_keywords:
  cologne: 32
  "90% off": 55
  liquidation: 18

sources:
  - name: RedFlagDeals Hot Deals
    type: atom
    url: https://forums.redflagdeals.com/feed/forum/9
    tags: [canada, online, rfd]
```

## Scoring

Scores are intentionally simple:

- larger discount percentage means a higher score
- cheap absolute price gets a boost
- priority keywords add configured points
- large inferred savings add a small boost

This makes the ranking easy to understand and easy to tune.

## Filters

Use `blocked_keywords` for hard exclusions. The Calgary profile blocks pork
terms globally:

```yaml
blocked_keywords:
  - pork
  - bacon
  - ham
  - pepperoni
```

Each source can also block source-specific noise:

```yaml
sources:
  - name: PerfumeOnline Clearance
    type: merchant_page
    url: https://perfumeonline.ca/
    blocked_keywords: [sample vial, travel size, body spray]
```

## Source Types

### `atom`

Reads Atom feeds such as RedFlagDeals.

```yaml
- name: RedFlagDeals Hot Deals
  type: atom
  url: https://forums.redflagdeals.com/feed/forum/9
```

### `reddit`

Reads Reddit JSON listing/search endpoints.

```yaml
- name: Calgary Reddit Deals Search
  type: reddit
  url: https://www.reddit.com/r/Calgary/search.json?q=deals&restrict_sr=1&sort=new&limit=25
```

### `merchant_page`

Reads product cards from a merchant page. Set `follow_product_pages` for
variant-level extraction on Shopify-style product pages.

```yaml
- name: PerfumeOnline Clearance
  type: merchant_page
  url: https://perfumeonline.ca/
  follow_product_pages: true
  max_links: 35
  include_keywords: [clearance, cologne, fragrance, men, edt, edp, tester]
```

