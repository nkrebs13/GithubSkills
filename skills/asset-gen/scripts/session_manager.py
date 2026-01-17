#!/usr/bin/env python3
"""
Session Manager

Handles session state persistence for resume support in asset generation.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Any


class SessionManager:
    """Manages session state for asset generation with full resume support."""

    def __init__(self, session_file: Path):
        self.session_file = Path(session_file)
        self.state: dict[str, Any] = {}

    def create(
        self,
        project_name: str,
        asset_types: list[str],
        style_profile: dict,
        settings: dict,
    ) -> str:
        """Create a new session and return session ID."""
        session_id = f"{project_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        self.state = {
            "session_id": session_id,
            "project_name": project_name,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "status": "in_progress",
            "asset_types": asset_types,
            "style_profile": style_profile,
            "settings": settings,
            "iterations": {},
            "best_selections": {},
            "current_asset_type": None,
            "current_iteration": 0,
        }

        self._save()
        return session_id

    def load(self, session_id: str | None = None) -> dict[str, Any]:
        """Load existing session state."""
        if self.session_file.exists():
            try:
                self.state = json.loads(self.session_file.read_text())
            except json.JSONDecodeError as e:
                raise ValueError(f"Session file is corrupted: {e}")

            if session_id and self.state.get("session_id") != session_id:
                raise ValueError(f"Session ID mismatch: expected {session_id}")

        return self.state

    def exists(self) -> bool:
        """Check if a session file exists."""
        return self.session_file.exists()

    def save_iteration(
        self,
        asset_type: str,
        iteration: int,
        variants: list[dict],
    ) -> None:
        """Save results of an iteration."""
        if asset_type not in self.state["iterations"]:
            self.state["iterations"][asset_type] = {}

        self.state["iterations"][asset_type][str(iteration)] = {
            "variants": variants,
            "completed_at": datetime.now().isoformat(),
        }

        self.state["current_asset_type"] = asset_type
        self.state["current_iteration"] = iteration
        self.state["updated_at"] = datetime.now().isoformat()

        self._save()

    def get_scores(self, asset_type: str) -> list[dict]:
        """Get all scores for an asset type across iterations."""
        scores = []

        if asset_type in self.state.get("iterations", {}):
            for iteration_data in self.state["iterations"][asset_type].values():
                for variant in iteration_data.get("variants", []):
                    if "score" in variant:
                        scores.append({
                            "score": variant["score"],
                            "prompt": variant.get("prompt", ""),
                            "iteration": variant.get("iteration", 0),
                        })

        return sorted(scores, key=lambda x: x["score"], reverse=True)

    def get_all_variants(self, asset_type: str) -> list[dict]:
        """Get all variants for an asset type across all iterations."""
        variants = []

        if asset_type in self.state.get("iterations", {}):
            for iteration_num, iteration_data in self.state["iterations"][asset_type].items():
                for variant in iteration_data.get("variants", []):
                    # Create copy to avoid mutating original data
                    variant_copy = variant.copy()
                    try:
                        variant_copy["iteration"] = int(iteration_num)
                    except ValueError:
                        variant_copy["iteration"] = 0
                    variants.append(variant_copy)

        return variants

    def set_best(self, asset_type: str, variant: dict) -> None:
        """Record best selection for asset type."""
        self.state["best_selections"][asset_type] = {
            "path": variant["path"],
            "filename": variant["filename"],
            "score": variant.get("score", 0),
            "iteration": variant.get("iteration", 0),
            "selected_at": datetime.now().isoformat(),
        }
        self._save()

    def get_best_selections(self) -> dict[str, dict]:
        """Get all best selections."""
        return self.state.get("best_selections", {})

    def mark_complete(self) -> None:
        """Mark session as complete."""
        self.state["status"] = "complete"
        self.state["completed_at"] = datetime.now().isoformat()
        self._save()

    def get_resume_point(self) -> tuple[str | None, int]:
        """Get the point to resume from (asset_type, iteration)."""
        return (
            self.state.get("current_asset_type"),
            self.state.get("current_iteration", 0),
        )

    def get_pending_asset_types(self) -> list[str]:
        """Get asset types that haven't been completed yet."""
        all_types = self.state.get("asset_types", [])
        completed = set(self.state.get("best_selections", {}).keys())
        return [t for t in all_types if t not in completed]

    def get_settings(self) -> dict:
        """Get session settings."""
        return self.state.get("settings", {"iterations": 3, "variants": 3})

    def get_style_profile(self) -> dict:
        """Get the style profile."""
        return self.state.get("style_profile", {})

    def get_project_name(self) -> str:
        """Get the project name."""
        return self.state.get("project_name", "unknown")

    def _save(self) -> None:
        """Save state to file."""
        self.session_file.parent.mkdir(parents=True, exist_ok=True)
        self.session_file.write_text(json.dumps(self.state, indent=2))


def find_session_by_id(session_id: str, base_dir: Path | None = None) -> Path | None:
    """Find a session file by its ID in the asset-gen directory."""
    if base_dir is None:
        base_dir = Path.home() / "Downloads" / "asset-gen"

    if not base_dir.exists():
        return None

    # Session ID format: {project_name}_{timestamp}
    # Project name is everything before the last underscore + timestamp
    parts = session_id.rsplit("_", 2)
    if len(parts) >= 3:
        project_name = parts[0]
    else:
        project_name = session_id.split("_")[0]

    # Look for session.json in the project directory
    session_file = base_dir / project_name / "session.json"
    if session_file.exists():
        try:
            data = json.loads(session_file.read_text())
            if data.get("session_id") == session_id:
                return session_file
        except (json.JSONDecodeError, KeyError):
            pass

    # Fallback: search all project directories
    for project_dir in base_dir.iterdir():
        if project_dir.is_dir():
            session_file = project_dir / "session.json"
            if session_file.exists():
                try:
                    data = json.loads(session_file.read_text())
                    if data.get("session_id") == session_id:
                        return session_file
                except (json.JSONDecodeError, KeyError):
                    pass

    return None
