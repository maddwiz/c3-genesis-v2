"""
narrative/engine.py — Narrative Engine v1 (chaptering stub)

Goal:
- Take a list of memory events (from MemorySpine)
- Produce a very simple "chapter summary" as a dict

Right now:
- Does NOT call any model
- Uses stupid-simple heuristics:
  - counts events
  - looks at first + last event texts if present
- Returns a JSON-serializable chapter object

Later:
- Will call an LLM (Architect/Oracle) to write rich summaries
- Will be wired into Time Weaver and UI
"""

from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from typing import Any, Dict, List, Optional


@dataclass
class Chapter:
    """
    A very small narrative "chapter" representation.

    - index: chapter number (caller decides)
    - title: short label for the chapter
    - event_count: how many events went into this chapter
    - first_event_preview: small text from the first event (if any)
    - last_event_preview: small text from the last event (if any)
    """

    index: int
    title: str
    event_count: int
    first_event_preview: str
    last_event_preview: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    def to_json(self, indent: Optional[int] = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent)


class NarrativeEngine:
    """
    NarrativeEngine v1 — tiny heuristic chapter maker.

    Takes:
    - events: list of dicts, each like:
      { "ts": ..., "type": "note", "data": { "text": "..." } }

    Returns:
    - Chapter object
    """

    def __init__(self) -> None:
        pass

    def make_chapter(self, events: List[Dict[str, Any]], index: int = 1) -> Chapter:
        """
        Build a tiny chapter from a list of memory events.

        Heuristics:
        - title: "Chapter {index} — {event_count} events"
        - first_event_preview: best-effort text from events[0]
        - last_event_preview: best-effort text from events[-1]
        """

        event_count = len(events)

        if event_count == 0:
            return Chapter(
                index=index,
                title=f"Chapter {index} — empty",
                event_count=0,
                first_event_preview="",
                last_event_preview="",
            )

        def _extract_text(evt: Dict[str, Any]) -> str:
            data = evt.get("data") or {}
            text = data.get("text") or ""
            if not isinstance(text, str):
                text = str(text)
            return text

        first_event_preview = _extract_text(events[0])
        last_event_preview = _extract_text(events[-1])

        title = f"Chapter {index} — {event_count} events"

        return Chapter(
            index=index,
            title=title,
            event_count=event_count,
            first_event_preview=first_event_preview[:200],
            last_event_preview=last_event_preview[:200],
        )


def demo_from_jsonl(path: str, index: int = 1) -> str:
    """
    Convenience function:

    - Reads a JSONL file of events (like MemorySpine writes)
    - Builds a Chapter
    - Returns pretty-printed JSON string
    """

    events: List[Dict[str, Any]] = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                events.append(json.loads(line))
            except json.JSONDecodeError:
                continue

    engine = NarrativeEngine()
    chapter = engine.make_chapter(events, index=index)
    return chapter.to_json(indent=2)


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python -m narrative.engine <path_to_events.jsonl> [chapter_index]")
        raise SystemExit(1)

    path = sys.argv[1]
    if len(sys.argv) >= 3:
        try:
            idx = int(sys.argv[2])
        except ValueError:
            idx = 1
    else:
        idx = 1

    print(demo_from_jsonl(path, index=idx))
