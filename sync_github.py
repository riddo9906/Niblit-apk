import git
import os
import sys

# --- CONFIGURATION ---
# Path to your Niblit project folder
PROJECT_PATH = "/storage/emulated/0/Download/NiblitProV5"
# Commit message template
COMMIT_MESSAGE = "Auto-commit from Pydroid"

# --- FUNCTION ---
def sync_repo(path, commit_message):
    try:
        # Open repo
        repo = git.Repo(path)
    except git.exc.InvalidGitRepositoryError:
        print(f"[ERROR] No Git repository found at {path}")
        sys.exit(1)

    try:
        # Stage all changes
        repo.git.add(A=True)

        # Commit
        if repo.is_dirty():
            repo.index.commit(commit_message)
            print("[INFO] Changes committed.")
        else:
            print("[INFO] No changes to commit.")

        # Push to origin
        origin = repo.remote(name='origin')
        origin.push()
        print("[INFO] Changes pushed to GitHub.")
    except Exception as e:
        print(f"[ERROR] {e}")

# --- RUN ---
if __name__ == "__main__":
    sync_repo(PROJECT_PATH, COMMIT_MESSAGE)