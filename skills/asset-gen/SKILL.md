---
name: asset-gen
description: This skill should be used when generating app icons, splash screens, store assets, or marketing materials using the Gemini API. It applies when the user needs to create visual assets for Android or iOS projects, with support for iterative refinement, AI-powered evaluation, style extraction from existing projects, and automatic deployment to project directories.
version: "1.0.0"
author: Nathan Krebs
publish: true
triggers:
  - /asset-gen
---

# Asset Generation Skill

Generate professional app assets (icons, splash screens, store graphics) using the Gemini API with iterative refinement and AI-powered evaluation.

## Prerequisites

- Environment variable `GEMINI_API_KEY` must be set
- Python 3.11+ with dependencies installed

Install dependencies:

```bash
pip install -r ~/.claude/skills/asset-gen/requirements.txt
```

## Quick Start

Run the interactive wizard:

```bash
python ~/.claude/skills/asset-gen/scripts/asset_gen.py
```

With options:

```bash
python ~/.claude/skills/asset-gen/scripts/asset_gen.py --project /path/to/project --iterations 3 --variants 3
```

Custom output directory:

```bash
python ~/.claude/skills/asset-gen/scripts/asset_gen.py --output ~/MyAssets
```

Resume an interrupted session:

```bash
python ~/.claude/skills/asset-gen/scripts/asset_gen.py --resume Cloudy_20260116_220000
```

## Workflow Overview

### 1. Project Discovery

The skill auto-detects project type and existing assets:

- **Android**: Parses `build.gradle`, `AndroidManifest.xml`, checks `res/mipmap-*`
- **iOS**: Parses `Info.plist`, checks `Assets.xcassets/AppIcon.appiconset`
- **KMP**: Detects both platforms via `shared/` and platform-specific modules

### 2. Style Extraction

Builds a style profile from multiple sources:

- **Existing assets**: Analyzes colors, shapes from current icons
- **Theme files**: Extracts colors from `colors.xml`, Compose themes
- **Category inference**: Derives defaults from app category (weather = clean, game = bold)
- **Interactive confirmation**: User reviews and can modify the style profile

### 3. Certainty Calculation

AI determines prompt variation strategy based on style completeness:

| Certainty | Condition | Strategy |
|-----------|-----------|----------|
| High (>0.8) | Existing assets + colors + user confirmed | Consistent prompts |
| Medium (0.5-0.8) | Some style data available | Moderate exploration |
| Low (<0.5) | Cold start, minimal context | Wide exploration |

### 4. Iterative Generation

For each asset type:

1. Generate N variants using certainty-adjusted prompts
2. AI evaluates each variant against style requirements
3. Build on learnings for next iteration
4. Repeat for M iterations

### 5. Best Selection

After all iterations:

- AI scores all variants per asset type
- Winner marked with `_best` suffix in filename
- Single best asset selected per type

### 6. Deployment

Copies best assets to project directories with proper resizing:

- **Android**: `res/mipmap-*`, `drawable/`, Play Store icon
- **iOS**: `Assets.xcassets/AppIcon.appiconset/` with `Contents.json`

## Command Arguments

| Argument | Default | Description |
|----------|---------|-------------|
| `--project`, `-p` | Current directory | Path to project |
| `--output`, `-o` | `~/Downloads/asset-gen/{project}` | Output directory for generated assets |
| `--iterations`, `-i` | 3 | Number of generation iterations (max: 20) |
| `--variants`, `-v` | 3 | Variants generated per iteration (max: 10) |
| `--asset-types` | Auto-detect | Comma-separated: `icon,splash,feature,screenshot` |
| `--resume` | None | Resume from session ID |
| `--deploy` | True | Auto-deploy best assets to project |
| `--no-deploy` | - | Skip deployment, keep assets in output folder only |

## Asset Types

