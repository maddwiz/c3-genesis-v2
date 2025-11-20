import json
import difflib
from dataclasses import dataclass
from typing import List, Optional

# ------------------------------------------------------------
# Forge v1 — C.3 Self-Improvement Simulator (MVP)
# ------------------------------------------------------------
# This version:
#  - Reads two text blocks (old code, new code)
#  - Computes a unified diff
#  - Stores it in forge/staging.json
#  - Does NOT apply changes automatically (safety)
#  - Full auto-apply comes in Forge v2
# ------------------------------------------------------------

STAGING_PATH = "forge/staging.json"


@dataclass
class ForgeSuggestion:
    file: str
    rationale: str
    diff: List[str]

    def to_dict(self):
        return {
            "file": self.file,
            "rationale": self.rationale,
            "diff": self.diff,
        }


def compute_diff(old_text: str, new_text: str) -> List[str]:
    """Compute a unified diff between two code versions."""
    old_lines = old_text.splitlines(keepends=True)
    new_lines = new_text.splitlines(keepends=True)

    return list(difflib.unified_diff(
        old_lines,
        new_lines,
        fromfile="old",
        tofile="new"
    ))


def save_suggestion(suggestion: ForgeSuggestion):
    """Save suggestion to staging.json (append mode)."""
    try:
        with open(STAGING_PATH, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = []

    data.append(suggestion.to_dict())

    with open(STAGING_PATH, "w") as f:
        json.dump(data, f, indent=2)


def propose_change(
    file_path: str,
    old_text: str,
    new_text: str,
    rationale: str = "Auto-improvement proposal"
):
    """Main entry point for Forge v1."""
    diff = compute_diff(old_text, new_text)
    suggestion = ForgeSuggestion(
        file=file_path,
        rationale=rationale,
        diff=diff
    )
    save_suggestion(suggestion)
    print(f"[Forge] Proposed change saved for {file_path}")
    print(f"[Forge] Diff lines: {len(diff)}")


# ------------------------------------------------------------
# CLI
# ------------------------------------------------------------
# Usage:
#   python3 -m forge.pr old.txt new.txt target_file.py
# ------------------------------------------------------------

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 4:
        print("Usage: python3 -m forge.pr <old_file> <new_file> <target_c3_file>")
        sys.exit(1)

    old_path = sys.argv[1]
    new_path = sys.argv[2]
    target = sys.argv[3]

    with open(old_path, "r") as f:
        old_text = f.read()
    with open(new_path, "r") as f:
        new_text = f.read()

    propose_change(target, old_text, new_text)
