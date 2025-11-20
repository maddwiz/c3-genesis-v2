# reasoning/mre.py
# C.3 — Markovian Reasoning Engine (Soft Mode)
# v1 — lightweight carry-over summaries for long reasoning runs

from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Dict, Any
import json
import time


@dataclass
class MREState:
    """
    Holds the current Markovian 'carry-over summary' (COS).
    Only stores small distilled reasoning snapshots to keep things light.
    """
    step_id: int = 0
    summary: str = ""
    timestamp: float = field(default_factory=time.time)


class MarkovianReasoningEngine:
    """
    Soft MRE:
    - No forced linear chain for all turns.
    - Runs ONLY when Reconciler explicitly requests it.
    - Stores 1–3 sentence summaries => ultra-small footprint.
    """

    def __init__(self):
        self.state = MREState()

    def update_summary(self, text: str) -> MREState:
        """
        Create a new short distilled summary of the last reasoning step.
        """
        self.state.step_id += 1
        self.state.timestamp = time.time()

        # Extremely small compressor — keeps only the core intent.
        distilled = text.strip()
        if len(distilled) > 200:
            distilled = distilled[:200] + "..."

        self.state.summary = distilled
        return self.state

    def get_summary(self) -> str:
        """
        Get the current COS (carry-over summary).
        """
        return self.state.summary

    def export_state(self) -> Dict[str, Any]:
        """
        JSON-ready state for debugging, logging, or Narrative Engine.
        """
        return {
            "step_id": self.state.step_id,
            "summary": self.state.summary,
            "timestamp": self.state.timestamp,
        }


# Singleton used by Reconcile
mre_engine = MarkovianReasoningEngine()
