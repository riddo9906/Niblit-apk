"""Helper functions for scanning repository structure."""

import os


def scan_tree(root):
    """Return all files under root."""
    out = []
    for path, _, files in os.walk(root):
        for f in files:
            out.append(os.path.join(path, f))
    return out


def get_all_py_files(root):
    """
    Returns all .py files under root.
    Used by repo_audit and orchestrator.
    """
    py_files = []
    for path, _, files in os.walk(root):
        for f in files:
            if f.endswith(".py"):
                py_files.append(os.path.join(path, f))
    return py_files


def find_missing_init(root):
    """
    Finds directories containing .py files that are missing __init__.py.
    Only checks directories that contain at least one Python file.
    """
    missing = []
    for path, _, files in os.walk(root):
        py_files = [f for f in files if f.endswith(".py")]
        if py_files and "__init__.py" not in files:
            missing.append(path)
    return missing


if __name__ == "__main__":
    print('Running structural_helper.py')
