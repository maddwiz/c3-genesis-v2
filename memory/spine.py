"""
memory/spine.py

Memory Spine v2 for C.3

- Append-only JSONL event log
- Each event has:
    - ts          : ISO timestamp
    - event_type  : short label (e.g., "architect_output")
    - payload     : arbitrary dict (task, text, etc.)
    - meta        : extra info (source, tags, etc.)

Used by:
- core/runner.C3Core  -> self.memory.store(...)
- tools.c3_memory_diff -> to inspect last N events
"""

import json
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional


DEFAULT_EVENTS_PATH = Path(__file__).with_name("events.jsonl")


@dataclass
class MemoryEvent:
    ts: str
    event_type: str
    payload: Dict[str, Any]
    meta: Dict[str, Any]


class MemorySpine:
    """
    Minimal, robust Memory Spine v2.

    Responsibilities:
    - append events via store()
    - read back events for tools (like c3_memory_diff)
    """

    def __init__(self, path: Optional[str] = None):
        if path is None:
            self.path = DEFAULT_EVENTS_PATH
        else:
            self.path = Path(path)

        # Make sure directory exists
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def _now_iso(self) -> str:
        return datetime.now(timezone.utc).isoformat()

    def store(
        self,
        event_type: str,
        payload: Dict[str, Any],
        meta: Optional[Dict[str, Any]] = None,
    ) -> MemoryEvent:
        """
        Main API used by the rest of C.3.

        Example:
            self.memory.store(
                "architect_output",
                {"task": task, "text": arch_out},
                {"source": "c3_core"}
            )
        """
        if meta is None:
            meta = {}

        evt = MemoryEvent(
            ts=self._now_iso(),
            event_type=event_type,
            payload=payload,
            meta=meta,
        )

        line = json.dumps(asdict(evt), ensure_ascii=False)
        with self.path.open("a", encoding="utf-8") as f:
            f.write(line + "\n")

        return evt

    def read_last(self, n: int = 10) -> List[MemoryEvent]:
        """
        Utility used by tools.c3_memory_diff to fetch the last N events.
        """
        if not self.path.exists():
            return []

        with self.path.open("r", encoding="utf-8") as f:
            lines = f.readlines()

        events: List[MemoryEvent] = []
        for raw in lines[-n:]:
            raw = raw.strip()
            if not raw:
                continue
            try:
                data = json.loads(raw)
                events.append(
                    MemoryEvent(
                        ts=data.get("ts", ""),
                        event_type=data.get("event_type", ""),
                        payload=data.get("payload", {}) or {},
                        meta=data.get("meta", {}) or {},
                    )
                )
            except json.JSONDecodeError:
                # Skip bad lines instead of crashing
                continue

        return events
