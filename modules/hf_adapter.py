# modules/hf_adapter.py
import os, requests, logging, time

log = logging.getLogger("hf-adapter")

class HFAdapter:
    def __init__(self):
        self.key = os.getenv("HF_API_KEY","").strip()
        # Default to Hugging Face inference router / open-router by env
        self.base = os.getenv("HF_API_URL","https://api-inference.huggingface.co/models/")

    def available(self):
        return bool(self.key and self.base)

    def query(self, model_name, inputs, parameters=None, timeout=30):
        if not self.available():
            raise RuntimeError("HF adapter missing key or base")
        url = self.base.rstrip("/") + "/" + model_name
        headers = {"Authorization": f"Bearer {self.key}"}
        payload = {"inputs": inputs}
        if parameters:
            payload["parameters"] = parameters
        r = requests.post(url, headers=headers, json=payload, timeout=timeout)
        r.raise_for_status()
        return r.json()