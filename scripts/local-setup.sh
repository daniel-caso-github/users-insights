#!/usr/bin/env bash
set -e

echo "Installing backend dependencies..."
cd "$(dirname "$0")/../backend"
uv sync --group dev

echo "Installing frontend dependencies..."
cd "../frontend"
npm install

echo "Done."
