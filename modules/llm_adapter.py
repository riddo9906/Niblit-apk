# modules/llm_adapter.py
import os, time
from .llm_module import OpenAIClient, HFClient

class LLMAdapter:
    def __init__(self, db=None):
        # priority: OpenAI -> HF
        self.db = db
        self.openai = OpenAIClient()
        self.hf = HFClient()
        self._last_check = 0
        self._last_result = False

    def is_available(self):
        # cache for 5s
        now = time.time()
        if now - self._last_check < 5:
            return self._last_result
        ok = self.openai.is_available() or self.hf.is_available()
        self._last_check = now
        self._last_result = ok
        return ok

    def query(self, prompt, context=None, max_tokens=300):
        # build messages
        messages = [{"role":"system","content":"You are Niblit, a helpful assistant."}]
        if context:
            # context is list of interactions
            for it in context[-10:]:
                role = it.get('role', 'user')
                messages.append({"role": role, "content": it.get('text','')})
        messages.append({"role":"user","content": prompt})

        # prefer OpenAI if available
        if self.openai.is_available():
            try:
                return self.openai.query_chat(messages, max_tokens=max_tokens)
            except Exception as e:
                # fallback to HF
                pass
        if self.hf.is_available():
            try:
                return self.hf.query_chat(messages, max_tokens=max_tokens)
            except Exception as e:
                pass
        # fallback heuristic
        if self.db:
            facts = self.db.list_facts(10)
            if facts:
                return f"I recall: {facts[0]['value']}"
        return f"(No LLM configured) Echo: {prompt[:200]}"