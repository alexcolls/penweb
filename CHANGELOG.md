# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.3.0] - 2025-10-02

### Added
- **Git Submodule Integration**
  - Added `gps-cli` as git submodule for device location tracking
  - Added `vpn-cli` as git submodule for multi-provider VPN management
  - Added `email-cli` as git submodule for temporary email management
  - New `modules/` directory containing all CLI submodules
  - Integrated submodule CLIs into main menu as options 1, 2, and 3

- **Enhanced CLI Menu**
  - Expanded main menu from 4 to 7 tool options
  - Added GPS CLI tool (Option 1) - Device location tracker with multi-provider support
  - Added VPN CLI tool (Option 2) - Multi-provider VPN manager (ProtonVPN, Free VPN)
  - Added Email CLI tool (Option 3) - Temporary email address manager
  - Reorganized existing tools: Ping (4), Clone (5), DDoS (6), Login (7)
  - Added DEFENSIVE labels to GPS and VPN tools for clarity
  - Updated menu navigation to support 0-7 options

### Changed
- **Menu Structure**
  - Reordered tools with defensive tools (GPS, VPN, Email) listed first
  - Offensive tools (DDoS, Login) moved to end of menu
  - Updated color coding: Cyan for defensive tools, Green for utilities, Red for offensive
  - Improved menu descriptions for better clarity

- **Code Organization**
  - Added `subprocess` module import for external CLI execution
  - Implemented subprocess-based tool launchers for submodule CLIs
  - Enhanced error handling for missing submodules with helpful instructions
  - Added proper logging for submodule CLI launches and exits

### Technical Details
- Git submodules reference GitHub repositories:
  - `git@github.com:alexcolls/gps-cli.git`
  - `git@github.com:alexcolls/vpn-cli.git`
  - `git@github.com:alexcolls/email-cli.git`
- Submodules are executed in their respective directories with full interactivity
- Each tool includes validation to ensure submodules are initialized

## [0.2.0] - 2025-10-01

### Added
- **Automated Installation System**
  - Universal `install.sh` script for Linux and macOS
  - Two installation modes: Development Mode and User/System Mode
  - Auto-detection of OS (Linux/macOS) and shell (bash/zsh)
  - Automatic dependency installation (Python 3.9+, curl/wget, Poetry)
  - System-wide `penweb` command for User/System Mode
  - PATH configuration and shell RC file setup
  - Colored output, progress indicators, and detailed logging
  - `--force` flag for reinstallation
  - Support for virgin machines with no dependencies

### Changed
- **Complete Rebranding to PenWeb**
  - Updated ASCII art banner from "BLUE YELL" to "PENWEB"
  - Changed project name in `pyproject.toml` from "blue-yellow" to "penweb"
  - Updated all docstrings and code comments
  - Modified CLI goodbye message to "PenWeb"
  - Changed logging namespace from "blue-yellow" to "penweb"
  - Updated all references in README and documentation
- **Poetry Configuration**
  - Configured virtualenvs to be created in-project (`.venv`)
  - Updated `poetry.lock` with latest dependency resolutions
  - Aligns with `install.sh` expectations for consistent environment setup

### Fixed
- Installation process now works on virgin Linux and macOS machines
- Proper virtual environment isolation with in-project `.venv`

## [0.1.0] - 2025-10-01

### Added
- **Interactive CLI Application**
  - Beautiful ASCII art banner with legal warning
  - Interactive menu system with 4 pentesting tools
  - Authorization confirmation prompts for offensive tools
  - Colored terminal output with emojis
  - Graceful error handling and user input validation
  - `run.sh` convenience script for easy launching

- **Core Services**
  - URL Ping utility (`services/ping.py`) - Test URL availability and response times
  - Website Cloner (`services/clone.py`) - Download HTML, CSS, and JavaScript files
  - DDoS/Rate Limit Tester (`services/d2.py`) - Test rate limiting with repeated requests
  - Login Security Tester (`services/attempt_login.py`) - Test credential combinations and security mechanisms

- **AWS Lambda Integration**
  - Lambda function (`lambda/entrypoint.py`) for URL pinging via SQS
  - Batch processing support for SQS messages
  - Comprehensive error handling and logging
  - No external dependencies (uses Python standard library only)

- **Logging System**
  - Structured logging with `utils/logger.py`
  - Configurable file logging via `.env` (SAVE_LOGS)
  - Timestamped log files in `logs/` directory
  - Separate loggers for different components

- **Testing Infrastructure**
  - Unit tests for Lambda function
  - End-to-end tests for services
  - pytest configuration with coverage support
  - Test fixtures and mocks

- **Documentation**
  - Comprehensive `README.md` with usage examples
  - `docs/SETUP.md` - Detailed setup instructions
  - `docs/CLI_USAGE.md` - Interactive CLI usage guide
  - `docs/LOGGING.md` - Logging system documentation
  - `docs/LOGGING_SETUP.md` - Advanced logging configuration
  - `docs/LAMBDA.md` - AWS Lambda deployment guide

