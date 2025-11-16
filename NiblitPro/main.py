"""
MAIN.PY - Boots Niblit with Core + Brain + Divine Source
"""

import time
import json
import datetime
from niblit_core import generate_code, sandbox_execute
from niblit_brain import evaluate_snippet, generate_higher_module, log, load_knowledge
from one import ETHICAL_RULES, is_snippet_safe

KNOWLEDGE_FILE = "knowledge_db.json"
EVOLUTION_INTERVAL = 5  # seconds

def save_knowledge(db):
    with open(KNOWLEDGE_FILE, "w") as f:
        json.dump(db, f, indent=2)

# ------------------------------
# Main Loop
# ------------------------------
def main():
    log("Niblit Main Booting...")
    knowledge_db = load_knowledge()
    
    while True:
        # 1. Generate new snippet from core
        new_code = generate_code(knowledge_db)
        
        # 2. Evaluate snippet using Brain
        usefulness = evaluate_snippet(new_code)
        
        if is_snippet_safe(new_code) and usefulness >= 0.2:
            success, result = sandbox_execute(new_code)
            if success:
                knowledge_db.append(new_code)
                save_knowledge(knowledge_db)
                log(f"[EVOLVED] Snippet integrated: {new_code.splitlines()[0]}")
            else:
                log(f"[FAILED] Snippet failed sandbox: {result}")
        else:
            log(f"[BLOCKED] Snippet failed evaluation or ethical check")
        
        # 3. Generate higher-order module
        module = generate_higher_module(knowledge_db)
        success, _ = sandbox_execute(module)
        if success:
            knowledge_db.append(module)
            save_knowledge(knowledge_db)
            log(f"[HIGHER] Higher-order module added")
        
        time.sleep(EVOLUTION_INTERVAL)

# ------------------------------
# Boot Niblit
# ------------------------------
if __name__ == "__main__":
    main()