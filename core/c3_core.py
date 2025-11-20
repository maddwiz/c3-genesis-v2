"""
core/c3_core.py

Main orchestrator for C.3 in MVP form.

Responsibilities:
- Accept a task string from the user or system.
- Use BrainSelector (Architect + Oracle + Reconcile) to get a final answer.
- Optionally query the intrinsic Motivation Engine when idle to pick an internal goal.
"""

from core.brain_selector import BrainSelector
from curiosity.motivation import motivation_engine


class C3Core:
    def __init__(self, mode: str = "default"):
        self.mode = mode
        self.brains = BrainSelector()

    def run_task(self, task: str) -> dict:
        """
        Run a single user-facing task through the dual brain.

        Returns a dict containing:
            - task
            - final_text
            - reconcile_result (full reconcile info)
        """
        final_text, reconcile_result = self.brains.choose(task)

        return {
            "task": task,
            "final_text": final_text,
            "reconcile_result": reconcile_result,
        }

    def pick_internal_goal(self) -> dict:
        """
        Ask the intrinsic Motivation Engine what C.3 should work on
        when it is not handling a direct user request.

        For now, we just use default chemical levels.
        Later, this will be driven by:
            - Memory health
            - Forge backlog
            - Curiosity frontier queue
        """
        # Default emotional baselines:
        emotions = {
            "dopamine": 0.5,
            "serotonin": 0.5,
            "norepinephrine": 0.5,
            "oxytocin": 0.5,
        }
        goal = motivation_engine.generate_goal(emotions)
        return goal
