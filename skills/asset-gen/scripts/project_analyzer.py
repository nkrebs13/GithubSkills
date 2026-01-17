#!/usr/bin/env python3
"""
Project Analyzer

Detects project type, existing assets, and extracts style information
from Android, iOS, KMP, and other project types.
"""

import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any


class ProjectAnalyzer:
    """Analyzes project structure and extracts style information."""

    # Category keywords for style inference
    CATEGORY_KEYWORDS = {
        "weather": ["weather", "forecast", "climate", "temperature", "rain", "sun", "cloud"],
        "game": ["game", "play", "level", "score", "player", "arcade"],
        "finance": ["finance", "bank", "money", "payment", "wallet", "crypto", "stock"],
        "health": ["health", "fitness", "workout", "medical", "wellness", "diet"],
        "social": ["social", "chat", "message", "friend", "community", "feed"],
        "productivity": ["task", "todo", "note", "calendar", "schedule", "reminder"],
        "travel": ["travel", "trip", "flight", "hotel", "map", "navigation"],
        "food": ["food", "recipe", "restaurant", "delivery", "meal", "cook"],
        "music": ["music", "audio", "song", "playlist", "podcast", "radio"],
        "photo": ["photo", "camera", "gallery", "image", "filter", "edit"],
        "news": ["news", "article", "feed", "magazine", "blog"],
        "education": ["learn", "study", "course", "education", "quiz", "flashcard"],
        "ecommerce": ["shop", "store", "cart", "product", "buy", "sell"],
        "space": ["space", "rocket", "launch", "astronaut", "satellite", "orbit"],
    }

    # Default styles by category
    CATEGORY_STYLES = {
        "weather": {
            "aesthetic": "clean, minimal, airy, light",
            "colors": "sky blue, white, soft gradients, cloud gray",
            "iconography": "simple weather symbols, thin lines, rounded",
        },
        "game": {
            "aesthetic": "bold, playful, dynamic, energetic",
            "colors": "vibrant, high contrast, gradients, neon accents",
            "iconography": "mascot-friendly, 3D depth, fun shapes",
        },
        "finance": {
            "aesthetic": "professional, trustworthy, clean, secure",
            "colors": "navy, green, gold accents, white",
            "iconography": "geometric, symmetric, minimal, sharp",
        },
        "health": {
            "aesthetic": "calming, approachable, organic, fresh",
            "colors": "green, teal, soft pastels, white",
            "iconography": "rounded, friendly, nature-inspired",
        },
        "social": {
            "aesthetic": "friendly, vibrant, modern, connected",
            "colors": "bright primaries, gradients, white",
            "iconography": "speech bubbles, people, hearts, rounded",
        },
        "productivity": {
            "aesthetic": "focused, efficient, clean, organized",
            "colors": "blue, gray, white, accent color",
            "iconography": "checkmarks, lists, geometric, minimal",
        },
        "travel": {
            "aesthetic": "adventurous, exciting, worldly",
            "colors": "sky blue, earth tones, sunset orange",
            "iconography": "maps, planes, landmarks, compass",
        },
        "food": {
            "aesthetic": "warm, appetizing, inviting",
            "colors": "warm reds, orange, green, cream",
            "iconography": "utensils, plates, ingredients, rounded",
        },
        "music": {
            "aesthetic": "dynamic, rhythmic, expressive",
            "colors": "purple, pink, black, neon",
            "iconography": "notes, waves, headphones, abstract",
        },
        "photo": {
            "aesthetic": "creative, artistic, visual",
            "colors": "gradient, colorful, black/white contrast",
            "iconography": "camera, aperture, frames, filters",
        },
        "space": {
            "aesthetic": "cosmic, futuristic, dynamic, awe-inspiring",
            "colors": "deep navy, flame orange, cosmic blue, star white",
            "iconography": "rockets, stars, planets, orbits, gradients",
        },
        "default": {
            "aesthetic": "modern, clean, professional",
            "colors": "balanced palette with primary accent color",
            "iconography": "clear, recognizable, scalable, minimal",
        },
    }

    def __init__(self, project_path: Path):
        self.project_path = Path(project_path).resolve()

    def analyze(self) -> dict[str, Any]:
        """Perform full project analysis."""
        platform = self._detect_platform()

        return {
            "platform": platform,
            "project_name": self._extract_project_name(platform),
            "package_name": self._extract_package_name(platform),
            "existing_assets": self._find_existing_assets(platform),
            "suggested_assets": self._suggest_assets(platform),
            "app_category": self._infer_category(),
        }

    def _detect_platform(self) -> str:
        """Detect project platform from file markers."""
        markers = {
            "kmp": [
                ("shared/build.gradle.kts", "composeApp"),
                ("shared/build.gradle", "iosApp"),
                ("composeApp/build.gradle.kts", "iosApp"),
            ],
            "android": [
                ("app/build.gradle.kts", None),
                ("app/build.gradle", None),
                ("build.gradle.kts", "android"),
                ("build.gradle", "android"),
            ],
            "ios": [
                ("*.xcodeproj", None),
                ("Package.swift", None),
                ("Info.plist", None),
            ],
            "flutter": [
                ("pubspec.yaml", None),
            ],
            "react-native": [
                ("app.json", "react-native"),
                ("metro.config.js", None),
            ],
        }

        # Check KMP first (has both Android and iOS)
        for primary, secondary in markers["kmp"]:
            if list(self.project_path.rglob(primary)):
                if secondary is None or list(self.project_path.rglob(f"*{secondary}*")):
                    return "kmp"

        # Check other platforms
        for platform in ["android", "ios", "flutter", "react-native"]:
            for primary, secondary in markers.get(platform, []):
                matches = list(self.project_path.rglob(primary))
                if matches:
                    if secondary is None:
                        return platform
                    # Check file content for keyword
                    for match in matches:
                        if match.is_file():
                            try:
                                content = match.read_text()
                                if secondary in content:
                                    return platform
                            except (OSError, UnicodeDecodeError):
                                pass

        return "unknown"

    def _extract_project_name(self, platform: str) -> str:
        """Extract project/app name from config files."""
        if platform in ["android", "kmp"]:
            # Try AndroidManifest.xml
            for manifest in self.project_path.rglob("**/AndroidManifest.xml"):
                try:
                    tree = ET.parse(manifest)
                    ns = {"android": "http://schemas.android.com/apk/res/android"}
                    app = tree.find(".//application", ns)
                    if app is not None:
                        label = app.get("{http://schemas.android.com/apk/res/android}label")
                        if label and not label.startswith("@"):
                            return label
                except (ET.ParseError, OSError):
                    pass

            # Try strings.xml for app_name
            for strings in self.project_path.rglob("**/strings.xml"):
                try:
                    tree = ET.parse(strings)
                    for string in tree.findall(".//string[@name='app_name']"):
                        if string.text:
                            return string.text
                except (ET.ParseError, OSError):
                    pass

        if platform in ["ios", "kmp"]:
            # Try Info.plist
            for plist in self.project_path.rglob("**/Info.plist"):
                try:
                    content = plist.read_text()
                    # Simple regex for CFBundleDisplayName or CFBundleName
                    match = re.search(
                        r"<key>CFBundleDisplayName</key>\s*<string>([^<]+)</string>",
                        content
                    )
                    if match:
                        return match.group(1)
                    match = re.search(
                        r"<key>CFBundleName</key>\s*<string>([^<]+)</string>",
                        content
                    )
                    if match:
                        return match.group(1)
                except (OSError, UnicodeDecodeError):
                    pass

        # Fallback to directory name
        return self.project_path.name

    def _extract_package_name(self, platform: str) -> str | None:
        """Extract package/bundle identifier."""
        if platform in ["android", "kmp"]:
            # Try AndroidManifest.xml
            for manifest in self.project_path.rglob("**/AndroidManifest.xml"):
                try:
                    tree = ET.parse(manifest)
                    root = tree.getroot()
                    package = root.get("package")
                    if package:
                        return package
                except (ET.ParseError, OSError):
                    pass

            # Try build.gradle for applicationId
            for gradle in self.project_path.rglob("**/build.gradle*"):
                try:
                    content = gradle.read_text()
                    match = re.search(r'applicationId\s*[=:]\s*["\']([^"\']+)["\']', content)
                    if match:
                        return match.group(1)
                except (OSError, UnicodeDecodeError):
                    pass

        return None

    def _find_existing_assets(self, platform: str) -> dict[str, list[str]]:
        """Find existing asset files in the project."""
        assets = {"icons": [], "splash": [], "feature": [], "other": []}

        if platform in ["android", "kmp"]:
            # Check mipmap directories
            for mipmap in self.project_path.rglob("**/mipmap-*/ic_launcher*.png"):
                assets["icons"].append(str(mipmap))

            # Check drawable for adaptive icons
            for drawable in self.project_path.rglob("**/drawable*/ic_launcher*.png"):
                assets["icons"].append(str(drawable))
            for drawable in self.project_path.rglob("**/drawable*/ic_launcher*.xml"):
                assets["icons"].append(str(drawable))

        if platform in ["ios", "kmp"]:
            # Check AppIcon.appiconset
            for icon in self.project_path.rglob("**/AppIcon.appiconset/*.png"):
                assets["icons"].append(str(icon))

        # Deduplicate
        for key in assets:
            assets[key] = list(set(assets[key]))

        return assets

    def _suggest_assets(self, platform: str) -> list[str]:
        """Suggest which assets to generate based on platform."""
        base_assets = ["icon"]

        if platform in ["android", "kmp"]:
            base_assets.extend(["icon-adaptive-fg", "icon-adaptive-bg", "feature"])

        if platform in ["ios", "kmp"]:
            # iOS uses standard icons, no adaptive
            pass

        base_assets.append("splash")

        return base_assets

    def extract_style(self) -> dict[str, Any]:
        """Extract style profile from project."""
        colors = self._extract_colors()
        existing = self._analyze_existing_assets()
        category = self._infer_category()
        inferred = self._get_style_for_category(category)

        # Calculate certainty
        certainty = 0.5  # Base
        if colors:
            certainty += 0.15
        if existing.get("has_assets"):
            certainty += 0.2
        # User confirmation adds 0.15 (done in orchestrator)

        return {
            "colors": colors,
            "existing_assets": existing,
            "category": category,
            "inferred_style": inferred,
            "certainty": min(certainty, 1.0),
            "user_confirmed": False,
        }

    def _extract_colors(self) -> list[str]:
        """Extract color palette from theme files."""
        colors = []

        # Android colors.xml
        for colors_xml in self.project_path.rglob("**/colors.xml"):
            try:
                tree = ET.parse(colors_xml)
                for color in tree.findall(".//color"):
                    if color.text:
                        colors.append(color.text.strip())
            except (ET.ParseError, OSError):
                pass

        # Compose theme files (Kotlin)
        for kt_file in self.project_path.rglob("**/*Theme*.kt"):
            try:
                content = kt_file.read_text()
                # Match Color(0xFFRRGGBB) patterns
                hex_colors = re.findall(r"Color\(0x([0-9A-Fa-f]{8})\)", content)
                for hex_color in hex_colors:
                    # Convert to #RRGGBB (skip alpha)
                    colors.append(f"#{hex_color[2:]}")
            except (OSError, UnicodeDecodeError):
                pass

        # Color.kt or Colors.kt files
        for kt_file in self.project_path.rglob("**/*Color*.kt"):
            try:
                content = kt_file.read_text()
                hex_colors = re.findall(r"Color\(0x([0-9A-Fa-f]{8})\)", content)
                for hex_color in hex_colors:
                    colors.append(f"#{hex_color[2:]}")
            except (OSError, UnicodeDecodeError):
                pass

        # Deduplicate and limit
        return list(set(colors))[:10]

    def _analyze_existing_assets(self) -> dict[str, Any]:
        """Analyze existing assets for style information."""
        platform = self._detect_platform()
        existing = self._find_existing_assets(platform)

        has_assets = any(len(v) > 0 for v in existing.values())

        if has_assets:
            # Get the largest/best quality icon for reference
            icon_paths = existing.get("icons", [])
            best_icon = None
            if icon_paths:
                # Prefer larger icons
                for path in sorted(icon_paths, reverse=True):
                    if "xxxhdpi" in path or "1024" in path:
                        best_icon = path
                        break
                if not best_icon:
                    best_icon = icon_paths[0]

            return {
                "has_assets": True,
                "icon_count": len(existing.get("icons", [])),
                "best_icon_path": best_icon,
            }

        return {"has_assets": False}

    def _infer_category(self) -> str:
        """Infer app category from project structure and keywords."""
        # Collect text to analyze
        text_sources = []

        # Project name
        text_sources.append(self.project_path.name.lower())

        # Package name
        package = self._extract_package_name(self._detect_platform())
        if package:
            text_sources.append(package.lower())

        # App name from strings.xml
        for strings in self.project_path.rglob("**/strings.xml"):
            try:
                tree = ET.parse(strings)
                for string in tree.findall(".//string"):
                    if string.text:
                        text_sources.append(string.text.lower())
            except (ET.ParseError, OSError):
                pass

        # CLAUDE.md if present
        claude_md = self.project_path / "CLAUDE.md"
        if claude_md.exists():
            try:
                text_sources.append(claude_md.read_text().lower())
            except (OSError, UnicodeDecodeError):
                pass

        # Score categories
        combined_text = " ".join(text_sources)
        scores = {}

        for category, keywords in self.CATEGORY_KEYWORDS.items():
            score = sum(1 for kw in keywords if kw in combined_text)
            if score > 0:
                scores[category] = score

        if scores:
            return max(scores, key=scores.get)

        return "default"

    def _get_style_for_category(self, category: str) -> dict[str, str]:
        """Get default style for a category."""
        return self.CATEGORY_STYLES.get(category, self.CATEGORY_STYLES["default"])


