#!/usr/bin/env bash
set -euo pipefail

echo "==> isort format"
uv run isort .

echo "==> Ruff format"
uv run ruff format .