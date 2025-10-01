# blue-yellow

A collection of security testing utilities and AWS Lambda functions for URL monitoring and rate limit testing.

## Overview

This repository contains tools designed for security testing, penetration testing, and monitoring. It includes an AWS Lambda function for URL health checks and utilities for testing rate limiting and authentication mechanisms.

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

### 🔧 Security Testing Utilities (`src/utils/`)

#### 🔐 Credential Testing (`cred.py`)

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
poetry run python src/utils/cred.py https://example.com/login
```

**Use Cases:**
- Testing login rate limiting effectiveness
- Verifying security mechanisms (CAPTCHA, account lockout)
- Penetration testing authorization flows
- Security audit compliance validation

#### 🌐 Rate Limit Testing (`ddos.py`)

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
poetry run python src/utils/ddos.py https://api.example.com 0.5
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

#### 📋 Clone Utility (`clone.py`)

Placeholder utility for future development.

## Project Structure

```
blue-yellow/
├── pyproject.toml          # Poetry configuration and dependencies
├── poetry.lock             # Locked dependency versions
├── poetry.toml             # Local Poetry settings
├── README.md               # This file
├── SETUP.md               # Detailed setup instructions
├── LICENSE                # License information
├── .env                   # Environment variables (not tracked)
├── .env.sample            # Environment variable template
├── src/
│   ├── lambda/
│   │   ├── entrypoint.py  # AWS Lambda handler
│   │   └── README.md      # Lambda documentation
│   └── utils/
│       ├── ping.py        # URL ping utility
│       ├── cred.py        # Credential testing utility
│       ├── ddos.py        # Rate limit testing utility
│       └── clone.py       # Clone utility (placeholder)
└── test/
    └── test_lambda.py     # Lambda function tests
```

## Setup

See [`SETUP.md`](SETUP.md) for detailed setup instructions.

**Quick Start:**

```bash
# Install Poetry if not already installed
curl -sSL https://install.python-poetry.org | python3 -

# Install project dependencies
poetry install --no-root

# Activate the virtual environment
poetry shell

# Run Lambda tests
poetry run python test/test_lambda.py

# Test credential functionality
poetry run python src/utils/cred.py https://example.com/login

# Test rate limiting
poetry run python src/utils/ddos.py https://example.com 1.0
```

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
