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
   # Using poetry (from project root)
   poetry run python test/test_lambda.py

   # Or inside poetry shell
   python test/test_lambda.py
   ```

4. **Try the utilities:**

   ```bash
   # Test credential combinations (educational/testing only)
   poetry run python src/utils/cred.py https://example.com/login
   
   # Test rate limiting
   poetry run python src/utils/ddos.py https://api.example.com 1.0
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
poetry run black src/ test/
```

**Lint code:**

```bash
poetry run flake8 src/ test/
```

**Type check:**

```bash
poetry run mypy src/ test/
```

**Run all tests:**

```bash
poetry run pytest test/ -v
```

**Run tests with coverage:**

```bash
poetry run pytest test/ --cov=src --cov-report=html
```

## Project Structure

```
blue-yellow/
├── pyproject.toml          # Poetry configuration
├── poetry.toml             # Local Poetry settings
├── poetry.lock             # Locked dependencies (generated)
├── README.md               # Main project README
├── SETUP.md               # This file
├── LICENSE                # License information
├── .env                   # Environment variables (not tracked)
├── .env.sample            # Environment variable template
├── .gitignore             # Git ignore rules
├── src/
│   ├── lambda/
│   │   ├── entrypoint.py  # AWS Lambda function
│   │   └── README.md      # Lambda documentation
│   └── utils/
│       ├── ping.py        # URL ping utility
│       ├── cred.py        # Credential testing utility
│       ├── ddos.py        # Rate limit testing utility
│       └── clone.py       # Clone utility (placeholder)
└── test/
    └── test_lambda.py     # Lambda function tests
```

## Quick Start

```bash
# Install Poetry if needed
curl -sSL https://install.python-poetry.org | python3 -

# Install project dependencies
cd /home/kali/labs/blue-yellow
poetry install --no-root

# Run Lambda tests
poetry run python test/test_lambda.py

# Test security utilities
poetry run python src/utils/cred.py https://example.com/login
poetry run python src/utils/ddos.py https://example.com 1.0
```

## AWS Lambda Deployment

See `src/lambda/README.md` for Lambda-specific deployment instructions.

### Quick Deployment Package

```bash
# Create deployment package
mkdir -p lambda-package/utils
cp src/lambda/entrypoint.py lambda-package/
cp src/utils/ping.py lambda-package/utils/
cd lambda-package
zip -r ../lambda-function.zip .
cd ..
rm -rf lambda-package

# Now upload lambda-function.zip to AWS Lambda
```

## Security Utilities Usage

### Credential Testing Tool

Tests login forms for rate limiting and security mechanisms:

```bash
poetry run python src/utils/cred.py <login_url>

# Example with verbose output
poetry run python src/utils/cred.py https://example.com/login
```

**Important**: Only use on systems you own or have permission to test.

### Rate Limit Testing Tool

Tests API endpoints for rate limiting:

```bash
poetry run python src/utils/ddos.py <url> [period_seconds]

# Example: Test with 0.5 second intervals
poetry run python src/utils/ddos.py https://api.example.com 0.5
```

## Environment Variables

Copy `.env.sample` to `.env` and configure as needed:

```bash
cp .env.sample .env
# Edit .env with your settings
```

## Troubleshooting

### Poetry Installation Issues

If Poetry installation fails:

```bash
# Try pip installation
pip install --user poetry

# Or use pipx (recommended)
python3 -m pip install --user pipx
python3 -m pipx ensurepath
pipx install poetry
```

### Import Errors

If you get import errors when running scripts:

```bash
# Make sure you're in the project root
cd /home/kali/labs/blue-yellow

# Activate the virtual environment
poetry shell

# Or use poetry run
poetry run python test/test_lambda.py
```

### Dependency Issues

If dependencies are out of sync:

```bash
# Remove lock file and reinstall
rm poetry.lock
poetry install

# Or update all dependencies
poetry update
```

## Additional Resources

- [Poetry Documentation](https://python-poetry.org/docs/)
- [AWS Lambda Python Runtime](https://docs.aws.amazon.com/lambda/latest/dg/lambda-python.html)
- [AWS SQS Documentation](https://docs.aws.amazon.com/sqs/)
- [Python Type Hints](https://docs.python.org/3/library/typing.html)
