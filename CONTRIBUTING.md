# Contributing

Deal Scout should stay easy to run, easy to inspect, and polite to sources.

## Development

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -e ".[dev]"
pytest -q
deal-scout doctor
deal-scout scan --limit 10
```

## Pull Request Checklist

- Add or update tests for parser/filter/scoring changes.
- Keep source adapters small and source-specific.
- Do not add high-frequency crawling behavior.
- Update docs when config keys or commands change.
- Keep generated caches, virtualenvs, and install metadata out of git.

