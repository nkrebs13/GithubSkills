#!/usr/bin/env python3
"""
Asset Generation Orchestrator

Main entry point for the asset-gen skill. Coordinates project analysis,
style extraction, iterative generation, evaluation, and deployment.

Usage:
    python asset_gen.py                           # Interactive wizard
    python asset_gen.py --project /path/to/app    # Specify project
    python asset_gen.py --resume session_123      # Resume session
"""

import argparse
import sys
from pathlib import Path
from typing import Any

from project_analyzer import ProjectAnalyzer
from image_generator import ImageGenerator
from asset_evaluator import AssetEvaluator
from session_manager import SessionManager, find_session_by_id
from deployer import Deployer


# Prompt templates for different asset types
ASSET_PROMPTS = {
    "icon": """Design a professional app icon for '{app_name}'.

Style: {aesthetic}
Colors: {colors}
Iconography: {iconography}

Requirements:
- Square format, App Store ready
- No text unless the brand requires it
- Professional quality, polished finish
- Clean edges, no artifacts
- Must read clearly at small sizes (48px)

{variation_directive}
""",

    "icon-adaptive-fg": """Design the FOREGROUND layer for an Android adaptive app icon for '{app_name}'.

This is the foreground layer that will be composited over a background layer.
The design should have transparent or semi-transparent areas to let the background show through.

Style: {aesthetic}
Colors: {colors}
Iconography: {iconography}

Requirements:
- Must work as a composited layer
- Central element should be within the safe zone (centered 66% of canvas)
- Professional quality
- PNG with transparency where appropriate

{variation_directive}
""",

    "icon-adaptive-bg": """Design the BACKGROUND layer for an Android adaptive app icon.

This layer will appear behind the foreground icon layer for '{app_name}'.
It should complement the brand without distracting from the foreground.

Style: {aesthetic}
Colors: {colors}

Requirements:
- Solid color, gradient, or subtle pattern
- Must complement the app's brand
- No complex details (will be partially covered)
- Professional quality

{variation_directive}
""",

    "splash": """Create a mobile splash screen for '{app_name}'.

Style: {aesthetic}
Colors: {colors}

Layout:
- App name or logo centered
- Premium, polished appearance
- Portrait orientation (9:16)
- Should feel like a luxury app loading experience

{variation_directive}
""",

    "feature": """Design a Play Store feature graphic for '{app_name}'.

Style: {aesthetic}
Colors: {colors}

Requirements:
- Wide landscape format (16:9, 1024x500)
- App name prominently displayed
- Compelling visual that represents the app
- Professional marketing quality
- Text readable at thumbnail size

{variation_directive}
""",
}

# Variation directives based on certainty
VARIATION_DIRECTIVES = {
    "high": [
        "Create a polished version maintaining the established style.",
        "Refine with subtle polish and perfect execution.",
        "Perfect the established design direction.",
    ],
    "medium": [
        "Try a slightly bolder approach with the color palette.",
        "Experiment with a more minimal interpretation.",
        "Focus on iconography that's immediately recognizable.",
        "Add subtle depth and dimension.",
    ],
    "low": [
        "Explore a clean, minimalist geometric approach.",
        "Try a bold, vibrant, modern interpretation.",
        "Create an abstract, artistic version.",
        "Design with playful, friendly aesthetics.",
        "Focus on professional, trustworthy appearance.",
        "Experiment with gradient depth and dimension.",
    ],
}


