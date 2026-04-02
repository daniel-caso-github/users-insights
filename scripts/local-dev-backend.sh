#!/usr/bin/env bash
set -e

cd "$(dirname "$0")/../backend"
uv run uvicorn main:app --reload
