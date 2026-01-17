# Frontmatter Specification

SKILL.md files must include YAML frontmatter to define skill metadata.

## Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Skill identifier (lowercase, hyphens) |
| `description` | string | Brief description for Claude to understand when to invoke |

## Optional Fields

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `publish` | boolean | `true` | Whether to sync to public repo |
| `version` | string | - | Semantic version (e.g., "1.0.0") |
| `author` | string | - | Author name |
| `triggers` | list | - | Slash commands that invoke this skill |
| `model` | string | - | Preferred model (sonnet, opus, haiku) |

## Publish Flag Behavior

### `publish: true` (default)

- Skill is synced to repository during push
- Appears in GitHub Pages catalog
- Included in plugin package

### `publish: false`

- Skill stays local only
- Never copied to repository
- Not visible in public catalog

## Examples

### Minimal Frontmatter

```yaml
---
name: my-skill
description: Brief description of what this skill does
---
```

### Full Frontmatter

```yaml
---
name: my-skill
description: Detailed description for Claude to understand when and how to use this skill
version: "1.0.0"
author: Your Name
publish: true
triggers:
  - /my-skill
  - /alias-command
model: sonnet
---
```

### Private Skill

```yaml
---
name: my-private-skill
description: This skill contains proprietary workflows
publish: false
---
```

## Parsing Rules

1. Frontmatter must be at the start of the file
2. Must be enclosed by `---` on separate lines
3. YAML must be valid
4. Strings with special characters should be quoted
5. Boolean values: `true`/`false` (lowercase)

## Validation

The `parse_frontmatter.py` script validates:

- Presence of frontmatter block
- Required `name` field
- Required `description` field
- Valid YAML syntax
