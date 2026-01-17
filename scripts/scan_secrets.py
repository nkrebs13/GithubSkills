#!/usr/bin/env python3
"""
Secret Scanner - Paranoid Mode

Scans files for secrets, API keys, tokens, personal paths, and other sensitive data.
Used by pre-commit hook and sync-skills command.

Usage:
    python scan_secrets.py [file1] [file2] ...
    python scan_secrets.py --directory <path>
    python scan_secrets.py --staged  # Scan git staged files

Exit codes:
    0 - No secrets found
    1 - Secrets detected (blocked)
    2 - Error during scan
"""

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import List, Tuple, Optional

# ANSI colors for output
RED = "\033[91m"
YELLOW = "\033[93m"
GREEN = "\033[92m"
RESET = "\033[0m"
BOLD = "\033[1m"

# Patterns to detect secrets and sensitive data
# Each tuple: (pattern, description, severity)
SECRET_PATTERNS: List[Tuple[re.Pattern, str, str]] = [
    # API Keys and Tokens
    (re.compile(r'(?i)(api[_-]?key|apikey)\s*[=:]\s*["\']?[\w-]{16,}', re.MULTILINE),
     "API key assignment", "HIGH"),
    (re.compile(r'(?i)(secret[_-]?key|secretkey)\s*[=:]\s*["\']?[\w-]{16,}', re.MULTILINE),
     "Secret key assignment", "HIGH"),
    (re.compile(r'(?i)(access[_-]?token|accesstoken)\s*[=:]\s*["\']?[\w-]{16,}', re.MULTILINE),
     "Access token assignment", "HIGH"),
    (re.compile(r'(?i)(auth[_-]?token|authtoken)\s*[=:]\s*["\']?[\w-]{16,}', re.MULTILINE),
     "Auth token assignment", "HIGH"),
    (re.compile(r'(?i)bearer\s+[a-zA-Z0-9_-]{20,}', re.MULTILINE),
     "Bearer token", "HIGH"),

    # Provider-specific patterns
    (re.compile(r'sk-[a-zA-Z0-9]{32,}'),
     "OpenAI API key", "CRITICAL"),
    (re.compile(r'sk-proj-[a-zA-Z0-9_-]{32,}'),
     "OpenAI project API key", "CRITICAL"),
    (re.compile(r'sk-ant-[a-zA-Z0-9_-]{32,}'),
     "Anthropic API key", "CRITICAL"),
    (re.compile(r'AIza[0-9A-Za-z_-]{35}'),
     "Google API key", "CRITICAL"),
    (re.compile(r'ghp_[a-zA-Z0-9]{36}'),
     "GitHub personal access token", "CRITICAL"),
    (re.compile(r'gho_[a-zA-Z0-9]{36}'),
     "GitHub OAuth token", "CRITICAL"),
    (re.compile(r'github_pat_[a-zA-Z0-9]{22}_[a-zA-Z0-9]{59}'),
     "GitHub fine-grained PAT", "CRITICAL"),
    (re.compile(r'xox[baprs]-[0-9]{10,13}-[0-9]{10,13}[a-zA-Z0-9-]*'),
     "Slack token", "CRITICAL"),
    (re.compile(r'AKIA[0-9A-Z]{16}'),
     "AWS access key ID", "CRITICAL"),
    (re.compile(r'(?i)aws[_-]?secret[_-]?access[_-]?key\s*[=:]\s*["\']?[A-Za-z0-9/+=]{40}'),
     "AWS secret access key", "CRITICAL"),

    # Private keys
    (re.compile(r'-----BEGIN (RSA |DSA |EC |OPENSSH )?PRIVATE KEY-----'),
     "Private key header", "CRITICAL"),
    (re.compile(r'-----BEGIN PGP PRIVATE KEY BLOCK-----'),
     "PGP private key", "CRITICAL"),

    # Passwords
    (re.compile(r'(?i)password\s*[=:]\s*["\'][^"\']{4,}["\']', re.MULTILINE),
     "Password assignment", "HIGH"),
    (re.compile(r'(?i)passwd\s*[=:]\s*["\'][^"\']{4,}["\']', re.MULTILINE),
     "Password assignment", "HIGH"),
    (re.compile(r'(?i)pwd\s*[=:]\s*["\'][^"\']{4,}["\']', re.MULTILINE),
     "Password assignment", "MEDIUM"),

    # URLs with credentials
    (re.compile(r'[a-zA-Z][a-zA-Z0-9+.-]*://[^:]+:[^@]+@[^\s"\']+'),
     "URL with embedded credentials", "HIGH"),

    # Personal paths (macOS/Linux)
    (re.compile(r'/Users/[a-zA-Z0-9_-]+/'),
     "Personal macOS path", "MEDIUM"),
    (re.compile(r'/home/[a-zA-Z0-9_-]+/'),
     "Personal Linux home path", "MEDIUM"),
    (re.compile(r'C:\\Users\\[a-zA-Z0-9_-]+\\'),
     "Personal Windows path", "MEDIUM"),

    # Database connection strings
    (re.compile(r'(?i)(mongodb|postgres|mysql|redis)://[^\s"\']+:[^\s"\']+@[^\s"\']+'),
     "Database connection string with credentials", "HIGH"),

    # .env patterns
    (re.compile(r'^[A-Z_]+_KEY\s*=\s*[^\s]{10,}$', re.MULTILINE),
     "Environment variable key pattern", "MEDIUM"),
    (re.compile(r'^[A-Z_]+_SECRET\s*=\s*[^\s]{10,}$', re.MULTILINE),
     "Environment variable secret pattern", "MEDIUM"),
    (re.compile(r'^[A-Z_]+_TOKEN\s*=\s*[^\s]{10,}$', re.MULTILINE),
     "Environment variable token pattern", "MEDIUM"),

    # Base64-encoded secrets (long strings)
    (re.compile(r'(?i)(secret|key|token|password)\s*[=:]\s*["\']?[A-Za-z0-9+/]{40,}={0,2}["\']?'),
     "Possible base64-encoded secret", "MEDIUM"),

    # IP addresses (internal)
    (re.compile(r'\b10\.\d{1,3}\.\d{1,3}\.\d{1,3}\b'),
     "Internal IP address (10.x.x.x)", "LOW"),
    (re.compile(r'\b172\.(1[6-9]|2[0-9]|3[0-1])\.\d{1,3}\.\d{1,3}\b'),
     "Internal IP address (172.16-31.x.x)", "LOW"),
    (re.compile(r'\b192\.168\.\d{1,3}\.\d{1,3}\b'),
     "Internal IP address (192.168.x.x)", "LOW"),
]

