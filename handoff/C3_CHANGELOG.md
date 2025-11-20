# C.3 Genesis v2 – Handoff Changelog

This file is for new chat windows.  
It explains how the repo has evolved and what is SAFE to build on.

---

## 2025-11-18 — Clean MVP Snapshot + Dual-Brain Core

**Status:** ✅ Stable, do NOT delete without explicit migration.

- Nuked old git history and large `.venv` garbage.
- Re-initialized repo as `c3-genesis-v2` with a clean MVP skeleton.
- Added `.gitignore` so virtualenvs and heavy artifacts are never tracked again.
- Created top-level structure:
  - `bootstrap.py` – main CLI entry
  - `core/` – orchestrator + runner + brain selector
  - `reasoning/` – Architect, Oracle, MRE, emotions, reconcile
  - `memory/` – Spine v2 + diff + tests
  - `curiosity/` – curiosity + motivation stubs
  - `forge/` – Forge v1 self-improvement core
  - `meta/` – Meta-C3 stub + CoVe
  - `tools/` – CLI tools (demo, memory diff, forge, tests)
  - `docs/` + `handoff/` – handoff docs, filemap, changelog

**Key idea:** This snapshot is the **new ground zero** for C.3.

---

## 2025-11-18 — Memory Layer v2 (Spine + Diff)

**Status:** ✅ Stable, safe to extend.

- Implemented `memory/spine.py`:
  - Local JSONL-based Memory Spine v2 (append-only events, timestamped).
  - Simple load/save helpers for early MVP.
- Implemented `memory/diff.py`:
  - Compare two JSONL files and show differences.
  - Used by `tools/c3_memory_diff.py`.
- Added test artifacts:
  - `memory/events.jsonl`
  - `memory/memory.jsonl`
  - `memory/test_events.jsonl`
  - `memory/test_memory.py`

**Why it matters:** Proves **identity continuity** and enables demos where C.3 “remembers” across runs.

---

## 2025-11-18 — Dual-Brain + MRE + Emotions

**Status:** ✅ Core design locked in; implementations are MVP but correct shape.

- `reasoning/architect.py`
  - ArchitectBrain: slow, logical, planning-oriented.
- `reasoning/oracle.py`
  - OracleBrain: fast, creative, divergent.
- `reasoning/mre.py`
  - Markovian Reasoning Engine (MRE) v1:
    - Chunked context
    - Carry-over summaries (COS)
- `reasoning/emotions.py`
  - Chemical model:
    - dopamine, serotonin, cortisol, focus (all in [0.0, 1.0])
    - used to modulate style/temperature.
- `reasoning/reconcile.py`
  - Reconcile dual outputs from Architect + Oracle.
  - Uses chemical state to decide how much to trust each brain.

**Why it matters:** This is C.3’s **System 1 / System 2 duality**.

---

## 2025-11-18 — Curiosity + Motivation v0.1

**Status:** ✅ MVP complete; can be deepened later.

- `curiosity/curiosity.py`
  - Frontier queue + basic curiosity hooks.
- `curiosity/motivation.py`
  - MotivationEngine v0.1:
    - Takes task + chemicals
    - Produces a MotivationState used by reconcile / runner.
- `tools/test_motivation.py`
  - Tiny harness to exercise MotivationEngine and print chemicals/state.

**Why it matters:** Gives the dual-brain a **reason** to choose different modes per task.

---

## 2025-11-18 — Meta-C3 + CoVe Stubs

**Status:** ✅ Lightweight but important; keep and extend.

- `meta/c3_sim.py`
  - Meta-C3 stub to simulate C.3 on a task in a sandbox.
- `meta/c3_sim_cli.py`
  - CLI wrapper so we can call Meta-C3 from terminal.
- `meta/cove.py`
  - CoVe / verification budget stubs:
    - Placeholders for meta-verification and token/latency budgeting.

**Why it matters:** This is the **hook for future self-modeling and safe self-play**.

---

## 2025-11-18 — Forge v1 (Self-Improvement Engine)

**Status:** ✅ MVP milestone; central to the story.

- `forge/forge.py`
  - Core orchestrator for self-improvement:
    - Reads targets
    - Plans small changes
    - Writes suggestions to staging.
- `forge/pr.py`
  - Helper logic for “PR-like” suggestions.
- `forge/staging.json`
  - Simple JSON file for recording suggested changes.
- `tools/forge_suggest.py`
  - CLI tool to:
    - Analyze `reasoning/reconcile.py`
    - Propose a tiny, safe change
    - Write a `*.suggested.py` file.

**Why it matters:** Demonstrates that **C.3 can reason about its own code and propose improvements**.

---

## 2025-11-18 — MVP Demo Script + Runner

**Status:** ✅ Working MVP; safe to show in early demos.

- `core/c3_core.py`
  - Orchestrator that ties:
    - brains (Architect/Oracle),
    - MRE,
    - emotions,
    - motivation,
    - memory (where needed).
- `core/runner.py`
  - Simple CLI runner used by the MVP demo.
- `bootstrap.py`
  - Entry point used by demo and tools.
- `tools/demo_mvp.py`
  - Main MVP demo script:
    - Takes a simple task (e.g., “Plan my day”)
    - Runs dual-brain reasoning
    - Prints out:
      - Architect output
      - Oracle output
      - Reconciled output
      - Chemical/motivation state

**Why it matters:** This is the **Dec 16 / 30-day MVP spine**.

---

## 2025-11-18 — Handoff System v2 (This Folder)

**Status:** ✅ Critical for cross-window continuity.

- `handoff/C3_MASTER_HANDOFF.md`
  - High-level architecture + build order for new windows.
- `handoff/C3_FILEMAP.json`
  - Machine-friendly index of important files (used first in new windows).
- `handoff/C3_CHANGELOG.md` (this file)
  - Short, focused evolution log.

---

## What’s Next (Not Done Yet, but Planned)

These items are **planned** but not yet implemented.  
New windows should **not assume they exist** until changelog says so.

- Wire real local models into `models/local_backend.py` and `models/local_text_model.py`.
- Use MotivationEngine output directly inside `core/c3_core.py` and `reasoning/reconcile.py` for more visible behavior differences.
- Add a tiny, scripted “first dollar to a user” path for future Lightning mesh rewards (no crypto infra yet).
- Expand Meta-C3 and Forge to run real A/B tests on suggested changes before a human applies them.

When these land, they should be added here with date + status.
