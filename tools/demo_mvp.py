"""
tools/demo_mvp.py

Super simple MVP demo wrapper for C.3.

Instead of importing C3Core directly (and fighting Python package paths),
this script just shells out to:

    python3 -m core.runner "your task here"

So the source of truth remains core/runner.py, and this is a thin UX layer.
"""

import argparse
import subprocess
import shlex


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="python3 -m tools.demo_mvp",
        description="Run the C.3 MVP demo (dual-brain core) on a single task.",
    )
    parser.add_argument(
        "task",
        nargs="+",
        help="The task or request you want C.3 to think about.",
    )
    args = parser.parse_args()
    task_text = " ".join(args.task)

    print("=== C.3 MVP DEMO ===")
    print("--------------------")
    print(f"Task: {task_text}\n")

    # Build the command that we ALREADY know works:
    cmd = f'python3 -m core.runner {shlex.quote(task_text)}'
    print(f"[demo_mvp] Running: {cmd}\n")

    # Run core.runner as a subprocess and stream its output.
    completed = subprocess.run(cmd, shell=True)

    if completed.returncode != 0:
        print(f"\n[demo_mvp] core.runner exited with code {completed.returncode}")
    else:
        print("\n[demo_mvp] Done.")


if __name__ == "__main__":
    main()
