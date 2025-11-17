# niblit_bridge.py

import logging

log = logging.getLogger("NiblitBridge")

def call_external(prompt):
    log.debug(f"[External LLM] Called with prompt: {prompt}")
    return f"External response to: {prompt}"