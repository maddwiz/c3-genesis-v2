"""
tools/test_motivation.py

Tiny CLI helper to see the Intrinsic Motivation Engine v0.1 in action.

Usage (from repo root):

  python3 -m tools.test_motivation "some task description"

It will:
- Build a simple context from the task text.
- Run curiosity/motivation.update_chemicals().
- Print the chemicals, motivation score, and mode (explore / exploit / idle).
"""

from __future__ import annotations

import sys
from pprint import pprint

from curiosity.motivation import (
    default_chemicals,
    simple_context_from_task,
    update_chemicals,
)


def main() -> None:
    # Take the task from the first CLI argument, or use a default.
    if len(sys.argv) > 1:
        task = sys.argv[1]
    else:
        task = "test the motivation engine"

    print("=== C3 MOTIVATION TEST ===")
    print(f"Task: {task}")
    print("-" * 40)

    # Build a rough context from the task text.
    ctx = simple_context_from_task(task)
    print("Context guess:")
    pprint(ctx)

    # Start from neutral chemicals and update once.
    chemicals0 = default_chemicals()
    result = update_chemicals(chemicals=chemicals0, context=ctx)

    print("\nUpdated chemicals:")
    pprint(result.chemicals)
    print(f"\nMotivation score: {result.score:.3f}")
    print(f"Mode: {result.mode}")
    print("\n(done)")


if __name__ == "__main__":
    main()
