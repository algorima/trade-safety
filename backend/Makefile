.PHONY: lint code-style type-check unit-test integration-test format migrate check-migrations

PY_FILES=$(shell find trade_safety -type f -name '*.py' -print)

lint:
	poetry run pylint $(PY_FILES)

code-style:
	poetry run isort --check-only --diff trade_safety
	poetry run black --check trade_safety

type-check:
	poetry run mypy --check-untyped-defs trade_safety
	poetry run pyright

unit-test:
	poetry run python -m unittest discover -s tests/unit -v

integration-test:
	poetry run python -m unittest discover -s tests/integration -v

format:
	poetry run isort trade_safety
	poetry run black trade_safety

migrate:
	poetry run alembic upgrade head

check-migrations:
	poetry run alembic check
