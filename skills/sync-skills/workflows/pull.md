# Pull Workflow

Pull repository skills to local installation.

## Steps

### 1. Get Repository Skills

```bash
ls ~/Personal/GithubSkills/skills/
```

### 2. For Each Skill

#### 2a. Check Local Existence

```bash
ls ~/.claude/skills/<skill-name> 2>/dev/null
```

#### 2b. Handle Conflicts

If skill exists locally, compare hashes:

```bash
python3 ~/Personal/GithubSkills/skills/sync-skills/scripts/compute_hash.py --compare ~/Personal/GithubSkills/skills/<name> ~/.claude/skills/<name>
```

**If different:**

Present options:
1. Skip (keep local)
2. Overwrite with repo version
3. Show diff (if git available)

#### 2c. Copy to Local

```bash
cp -r ~/Personal/GithubSkills/skills/<skill-name> ~/.claude/skills/
```

### 3. Verify Copy

```bash
python3 ~/Personal/GithubSkills/skills/sync-skills/scripts/compute_hash.py --compare ~/Personal/GithubSkills/skills/<name> ~/.claude/skills/<name>
```

### 4. Report Results

```markdown
## Pull Results

| Skill | Status |
|-------|--------|
| sync-skills | ✓ Pulled (new) |
| asset-gen | ✓ Updated |
| audit-project | ⏭ Skipped (local same) |
| my-skill | ⏭ Skipped (kept local) |

New: X skills
Updated: Y skills
Skipped: Z skills
```

## Conflict Resolution

When prompting for conflict resolution:

```
Conflict: asset-gen

Local:  abc123def456 (modified 2026-01-15 10:30)
Repo:   789xyz123abc (modified 2026-01-14 15:45)

What would you like to do?
1. Keep local version
2. Overwrite with repo version
3. Show diff

Enter choice [1/2/3]:
```
