"""
forge/forge.py — Forge v1 (MVP)
C.3’s self-improvement engine.

This version does THREE things:
1. Loads the current C.3 architecture snapshot
2. Generates a tiny “auto-PR idea” using Meta-C3
3. Saves the suggestion to forge/auto_pr.json (no side effects)
"""

import json
from datetime import datetime
from meta.c3_sim import simulate_c3


def load_blueprint():
    """
    Loads a minimal blueprint snapshot for simulation.
    Later versions will load the real architecture + memory.
    """
    return {
        "version": "1.0",
        "timestamp": datetime.utcnow().isoformat(),
        "components": [
            "architect",
            "oracle",
            "reconciler",
            "mre",
            "memory_spine",
            "narrative_engine",
            "cove",
            "curiosity"
        ]
    }


def propose_auto_pr(user_task: str = "Improve C3"):
    """
    Uses Meta-C3 simulation mode to generate a small PR suggestion.
    It DOES NOT MODIFY any real files.
    """
    blueprint = load_blueprint()
    sim_result = simulate_c3(user_task)

    pr = {
        "task": user_task,
        "timestamp": datetime.utcnow().isoformat(),
        "blueprint_snapshot": blueprint,
        "simulation": sim_result,
        "status": "suggestion_only",
        "notes": [
            "Forge v1 does not change code.",
            "User must review the suggestion manually.",
            "Future: auto-apply small safe PRs with simulation checks."
        ]
    }

    return pr


def save_auto_pr(pr):
    """
    Saves the PR suggestion to forge/auto_pr.json
    """
    path = "forge/auto_pr.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(pr, f, indent=2)
    return path


def run(user_task: str = "Improve C3"):
    """
    Main entry point.
    Example:
        python3 -m forge.forge "Find weak spots in C3"
    """
    pr = propose_auto_pr(user_task)
    path = save_auto_pr(pr)
    print(json.dumps({
        "status": "ok",
        "saved_to": path,
        "message": "Auto-PR suggestion generated (v1).",
    }, indent=2))


if __name__ == "__main__":
    import sys
    task = "Improve C3"
    if len(sys.argv) > 1:
        task = " ".join(sys.argv[1:])
    run(task)
