"""
reasoning/oracle.py

OracleBrain = the intuitive / creative half of C.3's dual brain.

This version uses the shared LocalTextModel backend so we can swap
models in one place (models/local_text_model.py).

It also takes an "emotion state" dict so the Motivation Engine
can nudge the creativity level via temperature.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional, Tuple

from models.local_text_model import LocalTextModel, LocalTextModelConfig


EmotionState = Dict[str, float]


@dataclass
class OracleConfig:
    """
    Config for the OracleBrain.

    You can tweak:
      - base_temperature: default "creative" temp
      - max_tokens: how long Oracle answers can be
    """

    base_temperature: float = 0.8
    max_tokens: int = 256


class OracleBrain:
    """
    The intuitive / divergent brain.

    Responsibilities:
      - Take a task + optional context
      - Use LOCAL model to generate imaginative, alternative ideas
      - Run hotter (more creative) than Architect
      - Adjust temperature based on EmotionState
    """

    def __init__(
        self,
        config: Optional[OracleConfig] = None,
        model: Optional[LocalTextModel] = None,
    ) -> None:
        if config is None:
            config = OracleConfig()
        self.config = config

        # Shared model backend (TinyLlama or whatever C3_LOCAL_MODEL points to)
        self.model = model or LocalTextModel(LocalTextModelConfig())

    # --- internal helpers -------------------------------------------------

    def _compute_temperature(self, emotions: Optional[EmotionState]) -> float:
        """
        Map emotion signals to a creative temperature.

        Simple heuristic:
          - start from base_temperature
          - dopamine raises temp (more wild / explore)
          - serotonin slightly stabilizes (less chaos)
        """

        t = self.config.base_temperature

        if not emotions:
            return max(0.1, min(1.2, t))

        dopamine = float(emotions.get("dopamine", 0.6))      # 0..1
        serotonin = float(emotions.get("serotonin", 0.5))    # 0..1

        d_centered = dopamine - 0.5
        s_centered = serotonin - 0.5

        # Dopamine: lean into novelty
        t += 0.25 * d_centered
        # Serotonin: calm things down
        t -= 0.15 * s_centered

        return max(0.1, min(1.2, t))

    def _build_prompt(self, task: str, context: Optional[str]) -> str:
        """
        Build a creative prompt for the Oracle model.
        """

        base = (
            "You are the ORACLE brain of C.3.\n"
            "Your job is to be imaginative, lateral, and creative, while still being useful.\n"
            "Offer alternative angles, surprising ideas, and new ways to see the problem.\n\n"
        )

        task_line = f"Task: {task}\n"
        if context:
            ctx = f"Context:\n{context}\n\n"
        else:
            ctx = ""

        instructions = (
            "Please answer with:\n"
            "1. A surprising or creative reframe of the goal.\n"
            "2. Several unconventional ideas or options (bullet points).\n"
            "3. One bold suggestion and why it might work.\n"
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

          text, used_temp = oracle.think(task, context, emotions)

        Returns:
          - text: model's creative output
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
