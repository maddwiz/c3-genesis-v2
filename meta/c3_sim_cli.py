"""
meta/c3_sim_cli.py — Meta-C3 Command-Line Runner

Lets you run a Meta-C3 simulation from the terminal:

    python3 -m meta.c3_sim_cli "plan my day"
"""

import argparse

from .c3_sim import simulate_c3


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a Meta-C3 simulation")
    parser.add_argument(
        "task",
        type=str,
        help="Task description to simulate (e.g., 'plan my day')",
    )
    parser.add_argument(
        "--mode",
        type=str,
        default="default",
        help="Optional simulation mode tag.",
    )

    args = parser.parse_args()

    sim_result = simulate_c3(task=args.task, mode=args.mode)

    print("\n=== Meta-C3 Simulation Result ===")
    print(sim_result.to_json())


if __name__ == "__main__":
    main()
