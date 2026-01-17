#!/usr/bin/env python3
"""
Asset Evaluator

Scores generated assets using AI-powered analysis against style requirements.
Uses Gemini's vision capabilities to evaluate image quality and brand alignment.
"""

import json
import os
from pathlib import Path

from PIL import Image

from google import genai
from google.genai import types


class AssetEvaluator:
    """AI-powered asset evaluation and scoring."""

    EVALUATION_PROMPT = """Evaluate this {asset_type} image for a mobile app.

Style Requirements:
{style_requirements}

Score the image on these criteria (0-10 each):
1. **Brand Alignment**: Does it match the specified style, colors, and aesthetic?
2. **Clarity**: Is the design clear and readable at small sizes (48px for icons)?
3. **Professionalism**: Does it look polished and app-store ready?
4. **Uniqueness**: Is it distinctive and memorable?
5. **Technical Quality**: No artifacts, proper composition, good contrast?

IMPORTANT: Respond with ONLY a valid JSON object, no other text:
{{"brand_alignment": <0-10>, "clarity": <0-10>, "professionalism": <0-10>, "uniqueness": <0-10>, "technical": <0-10>, "overall": <0-10>, "notes": "<brief feedback>"}}
"""

    # Scoring weights
    WEIGHTS = {
        "brand_alignment": 0.25,
        "clarity": 0.25,
        "professionalism": 0.20,
        "uniqueness": 0.15,
        "technical": 0.15,
    }

    def __init__(self, model: str = "gemini-3-pro-image-preview"):
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise EnvironmentError("GEMINI_API_KEY not set")

        self.client = genai.Client(api_key=api_key)
        self.model = model

    def evaluate(
        self,
        image_path: str | Path,
        asset_type: str,
        style_profile: dict,
    ) -> float:
        """Evaluate an image and return overall score (0-1).

        Args:
            image_path: Path to the image file
            asset_type: Type of asset being evaluated
            style_profile: Style requirements to evaluate against

        Returns:
            Overall score from 0.0 to 1.0
        """
        try:
            image = Image.open(image_path)

            style_requirements = self._format_style_requirements(style_profile)
            prompt = self.EVALUATION_PROMPT.format(
                asset_type=asset_type,
                style_requirements=style_requirements,
            )

            response = self.client.models.generate_content(
                model=self.model,
                contents=[prompt, image],
                config=types.GenerateContentConfig(
                    response_modalities=["TEXT"],
                ),
            )

            # Parse JSON response
            result = self._parse_evaluation_response(response.text)

            if result:
                # Calculate weighted score
                weighted_score = self._calculate_weighted_score(result)
                return weighted_score

            return 0.5  # Default neutral score on parse error

        except Exception as e:
            print(f"  Evaluation error: {e}")
            return 0.5

    def _format_style_requirements(self, style_profile: dict) -> str:
        """Format style profile for the evaluation prompt."""
        parts = []

        # Colors
        if style_profile.get("colors"):
            colors = style_profile["colors"][:5]
            parts.append(f"Colors: {', '.join(colors)}")

        # Inferred style
        if style_profile.get("inferred_style"):
            style = style_profile["inferred_style"]
            if style.get("aesthetic"):
                parts.append(f"Aesthetic: {style['aesthetic']}")
            if style.get("colors"):
                parts.append(f"Color palette: {style['colors']}")
            if style.get("iconography"):
                parts.append(f"Iconography: {style['iconography']}")

        # Category
        if style_profile.get("category"):
            parts.append(f"App category: {style_profile['category']}")

        if not parts:
            return "Professional, modern mobile app design. Clean, clear, app-store ready."

        return "\n".join(parts)

    def _parse_evaluation_response(self, response_text: str) -> dict | None:
        """Parse JSON from evaluation response."""
        try:
            # Try direct JSON parse
            return json.loads(response_text.strip())
        except json.JSONDecodeError:
            pass

        # Try to extract JSON from response
        try:
            # Look for JSON object in response
            start = response_text.find("{")
            end = response_text.rfind("}") + 1
            if start >= 0 and end > start:
                json_str = response_text[start:end]
                return json.loads(json_str)
        except json.JSONDecodeError:
            pass

        return None

    def _calculate_weighted_score(self, scores: dict) -> float:
        """Calculate weighted overall score (0-1)."""
        total = 0.0
        weight_sum = 0.0

        for criterion, weight in self.WEIGHTS.items():
            if criterion in scores:
                # Normalize from 0-10 to 0-1
                total += (scores[criterion] / 10.0) * weight
                weight_sum += weight

        if weight_sum > 0:
            return total / weight_sum

        # Fallback to 'overall' if individual scores missing
        if "overall" in scores:
            return scores["overall"] / 10.0

        return 0.5
