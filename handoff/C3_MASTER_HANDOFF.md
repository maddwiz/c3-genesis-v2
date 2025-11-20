# C.3 MASTER HANDOFF (v2, Spark Rig)

Owner: Desmond  
Repo: `c3-genesis-v2`  
Mode: MVP Skeleton + Dual-Brain + Memory + Forge v1

This file tells any new chat window:
- What C.3 is right now
- What files exist and what they do
- What is safe/stable
- What to build next (in order)

---

## 0. HIGH-LEVEL SNAPSHOT

C.3 is a **local, sovereign cognitive OS** with:

- Dual-brain architecture:
  - ArchitectBrain = logical / planner
  - OracleBrain    = creative / explorer
- Emotion engine that modulates both brains
- Memory Spine + diff tools for identity over time
- Meta-C3 simulator for safe self-testing
- Forge v1 for self-improvement (proposing code diffs)
- Intrinsic Motivation Engine v0.1 (chemical-style curiosity)

This repo is **v2**, a clean skeleton.  
The older, heavier experiments live in the original `c3-genesis` repo and are treated as an archive.

---

## 1. DIRECTORY MAP (CURRENT STATE)

### 1.1 Core

**`core/`**

- `core/context.py`  
  - Defines the minimal C.3 context object (config, mode, etc.).
  - Used by C3Core and Meta-C3.
- `core/c3_core.py`  
  - High-level “brain” orchestrator for Architect + Oracle + Reconcile + Memory.
- `core/runner.py`  
  - Simple CLI entrypoint to run C.3 on a task (MVP demo).

**`core/interfaces/`**

- `core/interfaces/brain_interface.py`  
  - Base class for all “brains” (ArchitectBrain, OracleBrain).
  - Exposes `generate(prompt: str) -> str` as the standard API.

- `core/interfaces/context_interface.py`  
  - Base interface for context objects (clone, read-only access, etc.).
  - Used by Meta-C3 Simulator.

---

### 1.2 Reasoning (Dual-Brain + Emotions)

**`reasoning/`**

- `reasoning/architect.py`  
  - ArchitectBrain (logical / structured reasoning brain).
  - Currently a stub:
    - `generate(prompt)` → `[ARCH] Logical reasoning for: ...`
    - `think(task)` → wrapper around `generate(task)` for backwards compatibility.
  - In Phase 2, this will call a real local model (e.g., Qwen, Llama).

- `reasoning/oracle.py`  
  - OracleBrain (creative / exploratory brain).
  - Currently a stub:
    - `generate(prompt)` → `[ORACLE] Creative idea for: ...`
    - `think(task)` → wrapper around `generate(task)`.

- `reasoning/emotions.py`  
  - EmotionEngine:
    - Tracks simple chemical-style signals: dopamine, serotonin, norepinephrine, oxytocin.
    - Computes temperatures for Architect and Oracle.
    - Used by Reconcile to bias decisions.

- `reasoning/reconcile.py`  
  - Reconcile engine:
    - Takes Architect + Oracle outputs + emotions.
    - Decides who “wins” for this step.
    - Outputs:
      - choice (architect/oracle)
      - rationale
      - updated emotions
      - architect_temperature
      - oracle_temperature
      - final_text (for user / downstream tools).

- `reasoning/mre.py`  
  - Markovian Reasoning Engine (MRE) v1 skeleton.
  - Chunked reasoning with carry-over summaries (COS).
  - Will integrate with Memory Spine and Compression later.

---

### 1.3 Memory

**`memory/`**

- `memory/spine.py`  
  - Memory Spine v2 (MVP):
    - Append-only log of events.
    - In-memory index for now (future: SQLite + vector index).
    - Basic `add_event`, `get_events`, etc.

- `memory/diff.py`  
  - Memory diff tools:
    - Compare snapshots of events.
    - Powers the “memory diff” CLI tool.

---

### 1.4 Tools / CLI

**`tools/`**

- `tools/c3_memory_diff.py`  
  - CLI:
    - `python3 -m tools.c3_memory_diff`  
      → prints a simple diff between two snapshots (placeholder).
  - Uses `memory/spine.py` + `memory/diff.py`.

---

### 1.5 Meta / Simulation

**`meta/`**

- `meta/c3_sim.py`  
  - Meta-C3 simulator:
    - Clones context.
    - Runs Architect + Oracle + Reconcile in **simulation mode**.
    - Does NOT touch real memory/state.
    - Returns a structured trace (JSON-like dict).

- `meta/c3_sim_cli.py`  
  - CLI:
    - `python3 -m meta.c3_sim_cli "your task"`  
    - Runs a simulation and prints a pretty JSON result.

---

### 1.6 Forge (Self-Improvement)

**`forge/`**

- `forge/pr.py`  
  - Forge v1 — Auto-PR Simulator (MVP):
    - Takes `old_text` and `new_text` of a file.
    - Computes a unified diff.
    - Appends suggestion to `forge/staging.json`.
    - Does **NOT** auto-apply changes yet (safety).
  - CLI:
    - `python3 -m forge.pr old.txt new.txt target_file.py`

---

### 1.7 Curiosity / Motivation

**`curiosity/`**

- `curiosity/motivation.py`  
  - Intrinsic Motivation Engine v0.1:
    - Reads chemical signals:
      - dopamine, serotonin, norepinephrine, oxytocin.
    - Generates small internal goals like:
      - `explore_new_skill`
      - `simplify_internal_plan`
      - `continue_current_task`
      - `improve_companion_dialogue`
      - or neutral self-improvement actions.
    - Exposes a singleton `motivation_engine`.

---

## 2. WHAT IS STABLE VS EXPERIMENTAL

**Stable (do NOT casually rewrite):**

- `core/context.py`
- `core/interfaces/brain_interface.py`
- `core/interfaces/context_interface.py`
- `reasoning/emotions.py`
- `reasoning/reconcile.py`
- `meta/c3_sim.py`
- `meta/c3_sim_cli.py`
- `memory/spine.py`
- `memory/diff.py`
- `tools/c3_memory_diff.py`
- `forge/pr.py`
- `curiosity/motivation.py`

**Flexible / can be expanded but keep the shape:**

- `core/c3_core.py`
- `core/runner.py`
- `reasoning/architect.py`
- `reasoning/oracle.py`
- `reasoning/mre.py`

---

## 3. CURRENT MVP DEMOS

These should work without real models (using stubs):

1. **Meta-C3 Simulation**

   ```bash
   cd ~/c3-genesis-v2
   python3 -m meta.c3_sim_cli "test the dual brain"
