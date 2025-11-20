"""
tools/c3_memory_diff.py

Simple CLI to inspect the latest events in the C.3 Memory Spine.

Usage:
    python3 -m tools.c3_memory_diff --last 5
"""

import argparse
from memory.spine import MemorySpine, MemoryEvent  # type: ignore[import]


def main() -> None:
    parser = argparse.ArgumentParser(description="Inspect C.3 Memory Spine events")
    parser.add_argument(
        "--last",
        type=int,
        default=10,
        help="Number of most recent events to show (default: 10)",
    )
    args = parser.parse_args()

    spine = MemorySpine()
    events = spine.read_last(args.last)

    if not events:
        print("No memory events found yet.")
        return

    for evt in events:
        # evt is a MemoryEvent dataclass in the new v2 format
        ts = evt.ts
        event_type = evt.event_type or "<no_type>"
        payload = evt.payload or {}
        meta = evt.meta or {}

        # Print in a compact, human-readable way
        print(f"- [{ts}] ({event_type}) {payload} | meta={meta}")


if __name__ == "__main__":
    main()