# Files/patterns to skip
SKIP_PATTERNS = [
    r'\.git/',
    r'node_modules/',
    r'__pycache__/',
    r'\.pyc$',
    r'\.png$',
    r'\.jpg$',
    r'\.jpeg$',
    r'\.gif$',
    r'\.ico$',
    r'\.woff2?$',
    r'\.ttf$',
    r'\.eot$',
    r'\.svg$',
    r'\.pdf$',
    r'\.zip$',
    r'\.tar\.gz$',
    r'\.lock$',
    r'package-lock\.json$',
    r'yarn\.lock$',
]

# Allowlist patterns (false positives to ignore)
ALLOWLIST_PATTERNS = [
    r'~/.claude/',  # Standard Claude path reference
    r'\$HOME/',     # Environment variable reference
    r'\${HOME}',    # Environment variable reference
    r'example\.com',
    r'your-.*-here',
    r'<your-.*>',
    r'YOUR_.*_HERE',
    r'xxx+',
    r'placeholder',
    # XML/SDK namespace URLs (not credentials)
    r'schemas\.android\.com',
    r'schemas\.microsoft\.com',
    r'www\.w3\.org',
    r'xmlns[=:]',
    r'developer\.apple\.com',
    r'maven\.apache\.org',
    r'gradle\.org',
    r'rubygems\.org',
    r'pypi\.org',
    r'npmjs\.com',
    # Documentation examples (patterns used in docs/examples)
    r're\.compile\(',     # Regex pattern definitions
    r'Pattern\s*\|',      # Markdown table headers
    r'\|\s*Example\s*\|', # Example columns in tables
    r'user:pass@host',    # Generic credential examples
    r'mypass\.\.\.',      # Truncated example passwords
    r'"secret"',          # Literal example strings
    r'sk-abc123',         # Example/fake API keys
    r'/Users/username/',  # Generic username in docs
    r'-----BEGIN.*-----', # Pattern definitions for keys
]


def should_skip_file(filepath: str) -> bool:
    """Check if file should be skipped based on patterns."""
    for pattern in SKIP_PATTERNS:
        if re.search(pattern, filepath):
            return True
    return False


def is_allowlisted(match: str, line: str) -> bool:
    """Check if a match is in the allowlist (false positive)."""
    for pattern in ALLOWLIST_PATTERNS:
        if re.search(pattern, match, re.IGNORECASE) or re.search(pattern, line, re.IGNORECASE):
            return True
    return False


