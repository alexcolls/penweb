#!/bin/bash
# PenWeb Installation Script
# Supports Linux and macOS with automatic dependency installation
# Offers Development Mode and User/System Mode installations

set -e  # Exit on error

# ============================================================================
# Color definitions for output formatting
# ============================================================================
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
BOLD='\033[1m'
RESET='\033[0m'

# ============================================================================
# Global variables
# ============================================================================
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OS_TYPE=""
SHELL_TYPE=""
SHELL_CONFIG=""
PYTHON_CMD=""
DOWNLOAD_CMD=""
INSTALL_DIR="$HOME/.local/share/penweb"
BIN_DIR="$HOME/.local/bin"
WRAPPER_SCRIPT="$BIN_DIR/penweb"
LOG_FILE="/tmp/penweb_install.log"
FORCE_INSTALL=false

# ============================================================================
# Utility Functions
# ============================================================================

print_header() {
    echo -e "${CYAN}${BOLD}"
    echo "╔════════════════════════════════════════════════════════════════════╗"
    echo "║                    PenWeb Installation Script                      ║"
    echo "║              Security Testing Utilities & Tools                    ║"
    echo "╚════════════════════════════════════════════════════════════════════╝"
    echo -e "${RESET}"
}

print_status() {
    local status=$1
    local message=$2
    
    case $status in
        "success")
            echo -e "${GREEN}✓${RESET} $message"
            ;;
        "error")
            echo -e "${RED}✗${RESET} $message"
            ;;
        "info")
            echo -e "${BLUE}ℹ${RESET} $message"
            ;;
        "warning")
            echo -e "${YELLOW}⚠${RESET} $message"
            ;;
        "progress")
            echo -e "${CYAN}→${RESET} $message"
            ;;
    esac
}

log_message() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}

handle_error() {
    local message=$1
    print_status "error" "$message"
    log_message "ERROR: $message"
    echo -e "\n${YELLOW}Check log file for details: $LOG_FILE${RESET}"
    exit 1
}

# ============================================================================
# Detection Functions
# ============================================================================

detect_os() {
    print_status "progress" "Detecting operating system..."
    
    case "$(uname -s)" in
        Linux*)
            OS_TYPE="Linux"
            print_status "success" "Detected: Linux"
            ;;
        Darwin*)
            OS_TYPE="macOS"
            print_status "success" "Detected: macOS"
            ;;
        *)
            handle_error "Unsupported operating system: $(uname -s)"
            ;;
    esac
    
    log_message "Detected OS: $OS_TYPE"
}

detect_shell() {
    print_status "progress" "Detecting shell environment..."
    
    if [ -n "$ZSH_VERSION" ]; then
        SHELL_TYPE="zsh"
    elif [ -n "$BASH_VERSION" ]; then
        SHELL_TYPE="bash"
    else
        # Fallback to $SHELL variable
        case "$SHELL" in
            */zsh)
                SHELL_TYPE="zsh"
                ;;
            */bash)
                SHELL_TYPE="bash"
                ;;
            *)
                SHELL_TYPE="bash"  # Default to bash
                ;;
        esac
    fi
    
    print_status "success" "Detected shell: $SHELL_TYPE"
    log_message "Detected shell: $SHELL_TYPE"
}

detect_shell_config() {
    print_status "progress" "Locating shell configuration file..."
    
    # Priority order for config files
    if [ "$SHELL_TYPE" = "zsh" ]; then
        if [ -f "$HOME/.zshrc" ]; then
            SHELL_CONFIG="$HOME/.zshrc"
        elif [ "$OS_TYPE" = "macOS" ] && [ -f "$HOME/.zprofile" ]; then
            SHELL_CONFIG="$HOME/.zprofile"
        else
            SHELL_CONFIG="$HOME/.zshrc"  # Will be created
        fi
    else  # bash
        if [ -f "$HOME/.bashrc" ]; then
            SHELL_CONFIG="$HOME/.bashrc"
        elif [ -f "$HOME/.bash_profile" ]; then
            SHELL_CONFIG="$HOME/.bash_profile"
        elif [ "$OS_TYPE" = "macOS" ]; then
            SHELL_CONFIG="$HOME/.bash_profile"  # macOS preference
        else
            SHELL_CONFIG="$HOME/.bashrc"  # Linux preference
        fi
    fi
    
    print_status "success" "Shell config: $SHELL_CONFIG"
    log_message "Shell config file: $SHELL_CONFIG"
}

