"""
reasoning/architect.py

ArchitectBrain = the logical, structured half of C.3's dual brain.

This version uses the shared LocalTextModel backend so we can swap
models in one place (models/local_text_model.py).

It also takes a simple "emotion state" dict so the Motivation Engine
can slightly cool/warm the temperature when needed.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional, Tuple

from models.local_text_model import LocalTextModel, LocalTextModelConfig


EmotionState = Dict[str, float]


@dataclass
class ArchitectConfig:
    """
    Config for the ArchitectBrain.

    You can tweak:
      - base_temperature: default "cool" thinking temp
      - max_tokens: how long Architect answers can be
    """

    base_temperature: float = 0.4
    max_tokens: int = 256


class ArchitectBrain:
    """
    The logical / planning brain.

    Responsibilities:
      - Take a task + optional context
      - Use LOCAL model to generate a structured, stepwise plan
      - Stay relatively low-temperature (more deterministic)
      - Slightly adjust temperature based on EmotionState
    """

    def __init__(
        self,
        config: Optional[ArchitectConfig] = None,
        model: Optional[LocalTextModel] = None,
    ) -> None:
        if config is None:
            config = ArchitectConfig()
        self.config = config

        # Shared model backend (TinyLlama or whatever C3_LOCAL_MODEL points to)
        self.model = model or LocalTextModel(LocalTextModelConfig())

    # --- internal helpers -------------------------------------------------

    def _compute_temperature(self, emotions: Optional[EmotionState]) -> float:
        """
        Map emotion signals to a slight temperature adjustment.

        Simple heuristic:
          - start from base_temperature
          - norepinephrine (focus/alert): lowers temp a bit
          - dopamine (explore/reward): raises temp a bit
        """

        t = self.config.base_temperature

        if not emotions:
            return max(0.1, min(1.0, t))

        dopamine = float(emotions.get("dopamine", 0.5))          # 0..1
        norepi = float(emotions.get("norepinephrine", 0.5))      # 0..1

        # Center around 0.5 → [-0.5, +0.5]
        d_centered = dopamine - 0.5
        n_centered = norepi - 0.5

        # Dopamine nudges temp up a little, norepi nudges it down a little
        t += 0.2 * d_centered
        t -= 0.2 * n_centered

        return max(0.1, min(1.0, t))

    def _build_prompt(self, task: str, context: Optional[str]) -> str:
        """
        Build a structured prompt for the Architect model.
        """

        base = (
            "You are the ARCHITECT brain of C.3.\n"
            "Your job is to think logically, step-by-step, and create clear plans.\n"
            "Respond with a structured plan, numbered steps, and explicit decisions.\n\n"
        )

        task_line = f"Task: {task}\n"
        if context:
            ctx = f"Context:\n{context}\n\n"
        else:
            ctx = ""

        instructions = (
            "Please answer with:\n"
            "1. A short summary of the goal.\n"
            "2. A numbered list of steps.\n"
            "3. Risks or uncertainties to watch for.\n"
        )

        return base + task_line + ctx + instructions

    # --- public API -------------------------------------------------------

    def think(
        self,
        task: str,
        context: Optional[str] = None,
        emotions: Optional[EmotionState] = None,
    ) -> Tuple[str, float]:
        """
        Main call used by the core:

          text, used_temp = architect.think(task, context, emotions)

        Returns:
          - text: model's plan
          - used_temp: the final temperature we used (for logging)
        """

        temp = self._compute_temperature(emotions)
        prompt = self._build_prompt(task, context)

        text = self.model.generate(
            prompt=prompt,
            temperature=temp,
            max_tokens=self.config.max_tokens,
        )

        return text, temp

    # For backward-compat with older runner code that might call .run()
    def run(
        self,
        task: str,
        context: Optional[str] = None,
        emotions: Optional[EmotionState] = None,
    ) -> Tuple[str, float]:
        return self.think(task=task, context=context, emotions=emotions)
