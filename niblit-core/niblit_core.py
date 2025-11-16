# niblit_core.py
from prompts import SYSTEM_PROMPT, DEFAULT_BEHAVIOR
from memory import MemoryStore
from model_adapters import EchoAdapter, OpenAIAdapter, LlamaCppAdapter
import time
import json

class NiblitCore:
    def __init__(self, adapter=None, session_id="default"):
        self.mem = MemoryStore()
        self.session = session_id
        self.adapter = adapter or EchoAdapter()
        self.system_prompt = SYSTEM_PROMPT
        self.behavior = DEFAULT_BEHAVIOR.copy()
        self.short_window = []  # short-term messages (tuples role, text)

    def _build_prompt(self, user_message: str):
        # Retrieve top facts (simple) and recent history
        facts = self.mem.get_facts(limit=10)
        facts_text = "\n".join([f"{k}: {v}" for (k,v,_,_) in facts]) if facts else ""
        history = self.mem.get_recent_history(self.session, limit=8)
        history_text = "\n".join([f"{r.upper()}: {c}" for (r,c,_) in history])
        behavior_json = json.dumps(self.behavior)
        prompt = "\n".join([
            self.system_prompt,
            f"BEHAVIOR: {behavior_json}",
            "RETRIEVED_FACTS:",
            facts_text,
            "RECENT_HISTORY:",
            history_text,
            "USER:",
            user_message,
            "",
            "REPLY:"
        ])
        return prompt

    def ingest_user_message(self, text: str):
        self.mem.add_message(self.session, "user", text)
        self.short_window.append(("user", text))
        # auto-detect memory commands
        if text.startswith("!remember "):
            payload = text[len("!remember "):].strip()
            if ":" in payload:
                key, val = payload.split(":",1)
                self.mem.add_fact(key.strip(), val.strip())
                return "Saved."
            else:
                return "Use `!remember key: value` to save facts."
        if text.startswith("!forget "):
            key = text[len("!forget "):].strip()
            self.mem.forget_fact(key)
            return f"Forgot {key}."

        # normal flow
        prompt = self._build_prompt(text)
        resp = self.adapter.generate(prompt, max_tokens=512)
        self.mem.add_message(self.session, "assistant", resp)
        # simple adaptive behavior: if user says "be more concise" update behavior
        if "be more concise" in text.lower():
            self.behavior["verbosity"] = "low"
        if "be more detailed" in text.lower():
            self.behavior["verbosity"] = "high"
        return resp

    def review_memory(self):
        facts = self.mem.get_facts(limit=50)
        return facts