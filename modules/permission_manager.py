# modules/permission_manager.py
import json, os, time
FILE="data/permissions.json"
os.makedirs(os.path.dirname(FILE), exist_ok=True)

class PermissionManager:
    def __init__(self):
        try:
            with open(FILE,"r") as f:
                self._perms = json.load(f)
        except Exception:
            self._perms = {}
    def ask(self, key, reason=""):
        # Quick policy: check truthy mapping; default False
        val = self._perms.get(key)
        if val is None:
            # create prompt-ish entry (manual policy)
            self._perms[key] = False
            self._save()
            return False
        return bool(val)
    def grant(self, key):
        self._perms[key] = True
        self._save()
    def revoke(self, key):
        self._perms[key] = False
        self._save()
    def _save(self):
        with open(FILE,"w") as f:
            json.dump(self._perms,f,indent=2)