# Asset Gen

A Claude Code skill for generating professional app assets using the Gemini API with iterative refinement and AI-powered evaluation.

## Features

- **AI-Powered Generation**: Uses Gemini to generate app icons, splash screens, and store graphics
- **Iterative Refinement**: Multiple iterations with AI evaluation to improve quality
- **Style Extraction**: Auto-detects project style from existing assets and theme files
- **Smart Prompting**: Adjusts prompt variation based on style certainty
- **Platform Aware**: Generates correct sizes for Android (mipmap, adaptive) and iOS (appiconset)
- **Auto-Deploy**: Copies resized assets directly to project directories
- **Resume Support**: Full session persistence for crash recovery

## Prerequisites

1. **GEMINI_API_KEY**: Set your Gemini API key as an environment variable

   ```bash
   export GEMINI_API_KEY="your-api-key-here"
   ```

2. **Python 3.11+** with dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Installation

Copy this skill to your Claude Code skills directory:

```bash
cp -r asset-gen ~/.claude/skills/
```

## Usage

### Interactive Wizard

```bash
python ~/.claude/skills/asset-gen/scripts/asset_gen.py
```

### With Options

```bash
# Specify project path
python asset_gen.py --project /path/to/your/app

# Custom output directory
python asset_gen.py --output ~/MyAssets

# More iterations and variants
python asset_gen.py --iterations 5 --variants 5

# Skip auto-deployment
python asset_gen.py --no-deploy
```

### Resume Interrupted Session

```bash
python asset_gen.py --resume MyApp_20260116_220000
```

## Supported Asset Types

| Type | Description | Aspect Ratio |
|------|-------------|--------------|
| `icon` | App launcher icon | 1:1 |
| `icon-adaptive-fg` | Android adaptive foreground | 1:1 |
| `icon-adaptive-bg` | Android adaptive background | 1:1 |
| `splash` | Splash/launch screen | 9:16 |
| `feature` | Play Store feature graphic | 16:9 |
| `screenshot` | Store screenshot | 9:16 |
| `marketing` | Marketing banner | 16:9 |

## Output Structure

Assets are saved to `~/Downloads/asset-gen/{project}/` by default:

```
~/Downloads/asset-gen/MyApp/
├── session.json              # Session state (for resume)
├── icon_iter1_v1.jpg
├── icon_iter1_v2.jpg
├── icon_iter2_v1_best.jpg    # Best selection
├── splash_iter1_v1.jpg
└── ...
```

## How It Works

1. **Discovery**: Analyzes your project to detect platform, existing assets, and colors
2. **Style Extraction**: Builds a style profile from theme files and infers defaults from app category
3. **Generation**: Creates N iterations × M variants using certainty-adjusted prompts
4. **Evaluation**: AI scores each variant on brand alignment, clarity, professionalism, uniqueness, and technical quality
5. **Selection**: Best variant per asset type marked with `_best` suffix
6. **Deployment**: Resizes and copies to project's `res/mipmap-*` (Android) and `AppIcon.appiconset` (iOS)

## Platform Support

- **Android**: Standard icons, adaptive icons (foreground/background), Play Store icon
- **iOS**: All AppIcon sizes with Contents.json generation
- **KMP**: Both Android and iOS assets

## License

MIT License - see [LICENSE](LICENSE)
