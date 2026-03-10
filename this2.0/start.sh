#!/bin/bash
# ═══════════════════════════════════════════════════════════════════
#  MBot6.2.0 — Self-Setup Launcher
#  Usage:
#    bash start.sh          → setup + run (first time or re-run)
#    bash start.sh start    → start in background (screen)
#    bash start.sh stop     → stop background session
#    bash start.sh restart  → restart background session
#    bash start.sh logs     → view live logs
#    bash start.sh setup    → only run setup, don't start
# ═══════════════════════════════════════════════════════════════════

set -e
cd "$(dirname "$0")"

BOT_DIR="$(pwd)"
SESSION_NAME="mbot"
VENV_DIR="$BOT_DIR/venv"
VENV_PYTHON="$VENV_DIR/bin/python"
VENV_PIP="$VENV_DIR/bin/pip"

BOLD="\e[1m"
GREEN="\e[32m"
CYAN="\e[36m"
YELLOW="\e[33m"
RED="\e[31m"
RESET="\e[0m"

banner() {
  echo ""
  echo -e "${BOLD}${CYAN}  ╔══════════════════════════════╗${RESET}"
  echo -e "${BOLD}${CYAN}  ║    🎵 MBot6.2.0 Launcher     ║${RESET}"
  echo -e "${BOLD}${CYAN}  ╚══════════════════════════════╝${RESET}"
  echo ""
}

info()    { echo -e "${CYAN}[INFO]${RESET}  $*"; }
success() { echo -e "${GREEN}[OK]${RESET}    $*"; }
warn()    { echo -e "${YELLOW}[WARN]${RESET}  $*"; }
error()   { echo -e "${RED}[ERROR]${RESET} $*"; exit 1; }

# ─── STEP 1: System Dependencies ──────────────────────────────────
install_system_deps() {
  info "Checking system dependencies..."

  # Try to use sudo if available
  SUDO=""
  if command -v sudo &>/dev/null && sudo -n true 2>/dev/null; then
    SUDO="sudo"
  elif [ "$(id -u)" -eq 0 ]; then
    SUDO=""
  fi

  # Python3
  if ! command -v python3 &>/dev/null; then
    info "Installing Python3..."
    $SUDO apt-get update -qq && $SUDO apt-get install -y -qq python3 python3-pip python3-venv || \
      error "Could not install Python3. Please install it manually."
  fi

  # pip / venv
  if ! python3 -m pip --version &>/dev/null 2>&1; then
    $SUDO apt-get install -y -qq python3-pip python3-venv 2>/dev/null || true
  fi

  # ffmpeg
  if ! command -v ffmpeg &>/dev/null; then
    info "Installing ffmpeg..."
    $SUDO apt-get update -qq && $SUDO apt-get install -y -qq ffmpeg || \
      warn "Could not auto-install ffmpeg. Please install it manually: sudo apt install ffmpeg"
  fi

  # libopus (required for discord.py voice)
  if ! ldconfig -p 2>/dev/null | grep -q libopus && ! dpkg -s libopus-dev &>/dev/null 2>&1; then
    info "Installing libopus-dev..."
    $SUDO apt-get install -y -qq libopus-dev 2>/dev/null || true
  fi

  # screen (for background mode)
  if ! command -v screen &>/dev/null; then
    info "Installing screen..."
    $SUDO apt-get install -y -qq screen 2>/dev/null || warn "screen not installed. Background mode won't work."
  fi

  success "System dependencies OK"
}

# ─── STEP 2: Python Virtual Environment ───────────────────────────
setup_venv() {
  if [ ! -d "$VENV_DIR" ]; then
    info "Creating Python virtual environment..."
    python3 -m venv "$VENV_DIR" || error "Failed to create venv. Install: sudo apt install python3-venv"
    success "Virtual environment created"
  fi

  info "Installing/upgrading Python packages..."
  "$VENV_PIP" install --upgrade pip -q
  "$VENV_PIP" install -r requirements.txt -q
  "$VENV_PIP" install --upgrade yt-dlp -q
  success "Python packages installed"
}

