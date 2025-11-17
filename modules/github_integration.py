# modules/github_integration.py
import os, requests, logging
log = logging.getLogger("github-int")
TOKEN = os.getenv("GITHUB_TOKEN","").strip()
API = "https://api.github.com"

def create_issue(repo, title, body):
    if not TOKEN:
        raise RuntimeError("No GITHUB_TOKEN")
    url = f"{API}/repos/{repo}/issues"
    r = requests.post(url, json={"title":title,"body":body}, headers={"Authorization":f"token {TOKEN}"})
    r.raise_for_status()
    return r.json()