# C.3 Genesis v2 — Master H9andoff

Owner: Desmond  
Repo: `c3-genesis-v2`  
Date: 2025-11-19  
Status: MVP spine in place (no big models wired yet, safe to extend)

This file is for **new chat windows** and future you.  
It explains:

- What C.3 is (v2)
- How the repo is structured
- What is already implemented
- What is planned but NOT built yet
- How to safely evolve the code without breaking the vision

---

## 0. What C.3 Is (v2)

C.3 is a **local, sovereign cognitive OS**, not “just a chatbot”.

Core ideas:

- **Dual-brain reasoning**  
  - ArchitectBrain → slow, logical, planner
  - OracleBrain → fast, creative, divergent
  - Reconcile layer blends them.

- **Markovian Reasoning Engine (MRE)**  
  - Long reasoning is split into chunks.
  - A “carry-over summary” (COS) passes forward between chunks instead of reloading full history.

- **Memory Spine v2**  
  - Local JSONL memory that logs events, thoughts, and state.
  - Used for continuity and later continual learning.

- **Emotions & Motivation (v0.1)**  
  - Chemical-like signals: dopamine, serotonin, cortisol, focus.
  - Motivation engine will modulate how the dual-brain behaves on each task.

- **Forge v1**  
  - Self-improvement engine.
  - Reads code, suggests small changes, and writes them to a “staging” file instead of auto-editing.

- **Meta-C3 stub**  
  - A way to “simulate C.3 on a task” in a sandbox without touching real state.  
  - Future hook for recursive self-modeling.

All of this is designed to run:

- **fully offline**
- **inside your DGX / local machine**
- with **open models** later wired in.

---

## 1. Repo Layout (Authoritative for v2)

High-level directory map (this is the structure new windows should trust):

- `bootstrap.py`  
  - Entry point for CLI demos and tools.

- `core/`
  - `__init__.py`
  - `brain_selector.py` → Decides which brain(s) to use.
  - `c3_core.py` → Orchestrator tying together brains, MRE, motivation, etc.
  - `interfaces/brain_interface.py` → Base class / contract for any brain.
  - `runner.py` → Simple runner used by MVP demo.

- `reasoning/`
  - `__init__.py`
  - `architect.py` → ArchitectBrain implementation (logic).
  - `oracle.py` → OracleBrain implementation (creative).
  - `mre.py` → Markovian Reasoning Engine (chunked reasoning + COS).
  - `emotions.py` → Chemical state (dopamine, serotonin, cortisol, focus).
  - `reconcile.py` → Reconcile outputs from Architect + Oracle, using emotions/motivation.

- `memory/`
  - `__init__.py`
  - `spine.py` → Memory Spine v2 (JSONL, append-only events).
  - `diff.py` → Compare two memory files (old vs new, etc.).
  - `events.jsonl`, `memory.jsonl` → Example data for demos.
  - `test_events.jsonl`, `test_memory.py` → Small tests / harnesses.

- `curiosity/`
  - `__init__.py`
  - `curiosity.py` → Frontier queue + curiosity stubs.
  - `motivation.py` → MotivationEngine v0.1 (turns task + chemicals into a MotivationState).

- `forge/`
  - `forge.py` → Forge v1 orchestrator (self-improvement engine).
  - `pr.py` → Helper functions for “PR-like” suggestions.
  - `staging.json` → Where Forge records suggested changes.

- `meta/`
  - `__init__.py`
  - `c3_sim.py` → Meta-C3 stub (simulate C.3 on a task).
  - `c3_sim_cli.py` → CLI wrapper to call Meta-C3 from the terminal.
  - `cove.py` → Verification / budget stubs (for meta-verification later).

- `models/`
  - `local_backend.py` → Abstraction over whatever model backend we use locally (e.g., vLLM, llama.cpp, etc.).
  - `local_text_model.py` → Simple text model wrapper (currently stubbed).

- `narrative/`
  - `__init__.py`
  - `engine.py` → Narrative engine stubs (chapters, storyline over time).

- `simulation/`
  - `.keep` → Folder created, not yet used. Reserved for future world/simulation logic.

- `tooling/`
  - `tools.py` → Shared tool helpers (logging, printing, timing, etc.).

- `tools/` (CLI tools)
  - `__init__.py`
  - `demo_mvp.py` → MVP demo: runs dual-brain reasoning on a sample task.
  - `c3_memory_diff.py` → CLI wrapper for memory diff.
  - `forge_suggest.py` → Runs Forge v1 to suggest a small code change.
  - `test_motivation.py` → Quick test harness for MotivationEngine.

