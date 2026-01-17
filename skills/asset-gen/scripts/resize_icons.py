#!/usr/bin/env python3
"""
Icon Resizer

Generates platform-specific icon sizes from a source image.
Supports Android (mipmap, adaptive) and iOS (AppIcon.appiconset).
"""

import json
from pathlib import Path
from typing import NamedTuple

from PIL import Image


class IconSize(NamedTuple):
    """Represents an icon size configuration."""
    width: int
    height: int
    filename: str
    scale: str = "1x"
    idiom: str = ""
    size_pt: str = ""


# Android mipmap sizes (launcher icons)
ANDROID_MIPMAP_SIZES = {
    "mipmap-mdpi": IconSize(48, 48, "ic_launcher.png"),
    "mipmap-hdpi": IconSize(72, 72, "ic_launcher.png"),
    "mipmap-xhdpi": IconSize(96, 96, "ic_launcher.png"),
    "mipmap-xxhdpi": IconSize(144, 144, "ic_launcher.png"),
    "mipmap-xxxhdpi": IconSize(192, 192, "ic_launcher.png"),
}

# Android adaptive icon size (432x432 with 108dp safe zone)
ANDROID_ADAPTIVE_SIZE = 432

# Play Store icon size
ANDROID_PLAY_STORE_SIZE = IconSize(512, 512, "play_store_icon.png")

# iOS App Icon configurations: (size_pt, scale, idiom)
IOS_ICON_CONFIGS = [
    # iPhone icons
    (20, "2x", "iphone"),
    (20, "3x", "iphone"),
    (29, "2x", "iphone"),
    (29, "3x", "iphone"),
    (40, "2x", "iphone"),
    (40, "3x", "iphone"),
    (60, "2x", "iphone"),
    (60, "3x", "iphone"),
    # iPad icons
    (20, "1x", "ipad"),
    (20, "2x", "ipad"),
    (29, "1x", "ipad"),
    (29, "2x", "ipad"),
    (40, "1x", "ipad"),
    (40, "2x", "ipad"),
    (76, "1x", "ipad"),
    (76, "2x", "ipad"),
    (83.5, "2x", "ipad"),
    # App Store
    (1024, "1x", "ios-marketing"),
]


def get_scale_multiplier(scale: str) -> int:
    """Convert scale string to multiplier."""
    return int(scale.replace("x", ""))


def generate_ios_icon_sizes() -> list[IconSize]:
    """Generate list of iOS icon sizes with filenames."""
    sizes = []
    for size_pt, scale, idiom in IOS_ICON_CONFIGS:
        multiplier = get_scale_multiplier(scale)
        pixel_size = int(size_pt * multiplier)

        # Generate filename
        if size_pt == int(size_pt):
            size_str = str(int(size_pt))
        else:
            size_str = str(size_pt).replace(".", "_")

        filename = f"Icon-App-{size_str}x{size_str}@{scale}.png"

        sizes.append(IconSize(
            width=pixel_size,
            height=pixel_size,
            filename=filename,
            scale=scale,
            idiom=idiom,
            size_pt=f"{size_pt}x{size_pt}"
        ))

    return sizes


def resize_image(source: Image.Image, size: tuple[int, int]) -> Image.Image:
    """Resize image using high-quality LANCZOS resampling."""
    return source.resize(size, Image.Resampling.LANCZOS)


def validate_source_image(source_path: Path) -> Image.Image:
    """Validate and load source image."""
    if not source_path.exists():
        raise FileNotFoundError(f"Source image not found: {source_path}")

    img = Image.open(source_path)

    # Convert to RGBA if necessary
    if img.mode != "RGBA":
        img = img.convert("RGBA")

    # Warnings
    if img.width < 1024 or img.height < 1024:
        print(f"Warning: Source is {img.width}x{img.height}. "
              f"Recommended minimum is 1024x1024.")

    if img.width != img.height:
        print(f"Warning: Source is not square ({img.width}x{img.height}).")

    return img


