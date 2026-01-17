---
layout: default
title: Home
nav_order: 1
---

# My Claude Code Skills

A collection of Claude Code skills for AI-assisted development workflows.
{: .fs-6 .fw-300 }

[Get Started](#installation){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[View on GitHub](https://github.com/nkrebs13/GithubSkills){: .btn .fs-5 .mb-4 .mb-md-0 }

---

## Skills Catalog

| Skill | Description |
|:------|:------------|
| [asset-gen](./skills/asset-gen/) | Generate app icons, splash screens, and marketing assets using Gemini API |
| [audit-project](./skills/audit-project/) | Analyze Claude Code configuration and suggest improvements |
| [sync-skills](./skills/sync-skills/) | Bidirectional sync between local skills and repository |

---

## Installation

### Option 1: Install as Plugin (Recommended)

Clone the repository to your Claude plugins directory:

```bash
git clone https://github.com/nkrebs13/GithubSkills.git ~/.claude/plugins/nathankrebs-skills
```

All skills will be automatically available in Claude Code.

### Option 2: Install Individual Skills

Copy a specific skill to your skills directory:

```bash
# Clone the repo
git clone https://github.com/nkrebs13/GithubSkills.git /tmp/GithubSkills

# Copy the skill you want
cp -r /tmp/GithubSkills/skills/asset-gen ~/.claude/skills/
```

### Option 3: Install All Skills

```bash
# Clone and copy all skills
git clone https://github.com/nkrebs13/GithubSkills.git /tmp/GithubSkills
cp -r /tmp/GithubSkills/skills/* ~/.claude/skills/
```

---

## Quick Start

After installation, skills are available as slash commands:

```
/asset-gen           # Generate visual assets
/audit-project       # Audit Claude Code configuration
/sync-skills status  # Check sync state
```

---

## Security

This repository includes security scanning to prevent accidental secret commits:

- **Pre-commit hook**: Scans staged files for secrets
- **Sync scanning**: Security scan before skill push
- **Patterns detected**: API keys, tokens, passwords, personal paths

Install the security hook:

```bash
cd ~/.claude/plugins/nathankrebs-skills
./scripts/install-hooks.sh
```

---

## Contributing

Contributions are welcome! See the [Contributing Guide](https://github.com/nkrebs13/GithubSkills/blob/main/CONTRIBUTING.md) for guidelines.

---

## License

MIT License - see [LICENSE](https://github.com/nkrebs13/GithubSkills/blob/main/LICENSE)
