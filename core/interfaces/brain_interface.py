class BrainInterface:
    """
    A simple interface that all C.3 'brains' must follow.
    Both ArchitectBrain and OracleBrain will inherit from this.
    """

    def generate(self, prompt: str) -> str:
        """
        Generate text output given a prompt.

        In the MVP, this is simulated text.
        In Phase 2, this will call real model APIs / local inference.
        """
        raise NotImplementedError("generate() must be implemented by subclasses.")