def generate_android_icons(source: Image.Image, output_dir: Path) -> list[Path]:
    """Generate all Android mipmap icons."""
    generated = []

    # Mipmap icons
    for mipmap_dir, icon_size in ANDROID_MIPMAP_SIZES.items():
        target_dir = output_dir / mipmap_dir
        target_dir.mkdir(parents=True, exist_ok=True)

        resized = resize_image(source, (icon_size.width, icon_size.height))
        output_path = target_dir / icon_size.filename

        resized.save(output_path, "PNG", optimize=True)
        generated.append(output_path)

    # Adaptive icon foreground (432x432)
    drawable_dir = output_dir / "drawable"
    drawable_dir.mkdir(parents=True, exist_ok=True)

    adaptive_fg = resize_image(source, (ANDROID_ADAPTIVE_SIZE, ANDROID_ADAPTIVE_SIZE))
    adaptive_fg_path = drawable_dir / "ic_launcher_foreground.png"
    adaptive_fg.save(adaptive_fg_path, "PNG", optimize=True)
    generated.append(adaptive_fg_path)

    # Play Store icon (512x512)
    play_store_icon = resize_image(
        source,
        (ANDROID_PLAY_STORE_SIZE.width, ANDROID_PLAY_STORE_SIZE.height)
    )
    play_store_path = output_dir / ANDROID_PLAY_STORE_SIZE.filename
    play_store_icon.save(play_store_path, "PNG", optimize=True)
    generated.append(play_store_path)

    return generated


def generate_ios_icons(source: Image.Image, output_dir: Path) -> list[Path]:
    """Generate all iOS app icons and Contents.json."""
    generated = []
    output_dir.mkdir(parents=True, exist_ok=True)

    ios_sizes = generate_ios_icon_sizes()
    generated_sizes: dict[tuple[int, int], Path] = {}

    for icon_size in ios_sizes:
        size_key = (icon_size.width, icon_size.height)

        if size_key in generated_sizes:
            # Copy existing if same size
            import shutil
            existing_path = generated_sizes[size_key]
            output_path = output_dir / icon_size.filename
            if existing_path != output_path:
                shutil.copy(existing_path, output_path)
        else:
            resized = resize_image(source, (icon_size.width, icon_size.height))
            output_path = output_dir / icon_size.filename
            resized.save(output_path, "PNG", optimize=True)
            generated_sizes[size_key] = output_path

        generated.append(output_path)

    # Generate Contents.json
    contents_json = generate_ios_contents_json(ios_sizes)
    contents_path = output_dir / "Contents.json"
    contents_path.write_text(json.dumps(contents_json, indent=2))
    generated.append(contents_path)

    return generated


def generate_ios_contents_json(ios_sizes: list[IconSize]) -> dict:
    """Generate iOS Contents.json for AppIcon.appiconset."""
    images = []

    for icon_size in ios_sizes:
        image_entry = {
            "filename": icon_size.filename,
            "idiom": icon_size.idiom,
            "scale": icon_size.scale,
            "size": icon_size.size_pt
        }
        images.append(image_entry)

    return {
        "images": images,
        "info": {
            "author": "xcode",
            "version": 1
        }
    }


def resize_for_platform(
    source_path: Path,
    output_dir: Path,
    platform: str = "both",
) -> dict[str, list[Path]]:
    """Resize source icon for specified platform(s).

    Args:
        source_path: Path to source icon (1024x1024 recommended)
        output_dir: Base output directory
        platform: "android", "ios", or "both"

    Returns:
        Dict with lists of generated files per platform
    """
    source = validate_source_image(source_path)
    result = {"android": [], "ios": []}

    if platform in ["android", "both"]:
        android_dir = output_dir / "android" if platform == "both" else output_dir
        result["android"] = generate_android_icons(source, android_dir)

    if platform in ["ios", "both"]:
        ios_dir = output_dir / "ios" if platform == "both" else output_dir
        result["ios"] = generate_ios_icons(source, ios_dir)

    return result


def main():
    """CLI for icon resizing."""
    import argparse
    import sys

    parser = argparse.ArgumentParser(description="Resize app icon for Android/iOS")
    parser.add_argument("source", type=Path, help="Source icon (1024x1024 PNG)")
    parser.add_argument("-o", "--output", type=Path, default=Path.cwd(),
                        help="Output directory")
    parser.add_argument("-p", "--platform", choices=["android", "ios", "both"],
                        default="both", help="Target platform(s)")

    args = parser.parse_args()

    source_path = args.source.expanduser().resolve()
    output_dir = args.output.expanduser().resolve()

    print(f"Source: {source_path}")
    print(f"Output: {output_dir}")
    print(f"Platform: {args.platform}")

    try:
        result = resize_for_platform(source_path, output_dir, args.platform)

        print(f"\nGenerated {len(result['android'])} Android icons")
        print(f"Generated {len(result['ios'])} iOS icons")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
