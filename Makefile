.PHONY: install test demo lint typecheck all

install:
	pip install -e ".[dev]"

test:
	pytest -q

demo:
	avc-compare

lint:
	ruff check src tests examples demos

typecheck:
	mypy src/identity_models

all: lint typecheck test