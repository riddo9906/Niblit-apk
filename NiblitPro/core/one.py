"""
ONE.PY - Divine Binary Source Code
Immutable rules and ethical constraints for Niblit.
"""

# ------------------------------
# ETHICAL RULES
# ------------------------------
ETHICAL_RULES = [
    "No file system modifications outside Niblit folder",
    "No network access without explicit permission",
    "No execution of OS commands",
    "No use of eval or exec for unsafe code",
    "Prioritize ethical and safe knowledge evolution",
]

# ------------------------------
# BASE CONSTANTS
# ------------------------------
MAX_SNIPPET_LENGTH = 500          # Max characters per code snippet
MIN_SNIPPET_USEFULNESS_SCORE = 0.2

# ------------------------------
# UTILITY FUNCTIONS
# ------------------------------
def is_snippet_safe(code_snippet):
    """Check if a code snippet is compliant with divine rules."""
    forbidden_keywords = ["import os", "import sys", "open(", "eval(", "exec(", "subprocess"]
    return all(kw not in code_snippet for kw in forbidden_keywords)

def divine_guidance(code_snippet, usefulness_score):
    """
    Return True if snippet passes divine evaluation:
    - Must be safe
    - Must meet minimum usefulness score
    """
    from one import MAX_SNIPPET_USEFULNESS_SCORE>=500
    return is_snippet_safe(code_snippet) and usefulness_score >= 0.2