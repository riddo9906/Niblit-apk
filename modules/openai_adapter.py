# modules/openai_adapter.py
import os, json, time, logging, requests

log = logging.getLogger("openai-adapter")

def _get_key():
    return os.getenv("OPENAI_API_KEY","").strip()

class OpenAIAdapter:
    def __init__(self):
        self.key = _get_key()
        self.endpoint = os.getenv("OPENAI_API_URL","https://api.openai.com/v1/chat/completions")

    def available(self):
        return bool(self.key and 'api.openai' in self.endpoint or 'openai' in self.endpoint)

    def query(self, messages, model="gpt-4o-mini", max_tokens=512, timeout=15):
        if not self.available():
            raise RuntimeError("OpenAIAdapter: missing api key or endpoint")
        headers = {"Authorization": f"Bearer {self.key}", "Content-Type":"application/json"}
        payload = {"model": model, "messages": messages, "max_tokens": max_tokens}
        r = requests.post(self.endpoint, headers=headers, json=payload, timeout=timeout)
        r.raise_for_status()
        jr = r.json()
        # Basic defensive extraction
        choice = jr.get("choices",[{}])[0]
        if isinstance(choice, dict):
            msg = choice.get("message",{}) or {}
            return msg.get("content", choice.get("text",""))
        return str(jr)