- `handoff/`
  - `.keep`
  - `C3_MASTER_HANDOFF.md` → This file.
  - `C3_FILEMAP.json` → Machine-friendly map of important files.
  - `C3_CHANGELOG.md` → Evolution log (what changed, when, why).

- `docs/`
  - Currently mirrors some of the handoff docs.  
  - For v2: **`handoff/` is authoritative**.  
    `docs/` can be used for extended docs, but new logic should be documented in `handoff/` first.

- `.gitignore`
  - Ensures `.venv/`, big libs, and other junk are **not tracked**.

- `README.md`
  - High-level description of the project (can be expanded later).

---

## 2. Cognitive Architecture (Layer View)

For future reference, these are the **conceptual layers** C.3 is built around:

1. **Interface Layer**  
   - CLI, (later) UI, voice, user profile.

2. **Perception Layer**  
   - Text parsing now; OCR / multimodal later.

3. **Memory Layer**  
   - Memory Spine v2, Memory Diff, MRE integration.

4. **Reasoning Layer**  
   - ArchitectBrain, OracleBrain, MRE, Reconcile.

5. **Curiosity Layer**  
   - Frontier queue, unknown detection.

6. **Learning Layer** (future)  
   - EML, Skill Capsules, Meta-Lab.

7. **Tooling & Action Layer**  
   - Code execution, shell tools, API calls.

8. **Mesh Orchestration Layer** (future)  
   - Distributed jobs, node credits, etc.

9. **Sovereignty Layer** (future)  
   - Guardian Law, permissions, failsafes.

10. **Self-Reflection Layer** (future expansion of current meta/CoVe)  
    - Meta-thinking about strategies and mistakes.

11. **Simulation Layer** (future)  
    - Multi-world “what-if” sandbox.

12. **Compression Layer** (future)  
    - Concept cards, event horizon compression.

13. **Emotion / Value Layer**  
    - Chemicals, value estimation, priority.

14. **Concept Fusion Layer** (future)  
    - Cross-domain creativity.

15. **Strategic Autonomy Layer** (future)  
    - Goal-setting, task graphs, long-horizon planning.

Not all of these layers are fully implemented yet, but the file layout is designed to evolve into this structure.

---

## 3. What Is Already Implemented (MVP-Level)

### 3.1 Dual-Brain + MRE + Emotions

Implemented:

- `reasoning/architect.py`
- `reasoning/oracle.py`
- `reasoning/mre.py`
- `reasoning/emotions.py`
- `reasoning/reconcile.py`
- `core/brain_selector.py`
- `core/c3_core.py`
- `core/runner.py`

Capabilities:

- Run Architect + Oracle on a task.
- Use MRE to support longer reasoning via summaries.
- Maintain a simple chemical state.
- Reconcile outputs into a final answer (MVP logic).

### 3.2 Memory Spine v2 + Diff

Implemented:

- `memory/spine.py`
- `memory/diff.py`
- `tools/c3_memory_diff.py`
- `memory/events.jsonl`, `memory/memory.jsonl`, `memory/test_events.jsonl`
- `memory/test_memory.py`

Capabilities:

- Append events to a JSONL memory file.
- Compare two memory snapshots and show differences.
- Use as backend for demos showing “C.3 remembers”.

### 3.3 Curiosity + Motivation v0.1

Implemented:

- `curiosity/curiosity.py`
- `curiosity/motivation.py`
- `tools/test_motivation.py`

Capabilities:

- Basic curiosity stubs.
- MotivationEngine that:
  - Takes a task + chemicals.
  - Outputs a MotivationState.
- Test script to poke it and print out results.

### 3.4 Forge v1 + CLI

Implemented:

- `forge/forge.py`
- `forge/pr.py`
- `forge/staging.json`
- `tools/forge_suggest.py`

Capabilities:

- Inspect a target file (e.g. `reasoning/reconcile.py`).
- Generate a tiny “suggested” change.
- Write suggestions out to a `*.suggested.py` file and/or JSON staging.

### 3.5 Meta-C3 Stub + CLI

Implemented:

- `meta/c3_sim.py`
- `meta/c3_sim_cli.py`
- `meta/cove.py` (stubs)

Capabilities:

- Simulated C.3 runs in sandbox mode (MVP-level).
- CoVe stubs prepare for later meta-verification and budgets.

### 3.6 MVP Demo Script

Implemented:

- `tools/demo_mvp.py`
- `bootstrap.py`

Capabilities:

- Run a small MVP demo from the terminal:
  - Dual-brain reasoning on a toy task.
  - Show per-brain outputs and reconciled result.
  - Show some state (chemicals, motivation, etc).

---

## 4. What Is NOT Implemented Yet (Important)