def scan_content(content: str, filepath: str) -> List[Tuple[int, str, str, str]]:
    """
    Scan file content for secrets.

    Returns: List of (line_number, matched_text, description, severity)
    """
    findings = []
    lines = content.split('\n')

    for pattern, description, severity in SECRET_PATTERNS:
        for match in pattern.finditer(content):
            matched_text = match.group(0)

            # Find line number
            line_start = content.rfind('\n', 0, match.start()) + 1
            line_num = content.count('\n', 0, match.start()) + 1
            line_end = content.find('\n', match.end())
            if line_end == -1:
                line_end = len(content)
            line = content[line_start:line_end]

            # Check allowlist
            if is_allowlisted(matched_text, line):
                continue

            # Truncate long matches for display
            display_text = matched_text[:50] + "..." if len(matched_text) > 50 else matched_text

            findings.append((line_num, display_text, description, severity))

    return findings


def scan_file(filepath: str) -> List[Tuple[str, int, str, str, str]]:
    """
    Scan a single file for secrets.

    Returns: List of (filepath, line_number, matched_text, description, severity)
    """
    if should_skip_file(filepath):
        return []

    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
    except (IOError, OSError) as e:
        print(f"{YELLOW}Warning: Could not read {filepath}: {e}{RESET}", file=sys.stderr)
        return []

    findings = scan_content(content, filepath)
    return [(filepath, line, match, desc, sev) for line, match, desc, sev in findings]


def get_staged_files() -> List[str]:
    """Get list of files staged for commit."""
    try:
        result = subprocess.run(
            ['git', 'diff', '--cached', '--name-only', '--diff-filter=ACMR'],
            capture_output=True,
            text=True,
            check=True
        )
        return [f for f in result.stdout.strip().split('\n') if f]
    except subprocess.CalledProcessError:
        return []


def scan_directory(directory: str) -> List[Tuple[str, int, str, str, str]]:
    """Recursively scan a directory for secrets."""
    all_findings = []

    for root, dirs, files in os.walk(directory):
        # Skip hidden and common non-source directories
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', '__pycache__', 'venv', '.venv']]

        for filename in files:
            filepath = os.path.join(root, filename)
            findings = scan_file(filepath)
            all_findings.extend(findings)

    return all_findings


def print_findings(findings: List[Tuple[str, int, str, str, str]]) -> None:
    """Print findings in a formatted way."""
    if not findings:
        print(f"{GREEN}✓ No secrets detected{RESET}")
        return

    # Group by severity
    critical = [f for f in findings if f[4] == "CRITICAL"]
    high = [f for f in findings if f[4] == "HIGH"]
    medium = [f for f in findings if f[4] == "MEDIUM"]
    low = [f for f in findings if f[4] == "LOW"]

    print(f"\n{RED}{BOLD}⚠ SECRETS DETECTED{RESET}\n")

    for severity, items, color in [
        ("CRITICAL", critical, RED),
        ("HIGH", high, RED),
        ("MEDIUM", medium, YELLOW),
        ("LOW", low, YELLOW)
    ]:
        if items:
            print(f"{color}{BOLD}[{severity}]{RESET}")
            for filepath, line_num, match, desc, _ in items:
                print(f"  {filepath}:{line_num}")
                print(f"    {desc}: {match}")
            print()


def main():
    parser = argparse.ArgumentParser(description="Scan files for secrets and sensitive data")
    parser.add_argument('files', nargs='*', help="Files to scan")
    parser.add_argument('--directory', '-d', help="Directory to scan recursively")
    parser.add_argument('--staged', action='store_true', help="Scan git staged files")
    parser.add_argument('--quiet', '-q', action='store_true', help="Only output on findings")

    args = parser.parse_args()

    all_findings = []

    if args.staged:
        files = get_staged_files()
        if not files and not args.quiet:
            print("No staged files to scan")
            return 0
        for f in files:
            if os.path.isfile(f):
                all_findings.extend(scan_file(f))
    elif args.directory:
        all_findings = scan_directory(args.directory)
    elif args.files:
        for f in args.files:
            if os.path.isfile(f):
                all_findings.extend(scan_file(f))
            elif os.path.isdir(f):
                all_findings.extend(scan_directory(f))
    else:
        # Default: scan current directory
        all_findings = scan_directory('.')

    print_findings(all_findings)

    # Return 1 if critical or high severity findings
    critical_or_high = [f for f in all_findings if f[4] in ("CRITICAL", "HIGH")]
    if critical_or_high:
        print(f"\n{RED}Commit blocked: {len(critical_or_high)} critical/high severity issue(s) found{RESET}")
        print(f"Use '--force-secrets' in commit message to bypass (not recommended)")
        return 1
    elif all_findings:
        print(f"\n{YELLOW}Warning: {len(all_findings)} lower severity issue(s) found{RESET}")
        return 0

    return 0


if __name__ == "__main__":
    sys.exit(main())
