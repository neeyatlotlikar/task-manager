#!/usr/bin/env bash
set -euo pipefail

echo "==> Ruff lint"
uv run ruff check .

echo "==> Ruff format check"
uv run ruff format --check .

echo "==> isort check"
uv run isort --check-only .

echo "==> Django system checks"
uv run python manage.py check --fail-level WARNING

echo "==> Missing migrations check"
uv run python manage.py makemigrations --check --dry-run

echo "==> Tests"
uv run python manage.py test