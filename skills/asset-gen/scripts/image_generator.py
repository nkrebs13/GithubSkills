#!/usr/bin/env python3
"""
Image Generator

Wrapper for Gemini API with retry logic and rate limit handling.
Uses the best available Gemini image generation model.
"""

import os
import time
from pathlib import Path
from typing import Any

from google import genai
from google.genai import types


class ImageGenerator:
    """Gemini-based image generator with retry and rate limit handling."""

    # Asset type configurations: aspect ratio and resolution
    ASSET_CONFIGS = {
        "icon": {"aspect_ratio": "1:1", "image_size": "2K"},
        "icon-adaptive-fg": {"aspect_ratio": "1:1", "image_size": "2K"},
        "icon-adaptive-bg": {"aspect_ratio": "1:1", "image_size": "2K"},
        "icon-notification": {"aspect_ratio": "1:1", "image_size": "1K"},
        "splash": {"aspect_ratio": "9:16", "image_size": "2K"},
        "feature": {"aspect_ratio": "16:9", "image_size": "2K"},
        "screenshot": {"aspect_ratio": "9:16", "image_size": "2K"},
        "marketing": {"aspect_ratio": "16:9", "image_size": "4K"},
    }

    def __init__(
        self,
        model: str = "gemini-3-pro-image-preview",
        max_retries: int = 5,
        base_delay: float = 2.0,
        max_delay: float = 60.0,
    ):
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise EnvironmentError(
                "GEMINI_API_KEY environment variable not set. "
                "Add it to your ~/.zshrc or export it in your shell."
            )

        self.client = genai.Client(api_key=api_key)
        self.model = model
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.max_delay = max_delay

    def generate(
        self,
        prompt: str,
        asset_type: str,
        output_dir: Path,
        iteration: int,
        variant: int,
    ) -> dict[str, Any] | None:
        """Generate an image with retry logic.

        Args:
            prompt: The generation prompt
            asset_type: Type of asset (icon, splash, etc.)
            output_dir: Directory to save the image
            iteration: Current iteration number
            variant: Current variant number

        Returns:
            Dict with path, filename, and metadata, or None on failure.
        """
        config = self.ASSET_CONFIGS.get(
            asset_type,
            {"aspect_ratio": "1:1", "image_size": "2K"}
        )

        # Gemini returns JPEG by default - use .jpg extension
        filename = f"{asset_type}_iter{iteration}_v{variant}.jpg"
        output_path = output_dir / filename

        for attempt in range(self.max_retries):
            try:
                response = self.client.models.generate_content(
                    model=self.model,
                    contents=[prompt],
                    config=types.GenerateContentConfig(
                        response_modalities=["TEXT", "IMAGE"],
                        image_config=types.ImageConfig(**config),
                    ),
                )

                # Extract image from response
                for part in response.parts:
                    if part.inline_data:
                        image = part.as_image()
                        image.save(str(output_path))

                        return {
                            "path": str(output_path),
                            "filename": filename,
                            "asset_type": asset_type,
                            "iteration": iteration,
                            "variant": variant,
                            "config": config,
                        }

                # No image in response
                return None

            except Exception as e:
                error_str = str(e).lower()

                # Check for rate limit errors
                if "rate" in error_str or "quota" in error_str or "429" in error_str:
                    # Skip sleeping on final attempt
                    if attempt < self.max_retries - 1:
                        delay = min(self.base_delay * (2 ** attempt), self.max_delay)
                        print(f"  Rate limited. Retrying in {delay:.1f}s (attempt {attempt + 1}/{self.max_retries})")
                        time.sleep(delay)
                else:
                    # Non-rate-limit error, don't retry
                    print(f"  Generation error: {e}")
                    return None

        print(f"  Max retries exceeded for {asset_type}")
        return None

    @staticmethod
    def get_supported_asset_types() -> list[str]:
        """Return list of supported asset types."""
        return list(ImageGenerator.ASSET_CONFIGS.keys())
