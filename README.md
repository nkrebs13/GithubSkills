# Nathan Krebs Claude Code Skills

A collection of Claude Code skills for AI-assisted development workflows.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skills-blue)](https://claude.ai/code)

## Skills

### Core Skills

| Skill | Description |
|-------|-------------|
| [asset-gen](./skills/asset-gen/) | Generate app icons, splash screens, and marketing assets using Gemini API |
| [audit-project](./skills/audit-project/) | Analyze Claude Code configuration and suggest improvements |
| [sync-skills](./skills/sync-skills/) | Bidirectional sync between local skills and repository |

### Meta-Tooling

| Skill | Description |
|-------|-------------|
| [validate-skills](./skills/validate-skills/) | Validate skills for proper structure, frontmatter, and conventions |
| [scaffold-skill](./skills/scaffold-skill/) | Generate new skill from template with proper structure |
| [scan-secrets](./skills/scan-secrets/) | Security scan to detect API keys, tokens, and sensitive data |

## Installation

### Option 1: Install as Plugin (Recommended)

```bash
# Clone the repository
git clone https://github.com/nkrebs13/GithubSkills.git ~/.claude/plugins/nathankrebs-skills

# Skills are automatically available in Claude Code
```

### Option 2: Install Individual Skills

```bash
# Copy a specific skill to your skills directory
cp -r GithubSkills/skills/asset-gen ~/.claude/skills/
```

### Option 3: Install All Skills

```bash
# Copy all skills to your local Claude skills directory
cp -r GithubSkills/skills/* ~/.claude/skills/
```

## Security

This repository includes paranoid-level secret scanning:

- **Pre-commit hook**: Scans all staged files for secrets before commit
- **Sync scanning**: Security scan runs before any skill push
- **Patterns detected**: API keys, tokens, passwords, personal paths, credentials

### Installing the Security Hook

```bash
./scripts/install-hooks.sh
```

## Usage

Once installed, skills are available as slash commands in Claude Code:

```
/asset-gen           # Generate visual assets
/audit-project       # Audit Claude Code configuration
/sync-skills status  # Check sync state between local and repo
/validate-skills     # Validate all skills
/scaffold-skill      # Create new skill from template
/scan-secrets        # Run security scan
```

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines on contributing skills.

## Documentation

Visit the [Skills Catalog](https://nkrebs13.github.io/GithubSkills/) for detailed documentation.

## License

MIT License - see [LICENSE](./LICENSE) for details.
