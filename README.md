# 💻 Penweb CLI

A comprehensive security testing toolkit with integrated CLI utilities for penetration testing, privacy tools, and AWS Lambda functions for URL monitoring.

## Overview

This repository contains a unified collection of tools designed for security testing, penetration testing, privacy protection, and monitoring. It includes:
- **3 Integrated CLI Tools** (GPS tracking, VPN management, temporary email)
- **4 Core Security Testing Utilities** (URL ping, website cloning, rate limit testing, login testing)
- **AWS Lambda function** for serverless URL health checks

**NEW in v0.3.1:** 🎉 **Zero-Config Free Defaults** - All CLI tools now work immediately after installation with FREE options requiring NO account or signup! GPS uses free Traccar demo server, VPN uses free VPNGate servers, Email uses free 1secmail API.

**NEW in v0.3.0:** 🚀 **Expanded CLI with 7 Tools** - Three new defensive tools (GPS, VPN, Email) integrated via git submodules, plus reorganized menu with better tool categorization!

## Components

### 🛠️ GPS CLI - Device Location Tracker (`modules/gps-cli/`)

**NEW!** Multi-provider GPS tracking CLI that supports various tracking services.

**🆓 FREE Default:** Uses Traccar demo server (`https://demo2.traccar.org`) with IP-based geolocation - **NO account or GPS hardware required!**

**Features:**
- Multiple provider support: Traccar, OwnTracks, PhoneTrack, GPSLogger
- IP-based geolocation fallback (city-level accuracy)
- Real-time location tracking
- GPS hardware detection (optional)
- Session management and history
- Privacy-focused options
- **Works immediately after installation - zero configuration!**

**Providers:**
- **Traccar**: Free demo server (DEFAULT) or self-hosted option
- **OwnTracks**: Self-hosted MQTT/HTTP with encryption
- **PhoneTrack**: Nextcloud-based tracking
- **GPSLogger**: Custom HTTP endpoint support

**Usage:**
```bash
./run.sh  # Then select option 1 - GPS
```

**Use Cases:**
- Device location tracking and monitoring
- Fleet management
- Personal location history
- Emergency location services

### 🔐 VPN CLI - Multi-Provider VPN Manager (`modules/vpn-cli/`)

**NEW!** Unified VPN management CLI supporting multiple VPN providers.

**🆓 FREE Default:** Uses VPNGate public servers - **NO account or signup required!**

**Features:**
- Free VPN support via VPNGate (no account needed) - **DEFAULT**
- ProtonVPN integration (requires account for premium features)
- Multiple country selection (US, UK, JP, DE, FR, CA, AU, NL, KR, etc.)
- Connection history tracking
- Public IP and geolocation display
- Quick connect/disconnect
- **Works immediately after installation - zero configuration!**

**Usage:**
```bash
./run.sh  # Then select option 2 - VPN
```

**Providers:**
- **ProtonVPN**: Secure, trusted VPN (free tier: 3 countries)
- **Free VPN**: Completely free via VPNGate public servers

**Use Cases:**
- Privacy protection and anonymity
- Geo-restriction bypass
- Secure public WiFi usage
- Testing from different geographic locations

### 📧 Email CLI - Temporary Email Manager (`modules/email-cli/`)

**NEW!** Temporary email address manager for privacy and testing.

**🆓 FREE Default:** Uses 1secmail.com API - **NO account or signup required!**

**Features:**
- Create temporary email addresses instantly - **completely FREE**
- Receive emails immediately with no configuration
- No registration or signup required
- Multiple email management
- Inbox checking and message reading
- Custom or random email names
- Email history tracking
- **Optional:** SMTP configuration only needed for sending emails
- **Works immediately after installation - zero configuration!**

**Usage:**
```bash
./run.sh  # Then select option 3 - Email
```

**Use Cases:**
- Privacy protection for online registrations
- Testing email workflows
- Avoiding spam
- Temporary communications
- Security testing of email systems

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
./run.sh  # Then select option 7 - Login

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
./run.sh  # Then select option 6 - DDoS

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
./run.sh  # Then select option 5 - Clone

# Or directly
poetry run python src/services/clone.py https://example.com output_dir
```

## Project Structure

```
penweb/
├── install.sh             # Automated installation script (Linux/macOS)
├── run.sh                 # Convenience script to launch CLI
├── pyproject.toml          # Poetry configuration and dependencies
├── poetry.lock             # Locked dependency versions
├── poetry.toml             # Local Poetry settings
├── README.md               # This file
├── CHANGELOG.md           # Version history and release notes
├── LICENSE                # License information
├── .env                   # Environment variables (not tracked)
├── .env.sample            # Environment variable template
├── .gitmodules            # Git submodule configuration
├── docs/
│   ├── SETUP.md           # Detailed setup instructions
│   ├── CLI_USAGE.md       # Interactive CLI usage guide
│   └── LOGGING.md         # Logging system documentation
├── modules/               # Git submodules for external CLI tools
│   ├── gps-cli/           # GPS tracking CLI (submodule)
│   ├── vpn-cli/           # VPN management CLI (submodule)
│   └── email-cli/         # Temporary email CLI (submodule)
├── src/
│   ├── cli/               # Interactive CLI interface
│   │   ├── banner.py      # ASCII art and branding
│   │   └── menu.py        # Interactive menu system (7 tools)
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

## 🚀 Quick Start (Zero-Config!)

**Get started in 3 commands - all tools work immediately with FREE defaults:**