class AssetGenOrchestrator:
    """Main orchestrator for asset generation workflow."""

    # Bounds for user inputs
    MAX_ITERATIONS = 20
    MAX_VARIANTS = 10
    MIN_VALUE = 1

    def __init__(
        self,
        project_path: Path,
        output_base: Path | None = None,
        iterations: int = 3,
        variants: int = 3,
        auto_deploy: bool = True,
    ):
        self.project_path = project_path.resolve()
        self.iterations = max(self.MIN_VALUE, min(iterations, self.MAX_ITERATIONS))
        self.variants = max(self.MIN_VALUE, min(variants, self.MAX_VARIANTS))
        self.auto_deploy = auto_deploy

        # Derive output directory (default: ~/Downloads/asset-gen/{project})
        if output_base is None:
            output_base = Path.home() / "Downloads" / "asset-gen"
        self.project_name = self._sanitize_name(project_path.name)
        self.output_dir = (output_base / self.project_name).resolve()
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Initialize components
        self.analyzer = ProjectAnalyzer(project_path)
        self.generator = ImageGenerator()
        self.evaluator = AssetEvaluator()
        self.session = SessionManager(self.output_dir / "session.json")
        self.deployer = Deployer(project_path)

    @staticmethod
    def _sanitize_name(name: str) -> str:
        """Sanitize a name for safe use in paths."""
        import re
        # Remove path separators and traversal
        sanitized = re.sub(r'[/\\]', '', name)
        sanitized = re.sub(r'\.\.+', '', sanitized)
        # Keep alphanumeric, underscore, hyphen, space
        sanitized = re.sub(r'[^a-zA-Z0-9_\- ]', '', sanitized)
        return sanitized[:100] if sanitized else "project"

    def run_wizard(self) -> None:
        """Run interactive wizard for asset generation."""
        print("=" * 60)
        print("ASSET GENERATION WIZARD")
        print("=" * 60)

        # Step 1: Analyze project
        print("\n[1/5] Analyzing project...")
        project_info = self.analyzer.analyze()
        self._display_project_info(project_info)

        # Step 2: Confirm assets to generate
        print("\n[2/5] Asset Selection")
        asset_types = self._confirm_asset_types(project_info["suggested_assets"])

        # Step 3: Extract/confirm style
        print("\n[3/5] Style Profile")
        style_profile = self.analyzer.extract_style()
        style_profile = self._confirm_style(style_profile, project_info["project_name"])

        # Step 4: Confirm settings
        print("\n[4/5] Generation Settings")
        settings = self._confirm_settings()

        # Step 5: Generate assets
        print("\n[5/5] Generating Assets...")
        self._run_generation(asset_types, style_profile, settings)

    def resume(self, session_id: str) -> None:
        """Resume from a previous session."""
        print("=" * 60)
        print("RESUMING ASSET GENERATION")
        print("=" * 60)

        # Find and load session
        session_path = find_session_by_id(session_id)
        if not session_path:
            print(f"Error: Session '{session_id}' not found")
            sys.exit(1)

        # Update output dir based on found session
        self.output_dir = session_path.parent
        self.session = SessionManager(session_path)
        self.session.load(session_id)

        print(f"\nSession: {session_id}")
        print(f"Project: {self.session.get_project_name()}")

        # Get resume point
        current_type, current_iter = self.session.get_resume_point()
        pending = self.session.get_pending_asset_types()

        print(f"Resuming from: {current_type}, iteration {current_iter}")
        print(f"Pending assets: {', '.join(pending)}")

        # Continue generation
        style_profile = self.session.get_style_profile()
        settings = self.session.get_settings()

        self._run_generation(
            pending,
            style_profile,
            settings,
            resume_from=(current_type, current_iter),
        )

    def _display_project_info(self, info: dict) -> None:
        """Display detected project information."""
        print(f"\nProject: {info['project_name']}")
        print(f"Platform: {info['platform']}")
        print(f"Category: {info['app_category']}")

        existing = info['existing_assets']
        has_icons = len(existing.get('icons', [])) > 0
        print(f"Existing icons: {'Yes' if has_icons else 'No'}")

    def _confirm_asset_types(self, suggested: list[str]) -> list[str]:
        """Confirm which asset types to generate."""
        print(f"\nSuggested assets: {', '.join(suggested)}")

        response = input("Generate these assets? [Y/n/edit]: ").strip().lower()

        if response == 'n':
            print("Aborted.")
            sys.exit(0)
        elif response == 'edit':
            available = ImageGenerator.get_supported_asset_types()
            print(f"\nAvailable types: {', '.join(available)}")
            custom = input("Enter asset types (comma-separated): ").strip()
            return [t.strip() for t in custom.split(",") if t.strip() in available]

        return suggested

    def _confirm_style(self, style: dict, app_name: str) -> dict:
        """Confirm and optionally modify the style profile."""
        print(f"\nExtracted Style Profile:")
        print(f"  Category: {style.get('category', 'general')}")
        print(f"  Certainty: {style.get('certainty', 0.5):.2f}")

        if style.get('colors'):
            print(f"  Colors: {', '.join(style['colors'][:5])}")

        inferred = style.get('inferred_style', {})
        if inferred:
            print(f"  Aesthetic: {inferred.get('aesthetic', 'N/A')}")
            print(f"  Iconography: {inferred.get('iconography', 'N/A')}")

        response = input("\nAccept this style? [Y/n/edit]: ").strip().lower()

        if response == 'n':
            print("Aborted.")
            sys.exit(0)
        elif response == 'edit':
            # Allow editing
            aesthetic = input(f"Aesthetic [{inferred.get('aesthetic', '')}]: ").strip()
            if aesthetic:
                style['inferred_style']['aesthetic'] = aesthetic

            colors = input(f"Colors [{inferred.get('colors', '')}]: ").strip()
            if colors:
                style['inferred_style']['colors'] = colors

            iconography = input(f"Iconography [{inferred.get('iconography', '')}]: ").strip()
            if iconography:
                style['inferred_style']['iconography'] = iconography

        # Mark as user confirmed (boosts certainty)
        style['user_confirmed'] = True
        style['certainty'] = min(style.get('certainty', 0.5) + 0.15, 1.0)
        style['app_name'] = app_name

        return style

    def _confirm_settings(self) -> dict:
        """Confirm generation settings."""
        print(f"\nDefault settings:")
        print(f"  Iterations: {self.iterations}")
        print(f"  Variants per iteration: {self.variants}")
        print(f"  Auto-deploy: {self.auto_deploy}")

        response = input("\nAccept settings? [Y/n/edit]: ").strip().lower()

        if response == 'n':
            print("Aborted.")
            sys.exit(0)
        elif response == 'edit':
            try:
                iters = input(f"Iterations [{self.iterations}]: ").strip()
                if iters:
                    parsed = int(iters)
                    if self.MIN_VALUE <= parsed <= self.MAX_ITERATIONS:
                        self.iterations = parsed
                    else:
                        print(f"Must be {self.MIN_VALUE}-{self.MAX_ITERATIONS}. Using default.")

                variant_count = input(f"Variants [{self.variants}]: ").strip()
                if variant_count:
                    parsed = int(variant_count)
                    if self.MIN_VALUE <= parsed <= self.MAX_VARIANTS:
                        self.variants = parsed
                    else:
                        print(f"Must be {self.MIN_VALUE}-{self.MAX_VARIANTS}. Using default.")
            except ValueError:
                print("Invalid number, using defaults.")

        return {
            "iterations": self.iterations,
            "variants": self.variants,
            "auto_deploy": self.auto_deploy,
        }

    def _run_generation(
        self,
        asset_types: list[str],
        style_profile: dict,
        settings: dict,
        resume_from: tuple[str | None, int] | None = None,
    ) -> None:
        """Execute the generation loop."""
        # Create or load session
        if resume_from is None:
            session_id = self.session.create(
                project_name=self.project_name,
                asset_types=asset_types,
                style_profile=style_profile,
                settings=settings,
            )
            print(f"\nSession ID: {session_id}")
        else:
            session_id = self.session.state.get("session_id", "resumed")

        print(f"Output directory: {self.output_dir}")

        # Determine certainty level
        certainty = style_profile.get("certainty", 0.5)
        certainty_level = "high" if certainty > 0.8 else "medium" if certainty > 0.5 else "low"

        for asset_type in asset_types:
            print(f"\n{'='*50}")
            print(f"Generating: {asset_type}")
            print(f"{'='*50}")

            # Handle resume point
            start_iter = 1
            if resume_from and resume_from[0] == asset_type:
                start_iter = resume_from[1] + 1
                print(f"Resuming from iteration {start_iter}")

            all_variants = []

            # Load existing variants if resuming
            if start_iter > 1:
                all_variants = self.session.get_all_variants(asset_type)

            for iteration in range(start_iter, settings["iterations"] + 1):
                print(f"\n--- Iteration {iteration}/{settings['iterations']} ---")

                # Build prompts for this iteration
                prompts = self._build_prompts(
                    asset_type=asset_type,
                    style_profile=style_profile,
                    certainty_level=certainty_level,
                    iteration=iteration,
                    previous_variants=all_variants,
                )

                iteration_variants = []

                for var_num in range(1, settings["variants"] + 1):
                    # Cycle through prompts
                    prompt = prompts[(var_num - 1) % len(prompts)]

                    # Generate image
                    result = self.generator.generate(
                        prompt=prompt,
                        asset_type=asset_type,
                        output_dir=self.output_dir,
                        iteration=iteration,
                        variant=var_num,
                    )

                    if result:
                        # Evaluate the generated image
                        score = self.evaluator.evaluate(
                            image_path=result["path"],
                            asset_type=asset_type,
                            style_profile=style_profile,
                        )

                        result["score"] = score
                        result["prompt"] = prompt
                        iteration_variants.append(result)

                        print(f"  v{var_num}: {result['filename']} (score: {score:.2f})")
                    else:
                        print(f"  v{var_num}: FAILED")

                all_variants.extend(iteration_variants)

                # Save iteration progress
                self.session.save_iteration(asset_type, iteration, iteration_variants)

            # Select best for this asset type
            if all_variants:
                best = self._select_best(all_variants)
                if best:
                    self._mark_as_best(best, asset_type)
                    self.session.set_best(asset_type, best)
                    print(f"\nBest {asset_type}: {best['filename']} (score: {best['score']:.2f})")

        # Mark session complete
        self.session.mark_complete()

        # Final summary and deployment
        self._print_summary()

        if settings.get("auto_deploy", True):
            self._deploy_assets()

    def _build_prompts(
        self,
        asset_type: str,
        style_profile: dict,
        certainty_level: str,
        iteration: int,
        previous_variants: list[dict],
    ) -> list[str]:
        """Build prompts based on style and certainty."""
        base_template = ASSET_PROMPTS.get(asset_type, ASSET_PROMPTS["icon"])
        inferred = style_profile.get("inferred_style", {})

        # Get variation directives for this certainty level
        directives = VARIATION_DIRECTIVES.get(certainty_level, VARIATION_DIRECTIVES["medium"])

        # For later iterations, learn from previous scores
        if iteration > 1 and previous_variants:
            # Find top performers
            sorted_variants = sorted(previous_variants, key=lambda x: x.get("score", 0), reverse=True)
            if sorted_variants and sorted_variants[0].get("score", 0) > 0.7:
                # Add learning from best prompt
                best_prompt = sorted_variants[0].get("prompt", "")
                if best_prompt:
                    directives = [
                        f"Build on the successful approach. Refine and improve quality.",
                        f"Polish the winning direction with subtle improvements.",
                        f"Perfect the established style with professional finish.",
                    ]

        prompts = []
        for directive in directives:
            prompt = base_template.format(
                app_name=style_profile.get("app_name", "the app"),
                aesthetic=inferred.get("aesthetic", "modern, clean, professional"),
                colors=inferred.get("colors", style_profile.get("colors", ["balanced palette"])),
                iconography=inferred.get("iconography", "clear, recognizable, minimal"),
                variation_directive=directive,
            )
            prompts.append(prompt)

        return prompts

    def _select_best(self, variants: list[dict]) -> dict | None:
        """Select best variant by score."""
        if not variants:
            return None
        return max(variants, key=lambda v: v.get("score", 0))

    def _mark_as_best(self, variant: dict, asset_type: str) -> None:
        """Mark variant as best by creating a copy with _best suffix."""
        from shutil import copy2

        path = Path(variant["path"])
        best_path = path.with_stem(f"{path.stem}_best")

        # Copy the file (don't move, in case user wants to review all)
        copy2(path, best_path)

        variant["best_path"] = str(best_path)
        variant["best_filename"] = best_path.name

    def _print_summary(self) -> None:
        """Print generation summary."""
        print("\n" + "=" * 60)
        print("GENERATION COMPLETE")
        print("=" * 60)

        best_selections = self.session.get_best_selections()

        print(f"\nBest assets selected:")
        for asset_type, selection in best_selections.items():
            score = selection.get("score", 0)
            filename = selection.get("filename", "unknown")
            print(f"  {asset_type}: {filename} (score: {score:.2f})")

        print(f"\nAll assets saved to: {self.output_dir}")

    def _deploy_assets(self) -> None:
        """Deploy best assets to project."""
        print("\n" + "=" * 60)
        print("DEPLOYING TO PROJECT")
        print("=" * 60)

        try:
            result = self.deployer.deploy(self.output_dir / "session.json")
            total = len(result.get("android", [])) + len(result.get("ios", []))
            print(f"\nDeployed {total} files to project")
        except Exception as e:
            print(f"\nDeployment error: {e}")
            print("Assets remain in output folder for manual deployment.")


