# Contributing to Nathan Krebs Skills

Thank you for your interest in contributing! This document provides guidelines for contributing skills to this repository.

## Skill Structure

Each skill should follow this structure:

```
skills/skill-name/
├── SKILL.md              # Required: Main skill definition
├── README.md             # Recommended: Human-readable documentation
├── requirements.txt      # Optional: Python dependencies
├── scripts/              # Optional: Supporting scripts
├── workflows/            # Optional: Sub-workflow definitions
└── references/           # Optional: Reference documentation
```

## SKILL.md Requirements

### Frontmatter

Every SKILL.md must include YAML frontmatter:

```yaml
---
name: skill-name
description: Brief description for Claude to understand when to invoke this skill
version: "1.0.0"
author: Your Name
publish: true  # Set to false to keep skill private
triggers:
  - /skill-name
---
```

### Content Guidelines

1. **Clear trigger patterns**: Define when Claude should use this skill
2. **Structured instructions**: Use numbered steps or clear sections
3. **Examples**: Include concrete examples of usage
4. **Error handling**: Describe how to handle common errors

## Code Standards

### Python Scripts

- Use Python 3.9+ compatible syntax
- Include type hints where helpful
- Add docstrings to functions
- Handle errors gracefully
- No hardcoded paths (use `~/.claude/` or relative paths)

### Security Requirements

**CRITICAL**: Before submitting:

1. Run the security scanner: `/scan-secrets`
2. Ensure NO secrets, API keys, or personal paths are included
3. Use environment variables for any credentials
4. Test with the pre-commit hook enabled

## Submitting Changes

### For New Skills

1. Fork the repository
2. Create a branch: `git checkout -b skill/your-skill-name`
3. Add your skill to `skills/your-skill-name/`
4. Ensure security scan passes
5. Submit a pull request

### For Improvements

1. Fork the repository
2. Create a branch: `git checkout -b fix/description` or `git checkout -b feature/description`
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## Pull Request Checklist

- [ ] SKILL.md has proper frontmatter
- [ ] Security scan passes (`/scan-secrets` or pre-commit hook)
- [ ] README.md included for complex skills
- [ ] No hardcoded personal paths
- [ ] Examples included in documentation
- [ ] Tested with Claude Code

## Questions?

Open an issue if you have questions about contributing.
