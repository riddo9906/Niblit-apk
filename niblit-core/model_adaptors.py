# model_adapters.py
import os
import subprocess
import json
import time

# Adapter interface: implement .generate(prompt: str, max_tokens=256) -> str

class BaseAdapter:
    def generate(self, prompt: str, max_tokens=256, stream=False):
        raise NotImplementedError

class EchoAdapter(BaseAdapter):
    """Fallback adapter for testing: returns a simple echo + small logic"""
    def generate(self, prompt, max_tokens=256, stream=False):
        # very simple "intelligent" fallback
        if "what is" in prompt.lower():
            return "I don't have an LLM backend configured. This is a fallback answer. Try installing a local model or enabling an API adapter."
        return "Niblit (fallback): " + (prompt[:max_tokens])

class OpenAIAdapter(BaseAdapter):
    def __init__(self, api_key=None, model="gpt-3.5-turbo"):
        try:
            import openai
        except ImportError:
            raise RuntimeError("openai package not installed. pip install openai")
        self.openai = openai
        if api_key:
            self.openai.api_key = api_key
        self.model = model

    def generate(self, prompt, max_tokens=256, stream=False):
        # simple single-turn call
        resp = self.openai.ChatCompletion.create(
            model=self.model,
            messages=[{"role":"system","content":"You are Niblit."},
                      {"role":"user","content":prompt}],
            max_tokens=max_tokens,
            temperature=0.7
        )
        return resp.choices[0].message.content.strip()

class LlamaCppAdapter(BaseAdapter):
    """
    Adapter that calls a local `llama.cpp`-style binary.
    Requires you to have a llama.cpp or compatible binary that accepts stdin or args.
    Configure binary path and model path externally.
    """
    def __init__(self, binary_path="llama.cpp/llama", model_path=None, args=None):
        self.binary_path = binary_path
        self.model_path = model_path
        self.args = args or []

    def generate(self, prompt, max_tokens=256, stream=False):
        if not self.model_path:
            raise RuntimeError("LlamaCppAdapter requires model_path to be set.")
        # This is a generic example calling llama.cpp's `main` that accepts -m model -p prompt
        cmd = [self.binary_path, "-m", self.model_path, "-p", prompt, "-n", str(max_tokens)] + self.args
        try:
            out = subprocess.check_output(cmd, stderr=subprocess.STDOUT, universal_newlines=True, timeout=120)
            return out
        except subprocess.CalledProcessError as e:
            return f"Error calling local model: {e.output}"
        except Exception as e:
            return f"Failed to call local model: {e}"