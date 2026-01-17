# Push Workflow

Push publishable local skills to the repository.

## Steps

### 1. Get Publishable Skills

```bash
python3 ~/Personal/GithubSkills/skills/sync-skills/scripts/parse_frontmatter.py --directory ~/.claude/skills/ --publish-only
```

### 2. For Each Skill

#### 2a. Security Scan

```bash
python3 ~/Personal/GithubSkills/scripts/scan_secrets.py --directory ~/.claude/skills/<skill-name>
```

**If secrets found:**
- Show the findings
- Ask for confirmation to proceed or abort
- Only proceed with explicit `--force` flag

#### 2b. Copy to Repository

```bash
cp -r ~/.claude/skills/<skill-name> ~/Personal/GithubSkills/skills/
```

### 3. Verify Copy

```bash
python3 ~/Personal/GithubSkills/skills/sync-skills/scripts/compute_hash.py --compare ~/.claude/skills/<name> ~/Personal/GithubSkills/skills/<name>
```

### 4. Report Results

```markdown
## Push Results

| Skill | Status |
|-------|--------|
| asset-gen | ✓ Pushed |
| my-skill | ✗ Blocked (secrets found) |
| private-skill | ⏭ Skipped (publish: false) |

Pushed: X skills
Blocked: Y skills
Skipped: Z skills
```

## Error Handling

| Error | Action |
|-------|--------|
| Security scan fails | Block push, show details |
| Copy fails | Report error, continue with others |
| publish: false | Skip silently or with note |