These ideas are **planned** but not yet built (or only partially stubbed).  
New windows must **not assume** they exist:

- Real model wiring:
  - `models/local_backend.py` and `models/local_text_model.py` are stubs.
  - No real LLM is hooked up yet.

- Full Motivation wiring:
  - MotivationEngine exists, but c3_core / reconcile may still treat chemicals mostly as neutral.
  - We eventually want task → motivation → modulated brain behavior.

- Narrative auto-chaptering:
  - `narrative/engine.py` is still minimal.
  - No automated “chapters” from long memory timelines yet.

- Mesh / node credits / Lightning:
  - Mesh layer and real payments are not built yet.
  - Only concepts are reserved; no code exists.

- Advanced Self-Reflection / Evaluation:
  - `meta/cove.py` is a placeholder.
  - No real meta-verification logic yet.

- Sim / world model:
  - `simulation/` is empty (except `.keep`).
  - No world model, no Monte Carlo search, no Dreamer-like sims yet.

When any of these land, they should be added to `handoff/C3_CHANGELOG.md` with date + status.

---

## 5. How to Run the Main Demos (for Future You / New Windows)

From the project root (`~/c3-genesis-v2`), with your virtualenv active:

1. **MVP Dual-Brain Demo**

   ```bash
   python -m tools.demo_mvp

	2.	Memory Diff Demo
python -m tools.c3_memory_diff

3.	Motivation Test
python -m tools.test_motivation

4.	Forge Suggestion Demo
python -m meta.c3_sim_cli

5.	Meta-C3 Sim Demo
python -m meta.c3_sim_cli

If any of these fail in the future, fix them before adding new complexity.

⸻

6. Rules for Future Changes (Do Not Break These)

To keep C.3 coherent across windows:
	1.	Do not track .venv/ or big binaries
	•	.gitignore already handles this — don’t remove those rules.
	2.	Always update handoff + changelog after major changes
	•	If you add a new file or change behavior in a big way:
	•	Update handoff/C3_FILEMAP.json
	•	Append a section to handoff/C3_CHANGELOG.md
	3.	Never silently delete core modules
	•	If you deprecate a file:
	•	Note it explicitly in the changelog.
	4.	Keep tools working
	•	tools/demo_mvp.py, tools/c3_memory_diff.py, tools/forge_suggest.py should always work.
	•	They are the “health check” for the system.
	5.	Small, surgical changes
	•	Prefer tiny PR-like changes:
	•	E.g. tweak one function, then test.
	•	Avoid massive refactors in a single jump.

⸻

7. Short Build Order (Next Steps)

If a new window needs to know “what to build next”, this is the priority:
	1.	Tighten MVP demo and motivation wiring
	•	Make sure motivation is clearly visible in demo output.
	•	Use chemicals to change behavior (e.g., more exploratory vs more conservative).
	2.	Wire a real local model into models/local_text_model.py
	•	Start with a tiny open model that fits easily on the DGX.
	•	Connect brains to that backend cleanly.
	3.	Steady Forge v1
	•	Ensure Forge suggestions are safe, small, and easy to diff.
	•	Optionally add a “review” step that prints suggestions clearly.
	4.	Narrative v0.1
	•	From Memory Spine, auto-generate very simple “chapters” to summarize time ranges.
	5.	Meta-C3 improvements
	•	Make meta/c3_sim.py use the same core flows as the main C.3, but in a fully sandboxed context.

Only after these are stable should you move on to:
	•	Mesh / node credits
	•	Deeper world model
	•	Advanced self-reflection and evaluation
	•	Lightning payments, neuromorphic ports, etc.

⸻

8. How New Windows Should Sync

When a new chat window starts and needs repo context, it should:
	1.	Read this file first:
	•	handoff/C3_MASTER_HANDOFF.md
	2.	Then load the file map:
	•	handoff/C3_FILEMAP.json
	3.	Then read the changelog:
	•	handoff/C3_CHANGELOG.md
	4.	Only then, open specific files mentioned as important (e.g. core/c3_core.py, reasoning/reconcile.py, etc.), instead of trying to read the whole repo.

This keeps token usage low and continuity high.

⸻

End of Master Handoff v2

If you drastically change architecture, bump the version and document it here.


1. In your DGX terminal:

   ```bash
   cd ~/c3-genesis-v2
   nano handoff/C3_MASTER_HANDOFF.md

	2.	Hold Ctrl+A then Ctrl+K a bunch to delete everything (or just backspace until empty).
	3.	Paste the big block above (from # C.3 Genesis v2 — Master Handoff all the way to the end).
	4.	Press Ctrl+O, then Enter to save.
	5.	Press Ctrl+X to exit nano.

