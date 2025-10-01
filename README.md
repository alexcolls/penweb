# blue-yellow

A collection of security testing utilities and AWS Lambda functions for URL monitoring and rate limit testing.

## Overview

This repository contains tools designed for security testing, penetration testing, and monitoring. It includes an AWS Lambda function for URL health checks and utilities for testing rate limiting and authentication mechanisms.

**NEW:** 🎨 **Interactive CLI** - Run all tools through a beautiful, user-friendly command-line interface with ASCII art and interactive menus!

## Components

### 📡 AWS Lambda - URL Pinger (`src/lambda/`)

AWS Lambda function that processes SQS messages containing URLs and pings them via HTTP requests. Perfect for monitoring website availability and response times.

**Features:**
- Processes SQS events with batch support
- Supports plain URL strings or JSON formatted messages
- Returns detailed results with status codes and response times
- Comprehensive error handling and logging
- No external dependencies (uses Python standard library only)

See [`src/lambda/README.md`](src/lambda/README.md) for detailed documentation and deployment instructions.

### 🔧 Security Testing Utilities (`src/services/`)

#### 🔐 Credential Testing (`attempt_login.py`)

Tests login form security and rate limiting by attempting credential combinations.

**Features:**
- Automatic form field detection (email/username and password fields)
- Password variation generation from keywords
- Rate limiting detection
- CAPTCHA and blocking mechanism detection
- Session management with cookie support
- Detailed reporting of successful/blocked attempts

**Usage:**
```bash
# Via CLI (Recommended)
./run.sh  # Then select option 4

# Or directly
poetry run python src/services/attempt_login.py https://example.com/login
```

**Use Cases:**
- Testing login rate limiting effectiveness
- Verifying security mechanisms (CAPTCHA, account lockout)
- Penetration testing authorization flows
- Security audit compliance validation

#### 🌐 Rate Limit Testing (`d2.py`)

Tests API and web endpoint rate limiting by making repeated requests.

**Features:**
- Configurable request intervals
- User-Agent randomization
- Query parameter randomization
- Status code monitoring
- Blocking detection (429, 403, 503)
- Connection error handling

**Usage:**
```bash
# Via CLI (Recommended)
./run.sh  # Then select option 3

# Or directly
poetry run python src/services/d2.py https://api.example.com 0.5
```

**Use Cases:**
- Testing rate limiting configurations
- API endpoint stress testing
- WAF (Web Application Firewall) validation
- Load balancer behavior testing

#### 🔗 URL Ping (`ping.py`)

Core utility for making HTTP requests and measuring response times.

**Features:**
- HTTP/HTTPS support
- Configurable timeout
- Response time measurement
- Status code capture
- Error handling for network issues

#### 📋 Website Cloning (`clone.py`)

Downloads website HTML, CSS, and JavaScript files for offline analysis.

**Features:**
- Downloads HTML, CSS, and JS files
- Preserves relative links
- Extracts inline styles and scripts
- Resource detection and downloading
- BeautifulSoup HTML parsing

**Usage:**
```bash
# Via CLI (Recommended)
./run.sh  # Then select option 2

# Or directly
poetry run python src/services/clone.py https://example.com output_dir
```

## Project Structure

```
blue-yellow/
├── pyproject.toml          # Poetry configuration and dependencies
├── poetry.lock             # Locked dependency versions
├── poetry.toml             # Local Poetry settings
├── README.md               # This file
├── LICENSE                # License information
├── run.sh                 # Convenience script to launch CLI
├── .env                   # Environment variables (not tracked)
├── .env.sample            # Environment variable template
├── docs/
│   ├── SETUP.md           # Detailed setup instructions
│   ├── CLI_USAGE.md       # Interactive CLI usage guide
│   └── LOGGING.md         # Logging system documentation
├── src/
│   ├── cli/               # Interactive CLI interface
│   │   ├── banner.py      # ASCII art and branding
│   │   └── menu.py        # Interactive menu system
│   ├── lambda/
│   │   ├── entrypoint.py  # AWS Lambda handler
│   │   └── README.md      # Lambda documentation
│   ├── services/          # Core pentesting services
│   │   ├── ping.py        # URL ping utility
│   │   ├── clone.py       # Website cloning utility
│   │   ├── d2.py          # DDoS/rate limit testing
│   │   └── attempt_login.py # Login testing utility
│   ├── utils/             # Helper utilities
│   │   ├── logger.py      # Logging configuration
│   │   └── sqs.py         # SQS utilities
│   └── main.py            # CLI entry point
└── test/
    └── test_lambda.py     # Lambda function tests
```