# ============================================================================
# Dependency Checking Functions
# ============================================================================

check_command() {
    command -v "$1" >/dev/null 2>&1
}

check_python() {
    print_status "progress" "Checking Python installation..."
    
    # Try python3 first, then python
    for cmd in python3 python; do
        if check_command "$cmd"; then
            local version=$($cmd --version 2>&1 | grep -oE '[0-9]+\.[0-9]+' | head -1)
            local major=$(echo "$version" | cut -d. -f1)
            local minor=$(echo "$version" | cut -d. -f2)
            
            if [ "$major" -eq 3 ] && [ "$minor" -ge 9 ]; then
                PYTHON_CMD="$cmd"
                print_status "success" "Found Python $version ($cmd)"
                log_message "Python found: $cmd (version $version)"
                return 0
            fi
        fi
    done
    
    print_status "error" "Python 3.9+ not found"
    log_message "Python 3.9+ not found"
    return 1
}

check_curl_wget() {
    print_status "progress" "Checking download tools (curl/wget)..."
    
    if check_command curl; then
        DOWNLOAD_CMD="curl"
        print_status "success" "Found curl"
        log_message "Download tool: curl"
        return 0
    elif check_command wget; then
        DOWNLOAD_CMD="wget"
        print_status "success" "Found wget"
        log_message "Download tool: wget"
        return 0
    else
        print_status "error" "Neither curl nor wget found"
        log_message "Neither curl nor wget found"
        return 1
    fi
}

