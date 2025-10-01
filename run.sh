#!/bin/bash
# Convenience script to run the blue-yellow CLI

cd "$(dirname "$0")"
poetry run python src/main.py

