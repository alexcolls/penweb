# Setup Guide

## Poetry Installation and Usage

### Install Poetry

If you don't have Poetry installed, run:

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

Or using pip:

```bash
pip install poetry
```

### Project Setup

1. **Install dependencies:**

   ```bash
   poetry install
   ```

2. **Activate the virtual environment:**

   ```bash
   poetry shell
   ```

3. **Run tests:**

   ```bash
   # Using poetry
   cd src/d2
   poetry run python test_lambda.py

   # Or inside poetry shell
   cd src/d2
   python test_lambda.py
   ```

### Managing Dependencies

**Add a new dependency:**

```bash
poetry add package-name
```

**Add a development dependency:**

```bash
poetry add --group dev package-name
```

**Update dependencies:**

```bash
poetry update
```

**Show installed packages:**

```bash
poetry show
```

### Development Tools

The project includes these dev tools:

- **pytest**: Test framework
- **pytest-cov**: Coverage reporting
- **black**: Code formatter
- **flake8**: Linter
- **mypy**: Type checker

**Format code:**

```bash
poetry run black src/
```

**Lint code:**

```bash
poetry run flake8 src/
```

**Type check:**

```bash
poetry run mypy src/
```

## Project Structure

```
blue-yellow/
├── pyproject.toml          # Poetry configuration
├── poetry.toml             # Local Poetry settings
├── poetry.lock             # Locked dependencies (generated)
├── README.md               # Main project README
├── SETUP.md               # This file
├── .gitignore             # Git ignore rules
└── src/
    └── d2/
        ├── lambda.py      # AWS Lambda function
        ├── test_lambda.py # Test script
        └── README.md      # Lambda documentation
```

## Quick Start

```bash
# Install Poetry if needed
curl -sSL https://install.python-poetry.org | python3 -

# Install project dependencies
cd /home/quantium/labs/blue-yellow
poetry install --no-root

# Run tests
cd src/d2
poetry run python test_lambda.py
```

## AWS Lambda Deployment

See `src/d2/README.md` for Lambda-specific deployment instructions.
