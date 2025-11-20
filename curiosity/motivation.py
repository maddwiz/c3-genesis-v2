"""
curiosity/motivation.py

Intrinsic Motivation Engine v0.1 for C.3.

This module:
- Maintains a simple "chemical state" (dopamine, serotonin, norepinephrine, oxytocin).
- Takes a context dict (task, novelty, difficulty, user urgency, recent success/failure).
- Returns updated chemicals + a "motivation score" and a "mode" (explore vs exploit).

Architect / Oracle / Reconcile can use:
- chemicals["dopamine"] to bias curiosity / exploration.
- chemicals["norepinephrine"] to bias focus / urgency.
- chemicals["serotonin"] / chemicals["oxytocin"] for stability / social tasks.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Literal, Tuple


Chemicals = Dict[str, float]
MotivationMode = Literal["explore", "exploit", "idle"]


@dataclass
class MotivationResult:
    chemicals: Chemicals
    score: float
    mode: MotivationMode


def _clip01(x: float) -> float:
    return max(0.0, min(1.0, float(x)))


def default_chemicals() -> Chemicals:
    """
    Neutral baseline state.
    """
    return {
        "dopamine": 0.5,       # curiosity / reward anticipation
        "serotonin": 0.5,      # stability / mood
        "norepinephrine": 0.5, # alertness / urgency
        "oxytocin": 0.5,       # social / bonding
    }


def update_chemicals(
    *,
    chemicals: Chemicals | None,
    context: Dict[str, float],
) -> MotivationResult:
    """
    Compute a new chemical state from the previous state + a context.

    Expected context keys (all optional, default 0.0):
      - novelty            (0–1)   how new / unknown this situation feels
      - difficulty         (0–1)   how hard the task seems
      - user_urgency       (0–1)   how urgent the user made it sound
      - recent_success     (0–1)   1.0 if we just succeeded at something
      - recent_failure     (0–1)   1.0 if we just failed at something
      - social_relevance   (0–1)   how much this involves relationships / people
    """
    if chemicals is None:
        chemicals = default_chemicals()
    else:
        # make a shallow copy to avoid mutating caller state
        chemicals = dict(chemicals)

    novelty = float(context.get("novelty", 0.0))
    difficulty = float(context.get("difficulty", 0.0))
    user_urgency = float(context.get("user_urgency", 0.0))
    recent_success = float(context.get("recent_success", 0.0))
    recent_failure = float(context.get("recent_failure", 0.0))
    social_relevance = float(context.get("social_relevance", 0.0))

    # start from previous values
    dopa = chemicals.get("dopamine", 0.5)
    sero = chemicals.get("serotonin", 0.5)
    nore = chemicals.get("norepinephrine", 0.5)
    oxty = chemicals.get("oxytocin", 0.5)

    # --- update rules (super simple v0.1) ---

    # dopamine:
    # - up with novelty and success
    # - down a bit with repeated failure
    dopa += 0.3 * novelty
    dopa += 0.2 * recent_success
    dopa -= 0.2 * recent_failure

    # serotonin:
    # - up a bit with success
    # - down with failure and extreme difficulty
    sero += 0.1 * recent_success
    sero -= 0.2 * recent_failure
    sero -= 0.1 * max(0.0, difficulty - 0.7)

    # norepinephrine:
    # - up with urgency and difficulty
    # - down a bit with high serotonin (calm)
    nore += 0.3 * user_urgency
    nore += 0.2 * difficulty
    nore -= 0.1 * sero

    # oxytocin:
    # - up when tasks are social / relational
    # - down slightly if repeated failure (less trust / connection)
    oxty += 0.3 * social_relevance
    oxty -= 0.1 * recent_failure

    chemicals["dopamine"] = _clip01(dopa)
    chemicals["serotonin"] = _clip01(sero)
    chemicals["norepinephrine"] = _clip01(nore)
    chemicals["oxytocin"] = _clip01(oxty)

    # --- derive mode + score ---

    # "motivation score" is mostly dopamine + urgency
    score = float(0.6 * chemicals["dopamine"] + 0.4 * chemicals["norepinephrine"])

    if score < 0.25:
        mode: MotivationMode = "idle"
    elif chemicals["dopamine"] >= chemicals["norepinephrine"]:
        mode = "explore"
    else:
        mode = "exploit"

    return MotivationResult(
        chemicals=chemicals,
        score=score,
        mode=mode,
    )


def simple_context_from_task(task: str) -> Dict[str, float]:
    """
    Tiny helper to infer a rough context from a plain-text task string.
    This will be replaced later by a smarter classifier.

    Heuristics:
      - "debug", "error"  → high difficulty, high urgency
      - "learn", "explore" → high novelty
      - "friend", "relationship" → high social_relevance
    """
    t = task.lower()

    novelty = 0.0
    difficulty = 0.2
    user_urgency = 0.1
    social_relevance = 0.0

    if any(k in t for k in ["learn", "explore", "new", "unknown"]):
        novelty = 0.8
    if any(k in t for k in ["debug", "error", "bug", "fix"]):
        difficulty = 0.8
        user_urgency = 0.9
    if any(k in t for k in ["urgent", "asap", "now", "deadline"]):
        user_urgency = 0.9
    if any(k in t for k in ["friend", "relationship", "social", "family"]):
        social_relevance = 0.8

    return {
        "novelty": novelty,
        "difficulty": difficulty,
        "user_urgency": user_urgency,
        "social_relevance": social_relevance,
        "recent_success": 0.0,
        "recent_failure": 0.0,
    }
