#!/usr/bin/env python3
"""
Compute content hash for a skill directory.

Used to detect changes between local and repo versions.

Usage:
    python compute_hash.py <skill_directory>
    python compute_hash.py --compare <dir1> <dir2>

Output:
    SHA256 hash of all relevant files in the directory
"""

import argparse
import hashlib
import os
import sys
from pathlib import Path
from typing import List, Tuple

# Files/patterns to exclude from hashing
EXCLUDE_PATTERNS = [
    '__pycache__',
    '.pyc',
    '.DS_Store',
    '.git',
    '*.log',
    '*.tmp',
]

# Files to always include in hash
INCLUDE_EXTENSIONS = [
    '.md',
    '.py',
    '.sh',
    '.json',
    '.yaml',
    '.yml',
    '.txt',
    '.js',
    '.ts',
]


def should_include(filepath: str) -> bool:
    """Check if file should be included in hash."""
    path = Path(filepath)

    # Check exclude patterns
    for pattern in EXCLUDE_PATTERNS:
        if pattern in str(path):
            return False

    # Check include extensions
    if path.suffix.lower() in INCLUDE_EXTENSIONS:
        return True

    # Include files without extension (like LICENSE)
    if not path.suffix and path.is_file():
        return True

    return False


def get_files_sorted(directory: str) -> List[Tuple[str, str]]:
    """
    Get sorted list of (relative_path, absolute_path) for all relevant files.
    Sorting ensures consistent hash regardless of filesystem order.
    """
    files = []
    base_path = Path(directory)

    for root, dirs, filenames in os.walk(directory):
        # Skip hidden directories
        dirs[:] = [d for d in dirs if not d.startswith('.')]

        for filename in filenames:
            filepath = os.path.join(root, filename)
            if should_include(filepath):
                rel_path = os.path.relpath(filepath, directory)
                files.append((rel_path, filepath))

    return sorted(files, key=lambda x: x[0])


def compute_directory_hash(directory: str) -> str:
    """Compute SHA256 hash of directory contents."""
    hasher = hashlib.sha256()

    files = get_files_sorted(directory)

    for rel_path, abs_path in files:
        # Include relative path in hash (so renames are detected)
        hasher.update(rel_path.encode('utf-8'))

        try:
            with open(abs_path, 'rb') as f:
                # Read in chunks for large files
                while chunk := f.read(8192):
                    hasher.update(chunk)
        except (IOError, OSError) as e:
            print(f"Warning: Could not read {abs_path}: {e}", file=sys.stderr)

    return hasher.hexdigest()


def compare_directories(dir1: str, dir2: str) -> dict:
    """Compare hashes of two directories."""
    hash1 = compute_directory_hash(dir1)
    hash2 = compute_directory_hash(dir2)

    return {
        "dir1": {"path": dir1, "hash": hash1},
        "dir2": {"path": dir2, "hash": hash2},
        "match": hash1 == hash2,
        "status": "in_sync" if hash1 == hash2 else "modified"
    }


def main():
    parser = argparse.ArgumentParser(description="Compute skill directory hash")
    parser.add_argument('directory', nargs='?', help="Directory to hash")
    parser.add_argument('--compare', nargs=2, metavar=('DIR1', 'DIR2'),
                        help="Compare two directories")
    parser.add_argument('--short', action='store_true',
                        help="Output only first 12 characters of hash")

    args = parser.parse_args()

    if args.compare:
        result = compare_directories(args.compare[0], args.compare[1])
        if args.short:
            result["dir1"]["hash"] = result["dir1"]["hash"][:12]
            result["dir2"]["hash"] = result["dir2"]["hash"][:12]
        import json
        print(json.dumps(result, indent=2))
    elif args.directory:
        hash_value = compute_directory_hash(args.directory)
        if args.short:
            hash_value = hash_value[:12]
        print(hash_value)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
