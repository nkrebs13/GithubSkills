---
name: scan-secrets
description: Run security scan on skills or directories to detect API keys, tokens, passwords, personal paths, and other sensitive data. Use before pushing skills or committing code.
version: "1.0.0"
author: Nathan Krebs
publish: true
triggers:
  - /scan-secrets
  - /security-scan
---

# Scan Secrets

Run security scan to detect sensitive data before publishing.

## Usage

```
/scan-secrets                           # Scan all skills in repository
/scan-secrets <skill-name>              # Scan specific skill
/scan-secrets --local                   # Scan local skills (~/.claude/skills/)
/scan-secrets --directory <path>        # Scan any directory
```

## What It Detects

### Critical (blocks commit/push)

| Pattern | Example |
|---------|---------|
| OpenAI API keys | `sk-abc123...` |
| Anthropic API keys | `sk-ant-...` |
| Google API keys | `AIza...` |
| GitHub tokens | `ghp_...`, `gho_...` |
| AWS credentials | `AKIA...`, `aws_secret_access_key` |
| Private keys | `-----BEGIN PRIVATE KEY-----` |

### High (blocks commit/push)

| Pattern | Example |
|---------|---------|
| Generic API keys | `api_key = "..."` |
| Access tokens | `access_token = "..."` |
| Passwords | `password = "secret"` |
| URLs with credentials | `https://user:pass@host` |
| Database connection strings | `postgres://user:pass@host` |

### Medium (warning)

| Pattern | Example |
|---------|---------|
| Personal paths | `/Users/&lt;username&gt;/...` |
| Base64 encoded secrets | Long base64 strings in secret context |
| Environment variable patterns | `MY_SECRET_KEY = "..."` |

### Low (informational)

| Pattern | Example |
|---------|---------|
| Internal IP addresses | `192.168.x.x`, `10.x.x.x` |

## Workflow

### 1. Select Target

Determine what to scan:
- All repository skills
- Specific skill by name
- Local skills directory
- Custom directory path

### 2. Run Scanner

```bash
python3 ~/Personal/GithubSkills/scripts/scan_secrets.py --directory <target>
```

### 3. Review Results

If issues found:
- Show each finding with file, line number, and pattern
- Group by severity (Critical, High, Medium, Low)
- Provide remediation suggestions

### 4. Remediation Guidance

For each finding type:

| Finding | Remediation |
|---------|-------------|
| API key | Move to environment variable, use `$ENV_VAR` |
| Personal path | Use `~/.claude/` or relative path |
| Password | Use environment variable or secrets manager |
| Private key | Never commit, use SSH agent or secrets manager |

## Implementation

```bash
# Scan all skills
python3 ~/Personal/GithubSkills/scripts/scan_secrets.py --directory ~/Personal/GithubSkills/skills/

# Scan specific skill
python3 ~/Personal/GithubSkills/scripts/scan_secrets.py --directory ~/Personal/GithubSkills/skills/<name>

# Scan local skills
python3 ~/Personal/GithubSkills/scripts/scan_secrets.py --directory ~/.claude/skills/

# Scan staged git files
python3 ~/Personal/GithubSkills/scripts/scan_secrets.py --staged
```

## Output Format

### Clean Scan

```
✓ No secrets detected
```

### Findings Detected

```
⚠ SECRETS DETECTED

[CRITICAL]
  skills/my-skill/scripts/api.py:15
    OpenAI API key: sk-abc123def456...

[HIGH]
  skills/my-skill/config.py:8
    Password assignment: password = "mypass..."

[MEDIUM]
  skills/my-skill/SKILL.md:42
    Personal macOS path: /Users/&lt;username&gt;/...

Commit blocked: 2 critical/high severity issue(s) found
Use '--force-secrets' in commit message to bypass (not recommended)
```

## Force Bypass

In rare cases where a pattern is a false positive:

1. **For git commits:**
   ```bash
   git commit -m "message --force-secrets"
   ```

2. **For sync-skills push:**
   ```
   /sync-skills push --force
   ```

**Warning:** Use force bypass only when you're certain the finding is a false positive.

## Allowlisted Patterns

The scanner ignores known safe patterns:
- `~/.claude/` references
- `$HOME` environment variable references
- `schemas.android.com` and similar SDK URLs
- Placeholder patterns like `YOUR_API_KEY_HERE`

## Examples

### Scan before pushing

```
User: /scan-secrets

Claude: Scanning all skills in repository...

✓ asset-gen: Clean
✓ audit-project: Clean
✓ sync-skills: Clean
✓ validate-skills: Clean
✓ scaffold-skill: Clean
✓ scan-secrets: Clean

All skills passed security scan.
```

### Finding detected

```
User: /scan-secrets my-new-skill

Claude: Scanning my-new-skill...

⚠ SECRETS DETECTED

[HIGH]
  skills/my-new-skill/scripts/api.py:23
    API key assignment: api_key = "sk-proj-abc123..."

Recommendations:
1. Remove the hardcoded API key
2. Use environment variable: os.environ.get("OPENAI_API_KEY")
3. Update the code to read from environment

Would you like me to help fix this?
```
