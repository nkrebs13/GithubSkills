#!/usr/bin/env python3
"""
Asset Deployer

Copies best assets from the asset_gen output directory to the project's
platform-specific asset directories with proper resizing.
"""

import json
import shutil
from pathlib import Path

from PIL import Image

from resize_icons import (
    generate_android_icons,
    generate_ios_icons,
    validate_source_image,
    ANDROID_ADAPTIVE_SIZE,
)


class Deployer:
    """Deploys generated assets to project directories."""

    def __init__(self, project_path: Path):
        self.project_path = Path(project_path).resolve()
        self.platform = self._detect_platform()

    def deploy(self, session_path: Path) -> dict[str, list[Path]]:
        """Deploy all best assets from session to project.

        Args:
            session_path: Path to session.json file

        Returns:
            Dict with lists of deployed files per platform
        """
        session_data = json.loads(session_path.read_text())
        best_selections = session_data.get("best_selections", {})

        deployed = {"android": [], "ios": []}

        for asset_type, selection in best_selections.items():
            source = Path(selection["path"])
            if not source.exists():
                print(f"Warning: {source} not found, skipping")
                continue

            if asset_type == "icon":
                if self.platform in ["android", "kmp"]:
                    deployed["android"].extend(self._deploy_android_icons(source))
                if self.platform in ["ios", "kmp"]:
                    deployed["ios"].extend(self._deploy_ios_icons(source))

            elif asset_type == "icon-adaptive-fg":
                if self.platform in ["android", "kmp"]:
                    deployed["android"].extend(
                        self._deploy_android_adaptive(source, "foreground")
                    )

            elif asset_type == "icon-adaptive-bg":
                if self.platform in ["android", "kmp"]:
                    deployed["android"].extend(
                        self._deploy_android_adaptive(source, "background")
                    )

            elif asset_type == "splash":
                # Splash screens have different deployment patterns
                pass

            elif asset_type == "feature":
                # Feature graphic stays in asset_gen for manual upload
                pass

        return deployed

    def _deploy_android_icons(self, source: Path) -> list[Path]:
        """Deploy resized icons to Android mipmap directories."""
        deployed = []

        res_dir = self._find_android_res_dir()
        if not res_dir:
            print("Warning: Could not find Android res directory")
            return deployed

        try:
            img = validate_source_image(source)
            android_files = generate_android_icons(img, res_dir)
            deployed.extend(android_files)

            for f in android_files:
                print(f"  Deployed: {f.relative_to(self.project_path)}")

        except Exception as e:
            print(f"  Error deploying Android icons: {e}")

        return deployed

    def _deploy_ios_icons(self, source: Path) -> list[Path]:
        """Deploy resized icons to iOS Assets.xcassets."""
        deployed = []

        appiconset = self._find_ios_appiconset()
        if not appiconset:
            print("Warning: Could not find iOS AppIcon.appiconset")
            return deployed

        try:
            img = validate_source_image(source)
            ios_files = generate_ios_icons(img, appiconset)
            deployed.extend(ios_files)

            for f in ios_files:
                print(f"  Deployed: {f.relative_to(self.project_path)}")

        except Exception as e:
            print(f"  Error deploying iOS icons: {e}")

        return deployed

    def _deploy_android_adaptive(
        self,
        source: Path,
        layer: str,  # "foreground" or "background"
    ) -> list[Path]:
        """Deploy adaptive icon layer to drawable directory."""
        deployed = []

        res_dir = self._find_android_res_dir()
        if not res_dir:
            return deployed

        drawable_dir = res_dir / "drawable"
        drawable_dir.mkdir(parents=True, exist_ok=True)

        try:
            img = validate_source_image(source)
            resized = img.resize(
                (ANDROID_ADAPTIVE_SIZE, ANDROID_ADAPTIVE_SIZE),
                Image.Resampling.LANCZOS
            )

            target_path = drawable_dir / f"ic_launcher_{layer}.png"
            resized.save(target_path, "PNG", optimize=True)
            deployed.append(target_path)

            print(f"  Deployed: {target_path.relative_to(self.project_path)}")

        except Exception as e:
            print(f"  Error deploying adaptive {layer}: {e}")

        return deployed

    def _find_android_res_dir(self) -> Path | None:
        """Find Android res directory."""
        patterns = [
            "app/src/main/res",
            "androidApp/src/main/res",
            "composeApp/src/androidMain/res",
        ]

        for pattern in patterns:
            res_dir = self.project_path / pattern
            if res_dir.exists():
                return res_dir

        # Fallback: search
        for res in self.project_path.rglob("**/src/main/res"):
            if res.is_dir():
                return res

        return None

    def _find_ios_appiconset(self) -> Path | None:
        """Find iOS AppIcon.appiconset directory."""
        for appiconset in self.project_path.rglob("**/AppIcon.appiconset"):
            return appiconset

        # Create if Assets.xcassets exists
        for assets in self.project_path.rglob("**/Assets.xcassets"):
            appiconset = assets / "AppIcon.appiconset"
            appiconset.mkdir(parents=True, exist_ok=True)
            return appiconset

        return None

    def _detect_platform(self) -> str:
        """Detect project platform."""
        # KMP: has both Android and iOS directories
        has_android = bool(list(self.project_path.rglob("**/build.gradle*")))
        has_ios = bool(list(self.project_path.rglob("**/*.xcodeproj"))) or \
                  bool(list(self.project_path.rglob("**/iosApp")))

        if has_android and has_ios:
            return "kmp"
        if has_android:
            return "android"
        if has_ios:
            return "ios"

        return "unknown"


def deploy_from_session(session_path: Path, project_path: Path = None) -> dict:
    """Convenience function to deploy from a session file.

    Args:
        session_path: Path to session.json
        project_path: Project path (reads from session if not provided)

    Returns:
        Dict of deployed files
    """
    session_data = json.loads(session_path.read_text())

    if project_path is None:
        # Try to infer project path from session
        project_name = session_data.get("project_name")
        # Look in common locations
        for base in [
            Path.home() / "AndroidStudioProjects",
            Path.home() / "Developer",
            Path.home() / "Projects",
        ]:
            candidate = base / project_name
            if candidate.exists():
                project_path = candidate
                break

    if project_path is None:
        raise ValueError("Could not determine project path. Please specify explicitly.")

    deployer = Deployer(project_path)
    return deployer.deploy(session_path)


def main():
    """CLI for deploying assets."""
    import argparse
    import sys

    parser = argparse.ArgumentParser(description="Deploy generated assets to project")
    parser.add_argument("session", type=Path, help="Path to session.json")
    parser.add_argument("-p", "--project", type=Path, help="Project path")

    args = parser.parse_args()

    session_path = args.session.expanduser().resolve()
    if not session_path.exists():
        print(f"Error: Session file not found: {session_path}")
        sys.exit(1)

    project_path = args.project.expanduser().resolve() if args.project else None

    print("=" * 60)
    print("DEPLOYING ASSETS")
    print("=" * 60)

    try:
        result = deploy_from_session(session_path, project_path)

        total = len(result.get("android", [])) + len(result.get("ios", []))
        print(f"\nDeployed {total} files")
        print(f"  Android: {len(result.get('android', []))}")
        print(f"  iOS: {len(result.get('ios', []))}")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
