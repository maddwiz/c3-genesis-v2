"""
reasoning/emotions.py — EmotionEngine v1

This module defines a simple "chemical" state for C.3:
- dopamine: curiosity / exploration
- serotonin: stability / confidence
- norepinephrine: urgency / stress
- oxytocin: social / bonding

It exposes:
- EmotionEngine.current_state()      -> dict of chemicals
- EmotionEngine.brain_temperatures() -> architect/oracle temps

Both are used by the Reconcile engine and Meta-C3.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Dict


@dataclass
class EmotionState:
    dopamine: float = 0.5
    serotonin: float = 0.6
    norepinephrine: float = 0.3
    oxytocin: float = 0.6

    def to_dict(self) -> Dict[str, float]:
        return asdict(self)


class EmotionEngine:
    """
    Simple emotion engine v1.

    For now:
    - Holds a single EmotionState in memory.
    - Can return:
        * current_state()      -> raw chemicals
        * brain_temperatures() -> how "hot" each brain should run
    """

    def __init__(self) -> None:
        # Default "calm but slightly curious" state.
        self._state = EmotionState()

    def current_state(self) -> Dict[str, float]:
        """
        Return the current chemical levels as a dict.
        Keys: dopamine, serotonin, norepinephrine, oxytocin
        """
        return self._state.to_dict()

    def brain_temperatures(self) -> Dict[str, float]:
        """
        Map chemicals to two temperatures:

        - ArchitectBrain:
            * prefers high serotonin (stability)
            * prefers low norepinephrine (low stress)
            * slightly damped by very high dopamine (too chaotic)

        - OracleBrain:
            * prefers high dopamine (exploration)
            * can handle higher norepinephrine (urgency)
            * boosted a bit by oxytocin (social / creative bonding)
        """
        s = self._state

        architect_temperature = (
            0.2
            + 0.3 * (1.0 - s.dopamine)
            + 0.4 * s.serotonin
            - 0.3 * s.norepinephrine
        )

        oracle_temperature = (
            0.2
            + 0.5 * s.dopamine
            + 0.2 * s.norepinephrine
            + 0.3 * s.oxytocin
        )

        # Clamp to [0, 1]
        def clamp(x: float) -> float:
            return max(0.0, min(1.0, x))

        return {
            "architect_temperature": clamp(architect_temperature),
            "oracle_temperature": clamp(oracle_temperature),
        }


def main() -> None:
    """
    Tiny demo so you can run:

        python3 -m reasoning.emotions
    """
    engine = EmotionEngine()
    emotions = engine.current_state()
    temps = engine.brain_temperatures()

    print("Emotions:", emotions)
    print("Temps:", temps)


if __name__ == "__main__":
    main()
