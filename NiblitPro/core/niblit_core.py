"""
NIBLIT CORE SCRIPT
Author: Riyaad Behardien
Description: Core loop for Niblit - a self-evolving, ethically constrained AI system.
Requirements: Pydroid 3 Premium (for full package support)
"""

import os
import time
import random
import json
import datetime

# ------------------------------
# CONFIGURATION
# ------------------------------
KNOWLEDGE_FILE = "knowledge_db.json"   # Stores learned snippets/modules
LOG_FILE = "niblit_log.txt"            # Logs evolution and events
EVOLUTION_INTERVAL = 5                  # Seconds between evolution cycles

# ------------------------------
# UTILITIES
# ------------------------------
def log(message):
    timestamp = datetime.datetime.now().isoformat()
    with open(LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] {message}\n")
    print(f"[{timestamp}] {message}")

def load_knowledge():
    if os.path.exists(KNOWLEDGE_FILE):
        with open(KNOWLEDGE_FILE, "r") as f:
            return json.load(f)
    return []

def save_knowledge(db):
    with open(KNOWLEDGE_FILE, "w") as f:
        json.dump(db, f, indent=2)

# ------------------------------
# ETHICAL CHECKS
# ------------------------------
FORBIDDEN_KEYWORDS = ["import os", "import sys", "open(", "eval(", "exec(", "subprocess"]

def ethical_check(code_snippet):
    """Return True if the code snippet is safe."""
    return all(kw not in code_snippet for kw in FORBIDDEN_KEYWORDS)

# ------------------------------
# SANDBOX EXECUTION
# ------------------------------
def sandbox_execute(code_snippet):
    """Execute code in a restricted namespace."""
    try:
        local_env = {"random": random, "time": time}
        exec(code_snippet, {"__builtins__": {}}, local_env)
        return True, local_env
    except Exception as e:
        return False, str(e)

# ------------------------------
# CODE GENERATION
# ------------------------------
def generate_code(knowledge_db):
    """Create new ethical code snippets based on previous knowledge."""
    # Base templates for self-evolving behavior
    templates = [
        "def dynamic_func():\n    return random.randint(0, 100)",
        "def dynamic_func(x, y):\n    return x + y",
        "def dynamic_func():\n    return 'knowledge snippet generated'",
    ]
    
    # Choose random template or mutate existing knowledge
    if knowledge_db and random.random() > 0.5:
        snippet = random.choice(knowledge_db)
        snippet += f"\n# evolved at {datetime.datetime.now().isoformat()}"
    else:
        snippet = random.choice(templates)
    
    return snippet

# ------------------------------
# MAIN LOOP
# ------------------------------
def main():
    log("Niblit Core Booting...")
    knowledge_db = load_knowledge()
    
    while True:
        new_code = generate_code(knowledge_db)
        
        if ethical_check(new_code):
            success, result = sandbox_execute(new_code)
            if success:
                knowledge_db.append(new_code)
                save_knowledge(knowledge_db)
                log(f"New code integrated: {new_code.splitlines()[0]}")
            else:
                log(f"Code failed sandbox: {result}")
        else:
            log("Generated code blocked by ethical filter.")
        
        time.sleep(EVOLUTION_INTERVAL)

# ------------------------------
# BOOT NIBLIT
# ------------------------------
if __name__ == "__main__":
    main()