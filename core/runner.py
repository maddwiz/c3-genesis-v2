"""
core/runner.py
The small “conductor” that ties the whole C.3 brain together.

This file:
- Loads Architect + Oracle
- Loads Emotion Engine
- Runs reconcile()
- Logs memory events automatically
- Gives a final answer
"""

from reasoning.architect import ArchitectBrain
from reasoning.oracle import OracleBrain
from reasoning.reconcile import reconcile, ReconcileResult
from reasoning.emotions import EmotionEngine
from memory.spine import MemorySpine


class C3Core:
    def __init__(self):
        self.architect = ArchitectBrain()
        self.oracle = OracleBrain()
        self.emotions = EmotionEngine()
        self.memory = MemorySpine()   # auto-memory

    def run(self, task: str) -> ReconcileResult:
        """
        High-level brain loop.
        """

        # Architect thinks logically
        arch_out = self.architect.think(task)
        self.memory.store(
            "architect_output",
            {"task": task, "text": arch_out},
            {"source": "c3_core"}
        )

        # Oracle thinks creatively
        oracle_out = self.oracle.think(task)
        self.memory.store(
            "oracle_output",
            {"task": task, "text": oracle_out},
            {"source": "c3_core"}
        )

        # Confidence: simplest stub for now (will be upgraded later)
        confidence = 0.60

        # Reconcile picks which brain leads
        result: ReconcileResult = reconcile(
            architect_output=arch_out,
            oracle_output=oracle_out,
            confidence=confidence
        )

        # Store reconcile final
        self.memory.store(
            "final_choice",
            {
                "task": task,
                "choice": result.choice,
                "text": result.final_text,
                "emotions": result.emotions,
                "temperatures": result.temperatures,
            },
            {"source": "c3_core"}
        )

        return result


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Run C.3 Core Brain")
    parser.add_argument("task", type=str, help="Task for C.3 to think about")

    args = parser.parse_args()

    core = C3Core()
    result = core.run(args.task)

    print("\n=== C3 CORE RESULT ===")
    print("Choice:", result.choice)
    print("Reason:", result.rationale)
    print("Final Output:", result.final_text)
    print("Emotions:", result.emotions)
    print("Temperatures:", result.temperatures)
    print()


if __name__ == "__main__":
    main()
