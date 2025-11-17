# modules/niblit_bridge.py
import logging, time
from importlib import import_module

log = logging.getLogger("niblit-bridge")

# Attempt to import adapters lazily
try:
    from modules import openai_adapter as _openai_mod
except Exception:
    _openai_mod = None
try:
    from modules import hf_adapter as _hf_mod
except Exception:
    _hf_mod = None

class Bridge:
    def __init__(self):
        self.openai = _openai_mod.OpenAIAdapter() if _openai_mod else None
        self.hf = _hf_mod.HFAdapter() if _hf_mod else None

    def can_call(self):
        return (self.openai and self.openai.available()) or (self.hf and self.hf.available())

    def send_to_llm(self, text, prefer="openai"):
        """Return string reply or raise."""
        # Build a basic chat-like payload
        if prefer == "openai" and self.openai and self.openai.available():
            messages = [{"role":"system","content":"You are Niblit — concise assistant."},
                        {"role":"user","content": text}]
            return self.openai.query(messages)
        # fallback HF (assume model name in HF_MODEL env)
        if self.hf and self.hf.available():
            model = os.getenv("HF_MODEL","gpt2")
            out = self.hf.query(model, text)
            # hf model outputs vary; try to extract cleanly
            if isinstance(out, dict) and "generated_text" in out:
                return out["generated_text"]
            if isinstance(out, list) and out:
                return str(out[0])
            return str(out)
        raise RuntimeError("No LLM adapter available")