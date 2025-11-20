"""
core/brain_selector.py
Chooses which brain (Architect or Oracle) should handle a task.
Checks emotional state + task keywords + temperature logic.
"""

from reasoning.architect import ArchitectBrain
from reasoning.oracle import OracleBrain
from reasoning.reconcile import ReconcileBrain


class BrainSelector:
    def __init__(self):
        self.architect = ArchitectBrain()
        self.oracle = OracleBrain()
        self.reconcile = ReconcileBrain()

    def choose(self, task: str):
        """
        Returns:
            final_text   - which brain's output wins
            rationale    - explanation from reconcile
        """
        result = self.reconcile.decide(
            architect_output=self.architect.generate(task),
            oracle_output=self.oracle.generate(task),
            task=task
        )
        return result["final_text"], result
