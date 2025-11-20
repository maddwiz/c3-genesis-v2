"""
C.3 Memory Diff Engine
Version: v2 (with diff_from_timestamp)

This compares historical memory events stored in the Memory Spine.
"""

import json
import os
from typing import List, Dict, Any


EVENTS_PATH = os.path.join(os.path.dirname(__file__), "events.jsonl")


def load_events() -> List[Dict[str, Any]]:
    """Loads all events from events.jsonl"""
    if not os.path.exists(EVENTS_PATH):
        return []

    events = []
    with open(EVENTS_PATH, "r") as f:
        for line in f:
            try:
                events.append(json.loads(line.strip()))
            except json.JSONDecodeError:
                continue
    return events


def diff_since(n: int = 10) -> List[Dict[str, Any]]:
    """
    Returns the last N events from the spine.
    """
    events = load_events()
    return events[-n:] if n > 0 else []


def diff_from_timestamp(ts: float) -> List[Dict[str, Any]]:
    """
    Returns all events with timestamp greater than `ts`
    This is required for tools/c3_memory_diff.py
    """
    events = load_events()
    return [e for e in events if e.get("ts", 0) > ts]


def pretty_print(events: List[Dict[str, Any]]) -> str:
    """
    Converts event dicts into a nice human-readable string.
    """
    if not events:
        return "No events found."

    lines = []
    for e in events:
        lines.append(
            f"- [{e.get('ts')}] ({e.get('type')}) "
            f"{e.get('data')} | meta={e.get('meta')}"
        )
    return "\n".join(lines)


if __name__ == "__main__":
    print("=== Memory Diff Engine ===")
    sample = diff_since(5)
    print(pretty_print(sample))
