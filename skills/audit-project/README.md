# Audit Project Skill

Analyze your Claude Code project configuration and get actionable recommendations for improvement.

## Overview

This is a **prompt-based skill** - Claude executes the analysis steps directly by examining your project files and configuration. No external scripts or dependencies required.

## Installation

Copy the skill to your Claude skills directory:

```bash
cp -r skills/audit-project ~/.claude/skills/
```

Or install the entire plugin:

```bash
git clone https://github.com/nkrebs13/GithubSkills.git ~/.claude/plugins/nathankrebs-skills
```

## Usage

Navigate to any project and run:

```
/audit-project
```

Or use the alias:

```
/health-check
```

## What It Analyzes

| Component | Analysis |
|-----------|----------|
| **CLAUDE.md** | Presence, content quality, staleness |
| **MCP Config** | .mcp.json presence and relevance to project type |
| **Custom Skills** | Project-specific skills in .claude/skills/ |
| **Global Plugins** | Whether enabled plugins match project type |
| **Session History** | Recent conversation patterns and error frequency |

## Output

The skill generates a structured health report:

```
## Project Health Report: my-project

**Health Score: B**

### Configuration Status
| Item | Status |
|------|--------|
| CLAUDE.md | ✓ Present |
| MCP Config | ✗ Missing |
| Custom Skills | 2 found |
| Recent Sessions | 15 in last 7 days |

### Issues Found
1. **Medium** - No MCP configuration found

### Recommendations
1. **Add .mcp.json** - Configure relevant MCP servers for Node.js

### Quick Wins
- [ ] Create basic CLAUDE.md with build commands
- [ ] Add project-specific test skill
```

## Grading Scale

| Grade | Criteria |
|-------|----------|
| **A** | CLAUDE.md with good content, appropriate MCP config, custom skills, active sessions |
| **B** | CLAUDE.md present, has MCP config or custom skills |
| **C** | CLAUDE.md present but minimal content |
| **D** | No CLAUDE.md but has some configuration |
| **F** | No project-specific configuration |

## Project Type Detection

The skill auto-detects project type from:

- `build.gradle*` / `settings.gradle*` → Android/Gradle
- `package.json` → Node.js/JavaScript
- `pyproject.toml` / `requirements.txt` → Python
- `Cargo.toml` → Rust
- `go.mod` → Go
- `*.xcodeproj` / `Package.swift` → iOS/Swift

Project type influences MCP and skill recommendations.

## Tips

- Run after cloning a new repository to assess its Claude Code readiness
- Use the quick wins checklist to improve configuration incrementally
- Re-run after making changes to verify improvements

## License

MIT License - see [LICENSE](../../LICENSE)
