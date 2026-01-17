#!/bin/bash
#
# Install git hooks for the GithubSkills repository
#
# Usage:
#   ./scripts/install-hooks.sh
#

# Colors
RED='\033[0;91m'
GREEN='\033[0;92m'
YELLOW='\033[0;93m'
RESET='\033[0m'
BOLD='\033[1m'

# Get script directory and repo root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"
HOOKS_DIR="$REPO_ROOT/hooks"
GIT_HOOKS_DIR="$REPO_ROOT/.git/hooks"

echo -e "${BOLD}Installing git hooks...${RESET}"

# Check if we're in a git repository
if [ ! -d "$REPO_ROOT/.git" ]; then
    echo -e "${RED}Error: Not a git repository. Run 'git init' first.${RESET}"
    exit 1
fi

# Create .git/hooks directory if it doesn't exist
mkdir -p "$GIT_HOOKS_DIR"

# Install pre-commit hook
if [ -f "$HOOKS_DIR/pre-commit" ]; then
    cp "$HOOKS_DIR/pre-commit" "$GIT_HOOKS_DIR/pre-commit"
    chmod +x "$GIT_HOOKS_DIR/pre-commit"
    echo -e "${GREEN}✓ Installed pre-commit hook${RESET}"
else
    echo -e "${YELLOW}Warning: pre-commit hook not found in $HOOKS_DIR${RESET}"
fi

# Make scanner script executable
SCANNER="$REPO_ROOT/scripts/scan_secrets.py"
if [ -f "$SCANNER" ]; then
    chmod +x "$SCANNER"
    echo -e "${GREEN}✓ Made scan_secrets.py executable${RESET}"
fi

# Verify Python is available
if ! command -v python3 &> /dev/null; then
    echo -e "${YELLOW}Warning: python3 not found. Secret scanner requires Python 3.${RESET}"
fi

echo ""
echo -e "${GREEN}${BOLD}Hooks installed successfully!${RESET}"
echo ""
echo "The pre-commit hook will now scan for secrets before each commit."
echo "To bypass (not recommended): git commit -m \"message --force-secrets\""
