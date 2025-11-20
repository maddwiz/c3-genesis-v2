# C.3 — Core Architecture Handoff (v0.3, MVP Complete)

Owner: Desmond  
Repo: `c3-genesis-v2`  
Date: 2025-11-19 (Spark DGX)

This handoff describes **exactly what exists in this repo right now** and how it fits into the bigger C.3 vision.

It is the single source of truth for new chat windows and future refactors.

---

## 1. High-Level: What C.3 Is (Right Now)

C.3 is a **local, sovereign dual-brain cognitive OS** with:

- A **core runner** that calls:
  - Architect Brain (logic / planning)
  - Oracle Brain (creative / exploratory)
  - Reconcile Layer (chooses who to trust)
- A **Motivation Engine** with simple “chemical” signals:
  - `dopamine`, `norepinephrine`, `serotonin`, `oxytocin`
- A **Forge v1** lane for self-improvement:
  - CLI tools + a visible `forge_suggest` demo that generates a suggested version of a code file.
- A **one-line MVP demo tool**:
  - `python3 -m tools.demo_mvp "your task here"`

This repo is a **clean v2 skeleton**, not the old v1.  
The goal: be easy to evolve, easy to reason about, and easy to demo.

---

## 2. Directory Map (What Lives Where)

```text
c3-genesis-v2/
  bootstrap.py          # Ensures repo root is on sys.path
  pyproject.toml        # Python project metadata
  README.md             # High-level intro (can be expanded)

  core/
    __init__.py
    core.py             # C3Core class: main orchestrator
    runner.py           # CLI entry: python3 -m core.runner "task"

  reasoning/
    __init__.py
    architect.py        # ArchitectBrain: logical, step-by-step model
    oracle.py           # OracleBrain: creative / divergent model
    reconcile.py        # ReconcileResult + reconcile() dual-brain choice logic

  curiosity/
    __init__.py
    motivation.py       # MotivationEngine: chemicals + motivation score

  tools/
    __init__.py
    test_motivation.py  # CLI to test motivation engine
    forge_cli.py        # Forge v1: core CLI skeleton for self-improvement
    forge_suggest.py    # NEW: generates <file>.suggested.py for visible self-change
    demo_mvp.py         # MVP demo wrapper around core.runner

  docs/
    C3_MASTER_HANDOFF.md  # This file
