.PHONY: install test scan sources doctor

install:
	python3 -m pip install -e ".[dev]"

test:
	pytest -q

scan:
	deal-scout scan --config configs/calgary.yaml --limit 15

sources:
	deal-scout sources --config configs/calgary.yaml

doctor:
	deal-scout doctor --config configs/calgary.yaml