# ─── STEP 3: .env Setup Wizard ────────────────────────────────────
setup_env() {
  if [ -f ".env" ]; then
    # Check if token is already set (not the placeholder)
    current_token=$(grep -E "^DISCORD_TOKEN=" .env | cut -d= -f2 | tr -d '"')
    if [ -n "$current_token" ] && [ "$current_token" != "your_discord_bot_token" ]; then
      success ".env already configured, skipping wizard."
      return
    fi
  fi

  echo ""
  echo -e "${BOLD}${YELLOW}══════════════════════════════════════════${RESET}"
  echo -e "${BOLD}  🔧 First-Time Configuration Wizard${RESET}"
  echo -e "${BOLD}${YELLOW}══════════════════════════════════════════${RESET}"
  echo ""
  echo -e "  You'll need the following before continuing:"
  echo -e "  ${CYAN}1.${RESET} Discord Bot Token  → discord.com/developers"
  echo -e "  ${CYAN}2.${RESET} YouTube API Key     → console.cloud.google.com"
  echo -e "  ${CYAN}3.${RESET} A Discord channel ID for bot logs (optional)"
  echo ""

  read -rp "$(echo -e "${BOLD}  Discord Bot Token:${RESET} ")" DISCORD_TOKEN
  [ -z "$DISCORD_TOKEN" ] && error "Discord token cannot be empty."

  read -rp "$(echo -e "${BOLD}  YouTube API Key (press Enter to skip):${RESET} ")" YOUTUBE_API_KEY
  YOUTUBE_API_KEY="${YOUTUBE_API_KEY:-}"

  read -rp "$(echo -e "${BOLD}  Log Channel ID (press Enter to skip):${RESET} ")" LOG_CHANNEL_ID
  LOG_CHANNEL_ID="${LOG_CHANNEL_ID:-0}"

  cat > .env <<EOF
DISCORD_TOKEN="${DISCORD_TOKEN}"
YOUTUBE_API_KEY="${YOUTUBE_API_KEY}"
LOG_CHANNEL_ID="${LOG_CHANNEL_ID}"
EOF

  success ".env file created successfully!"
  echo ""
}

# ─── STEP 4: Init directories & __init__.py files ─────────────────
init_project() {
  touch cogs/__init__.py utils/__init__.py 2>/dev/null || true
  mkdir -p yt_dlp_cache
  success "Project structure OK"
}

# ─── Bot Control ──────────────────────────────────────────────────
start_foreground() {
  info "Starting bot in foreground (Ctrl+C to stop)..."
  echo ""
  exec "$VENV_PYTHON" bot.py
}

start_background() {
  if screen -list 2>/dev/null | grep -q "$SESSION_NAME"; then
    warn "Bot is already running. Use 'bash start.sh restart' or 'bash start.sh logs'."
    exit 0
  fi
  info "Starting bot in background screen session '${SESSION_NAME}'..."
  screen -dmS "$SESSION_NAME" bash -c "cd '$BOT_DIR' && '$VENV_PYTHON' bot.py 2>&1 | tee -a bot.log"
  sleep 1
  if screen -list 2>/dev/null | grep -q "$SESSION_NAME"; then
    success "Bot is running in the background!"
    echo -e "  ${CYAN}→ View logs:${RESET}  bash start.sh logs"
    echo -e "  ${CYAN}→ Stop bot:${RESET}   bash start.sh stop"
  else
    warn "Bot may have crashed. Check logs: bash start.sh logs"
  fi
}

stop_bot() {
  if screen -list 2>/dev/null | grep -q "$SESSION_NAME"; then
    screen -S "$SESSION_NAME" -X quit
    success "Bot stopped."
  else
    warn "Bot is not currently running."
  fi
}

show_logs() {
  if [ -f "bot.log" ]; then
    echo -e "${CYAN}━━━━━━━━━━━━━ bot.log (last 50 lines) ━━━━━━━━━━━━━${RESET}"
    tail -n 50 bot.log
    echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RESET}"
  fi
  if screen -list 2>/dev/null | grep -q "$SESSION_NAME"; then
    echo ""
    info "Attaching to live session (Ctrl+A then D to detach)..."
    sleep 1
    screen -r "$SESSION_NAME"
  else
    warn "Bot is not currently running."
  fi
}

# ─── Main Entry Point ─────────────────────────────────────────────
banner

case "${1:-run}" in
  start)
    install_system_deps
    setup_venv
    setup_env
    init_project
    start_background
    ;;
  stop)
    stop_bot
    ;;
  restart)
    stop_bot
    sleep 1
    install_system_deps
    setup_venv
    init_project
    start_background
    ;;
  logs)
    show_logs
    ;;
  setup)
    install_system_deps
    setup_venv
    setup_env
    init_project
    success "Setup complete! Run 'bash start.sh start' to launch the bot."
    ;;
  run|*)
    # Default: full setup then run in foreground (e.g. direct `bash start.sh`)
    install_system_deps
    setup_venv
    setup_env
    init_project
    start_foreground
    ;;
esac