def main():
    """CLI for testing project analysis."""
    import sys

    if len(sys.argv) < 2:
        print("Usage: python project_analyzer.py <project_path>")
        sys.exit(1)

    project_path = Path(sys.argv[1]).resolve()
    if not project_path.exists():
        print(f"Error: {project_path} does not exist")
        sys.exit(1)

    analyzer = ProjectAnalyzer(project_path)

    print("=" * 60)
    print("PROJECT ANALYSIS")
    print("=" * 60)

    info = analyzer.analyze()
    print(f"\nPlatform: {info['platform']}")
    print(f"Project Name: {info['project_name']}")
    print(f"Package: {info.get('package_name', 'N/A')}")
    print(f"Category: {info['app_category']}")

    print("\nExisting Assets:")
    for asset_type, paths in info['existing_assets'].items():
        if paths:
            print(f"  {asset_type}: {len(paths)} found")

    print(f"\nSuggested Assets: {', '.join(info['suggested_assets'])}")

    print("\n" + "=" * 60)
    print("STYLE PROFILE")
    print("=" * 60)

    style = analyzer.extract_style()
    print(f"\nColors Found: {len(style['colors'])}")
    for color in style['colors'][:5]:
        print(f"  - {color}")

    print(f"\nInferred Style ({style['category']}):")
    for key, value in style['inferred_style'].items():
        print(f"  {key}: {value}")

    print(f"\nCertainty: {style['certainty']:.2f}")


if __name__ == "__main__":
    main()
