# modules/llm_module.py
import os, json, requests, time

class HFClient:
    """Light wrapper for HuggingFace router chat completions (if you use it)."""
    def __init__(self, api_key=None, base_url=None, model=None):
        self.api_key = api_key or os.environ.get("HF_TOKEN")
        self.base = base_url or "https://router.huggingface.co/v1"
        self.model = model or os.environ.get("HF_MODEL", "moonshotai/Kimi-K2-instruct-0905")

    def is_available(self):
        return bool(self.api_key)

    def query_chat(self, messages, max_tokens=300):
        if not self.is_available():
            raise RuntimeError("No HF token")
        headers = {"Authorization": f"Bearer {self.api_key}"}
        payload = {"model": self.model, "messages": messages, "max_tokens": max_tokens}
        r = requests.post(f"{self.base}/chat/completions", headers=headers, json=payload, timeout=15)
        r.raise_for_status()
        js = r.json()
        choice = js.get("choices", [{}])[0]
        msg = choice.get("message") or choice.get("text") or ""
        if isinstance(msg, dict):
            return msg.get("content") or ""
        return str(msg)

class OpenAIClient:
    """Compatibility wrapper around OpenAI-style chat completions via openai.com API."""
    def __init__(self, api_key=None, base_url=None, model=None):
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        self.base = base_url or "https://api.openai.com/v1"
        self.model = model or os.environ.get("OPENAI_MODEL", "gpt-4o-mini")

    def is_available(self):
        return bool(self.api_key)

    def query_chat(self, messages, max_tokens=300):
        if not self.is_available():
            raise RuntimeError("No OpenAI key configured")
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        body = {"model": self.model, "messages": messages, "max_tokens": max_tokens}
        r = requests.post(f"{self.base}/chat/completions", headers=headers, json=body, timeout=15)
        r.raise_for_status()
        js = r.json()
        choice = js.get("choices", [{}])[0]
        msg = choice.get("message", {})
        return msg.get("content", "") if isinstance(msg, dict) else str(msg)