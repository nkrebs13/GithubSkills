# Sync Skills

Bidirectional synchronization between local Claude Code skills and the GithubSkills repository.

## Overview

This skill manages the flow of skills between your local Claude installation (`~/.claude/skills/`) and the shared repository (`~/Personal/GithubSkills/skills/`).

## Commands

### Check Status

```
/sync-skills status
```

Shows a comparison table of all skills and their sync state.

### Push to Repository

```
/sync-skills push
```

Pushes publishable local skills to the repository. Includes security scanning.

### Pull from Repository

```
/sync-skills pull
```

Pulls repository skills to your local installation.

### Security Scan

```
/sync-skills scan
```

Runs security scan on all skills without pushing.

## Publish Flag

By default, skills are **public** (`publish: true`). To keep a skill private:

```yaml
---
name: my-private-skill
publish: false
---
```

Private skills will never be synced to the repository.

## Security

All push operations include automatic secret scanning:

- API keys and tokens
- Passwords and credentials
- Personal file paths
- Private keys
- Database connection strings

If secrets are detected, the push is blocked until they're removed.

## Directory Structure

```
sync-skills/
├── SKILL.md              # Main skill definition
├── README.md             # This file
├── workflows/
│   ├── status.md         # Status comparison workflow
│   ├── push.md           # Push to repo workflow
│   └── pull.md           # Pull from repo workflow
├── scripts/
│   ├── parse_frontmatter.py  # Extract YAML frontmatter
│   └── compute_hash.py       # Compute directory hash
└── references/
    └── frontmatter-spec.md   # Frontmatter documentation
```

## Dependencies

- Python 3.9+
- No external packages required (uses standard library only)

## License

MIT License - see [LICENSE](../../LICENSE)
