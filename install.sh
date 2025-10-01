#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

# Penweb installer: bootstraps dependencies and sets up either
# - In-repo install using Poetry (.venv next to the project)
# - User-local install that copies the project to ~/.local/share/penweb and adds a `penweb` command
# Supports Linux (apt, dnf, yum, pacman, zypper, apk) and macOS (Homebrew)

REPO_DIR=$(cd "$(dirname "$0")" && pwd -P)
OS=$(uname -s)
EUID_REQ=${EUID:-$(id -u)}

# Colors
c_green="\033[0;32m"; c_yellow="\033[0;33m"; c_red="\033[0;31m"; c_reset="\033[0m"

log() { echo -e "${c_green}[penweb]${c_reset} $*"; }
warn() { echo -e "${c_yellow}[penweb] WARN:${c_reset} $*" >&2; }
die() { echo -e "${c_red}[penweb] ERROR:${c_reset} $*" >&2; exit 1; }

have_cmd() { command -v "$1" >/dev/null 2>&1; }

need_sudo() {
  if [ "$EUID_REQ" -ne 0 ]; then echo sudo; else echo; fi
}

PM=""
detect_pm() {
  case "$OS" in
    Darwin)
      PM="brew" ;;
    Linux)
      if have_cmd apt-get; then PM="apt"; elif have_cmd apt; then PM="apt";
      elif have_cmd dnf; then PM="dnf"; elif have_cmd yum; then PM="yum";
      elif have_cmd pacman; then PM="pacman"; elif have_cmd zypper; then PM="zypper";
      elif have_cmd apk; then PM="apk"; else PM=""; fi ;;
    *) PM="" ;;
  esac
}

install_pkgs() {
  # Args: packages...
  local pkgs=("$@")
  local SUDO
  SUDO=$(need_sudo)
  case "$PM" in
    apt)
      $SUDO apt-get update -y
      # Map common names
      $SUDO apt-get install -y "${pkgs[@]}" || true
      ;;
    dnf)
      $SUDO dnf install -y "${pkgs[@]}" || true
      ;;
    yum)
      $SUDO yum install -y "${pkgs[@]}" || true
      ;;
    pacman)
      $SUDO pacman -Sy --noconfirm "${pkgs[@]}" || true
      ;;
    zypper)
      $SUDO zypper --non-interactive install -y "${pkgs[@]}" || true
      ;;
    apk)
      $SUDO apk add --no-cache "${pkgs[@]}" || true
      ;;
    brew)
      brew update || true
      for p in "${pkgs[@]}"; do brew install "$p" || brew upgrade "$p" || true; done
      ;;
    *)
      warn "Unknown package manager. Please install: ${pkgs[*]} manually."
      ;;
  esac
}

ensure_homebrew() {
  if [ "$PM" = "brew" ] && ! have_cmd brew; then
    warn "Homebrew not found. Installing Homebrew (may prompt for password)."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)" || die "Homebrew install failed"
    eval "$([ -f /opt/homebrew/bin/brew ] && echo 'eval \"$(/opt/homebrew/bin/brew shellenv)\"' || echo 'eval \"$(/usr/local/bin/brew shellenv)\"')"
  fi
}

