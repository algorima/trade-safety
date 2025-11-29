.PHONY: lint code-style type-check unit-test integration-test format migrate check-migrations

PY_FILES=$(shell find . -type d -name '.venv' -prune -o -type f -name '*.py' -print | sed 's|^\./||')

lint:
	poetry run pylint $(PY_FILES)

code-style:
	poetry run isort --check-only --diff .
	poetry run black --check .

type-check:
	poetry run mypy --check-untyped-defs .
	poetry run pyright

unit-test:
	poetry run python -m unittest discover -s tests/unit -v

integration-test:
	poetry run python -m unittest discover -s tests/integration -v

format:
	poetry run isort .
	poetry run black .

migrate:
	poetry run alembic upgrade head

check-migrations:
	poetry run alembic check
