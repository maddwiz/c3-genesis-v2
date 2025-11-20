"""
models/local_text_model.py

Simple local text model wrapper for C.3.

Right now this uses a small open model (TinyLlama) by default so it can
run on a single GPU. Later we can upgrade the model name in one place.

Important:
- Architect / Oracle call this with max_tokens=...
- We accept max_tokens and map it to HF's max_new_tokens.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import os
import torch

from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
)


@dataclass
class LocalTextModelConfig:
    model_name: str = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
    max_tokens: int = 256          # architect/oracle use this name
    temperature: float = 0.7
    device: Optional[str] = None   # "cuda", "cpu", or None for auto


class LocalTextModel:
    """
    Thin wrapper around a local HF causal LM.

    We keep this very simple for now:
    - load tokenizer + model once
    - provide a generate(prompt, ...) method
    - no GenerationConfig.clone() or fancy features
    """

    def __init__(self, config: Optional[LocalTextModelConfig] = None) -> None:
        if config is None:
            config = LocalTextModelConfig()
        self.config = config

        model_name = config.model_name

        print(f"[LocalTextModel] Loading model: {model_name}", flush=True)
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name)

        # Choose device
        if config.device is not None:
            self.device = config.device
        else:
            # Auto-pick CUDA if available
            self.device = "cuda" if torch.cuda.is_available() else "cpu"

        self.model.to(self.device)

        # Some tiny models don't have a pad token; fall back to eos
        if self.tokenizer.pad_token_id is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token

    def generate(
        self,
        prompt: str,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        **_: object,
    ) -> str:
        """
        Generate a response for the given prompt.

        - Architect / Oracle pass max_tokens=...
        - We map to HF max_new_tokens.
        - We ignore any extra kwargs (**_) for now.
        """

        if max_tokens is None:
            max_tokens = self.config.max_tokens
        if temperature is None:
            temperature = self.config.temperature

        inputs = self.tokenizer(
            prompt,
            return_tensors="pt",
        ).to(self.device)

        input_ids = inputs["input_ids"]
        attention_mask = inputs.get("attention_mask", None)

        with torch.no_grad():
            output_ids = self.model.generate(
                input_ids=input_ids,
                attention_mask=attention_mask,
                max_new_tokens=max_tokens,
                temperature=temperature,
                do_sample=True,
                top_p=0.95,
                pad_token_id=self.tokenizer.eos_token_id,
            )

        # Take only the newly generated tokens after the prompt
        generated_ids = output_ids[0, input_ids.shape[1]:]
        text = self.tokenizer.decode(
            generated_ids,
            skip_special_tokens=True,
            clean_up_tokenization_spaces=True,
        )
        return text.strip()
