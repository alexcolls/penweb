# blue-yellow

A collection of utilities and AWS Lambda functions.

## Projects

### 📡 D2 - AWS Lambda URL Pinger (`src/d2/`)

AWS Lambda function that processes SQS messages containing URLs and pings them via HTTP requests.

**Features:**

- Processes SQS events with batch support
- Supports plain URL or JSON formatted messages
- Returns detailed results with status codes and response times
- Comprehensive error handling and logging

See [`src/d2/README.md`](src/d2/README.md) for detailed documentation.

### 🔧 Other Utilities

- `src/clone/` - Clone utilities
- `src/creds/` - Credentials management
- `src/wifi/` - WiFi utilities

## Setup

See [`SETUP.md`](SETUP.md) for detailed setup instructions.

**Quick Start:**

```bash
# Install dependencies with Poetry
poetry install --no-root

# Run tests
cd src/d2
poetry run python test_lambda.py
```

## Development

This project uses Poetry for dependency management and includes:

- **pytest**: Testing framework
- **black**: Code formatting
- **flake8**: Linting
- **mypy**: Type checking

## License

See [LICENSE](LICENSE) file for details.
