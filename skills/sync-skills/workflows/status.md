# Sync Status Workflow

Compare local skills (~/.claude/skills/) with repository skills (~/Personal/GithubSkills/skills/).

## Steps

### 1. Gather Local Skills

```bash
ls ~/.claude/skills/
```

For each skill, extract frontmatter:

```bash
python3 ~/Personal/GithubSkills/skills/sync-skills/scripts/parse_frontmatter.py --directory ~/.claude/skills/
```

### 2. Gather Repository Skills

```bash
python3 ~/Personal/GithubSkills/skills/sync-skills/scripts/parse_frontmatter.py --directory ~/Personal/GithubSkills/skills/
```

### 3. Compare Each Skill

For skills in both locations:

```bash
python3 ~/Personal/GithubSkills/skills/sync-skills/scripts/compute_hash.py --compare ~/.claude/skills/<name> ~/Personal/GithubSkills/skills/<name>
```

### 4. Generate Status Table

| Status | Meaning |
|--------|---------|
| In Sync | Same content hash in both locations |
| Modified (local newer) | Local has changes not in repo |
| Modified (repo newer) | Repo has changes not in local |
| Local Only | Exists only in ~/.claude/skills/ |
| Repo Only | Exists only in repo |

### 5. Output Format

```markdown
## Sync Status

| Skill | Local | Repo | Status | Publish |
|-------|-------|------|--------|---------|
| skill-name | ✓/- | ✓/- | Status | true/false |

Summary:
- X skills in sync
- Y skills with local changes
- Z skills with repo changes
```
