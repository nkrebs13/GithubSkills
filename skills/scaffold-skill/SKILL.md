---
name: scaffold-skill
description: Generate a new skill from a template with proper structure, frontmatter, and boilerplate files. Use when creating a new skill to ensure it follows conventions.
version: "1.0.0"
author: Nathan Krebs
publish: true
triggers:
  - /scaffold-skill
  - /new-skill
---

# Scaffold Skill

Generate a new skill from a template with proper structure and conventions.

## Usage

```
/scaffold-skill                     # Interactive mode
/scaffold-skill my-new-skill        # Create skill with name
```

## Workflow

### 1. Gather Information

Ask the user for:

1. **Skill name** (required)
   - Must be lowercase with hyphens
   - Example: `my-awesome-skill`

2. **Description** (required)
   - Brief description for Claude
   - Should explain when to use this skill

3. **Type** (optional)
   - `prompt` - Claude executes instructions (default)
   - `script` - Has Python/shell scripts
   - `hybrid` - Both prompt and scripts

4. **Publish** (optional)
   - `true` (default) - Sync to repository
   - `false` - Keep local only

### 2. Create Directory Structure

Based on type, create:

**Prompt-based skill:**
```
skills/my-skill/
├── SKILL.md
└── README.md
```

**Script-based skill:**
```
skills/my-skill/
├── SKILL.md
├── README.md
├── requirements.txt
└── scripts/
    └── main.py
```

**Hybrid skill:**
```
skills/my-skill/
├── SKILL.md
├── README.md
├── requirements.txt
├── scripts/
│   └── helper.py
├── workflows/
│   └── main.md
└── references/
    └── docs.md
```

### 3. Generate Files

#### SKILL.md Template

```markdown
---
name: {skill-name}
description: {description}
version: "1.0.0"
author: Nathan Krebs
publish: {publish}
triggers:
  - /{skill-name}
---

# {Skill Title}

{Description paragraph}

## Usage

\`\`\`
/{skill-name}
\`\`\`

## Workflow

### 1. Step One

Description of first step.

### 2. Step Two

Description of second step.

## Examples

### Example 1

\`\`\`
User: /{skill-name}
Claude: [Description of what happens]
\`\`\`
```

#### README.md Template

```markdown
# {Skill Title}

{Description}

## Installation

Copy the skill to your Claude skills directory:

\`\`\`bash
cp -r skills/{skill-name} ~/.claude/skills/
\`\`\`

## Usage

\`\`\`
/{skill-name}
\`\`\`

## License

MIT License - see [LICENSE](../../LICENSE)
```

#### requirements.txt Template (if script-based)

```
# {skill-name} dependencies
# Add your Python dependencies here
```

#### scripts/main.py Template (if script-based)

```python
#!/usr/bin/env python3
"""
{Skill Title}

{Description}
"""

import argparse
import sys


def main():
    parser = argparse.ArgumentParser(description="{description}")
    # Add arguments here
    args = parser.parse_args()

    # Implementation here
    print("Hello from {skill-name}!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

### 4. Post-Creation

After creating the skill:

1. Run validation: `/validate-skills {skill-name}`
2. Remind user to implement the skill logic
3. Suggest running security scan before push

## Implementation

```bash
# Create directory
mkdir -p ~/Personal/GithubSkills/skills/{skill-name}

# Create SKILL.md with frontmatter
cat > ~/Personal/GithubSkills/skills/{skill-name}/SKILL.md << 'EOF'
---
name: {skill-name}
...
---
EOF

# Make scripts executable if present
chmod +x ~/Personal/GithubSkills/skills/{skill-name}/scripts/*.py 2>/dev/null || true
```

## Examples

### Create simple prompt skill

```
User: /scaffold-skill weather-check

Claude: I'll create a new skill called "weather-check".

What should this skill do? (Brief description for Claude)

User: Check weather forecasts and provide recommendations

Claude: Should this skill have scripts, or is it prompt-based only?
1. Prompt-based (Claude follows instructions)
2. Script-based (has Python/shell scripts)

User: 1

Claude: Creating skill...

✓ Created skills/weather-check/SKILL.md
✓ Created skills/weather-check/README.md

Skill scaffolded successfully!

Next steps:
1. Edit SKILL.md to add your workflow instructions
2. Run /validate-skills weather-check to verify
3. Run /sync-skills push when ready to publish
```