- **Development Tools**
  - Poetry for dependency management
  - Black for code formatting
  - Flake8 for linting
  - Mypy for type checking
  - pytest for testing with coverage reporting

- **Configuration**
  - `.env.sample` template for environment variables
  - `poetry.toml` for local Poetry settings
  - `.gitignore` for Python/Poetry projects

### Project Structure
```
penweb/
├── install.sh             # Automated installation script
├── run.sh                 # Convenience script to launch CLI
├── pyproject.toml         # Poetry configuration
├── poetry.lock            # Locked dependency versions
├── .env.sample            # Environment variable template
├── docs/                  # Comprehensive documentation
├── src/
│   ├── cli/               # Interactive CLI interface
│   ├── lambda/            # AWS Lambda function
│   ├── services/          # Core pentesting services
│   ├── utils/             # Helper utilities
│   └── main.py            # CLI entry point
└── test/                  # Test suite
```

### Dependencies
- **Runtime**
  - Python ^3.9
  - requests ^2.31.0 - HTTP library
  - beautifulsoup4 ^4.12.0 - HTML parsing
  - python-dotenv ^1.0.0 - Environment management

- **Development**
  - pytest ^7.4.0 - Testing framework
  - pytest-cov ^4.1.0 - Coverage reporting
  - black ^23.7.0 - Code formatting
  - flake8 ^6.1.0 - Linting
  - mypy ^1.5.0 - Type checking

### Security & Legal
- Added legal warning banner in CLI
- Authorization confirmation for offensive tools
- Comprehensive security notice in documentation
- Emphasis on authorized testing only

## [0.0.1] - 2025-09-30

### Added
- Initial project setup
- Basic repository structure
- Initial commit with foundational files

---

## Release Notes

### Version 0.3.0 Highlights
This release focuses on **tool expansion** and **git submodule integration**:
- Three new CLI tools integrated via git submodules: GPS, VPN, and Email
- Expanded menu from 4 to 7 total tools
- Better organization with defensive tools listed first
- Seamless integration with external CLI tools through submodules
- Enhanced menu navigation and user experience

### Version 0.2.0 Highlights
This release focuses on **ease of installation** and **professional branding**:
- One-command installation with `./install.sh` that works on any Linux or macOS system
- Complete rebranding to "PenWeb" with new ASCII art and consistent naming
- Enhanced documentation with installation guides
- Ready for both development and production deployment

### Version 0.1.0 Highlights
The initial feature release includes:
- Full-featured interactive CLI with 4 pentesting tools
- AWS Lambda integration for serverless URL monitoring
- Comprehensive logging system
- Professional documentation
- Complete testing infrastructure
- Ready for security testing and penetration testing workflows

---

## Upgrade Guide

### From 0.2.0 to 0.3.0

**For All Users:**
```bash
# Pull the latest changes
git pull origin main

# Initialize and update git submodules
git submodule update --init --recursive

# Continue using the CLI as normal
./run.sh
```

**New Features to Try:**
- Option 1: GPS CLI - Track device location using multiple providers (Traccar, OwnTracks, etc.)
- Option 2: VPN CLI - Manage VPN connections (ProtonVPN, Free VPN)
- Option 3: Email CLI - Create and manage temporary email addresses
- All tools are now better organized with defensive tools first

**Breaking Changes:**
- Menu option numbers have changed:
  - Ping: 1 → 4
  - Clone: 2 → 5
  - DDoS: 3 → 6
  - Login: 4 → 7

### From 0.1.0 to 0.2.0

**For Development Users:**
```bash
# Pull the latest changes
git pull origin main

# Run the new installer
./install.sh
# Select option 1 (Development Mode)
```

**For System/User Installation:**
```bash
# Pull the latest changes
git pull origin main

# Run the installer with force flag if already installed
./install.sh --force
# Select option 2 (User/System Mode)
```

**Breaking Changes:**
- None - This release is fully backward compatible

**New Features to Try:**
- Use the new `install.sh` for automated setup
- Enjoy the new "PenWeb" branding with updated ASCII art
- Benefit from in-project `.venv` for better isolation

---

## Contributing

When contributing to this project, please:
1. Update the `[Unreleased]` section with your changes
2. Follow the established format (Added, Changed, Deprecated, Removed, Fixed, Security)
3. Include relevant issue/PR numbers
4. Group changes by category
5. Write clear, concise descriptions

---

## Links

- [Repository](https://github.com/yourusername/penweb)
- [Issue Tracker](https://github.com/yourusername/penweb/issues)
- [Documentation](./docs/)

[Unreleased]: https://github.com/yourusername/penweb/compare/v0.3.0...HEAD
[0.3.0]: https://github.com/yourusername/penweb/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/yourusername/penweb/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/yourusername/penweb/compare/v0.0.1...v0.1.0
[0.0.1]: https://github.com/yourusername/penweb/releases/tag/v0.0.1