ensure_system_deps() {
  detect_pm
  if [ -z "$PM" ]; then warn "Could not detect a package manager automatically."; fi

  if [ "$OS" = "Darwin" ]; then
    if ! xcode-select -p >/dev/null 2>&1; then
      warn "Installing Xcode Command Line Tools..."
      xcode-select --install || true
    fi
    ensure_homebrew
    install_pkgs bash curl git python pipx
  else
    # Linux
    # Base tools
    install_pkgs bash curl git python3
    # venv tooling by distro
    case "$PM" in
      apt) install_pkgs python3-venv pipx ;; 
      dnf|yum) install_pkgs python3-pip python3-virtualenv pipx ;; 
      pacman) install_pkgs python python-pipx ;; 
      zypper) install_pkgs python3 python311-pipx python3-virtualenv || install_pkgs python3-pipx ;; 
      apk) install_pkgs python3 py3-pip py3-virtualenv ;; 
    esac
  fi

  # Fallback pipx via pip if still missing
  if ! have_cmd pipx; then
    if have_cmd python3; then
      log "Installing pipx via pip --user"
      python3 -m pip install --user -q pipx
      python3 -m pipx ensurepath || true
    else
      die "python3 is required but not installed."
    fi
  fi

  # Ensure ~/.local/bin is on PATH
  case ":${PATH}:" in
    *:"${HOME}/.local/bin":*) : ;;
    *)
      warn "~/.local/bin not in PATH. Adding to your shell profile. Restart your shell after install."
      { echo "# Added by penweb installer"; echo "export PATH=\"$HOME/.local/bin:\$PATH\""; } >> "$HOME/.profile"
      { echo "# Added by penweb installer"; echo "export PATH=\"$HOME/.local/bin:\$PATH\""; } >> "$HOME/.bashrc" 2>/dev/null || true
      { echo "# Added by penweb installer"; echo "export PATH=\"$HOME/.local/bin:\$PATH\""; } >> "$HOME/.zshrc" 2>/dev/null || true
      export PATH="$HOME/.local/bin:$PATH"
      ;;
  esac

  # Poetry via pipx
  if ! pipx list | grep -q "package poetry" 2>/dev/null; then
    log "Installing Poetry via pipx"
    pipx install poetry >/dev/null || true
  else
    log "Poetry already installed"
  fi
  pipx ensurepath || true
}

ensure_env_file() {
  if [ -f "$REPO_DIR/.env" ]; then return; fi
  if [ -f "$REPO_DIR/.env.sample" ]; then
    cp "$REPO_DIR/.env.sample" "$REPO_DIR/.env"
    log "Created .env from .env.sample"
  else
    warn ".env.sample not found; skipping .env creation"
  fi
}

repo_install() {
  log "Setting up in-repo Poetry environment (.venv)"
  (cd "$REPO_DIR" && poetry config virtualenvs.in-project true --local || true)
  (cd "$REPO_DIR" && poetry install --no-interaction)
  chmod +x "$REPO_DIR/run.sh" || true
  ensure_env_file
  log "Done. Run: $REPO_DIR/run.sh"
}

copy_tree() {
  # copy repo to target dir without .git
  local target="$1"
  mkdir -p "$target"
  if have_cmd rsync; then
    rsync -a --delete --exclude ".git" --exclude "*.pyc" --exclude "__pycache__" "$REPO_DIR"/ "$target"/
  else
    tar -C "$REPO_DIR" -cf - . --exclude .git --exclude __pycache__ | tar -C "$target" -xf -
  fi
}

user_local_install() {
  local target_dir
  if [ "$OS" = "Darwin" ]; then
    target_dir="${HOME}/.local/share/penweb"
  else
    target_dir="${HOME}/.local/share/penweb"
  fi

  log "Installing to user-local folder: $target_dir"
  copy_tree "$target_dir"

  (cd "$target_dir" && poetry config virtualenvs.in-project true --local || true)
  (cd "$target_dir" && poetry install --no-interaction)

  # Wrapper command in ~/.local/bin
  mkdir -p "$HOME/.local/bin"
  cat > "$HOME/.local/bin/penweb" <<EOF
#!/usr/bin/env bash
set -euo pipefail
exec "$target_dir/run.sh" "${1-}" "$@"
EOF
  chmod +x "$HOME/.local/bin/penweb"

  ensure_env_file

  log "Installed penweb command at: $HOME/.local/bin/penweb"
  log "Invoke with: penweb"
}

prompt_mode() {
  echo "Select installation mode:"
  echo "  1) In-repo install (Poetry, .venv inside repo)"
  echo "  2) User-local install (~/.local/share/penweb) with 'penweb' command"
  read -r -p "Enter choice [1/2] (default 1): " choice || true
  case "${choice:-1}" in
    2) user_local_install ;;
    *) repo_install ;;
  esac
}

main() {
  log "Detecting and installing prerequisites..."
  ensure_system_deps
  # Make sure poetry is on PATH from pipx
  if have_cmd poetry; then :; else
    # shellcheck disable=SC1090
    [ -f "$HOME/.bashrc" ] && . "$HOME/.bashrc" || true
    [ -f "$HOME/.zshrc" ] && . "$HOME/.zshrc" || true
  fi
  if ! have_cmd poetry; then die "Poetry not found in PATH after installation. Please restart your shell and rerun this script."; fi

  prompt_mode
  log "Installation complete."
}

main "$@"