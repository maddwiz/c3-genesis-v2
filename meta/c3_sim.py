"""
meta/c3_sim.py — Meta-C3 simulation stub (v1)

Goal:
- Provide a safe "sandbox" entrypoint that *simulates* a C.3 run
  without actually changing any external state.

For now:
- Wraps the dual-brain reconcile() flow (Architect + Oracle + Emotion)
- Adds a `simulation` flag and a `mode` field
- Returns a SimulationResult that is JSON-serializable

Later:
- This is where Forge will run "what if C3 changed itself?" experiments.
- We can run multiple simulated variants and compare them before
  applying any real changes.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any, Dict
import json

from reasoning.reconcile import reconcile, ReconcileResult  # uses EmotionEngine internally


@dataclass
class SimulationResult:
    """
    A lightweight container for Meta-C3 simulations.

    Everything inside here is safe to serialize to JSON so Forge
    can log, diff, and compare simulations.
    """
    mode: str
    task: str
    simulation: bool
    reconcile_result: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(asdict(self), ensure_ascii=False, indent=2)


def simulate_c3(task: str, mode: str = "default") -> SimulationResult:
    """
    Run a *simulated* C.3 reasoning pass.

    For now:
    - We fake Architect + Oracle outputs based on the task.
    - We call reconcile() to decide which "brain" would win.
    - We mark the result as simulation=True.
    """

    # Stubbed dual-brain outputs for now.
    architect_output = f"[SIM-ARCH] Logical plan for task: {task}"
    oracle_output = f"[SIM-ORACLE] Creative angle for task: {task}"

    # Confidence stub — later this will come from ArchitectBrain.
    confidence = 0.65

    rec: ReconcileResult = reconcile(
        architect_output=architect_output,
        oracle_output=oracle_output,
        confidence=confidence,
    )

    # Try to convert ReconcileResult to a dict.
    if hasattr(rec, "to_dict"):
        rec_dict = rec.to_dict()
    else:
        # Fallback: best-effort dict
        rec_dict = rec.__dict__

    return SimulationResult(
        mode=mode,
        task=task,
        simulation=True,
        reconcile_result=rec_dict,
    )


def main() -> None:
    """
    Simple CLI entrypoint so you can run:

        python3 -m meta.c3_sim "plan my day"
    """
    import argparse

    parser = argparse.ArgumentParser(description="Meta-C3 simulation stub")
    parser.add_argument(
        "task",
        type=str,
        help="Task description to simulate (e.g., 'plan my day')",
    )
    parser.add_argument(
        "--mode",
        type=str,
        default="default",
        help="Simulation mode tag (for future experimentation).",
    )

    args = parser.parse_args()

    sim_result = simulate_c3(task=args.task, mode=args.mode)
    print(sim_result.to_json())


if __name__ == "__main__":
    main()