check_poetry() {
    print_status "progress" "Checking Poetry installation..."
    
    if check_command poetry; then
        local version=$(poetry --version 2>&1 | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' | head -1)
        print_status "success" "Found Poetry $version"
        log_message "Poetry found: version $version"
        return 0
    else
        print_status "warning" "Poetry not found"
        log_message "Poetry not found"
        return 1
    fi
}

# ============================================================================
# Dependency Installation Functions
# ============================================================================

install_python() {
    print_status "info" "Python 3.9+ is required but not found."
    echo ""
    
    if [ "$OS_TYPE" = "Linux" ]; then
        echo -e "${YELLOW}To install Python on Linux, try one of these commands:${RESET}"
        echo "  • Debian/Ubuntu/Kali: sudo apt-get update && sudo apt-get install python3 python3-pip python3-venv"
        echo "  • Fedora/RHEL/CentOS: sudo dnf install python3 python3-pip"
        echo "  • Arch Linux: sudo pacman -S python python-pip"
    else
        echo -e "${YELLOW}To install Python on macOS:${RESET}"
        echo "  • Using Homebrew: brew install python@3.11"
        echo "  • Or download from: https://www.python.org/downloads/"
    fi
    
    echo ""
    read -p "Would you like to try installing Python automatically? [y/N] " -n 1 -r
    echo
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        if [ "$OS_TYPE" = "Linux" ]; then
            if check_command apt-get; then
                sudo apt-get update && sudo apt-get install -y python3 python3-pip python3-venv
            elif check_command dnf; then
                sudo dnf install -y python3 python3-pip
            elif check_command pacman; then
                sudo pacman -S --noconfirm python python-pip
            else
                handle_error "Could not detect package manager. Please install Python manually."
            fi
        else
            if check_command brew; then
                brew install python@3.11
            else
                handle_error "Homebrew not found. Please install Python manually from https://www.python.org/"
            fi
        fi
        
        # Verify installation
        if check_python; then
            print_status "success" "Python installed successfully"
        else
            handle_error "Python installation failed"
        fi
    else
        handle_error "Python is required to continue. Please install it and run this script again."
    fi
}

install_curl_wget() {
    print_status "info" "curl or wget is required for downloading Poetry installer."
    echo ""
    
    if [ "$OS_TYPE" = "Linux" ]; then
        if check_command apt-get; then
            sudo apt-get update && sudo apt-get install -y curl
        elif check_command dnf; then
            sudo dnf install -y curl
        elif check_command pacman; then
            sudo pacman -S --noconfirm curl
        else
            handle_error "Could not install curl. Please install it manually."
        fi
    else
        # macOS should have curl by default, but try installing anyway
        if check_command brew; then
            brew install curl
        else
            handle_error "Please install curl manually."
        fi
    fi
    
    # Verify installation
    if check_curl_wget; then
        print_status "success" "Download tool installed successfully"
    else
        handle_error "Failed to install curl/wget"
    fi
}

install_poetry() {
    print_status "progress" "Installing Poetry..."
    log_message "Starting Poetry installation"
    
    # Ensure we have a download tool
    if [ -z "$DOWNLOAD_CMD" ]; then
        if ! check_curl_wget; then
            install_curl_wget
        fi
    fi
    
    # Download and run Poetry installer
    if [ "$DOWNLOAD_CMD" = "curl" ]; then
        curl -sSL https://install.python-poetry.org | $PYTHON_CMD -
    else
        wget -qO- https://install.python-poetry.org | $PYTHON_CMD -
    fi
    
    # Add Poetry to PATH for current session
    export PATH="$HOME/.local/bin:$PATH"
    
    # Verify installation
    if check_poetry; then
        print_status "success" "Poetry installed successfully"
        log_message "Poetry installation successful"
    else
        print_status "warning" "Poetry installed but not in PATH"
        print_status "info" "Adding Poetry to shell configuration..."
        
        # Add to shell config
        if ! grep -q ".local/bin" "$SHELL_CONFIG" 2>/dev/null; then
            echo "" >> "$SHELL_CONFIG"
            echo "# Added by PenWeb installer" >> "$SHELL_CONFIG"
            echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$SHELL_CONFIG"
            print_status "success" "Added Poetry to $SHELL_CONFIG"
        fi
        
        # Try checking again
        if check_command "$HOME/.local/bin/poetry"; then
            print_status "success" "Poetry is now available"
        else
            handle_error "Poetry installation failed. Please install manually from https://python-poetry.org/"
        fi
    fi
}

# ============================================================================
# Installation Functions
# ============================================================================

install_development_mode() {
    echo ""
    echo -e "${BOLD}${BLUE}═══════════════════════════════════════════════════════════════${RESET}"
    echo -e "${BOLD}${BLUE}  Development Mode Installation${RESET}"
    echo -e "${BOLD}${BLUE}═══════════════════════════════════════════════════════════════${RESET}"
    echo ""
    
    # Verify we're in the project directory
    if [ ! -f "$SCRIPT_DIR/pyproject.toml" ]; then
        handle_error "pyproject.toml not found. Please run this script from the penweb directory."
    fi
    
    cd "$SCRIPT_DIR"
    
    # Install dependencies with Poetry
    print_status "progress" "Installing project dependencies with Poetry..."
    log_message "Running poetry install in development mode"
    
    if poetry install --no-root; then
        print_status "success" "Dependencies installed successfully"
        log_message "Poetry dependencies installed"
    else
        handle_error "Failed to install dependencies with Poetry"
    fi
    
    # Create .env from .env.sample if it doesn't exist
    if [ ! -f "$SCRIPT_DIR/.env" ] && [ -f "$SCRIPT_DIR/.env.sample" ]; then
        print_status "progress" "Creating .env file from .env.sample..."
        cp "$SCRIPT_DIR/.env.sample" "$SCRIPT_DIR/.env"
        print_status "success" "Created .env file"
        log_message "Created .env file"
    fi
    
    # Verify installation by checking if main.py exists and Poetry environment is set up
    print_status "progress" "Verifying installation..."
    if [ -f "$SCRIPT_DIR/src/main.py" ] && poetry env info >/dev/null 2>&1; then
        print_status "success" "Installation verified"
        log_message "Development installation verified"
    else
        print_status "warning" "Could not fully verify installation"
    fi
    
    # Success message
    echo ""
    echo -e "${GREEN}${BOLD}✓ Development Mode Installation Complete!${RESET}"
    echo ""
    echo -e "${BOLD}Next steps:${RESET}"
    echo -e "  1. Review and customize ${CYAN}.env${RESET} file if needed"
    echo -e "  2. Run the application:"
    echo -e "     ${YELLOW}./run.sh${RESET}"
    echo -e "     or"
    echo -e "     ${YELLOW}poetry run python src/main.py${RESET}"
    echo ""
    echo -e "${BOLD}Development commands:${RESET}"
    echo -e "  • Activate virtual environment: ${YELLOW}poetry shell${RESET}"
    echo -e "  • Run tests: ${YELLOW}poetry run pytest test/${RESET}"
    echo -e "  • Format code: ${YELLOW}poetry run black src/${RESET}"
    echo -e "  • Lint code: ${YELLOW}poetry run flake8 src/${RESET}"
    echo ""
    
    log_message "Development mode installation completed successfully"
}

install_user_mode() {
    echo ""
    echo -e "${BOLD}${MAGENTA}═══════════════════════════════════════════════════════════════${RESET}"
    echo -e "${BOLD}${MAGENTA}  User/System Mode Installation${RESET}"
    echo -e "${BOLD}${MAGENTA}═══════════════════════════════════════════════════════════════${RESET}"
    echo ""
    
    # Check if already installed
    if [ -d "$INSTALL_DIR" ] && [ "$FORCE_INSTALL" = false ]; then
        print_status "warning" "PenWeb is already installed at $INSTALL_DIR"
        echo ""
        read -p "Do you want to reinstall? This will overwrite the existing installation. [y/N] " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            print_status "info" "Installation cancelled"
            exit 0
        fi
        print_status "progress" "Removing existing installation..."
        rm -rf "$INSTALL_DIR"
    fi
    
    # Create installation directory
    print_status "progress" "Creating installation directory at $INSTALL_DIR..."
    mkdir -p "$INSTALL_DIR"
    log_message "Created installation directory: $INSTALL_DIR"
    
    # Copy project files
    print_status "progress" "Copying project files..."
    cp -r "$SCRIPT_DIR/src" "$INSTALL_DIR/"
    cp "$SCRIPT_DIR/pyproject.toml" "$INSTALL_DIR/"
    cp "$SCRIPT_DIR/poetry.lock" "$INSTALL_DIR/"
    cp "$SCRIPT_DIR/poetry.toml" "$INSTALL_DIR/"
    
    if [ -f "$SCRIPT_DIR/.env.sample" ]; then
        cp "$SCRIPT_DIR/.env.sample" "$INSTALL_DIR/"
    fi
    
    print_status "success" "Project files copied"
    log_message "Project files copied to installation directory"
    
    # Install dependencies in the new location
    print_status "progress" "Installing dependencies in $INSTALL_DIR..."
    cd "$INSTALL_DIR"
    
    if poetry install --no-root; then
        print_status "success" "Dependencies installed"
        log_message "Dependencies installed in user mode"
    else
        handle_error "Failed to install dependencies"
    fi
    
    # Create .env from .env.sample
    if [ ! -f "$INSTALL_DIR/.env" ] && [ -f "$INSTALL_DIR/.env.sample" ]; then
        cp "$INSTALL_DIR/.env.sample" "$INSTALL_DIR/.env"
        print_status "success" "Created .env file"
        log_message "Created .env file in installation directory"
    fi
    
    # Create bin directory
    mkdir -p "$BIN_DIR"
    
    # Generate wrapper script
    print_status "progress" "Creating executable wrapper at $WRAPPER_SCRIPT..."
    generate_wrapper_script
    
    # Add to PATH if needed
    add_to_path
    
    # Verify installation by checking if files exist and wrapper is executable
    print_status "progress" "Verifying installation..."
    if [ -f "$INSTALL_DIR/src/main.py" ] && [ -x "$WRAPPER_SCRIPT" ] && poetry env info >/dev/null 2>&1; then
        print_status "success" "Installation verified"
        log_message "User mode installation verified"
    else
        print_status "warning" "Could not fully verify installation"
    fi
    
    # Success message
    echo ""
    echo -e "${GREEN}${BOLD}✓ User/System Mode Installation Complete!${RESET}"
    echo ""
    echo -e "${BOLD}Installation location:${RESET} ${CYAN}$INSTALL_DIR${RESET}"
    echo -e "${BOLD}Executable:${RESET} ${CYAN}$WRAPPER_SCRIPT${RESET}"
    echo ""
    echo -e "${BOLD}Next steps:${RESET}"
    
    if ! echo "$PATH" | grep -q "$BIN_DIR"; then
        echo -e "  1. ${YELLOW}Restart your terminal${RESET} or run: ${CYAN}source $SHELL_CONFIG${RESET}"
        echo -e "  2. Run the application: ${YELLOW}penweb${RESET}"
    else
        echo -e "  • Run the application: ${YELLOW}penweb${RESET}"
    fi
    
    echo ""
    echo -e "${BOLD}Configuration:${RESET}"
    echo -e "  • Edit ${CYAN}$INSTALL_DIR/.env${RESET} to customize settings"
    echo ""
    
    log_message "User mode installation completed successfully"
}

generate_wrapper_script() {
    cat > "$WRAPPER_SCRIPT" << 'EOF'
#!/bin/bash
# PenWeb CLI Wrapper Script
# Automatically generated by install.sh

INSTALL_DIR="$HOME/.local/share/penweb"

# Check if installation exists
if [ ! -d "$INSTALL_DIR" ]; then
    echo "Error: PenWeb installation not found at $INSTALL_DIR"
    echo "Please run the installer again."
    exit 1
fi

# Activate virtual environment and run the CLI
if [ -f "$INSTALL_DIR/.venv/bin/activate" ]; then
    source "$INSTALL_DIR/.venv/bin/activate"
    python "$INSTALL_DIR/src/main.py" "$@"
else
    # Fallback: use Poetry to run
    cd "$INSTALL_DIR" && poetry run python "$INSTALL_DIR/src/main.py" "$@"
fi
EOF
    
    chmod +x "$WRAPPER_SCRIPT"
    print_status "success" "Wrapper script created and made executable"
    log_message "Created wrapper script: $WRAPPER_SCRIPT"
}

add_to_path() {
    print_status "progress" "Checking PATH configuration..."
    
    # Check if $BIN_DIR is already in PATH
    if echo "$PATH" | grep -q "$BIN_DIR"; then
        print_status "success" "$BIN_DIR is already in PATH"
        log_message "$BIN_DIR already in PATH"
        return 0
    fi
    
    # Check if it's already in the shell config
    if [ -f "$SHELL_CONFIG" ] && grep -q "$BIN_DIR" "$SHELL_CONFIG"; then
        print_status "success" "$BIN_DIR is configured in $SHELL_CONFIG"
        log_message "$BIN_DIR already configured in shell config"
        return 0
    fi
    
    # Add to shell config
    print_status "progress" "Adding $BIN_DIR to PATH in $SHELL_CONFIG..."
    
    # Backup shell config
    if [ -f "$SHELL_CONFIG" ]; then
        cp "$SHELL_CONFIG" "${SHELL_CONFIG}.backup.$(date +%Y%m%d_%H%M%S)"
        print_status "info" "Backed up shell config"
    fi
    
    # Add to config file
    {
        echo ""
        echo "# Added by PenWeb installer on $(date)"
        echo 'export PATH="$HOME/.local/bin:$PATH"'
    } >> "$SHELL_CONFIG"
    
    print_status "success" "Added to PATH in $SHELL_CONFIG"
    log_message "Added $BIN_DIR to PATH in $SHELL_CONFIG"
    
    # Update current session
    export PATH="$BIN_DIR:$PATH"
}

# ============================================================================
# Menu System
# ============================================================================

show_menu() {
    echo ""
    echo -e "${BOLD}${CYAN}Please select an installation mode:${RESET}"
    echo ""
    echo -e "  ${BOLD}1)${RESET} ${GREEN}Development Mode${RESET}"
    echo -e "     Install for local development in the current directory"
    echo -e "     Creates .venv and installs dependencies with Poetry"
    echo -e "     Use ${YELLOW}./run.sh${RESET} or ${YELLOW}poetry run python src/main.py${RESET}"
    echo ""
    echo -e "  ${BOLD}2)${RESET} ${MAGENTA}User/System Mode${RESET}"
    echo -e "     Install as a system-wide CLI tool"
    echo -e "     Installs to ${CYAN}~/.local/share/penweb${RESET}"
    echo -e "     Creates ${YELLOW}penweb${RESET} command available system-wide"
    echo ""
    echo -e "  ${BOLD}3)${RESET} ${RED}Exit${RESET}"
    echo ""
}

# ============================================================================
# Main Installation Flow
# ============================================================================

main() {
    # Initialize log file
    echo "PenWeb Installation Log - $(date)" > "$LOG_FILE"
    log_message "Installation started"
    
    # Print header
    clear
    print_header
    
    # Detect environment
    detect_os
    detect_shell
    detect_shell_config
    
    echo ""
    print_status "info" "Environment detected: $OS_TYPE with $SHELL_TYPE"
    echo ""
    
    # Check dependencies
    echo -e "${BOLD}Checking dependencies...${RESET}"
    echo ""
    
    # Check Python
    if ! check_python; then
        install_python
    fi
    
    # Check curl/wget
    if ! check_curl_wget; then
        install_curl_wget
    fi
    
    # Check Poetry
    if ! check_poetry; then
        echo ""
        print_status "info" "Poetry is required for managing Python dependencies"
        read -p "Would you like to install Poetry now? [Y/n] " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Nn]$ ]]; then
            install_poetry
        else
            handle_error "Poetry is required to continue. Please install it from https://python-poetry.org/"
        fi
    fi
    
    echo ""
    print_status "success" "All dependencies are satisfied"
    echo ""
    
    # Show menu and get selection
    while true; do
        show_menu
        read -p "Enter your choice [1-3]: " choice
        
        case $choice in
            1)
                install_development_mode
                break
                ;;
            2)
                install_user_mode
                break
                ;;
            3)
                print_status "info" "Installation cancelled by user"
                log_message "Installation cancelled by user"
                exit 0
                ;;
            *)
                print_status "error" "Invalid choice. Please enter 1, 2, or 3."
                echo ""
                ;;
        esac
    done
    
    echo -e "${GREEN}${BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RESET}"
    echo -e "${GREEN}${BOLD}  Installation log saved to: $LOG_FILE${RESET}"
    echo -e "${GREEN}${BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RESET}"
    echo ""
    
    log_message "Installation completed successfully"
}

# ============================================================================
# Script Entry Point
# ============================================================================

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --force|-f)
            FORCE_INSTALL=true
            shift
            ;;
        --help|-h)
            print_header
            echo "Usage: $0 [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --force, -f    Force reinstallation even if already installed"
            echo "  --help, -h     Show this help message"
            echo ""
            echo "This script will guide you through installing PenWeb in either:"
            echo "  • Development Mode: For local development with Poetry"
            echo "  • User/System Mode: As a system-wide CLI tool"
            echo ""
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

# Run main installation
main
