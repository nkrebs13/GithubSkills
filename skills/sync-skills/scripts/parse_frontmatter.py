#!/usr/bin/env python3
"""
Parse YAML frontmatter from SKILL.md files.

Usage:
    python parse_frontmatter.py <skill_path>/SKILL.md
    python parse_frontmatter.py --directory <skills_directory>

Output:
    JSON object with frontmatter fields
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Dict, Any, Optional

# YAML frontmatter pattern
FRONTMATTER_PATTERN = re.compile(
    r'^---\s*\n(.*?)\n---\s*\n',
    re.DOTALL
)


def parse_yaml_simple(content: str) -> Dict[str, Any]:
    """
    Simple YAML parser for frontmatter (no external dependencies).
    Handles basic key: value pairs and simple lists.
    """
    result = {}
    current_key = None
    current_list = None

    for line in content.split('\n'):
        line = line.rstrip()

        # Skip empty lines
        if not line.strip():
            continue

        # Check for list item
        if line.startswith('  - '):
            if current_list is not None:
                current_list.append(line[4:].strip())
            continue

        # Check for key: value
        if ':' in line and not line.startswith(' '):
            key, _, value = line.partition(':')
            key = key.strip()
            value = value.strip()

            # Handle quoted strings
            if value.startswith('"') and value.endswith('"'):
                value = value[1:-1]
            elif value.startswith("'") and value.endswith("'"):
                value = value[1:-1]

            # Handle boolean values
            if value.lower() == 'true':
                value = True
            elif value.lower() == 'false':
                value = False

            # Handle empty value (potential list follows)
            if value == '':
                result[key] = []
                current_key = key
                current_list = result[key]
            else:
                result[key] = value
                current_key = key
                current_list = None

    return result


def extract_frontmatter(filepath: str) -> Optional[Dict[str, Any]]:
    """Extract and parse YAML frontmatter from a file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except (IOError, OSError) as e:
        print(f"Error reading file: {e}", file=sys.stderr)
        return None

    match = FRONTMATTER_PATTERN.match(content)
    if not match:
        return None

    yaml_content = match.group(1)
    return parse_yaml_simple(yaml_content)


def get_publish_status(frontmatter: Optional[Dict[str, Any]]) -> bool:
    """Get publish status, defaulting to True if not specified."""
    if frontmatter is None:
        return True  # Default to publish

    return frontmatter.get('publish', True)


def scan_skills_directory(directory: str) -> Dict[str, Dict[str, Any]]:
    """Scan a directory of skills and extract frontmatter from each."""
    results = {}

    skills_path = Path(directory)
    if not skills_path.exists():
        return results

    for skill_dir in skills_path.iterdir():
        if not skill_dir.is_dir():
            continue

        skill_md = skill_dir / 'SKILL.md'
        if not skill_md.exists():
            continue

        frontmatter = extract_frontmatter(str(skill_md))
        if frontmatter:
            frontmatter['_path'] = str(skill_dir)
            frontmatter['_publish'] = get_publish_status(frontmatter)
            results[skill_dir.name] = frontmatter

    return results


def main():
    parser = argparse.ArgumentParser(description="Parse SKILL.md frontmatter")
    parser.add_argument('file', nargs='?', help="Path to SKILL.md file")
    parser.add_argument('--directory', '-d', help="Scan directory of skills")
    parser.add_argument('--publish-only', action='store_true',
                        help="Only output skills with publish: true")

    args = parser.parse_args()

    if args.directory:
        results = scan_skills_directory(args.directory)
        if args.publish_only:
            results = {k: v for k, v in results.items() if v.get('_publish', True)}
        print(json.dumps(results, indent=2))
    elif args.file:
        frontmatter = extract_frontmatter(args.file)
        if frontmatter:
            frontmatter['_publish'] = get_publish_status(frontmatter)
            print(json.dumps(frontmatter, indent=2))
        else:
            print(json.dumps({"error": "No frontmatter found"}))
            sys.exit(1)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
