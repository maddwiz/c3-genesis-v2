"""
meta/cove.py — CoVe++ v1 (Coordinator / Verification Engine stub)

This sits *above* the dual-brain (Architect + Oracle) and does:

- Accepts a user task
- Enforces a simple "verification budget" (max work per turn)
- Calls the Reconciler to get a merged decision
- Wraps the result with meta info about:
  - budget_used
  - budget_limit
  - notes

Right now:
- Fully deterministic
- No heavy verification logic yet
- Safe to call from CLI or future agent loop
"""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass, asdict
from typing import Any, Dict, List

from reasoning.reconcile import Reconciler, ReconciledDecision


@dataclass
class CoVeConfig:
    """
    Configuration for CoVe (Coordinator / Verification Engine).

    verification_budget:
        Conceptual limit for how much "extra" checking we do per turn.
        For now, we only track and report it. Later, this will gate:
        - extra self-check passes
        - additional simulations
        - deeper tool verification
    """

    verification_budget: int = 200  # conceptual "token budget" for meta-work


@dataclass
class CoVeResult:
    """
    The result returned by CoVe.

    - task: original user task
    - decision: ReconciledDecision.to_dict()
    - budget_used: how much budget we conceptually consumed
    - budget_limit: from config
    - notes: list of strings describing what we did
    """

    task: str
    decision: Dict[str, Any]
    budget_used: int
    budget_limit: int
    notes: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    def to_json(self, indent: int | None = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent)


class CoVe:
    """
    CoVe++ v1 — very simple meta-coordinator.

    For now:
    - Calls Reconciler once
    - Pretends we used a fixed amount of budget
    - Returns structured result
    """

    def __init__(self, config: CoVeConfig | None = None) -> None:
        self.config = config or CoVeConfig()
        self.reconciler = Reconciler()

    def process_task(self, task: str) -> CoVeResult:
        """
        Main entrypoint:

        - Trim the task
        - Run through Reconciler
        - Compute a simple "budget_used" value
        - Attach notes about what we did
        """

        task = task.strip() or "(empty task)"

        decision: ReconciledDecision = self.reconciler.reconcile(task)

        # For v1, we just say we used a fixed amount of budget.
        # Later this will be tied to actual meta-operations.
        budget_used = 50  # arbitrary small fixed cost for now

        notes = [
            "Called Reconciler (Architect + Oracle).",
            "No extra self-check passes yet (v1 stub).",
            "verification_budget will control deeper checks in future versions.",
        ]

        return CoVeResult(
            task=task,
            decision=decision.to_dict(),
            budget_used=budget_used,
            budget_limit=self.config.verification_budget,
            notes=notes,
        )


def main(argv: List[str] | None = None) -> int:
    if argv is None:
        argv = sys.argv[1:]

    if not argv:
        task = "Plan and demo C3 in 30 days."
    else:
        task = " ".join(argv)

    cove = CoVe()
    result = cove.process_task(task)
    print(result.to_json(indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