def main():
    parser = argparse.ArgumentParser(
        description="Generate app assets using Gemini API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python asset_gen.py                      # Interactive wizard
  python asset_gen.py -p ~/MyApp           # Specify project
  python asset_gen.py --resume MyApp_123   # Resume session
  python asset_gen.py -i 5 -v 5            # 5 iterations, 5 variants
  python asset_gen.py -o ~/my-assets       # Custom output directory
"""
    )
    parser.add_argument("--project", "-p", type=Path, default=Path.cwd(),
                        help="Path to project (default: current directory)")
    parser.add_argument("--output", "-o", type=Path, default=None,
                        help="Output directory (default: ~/Downloads/asset-gen/{project})")
    parser.add_argument("--iterations", "-i", type=int, default=3,
                        help="Number of iterations (default: 3, max: 20)")
    parser.add_argument("--variants", "-v", type=int, default=3,
                        help="Variants per iteration (default: 3, max: 10)")
    parser.add_argument("--resume", type=str,
                        help="Resume from session ID")
    parser.add_argument("--no-deploy", action="store_true",
                        help="Skip auto-deployment to project")
    parser.add_argument("--asset-types", type=str,
                        help="Comma-separated asset types (e.g., icon,splash)")

    args = parser.parse_args()

    # Validate project path
    project_path = args.project.expanduser().resolve()
    if not project_path.exists():
        print(f"Error: Project path does not exist: {project_path}")
        sys.exit(1)

    try:
        orchestrator = AssetGenOrchestrator(
            project_path=project_path,
            output_base=args.output,
            iterations=args.iterations,
            variants=args.variants,
            auto_deploy=not args.no_deploy,
        )

        if args.resume:
            orchestrator.resume(args.resume)
        else:
            orchestrator.run_wizard()

    except EnvironmentError as e:
        print(f"Environment error: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\nInterrupted. Session saved for resume.")
        sys.exit(130)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