| Type | Description | Aspect Ratio | Resolution |
|------|-------------|--------------|------------|
| `icon` | App launcher icon | 1:1 | 2K (1024x1024) |
| `icon-adaptive-fg` | Android adaptive foreground | 1:1 | 2K |
| `icon-adaptive-bg` | Android adaptive background | 1:1 | 2K |
| `icon-notification` | Android notification icon | 1:1 | 1K |
| `splash` | Splash/launch screen | 9:16 | 2K |
| `feature` | Play Store feature graphic | 16:9 | 2K (1024x500) |
| `screenshot` | Store screenshot | 9:16 | 2K |
| `marketing` | Marketing banner | 16:9 | 4K |

## Output Structure

Assets are saved to `~/Downloads/asset-gen/{project_name}/` by default (customizable via `--output`):

```
~/Downloads/asset-gen/Cloudy/
├── session.json                    # Session state for resume
├── icon_iter1_v1.jpg
├── icon_iter1_v2.jpg
├── icon_iter1_v3.jpg
├── icon_iter2_v1.jpg
├── icon_iter2_v2.jpg
├── icon_iter2_v3_best.jpg          # Best selection marked
├── splash_iter1_v1.jpg
└── ...
```

## Session Management

Sessions persist full state for resume support:

```json
{
  "session_id": "Cloudy_20260116_220000",
  "project_name": "Cloudy",
  "status": "in_progress",
  "style_profile": { ... },
  "settings": { "iterations": 3, "variants": 3 },
  "iterations": { ... },
  "best_selections": { ... },
  "current_asset_type": "icon",
  "current_iteration": 2
}
```

Resume with: `--resume {session_id}`

## Platform Deployment

### Android Deployment

```
res/
├── mipmap-mdpi/ic_launcher.png      # 48x48
├── mipmap-hdpi/ic_launcher.png      # 72x72
├── mipmap-xhdpi/ic_launcher.png     # 96x96
├── mipmap-xxhdpi/ic_launcher.png    # 144x144
├── mipmap-xxxhdpi/ic_launcher.png   # 192x192
├── drawable/ic_launcher_foreground.png  # 432x432
└── drawable/ic_launcher_background.png  # 432x432
```

### iOS Deployment

```
Assets.xcassets/AppIcon.appiconset/
├── Icon-App-20x20@2x.png   # 40x40
├── Icon-App-20x20@3x.png   # 60x60
├── Icon-App-29x29@2x.png   # 58x58
├── Icon-App-29x29@3x.png   # 87x87
├── Icon-App-40x40@2x.png   # 80x80
├── Icon-App-40x40@3x.png   # 120x120
├── Icon-App-60x60@2x.png   # 120x120
├── Icon-App-60x60@3x.png   # 180x180
├── Icon-App-1024x1024@1x.png  # 1024x1024
└── Contents.json
```

## Error Handling

### Rate Limits

The generator uses exponential backoff:

1. Initial retry delay: 2 seconds
2. Max retries: 5
3. Max backoff: 60 seconds
4. User notified after each retry attempt

### Generation Failures

- Failed variants are logged but do not stop the session
- Minimum 1 variant required per iteration to continue
- Session saves progress after each iteration for safe resume

## Evaluation Criteria

Generated assets are scored on 5 criteria (0-10 scale):

| Criterion | Weight | Description |
|-----------|--------|-------------|
| Brand Alignment | 25% | Matches style profile, colors correct |
| Clarity | 25% | Readable at all sizes including 48px |
| Professionalism | 20% | App Store ready quality |
| Uniqueness | 15% | Distinctive and memorable |
| Technical | 15% | No artifacts, proper composition |

See [evaluation-criteria.md](./references/evaluation-criteria.md) for full rubric.

## References

- [Android Asset Requirements](./references/android-assets.md)
- [iOS Asset Requirements](./references/ios-assets.md)
- [Prompt Templates](./references/prompt-templates.md)
- [Evaluation Criteria](./references/evaluation-criteria.md)
