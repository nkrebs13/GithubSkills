---
name: sync-skills
description: Bidirectional sync between local Claude Code skills (~/.claude/skills/) and the GithubSkills repository. Use when you need to push local skills to the repo, pull repo skills to local, or check sync status.
version: "1.0.0"
author: Nathan Krebs
publish: true
triggers:
  - /sync-skills
  - /sync-skills status
  - /sync-skills push
  - /sync-skills pull
  - /sync-skills scan
---

# Sync Skills

Bidirectional synchronization between local Claude Code skills and the GithubSkills repository.

## Commands

| Command | Description |
|---------|-------------|
| `/sync-skills status` | Show sync status between local and repo |
| `/sync-skills push` | Push publishable local skills to repo |
| `/sync-skills pull` | Pull repo skills to local |
| `/sync-skills scan` | Run security scan on all skills |

## Locations

- **Local skills**: `~/.claude/skills/`
- **Repository**: `~/Personal/GithubSkills/skills/`

## Publish Flag

Skills are **public by default**. To keep a skill private:

```yaml
---
name: my-private-skill
publish: false  # This skill stays local only
---
```

Skills without a `publish` field or with `publish: true` will be synced to the repository.

## Command: status

Show what's different between local and repo skills.

### Workflow

1. List all skills in `~/.claude/skills/`
2. List all skills in `~/Personal/GithubSkills/skills/`
3. For each skill:
   - Check if exists in both locations
   - Compare content hashes if in both
   - Check `publish` flag in frontmatter
4. Output status table

### Output Format

```
## Sync Status

| Skill | Local | Repo | Status | Publish |
|-------|-------|------|--------|---------|
| asset-gen | ✓ | ✓ | In Sync | true |
| audit-project | ✓ | ✓ | Modified (local newer) | true |
| my-private | ✓ | - | Local Only | false |
| sync-skills | - | ✓ | Repo Only | true |
```

### Implementation

```bash
# Get local skills
ls ~/.claude/skills/

# Get repo skills
ls ~/Personal/GithubSkills/skills/

# For each skill, check frontmatter
python3 ~/Personal/GithubSkills/skills/sync-skills/scripts/parse_frontmatter.py <skill_path>/SKILL.md

# Compare hashes
python3 ~/Personal/GithubSkills/skills/sync-skills/scripts/compute_hash.py <directory>
```

## Command: push

Copy publishable local skills to the repository.

### Workflow

1. For each skill in `~/.claude/skills/`:
   a. Check `publish` flag (default: true)
   b. If `publish: false`, skip
   c. Run security scan
   d. If scan fails, abort (unless --force)
   e. Copy to `~/Personal/GithubSkills/skills/`
2. Report results

### Security Scan

Before pushing, run:

```bash
python3 ~/Personal/GithubSkills/scripts/scan_secrets.py --directory ~/.claude/skills/<skill-name>
```

If secrets detected:
- **Block the push**
- Show what was detected
- Suggest fixes
- Allow `--force` only with explicit confirmation

### Implementation

```bash
# Check publish flag
python3 ~/Personal/GithubSkills/skills/sync-skills/scripts/parse_frontmatter.py ~/.claude/skills/<name>/SKILL.md

# Run security scan
python3 ~/Personal/GithubSkills/scripts/scan_secrets.py --directory ~/.claude/skills/<name>

# Copy if clean
cp -r ~/.claude/skills/<name> ~/Personal/GithubSkills/skills/
```

## Command: pull

Copy repository skills to local.

### Workflow

1. For each skill in `~/Personal/GithubSkills/skills/`:
   a. Check if exists locally
   b. If exists, compare hashes
   c. If different, prompt for action (overwrite/skip/merge)
   d. Copy to `~/.claude/skills/`
2. Report results

### Conflict Handling

If skill exists in both locations with different content:

```
Conflict detected for: asset-gen

Local hash:  abc123...
Repo hash:   def456...
Local mtime: 2026-01-15 10:30
Repo mtime:  2026-01-14 15:45

Options:
1. Keep local (skip)
2. Overwrite with repo
3. Show diff

Choice [1/2/3]:
```

### Implementation

```bash
# Copy skill to local
cp -r ~/Personal/GithubSkills/skills/<name> ~/.claude/skills/
```

## Command: scan

Run security scan on all skills (local and repo).

### Workflow

1. Scan `~/.claude/skills/`
2. Scan `~/Personal/GithubSkills/skills/`
3. Report findings grouped by location

### Implementation

```bash
python3 ~/Personal/GithubSkills/scripts/scan_secrets.py --directory ~/.claude/skills/
python3 ~/Personal/GithubSkills/scripts/scan_secrets.py --directory ~/Personal/GithubSkills/skills/
```

## Helper Scripts

### parse_frontmatter.py

Extract YAML frontmatter from SKILL.md files.

```bash
python3 parse_frontmatter.py <skill_path>/SKILL.md
# Output: JSON with name, description, publish, etc.
```

### compute_hash.py

Compute content hash of a skill directory.

```bash
python3 compute_hash.py <skill_directory>
# Output: SHA256 hash of all files
```

## Error Handling

| Error | Action |
|-------|--------|
| Skill missing SKILL.md | Skip with warning |
| Invalid frontmatter | Skip with warning |
| Security scan fails | Block push, show details |
| Copy fails | Show error, continue with others |

## Examples

### Check status

```
User: /sync-skills status

Claude: Running sync status check...

## Sync Status

| Skill | Local | Repo | Status | Publish |
|-------|-------|------|--------|---------|
| asset-gen | ✓ | ✓ | In Sync | true |
| audit-project | ✓ | ✓ | In Sync | true |
| sync-skills | ✓ | ✓ | In Sync | true |

All skills are synchronized.
```

### Push with security issue

```
User: /sync-skills push

Claude: Scanning local skills for secrets...

⚠ SECRETS DETECTED in: my-new-skill

[HIGH] API key assignment
  scripts/api.py:15
  api_key = "sk-abc123..."

Push blocked. Please remove the secret before pushing.
```

### Pull new skill

```
User: /sync-skills pull

Claude: Checking repository skills...

New skill available: sync-skills
Copying to ~/.claude/skills/sync-skills...

✓ Pulled 1 skill successfully
```