```bash
# 1. Clone and enter the repository
git clone https://github.com/alexcolls/penweb.git && cd penweb

# 2. Initialize submodules and run automated installer
git submodule update --init --recursive && ./install.sh

# 3. Launch the CLI (select Development Mode during install)
./run.sh
```

**That's it!** All 7 tools are ready to use:
- 🛠️ **GPS**: Free Traccar demo server (no account, no GPS hardware)
- 🔐 **VPN**: Free VPNGate servers (no account)
- 📧 **Email**: Free 1secmail API (no account)
- Plus 4 security testing utilities ready to go!

---

## Setup

### 🚀 Automated Installation (Recommended)

The easiest way to get started is using our automated installer that handles all dependencies:

```bash
# Clone the repository
git clone https://github.com/alexcolls/penweb.git
cd penweb

# Initialize git submodules (REQUIRED for GPS, VPN, Email tools)
git submodule update --init --recursive

# Run the installer
./install.sh
```

The installer will:
- ✅ Detect your OS (Linux/macOS) and shell (bash/zsh)
- ✅ Install all required dependencies (Python 3.9+, Poetry, etc.)
- ✅ Initialize and configure git submodules (GPS, VPN, Email)
- ✅ **Automatically copy configuration templates to `~/.config/`**
  - GPS-CLI: `~/.config/gps-cli/.env.sample`
  - Email-CLI: `~/.config/tempmail/.env.sample`
  - VPN-CLI: `~/.config/vpn-cli/` (auto-generated on first run)
- ✅ Offer two installation modes:
  - **Development Mode**: Install in current directory with `.venv` for development
  - **User/System Mode**: Install to `~/.local/share/penweb` with system-wide `penweb` command
- ✅ Configure environment files automatically
- ✅ **All tools work immediately with FREE defaults - zero manual config!**
- ✅ Works on virgin Linux and macOS machines

**Installation Modes:**

1. **Development Mode** - For contributors and developers:
   ```bash
   ./install.sh  # Select option 1
   ./run.sh      # Run the application
   ```

2. **User/System Mode** - For end-users:
   ```bash
   ./install.sh  # Select option 2
   penweb        # Run from anywhere (after restarting terminal)
   ```

### 📖 Manual Installation

See [`docs/SETUP.md`](docs/SETUP.md) for detailed manual setup instructions.

**Quick Start (Manual):**

```bash
# Clone the repository
git clone https://github.com/alexcolls/penweb.git
cd penweb

# Initialize git submodules (REQUIRED)
git submodule update --init --recursive

# Install Poetry if not already installed
curl -sSL https://install.python-poetry.org | python3 -

# Install project dependencies
poetry install --no-root

# 🚀 Launch the Interactive CLI
./run.sh
# or
poetry run python src/main.py

# Alternative: Run tools directly
poetry run python test/test_lambda.py  # Lambda tests
```

### 🎨 Interactive CLI

The easiest way to use PenWeb is through the **interactive CLI**:

```bash
./run.sh
```

**Menu Options:**
- **[1] 🛰️ GPS (DEFENSIVE)** - Device location tracker with multi-provider support
- **[2] 🔐 VPN (DEFENSIVE)** - Multi-provider VPN manager (ProtonVPN, Free VPN)
- **[3] 📧 Email** - Temporary email address manager
- **[4] 🌐 Ping** - Test URL availability and response time
- **[5] 📋 Clone** - Download website HTML, CSS, and JS files
- **[6] 💥 DDoS (OFFENSIVE)** - Test rate limiting with repeated requests
- **[7] 🔐 Login (OFFENSIVE)** - Test login security with credentials
- **[0] 🚪 Exit** - Quit the application

Features:
- 🎨 Beautiful ASCII art banner
- 📋 Interactive menu with 7 integrated tools
- ⚖️ Built-in legal warnings and authorization checks
- 🎯 Guided workflows for each tool
- 🔵 Defensive tools (GPS, VPN, Email) listed first
- 🔴 Clear marking of offensive tools (DDoS, Login)
- ⌨️ Graceful error handling and keyboard interrupt support

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

- 📖 **[Setup Guide](docs/CLI_SETUP.md)** - Installation and configuration instructions
- 🎨 **[CLI Usage Guide](docs/CLI_USAGE.md)** - Interactive CLI documentation and examples
- 📝 **[Logging Guide](docs/LOGGING.md)** - Logging system overview and usage
- ⚙️  **[Logging Setup](docs/LOGGING_SETUP.md)** - Advanced logging configuration
- 🚀 **[Lambda Deployment](docs/LAMBDA.md)** - AWS Lambda deployment guide

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

### Privacy & Security Tools
- **GPS Tracking**: Device location monitoring and fleet management
- **VPN Management**: Privacy protection, geo-restriction bypass, secure browsing
- **Temporary Email**: Privacy protection, testing, spam avoidance

### Security Testing
- **DevOps**: Monitor website availability and response times
- **Security Testing**: Test rate limiting and authentication mechanisms
- **Penetration Testing**: Validate security controls and identify vulnerabilities
- **Compliance**: Verify security requirements are met
- **Quality Assurance**: Automated endpoint testing
- **Web Application Testing**: Clone and analyze website structure

## Contributing

Contributions are welcome! Please ensure:
1. All tests pass
2. Code is formatted with `black`
3. No linting errors from `flake8`
4. Type hints are used where appropriate
5. Security best practices are followed

## License

See [LICENSE](LICENSE) file for details.
