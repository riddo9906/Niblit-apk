# niblit_bridge.py - external AI bridge (disabled by default)
ENABLED = False
def call_external(prompt):
    if not ENABLED:
        return '[bridge disabled]'
    # Implement OpenAI or local LLM calls here
    return '[external response]'