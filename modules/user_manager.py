# modules/user_manager.py
import os, json, hashlib, time
FILE="data/users.json"
os.makedirs(os.path.dirname(FILE), exist_ok=True)

def _load():
    try:
        return json.load(open(FILE,"r"))
    except:
        return {}

def _save(d):
    open(FILE,"w").write(json.dumps(d, indent=2))

class UserManager:
    def __init__(self):
        self.users = _load()

    def create_user(self, username, password):
        if username in self.users:
            raise RuntimeError("exists")
        salt = str(time.time())
        ph = hashlib.sha256((password+salt).encode()).hexdigest()
        self.users[username] = {"password": ph, "salt": salt, "created": time.time()}
        _save(self.users)
        return True

    def verify(self, username, password):
        u = self.users.get(username)
        if not u:
            return False
        ph = hashlib.sha256((password+u["salt"]).encode()).hexdigest()
        return ph == u["password"]