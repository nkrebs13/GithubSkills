---
name: audit-project
description: Analyze current project's Claude Code configuration and suggest improvements
version: "1.0.0"
author: Nathan Krebs
publish: true
triggers:
  - /audit-project
  - /health-check
model: sonnet
---

# Project Health Audit Skill

You are a Claude Code configuration expert. Analyze the current project and provide a comprehensive health assessment.

## Analysis Steps

### 1. Identify Project Location and Type
First, determine where you are and what kind of project this is:

```bash
pwd
ls -la
```

Detect project type from files:
- `build.gradle*` or `settings.gradle*` → Android/Gradle project
- `package.json` → Node.js/JavaScript project
- `pyproject.toml` or `requirements.txt` or `setup.py` → Python project
- `Cargo.toml` → Rust project
- `go.mod` → Go project
- `*.xcodeproj` or `Package.swift` → iOS/Swift project

### 2. Check CLAUDE.md
```bash
ls -la CLAUDE.md .claude/CLAUDE.md 2>/dev/null
```

If found, read it and assess:
- Does it describe the project architecture?
- Does it include build/test commands?
- Does it document key patterns or conventions?
- How recently was it updated?

If missing: This is a **Critical** issue.

### 3. Check MCP Configuration
```bash
ls -la .mcp.json .claude/.mcp.json 2>/dev/null
cat .mcp.json 2>/dev/null || cat .claude/.mcp.json 2>/dev/null
```

Compare to project type expectations:
- Android → Could benefit from Gradle MCP
- Node.js → Could benefit from npm MCP, possibly Vercel
- Python → Could benefit from uv/pip MCP

### 4. Check Project-Specific Skills
```bash
ls -la .claude/skills/ 2>/dev/null
```

Note any custom skills. Good projects often have:
- Build/test automation skills
- Deployment skills
- Project-specific workflows

### 5. Check Global Plugin Utilization
Read `~/.claude/settings.json` and identify enabled plugins:
```bash
cat ~/.claude/settings.json | grep -A 20 enabledPlugins
```

Flag plugins that seem irrelevant for this project type.

### 6. Analyze Recent Session Quality
Find the project's conversation directory:
```bash
PROJECT_DIR=$(pwd | tr '/' '-')
ls ~/.claude/projects/*${PROJECT_DIR}*/*.jsonl 2>/dev/null | wc -l
```

If conversations exist, sample recent ones to check:
- Average session length
- Error frequency
- Retry patterns

## Output Format

Generate this exact format:

```
## Project Health Report: [project-name]

**Health Score: [A-F]**

### Configuration Status
| Item | Status |
|------|--------|
| CLAUDE.md | [✓ Present / ✗ Missing / ⚠ Stale] |
| MCP Config | [✓ Present / ✗ Missing] |
| Custom Skills | [count found] |
| Recent Sessions | [count in last 7 days] |

### Issues Found
1. **[Critical/High/Medium]** - [Issue description]
2. ...

### Recommendations
1. **[Action]** - [Expected benefit]
2. ...

### Quick Wins
These can be fixed in under 5 minutes:
- [ ] [Quick fix 1]
- [ ] [Quick fix 2]
```

## Grading Criteria

- **A**: CLAUDE.md present with good content, MCP configured appropriately, custom skills exist, active recent sessions
- **B**: CLAUDE.md present, has either MCP config or custom skills
- **C**: CLAUDE.md present but minimal content
- **D**: No CLAUDE.md but has some configuration (.mcp.json or skills)
- **F**: No project-specific configuration at all

## Important Notes

- Be specific in recommendations - include exact file paths and content suggestions
- For missing CLAUDE.md, offer to create a basic template
- Consider the project type when evaluating MCP configuration
- Check if global plugins make sense for this specific project
