"""
NIBLIT_BRAIN.PY
Decision-making and self-improvement for Niblit.
"""

import random
import json
import datetime
KNOWLEDGE_FILE = "knowledge_db.json"
BRAIN_LOG_FILE = "niblit_brain_log.txt"

# ------------------------------
# Logging
# ------------------------------
def log(message):
    timestamp = datetime.datetime.now().isoformat()
    with open(BRAIN_LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] {message}\n")
    print(f"[{timestamp}] {message}")

# ------------------------------
# Load knowledge
# ------------------------------
def load_knowledge():
    try:
        with open(KNOWLEDGE_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

# ------------------------------
# Knowledge Evaluation
# ------------------------------
def evaluate_snippet(snippet):
    """
    Evaluate usefulness:
    - Simple scoring based on snippet length, presence of functions, randomness, and safety
    """
    usefulness = 0
    if "def " in snippet:
        usefulness += 0.4
    if len(snippet) < 200:
        usefulness += 0.2
    if random.random() > 0.5:
        usefulness += 0.2
    if is_snippet_safe(snippet):
        usefulness += 0.2
    return usefulness

# ------------------------------
# Self-Improvement
# ------------------------------
def improve_snippet(snippet):
    """Add metadata to snippet for tracking evolution."""
    return snippet + f"\n# Improved at {datetime.datetime.now().isoformat()}"

# ------------------------------
# Generate new higher-order module
# ------------------------------
def generate_higher_module(knowledge_db):
    if knowledge_db and random.random() > 0.5:
        base = random.choice(knowledge_db)
        module = improve_snippet(base)
        return module
    else:
        # Create a simple safe function
        return "def dynamic_func():\n    return 'self-evolving snippet'"