"""
models/local_backend.py

Tiny local backend stub for C.3 brains.
Both ArchitectBrain and OracleBrain will call into this module.

For now, this does NOT use a real model.
It just returns a simple tagged string so we can see the plumbing working.

Later, we can:
- Swap this for a real local model (Qwen, LLaMA, etc.)
- Add different configs for Architect vs Oracle (temperature, system prompts, etc.)
"""


from typing import Literal


BrainName = Literal["architect", "oracle"]


class LocalModelBackend:
    """
    Shared backend for both brains.

    In the future:
    - Load a real model in __init__
    - Use different generation parameters per brain
    """

    def __init__(self):
        # Placeholder for future real model / tokenizer, etc.
        self._loaded = False

    def generate(self, brain: BrainName, prompt: str) -> str:
        """
        Simple stub generator.

        Args:
            brain: "architect" or "oracle"
            prompt: input text

        Returns:
            A tagged string indicating which brain generated the text.
        """
        if brain == "architect":
            prefix = "[ARCH-BACKEND]"
        elif brain == "oracle":
            prefix = "[ORACLE-BACKEND]"
        else:
            prefix = "[UNKNOWN-BACKEND]"

        return f"{prefix} Generated response for: {prompt!r}"


# Singleton instance to be imported by reasoning modules
backend = LocalModelBackend()