## Setup

See [`docs/SETUP.md`](docs/SETUP.md) for detailed setup instructions.

**Quick Start:**

```bash
# Install Poetry if not already installed
curl -sSL https://install.python-poetry.org | python3 -

# Install project dependencies
poetry install --no-root

# 🚀 Launch the Interactive CLI (Recommended!)
./run.sh
# or
poetry run python src/main.py

# Alternative: Run tools directly
poetry run python test/test_lambda.py  # Lambda tests
```

### 🎨 Interactive CLI

The easiest way to use Blue-Yellow is through the **interactive CLI**:

```bash
./run.sh
```

Features:
- 🎨 Beautiful ASCII art banner
- 📋 Interactive menu system
- ⚖️ Built-in legal warnings and authorization checks
- 🎯 Guided workflows for each tool
- 🔴 Clear marking of offensive tools
- ⌨️ Graceful error handling

See [`docs/CLI_USAGE.md`](docs/CLI_USAGE.md) for detailed usage guide.

## Dependencies

**Runtime:**
- `python` ^3.9
- `requests` ^2.31.0 - HTTP library for utilities
- `beautifulsoup4` ^4.12.0 - HTML parsing for form detection

**Development:**
- `pytest` ^7.4.0 - Testing framework
- `pytest-cov` ^4.1.0 - Coverage reporting
- `black` ^23.7.0 - Code formatting
- `flake8` ^6.1.0 - Linting
- `mypy` ^1.5.0 - Type checking

## 📚 Documentation

- 📖 **[Setup Guide](docs/SETUP.md)** - Installation and configuration instructions
- 🎨 **[CLI Usage Guide](docs/CLI_USAGE.md)** - Interactive CLI documentation and examples
- 📝 **[Logging Guide](docs/LOGGING.md)** - Logging system overview and usage
- ⚙️  **[Logging Setup](docs/LOGGING_SETUP.md)** - Advanced logging configuration
- 🚀 **[Lambda Deployment](src/lambda/README.md)** - AWS Lambda deployment guide

## Development

This project uses Poetry for dependency management.

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

**Run tests:**
```bash
poetry run pytest test/
```

**View logs:**
See [`docs/LOGGING.md`](docs/LOGGING.md) for logging configuration and usage.

## Security & Legal Notice

⚠️ **IMPORTANT**: These tools are designed for legitimate security testing purposes only.

- Always obtain proper authorization before testing any systems
- Only use on systems you own or have explicit permission to test
- Follow responsible disclosure practices
- Comply with all applicable laws and regulations
- Review and follow your organization's security testing policies

Unauthorized access to computer systems is illegal. The authors and contributors of this project assume no liability for misuse of these tools.

## AWS Lambda Deployment

The URL Pinger Lambda function can be deployed using:
- AWS Console (manual upload)
- AWS CLI
- Infrastructure as Code (Terraform, CloudFormation, AWS SAM)

See [`src/lambda/README.md`](src/lambda/README.md) for complete deployment instructions.

## Use Cases

- **DevOps**: Monitor website availability and response times
- **Security Testing**: Test rate limiting and authentication mechanisms
- **Penetration Testing**: Validate security controls
- **Compliance**: Verify security requirements are met
- **Quality Assurance**: Automated endpoint testing

## Contributing

Contributions are welcome! Please ensure:
1. All tests pass
2. Code is formatted with `black`
3. No linting errors from `flake8`
4. Type hints are used where appropriate
5. Security best practices are followed

## License

See [LICENSE](LICENSE) file for details.
