#!/bin/bash
# Convenience script to run the penweb CLI

cd "$(dirname "$0")"
poetry run python src/main.py

