---
name: validate-skills
description: Validate all skills in the repository for proper structure, frontmatter, naming conventions, and required files. Use when you need to check skill quality before publishing or after making changes.
version: "1.0.0"
author: Nathan Krebs
publish: true
triggers:
  - /validate-skills
  - /validate-skills all
---

# Validate Skills

Check all skills for proper structure, frontmatter, naming conventions, and required files.

## Usage

```
/validate-skills           # Validate all skills in repository
/validate-skills <name>    # Validate specific skill
```

## Validation Rules

### 1. Directory Structure

Each skill must have:

| Required | File | Purpose |
|----------|------|---------|
| ✓ | `SKILL.md` | Skill definition with frontmatter |
| Recommended | `README.md` | Human-readable documentation |

Optional directories:
- `scripts/` - Supporting scripts
- `workflows/` - Sub-workflow definitions
- `references/` - Reference documentation

### 2. Frontmatter Validation

Required fields in SKILL.md:

```yaml
---
name: skill-name        # Required: lowercase, hyphens only
description: ...        # Required: description for Claude
---
```

Optional fields:

```yaml
version: "1.0.0"        # Recommended
author: Name            # Recommended
publish: true/false     # Default: true
triggers:               # Recommended
  - /skill-name
model: sonnet           # Optional
```

### 3. Naming Conventions

| Rule | Valid | Invalid |
|------|-------|---------|
| Lowercase | `my-skill` | `My-Skill` |
| Hyphen separator | `my-skill` | `my_skill` |
| Directory matches name | `skills/foo/` with `name: foo` | Mismatch |
| No spaces | `my-skill` | `my skill` |

### 4. Content Checks

- SKILL.md has meaningful description (>20 chars)
- No hardcoded personal paths (`/Users/username/`)
- No secrets or API keys
- Scripts are executable (if present)

## Validation Workflow

1. List all skills in `~/Personal/GithubSkills/skills/`
2. For each skill:
   - Check directory structure
   - Parse and validate frontmatter
   - Check naming conventions
   - Run content checks
3. Generate report

## Implementation

```bash
# List skills
ls ~/Personal/GithubSkills/skills/

# For each skill, parse frontmatter
python3 ~/Personal/GithubSkills/skills/sync-skills/scripts/parse_frontmatter.py ~/Personal/GithubSkills/skills/<name>/SKILL.md

# Check for secrets
python3 ~/Personal/GithubSkills/scripts/scan_secrets.py --directory ~/Personal/GithubSkills/skills/<name>
```

## Output Format

```markdown
## Skill Validation Report

### Summary
- Total skills: 5
- Passed: 4
- Failed: 1
- Warnings: 2

### Results

| Skill | Status | Issues |
|-------|--------|--------|
| asset-gen | ✓ Pass | - |
| audit-project | ✓ Pass | 1 warning |
| sync-skills | ✓ Pass | - |
| my-skill | ✗ Fail | Missing description |

### Details

#### audit-project
⚠ **Warning**: No README.md found

#### my-skill
✗ **Error**: Frontmatter missing required field: description
```

## Error Levels

| Level | Meaning | Blocks Publish |
|-------|---------|----------------|
| Error | Critical issue | Yes |
| Warning | Recommended fix | No |
| Info | Suggestion | No |
