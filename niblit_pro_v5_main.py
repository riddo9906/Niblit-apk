#!/usr/bin/env python3
# niblit_pro_v5_main.py
# Unified Niblit Pro V5 master script — integrated from all project components.
# Python 3.9+ recommended. Put secrets in .env file.

import os
import sys
import time
import json
import base64
import random
import logging
import threading
import traceback
from datetime import datetime
from typing import Optional, Dict, Any, List

# optional libs — used if available
try:
    import requests
except Exception:
    requests = None

try:
    import tkinter as tk
    from tkinter import ttk, messagebox, scrolledtext, Toplevel
except Exception:
    tk = None

try:
    from cryptography.fernet import Fernet
    CRYPTO_AVAILABLE = True
except Exception:
    Fernet = None
    CRYPTO_AVAILABLE = False

try:
    import psutil
except Exception:
    psutil = None

# load .env if python-dotenv installed
try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

# ---------- Logging ----------
os.makedirs("niblit_logs", exist_ok=True)
LOG_PATH = os.path.join("niblit_logs", "system_log.jsonl")
logging.basicConfig(filename=LOG_PATH, level=logging.INFO, format="%(message)s")
def _log(payload: dict):
    payload["ts"] = time.time()
    try:
        logging.info(json.dumps(payload, default=str))
    except Exception:
        logging.info(json.dumps({"kind":"log_failure","payload":str(payload),"ts":time.time()}))

# ---------- Utilities ----------
def now_iso():
    return datetime.utcnow().isoformat() + "Z"

def safe_load_env(key: str, default: str = "") -> str:
    return os.getenv(key, default).strip()

# ---------- Encryption Manager ----------
KEY_FILE = os.getenv("NIBLIT_KEY_FILE", "niblit_key.key")
class EncryptionManager:
    def __init__(self, key_file: str = KEY_FILE):
        self.key_file = key_file
        self._lock = threading.Lock()
        self._cipher = None
        self._init_key()

    def _init_key(self):
        with self._lock:
            if os.path.exists(self.key_file):
                try:
                    key = open(self.key_file,"rb").read()
                except Exception:
                    key = None
            else:
                key = None
            if not key and CRYPTO_AVAILABLE:
                key = Fernet.generate_key()
                try:
                    open(self.key_file,"wb").write(key)
                except Exception:
                    _log({"kind":"key_write_error","note":"could_not_write_keyfile"})
            if key and CRYPTO_AVAILABLE:
                try:
                    self._cipher = Fernet(key)
                    _log({"kind":"encryption_init","mode":"fernet"})
                except Exception:
                    self._cipher = None
                    _log({"kind":"encryption_init","mode":"fernet_failed"})
            else:
                self._cipher = None
                _log({"kind":"encryption_init","mode":"base64_fallback"})

    def encrypt(self, b: bytes) -> bytes:
        if self._cipher:
            return self._cipher.encrypt(b)
        return base64.b64encode(b)

    def decrypt(self, b: bytes) -> bytes:
        if self._cipher:
            return self._cipher.decrypt(b)
        return base64.b64decode(b)

    def rotate(self):
        with self._lock:
            if CRYPTO_AVAILABLE:
                new = Fernet.generate_key()
                open(self.key_file,"wb").write(new)
                self._cipher = Fernet(new)
                _log({"kind":"rotate_key","status":"ok"})
                return True
            _log({"kind":"rotate_key","status":"not_available"})
            return False

# ---------- API Manager ----------
class APIManager:
    def __init__(self):
        self.keys = {}
        self.load_keys()

    def load_keys(self):
        mapping = {
            "openai": "OPENAI_API_KEY",
            "weather": "WEATHER_API_KEY",
            "wolfram": "WOLFRAM_API_KEY",
            "maps": "MAPS_API_KEY",
            "news": "NEWS_API_KEY"
        }
        for k, env in mapping.items():
            v = safe_load_env(env, "")
            if v:
                # keep base64-obf if desired
                self.keys[k] = base64.b64encode(v.encode()).decode()
            else:
                self.keys[k] = ""

    def get(self, name: str) -> str:
        v = self.keys.get(name, "")
        if not v:
            return ""
        try:
            return base64.b64decode(v.encode()).decode()
        except Exception:
            return ""

# ---------- Training DB Manager ----------
MEMORY_DIR = "niblit_memory"
os.makedirs(MEMORY_DIR, exist_ok=True)

class TrainingDB:
    def __init__(self, path=os.path.join(MEMORY_DIR,"niblit_memory.json")):
        self.path = path
        self._lock = threading.Lock()
        self.data = {"entries": [], "meta": {"created": now_iso()}}
        self._load()

    def _load(self):
        if os.path.exists(self.path):
            try:
                self.data = json.load(open(self.path,"r", encoding="utf-8"))
            except Exception:
                self.data = {"entries": [], "meta": {"created": now_iso()}}
        self._save()

    def _save(self):
        with self._lock:
            try:
                open(self.path,"w", encoding="utf-8").write(json.dumps(self.data, indent=2))
            except Exception:
                _log({"kind":"memory_save_error","err":traceback.format_exc()})

    def add_entry(self, user_input: str, response: str, source: str = "interactive"):
        entry = {
            "input": user_input,
            "response": response,
            "source": source,
            "ts": time.time()
        }
        with self._lock:
            self.data["entries"].append(entry)
            # keep memory bounded
            if len(self.data["entries"]) > 5000:
                self.data["entries"] = self.data["entries"][-4000:]
            self._save()

    def find_matches(self, text: str, cutoff: float = 0.45):
        # simple substring & simple ratio fallback
        results = []
        tl = text.lower()
        for e in self.data["entries"]:
            if tl in e["input"].lower():
                results.append((1.0, e))
        return results

    def review(self, n=20):
        return self.data["entries"][-n:]

# ---------- Membrane (Server) ----------
class Membrane:
    def __init__(self, brain_ref=None):
        self.brain = brain_ref
        self.config = {
            "trusted_domains": [d.strip() for d in safe_load_env("MEMBRANE_TRUSTED_DOMAINS","").split(",") if d.strip()],
            "max_upload_mb": float(safe_load_env("MEMBRANE_MAX_UPLOAD_MB","5")),
            "auto_sync": safe_load_env("MEMBRANE_AUTO_SYNC","True") == "True",
            "cloud_endpoint": safe_load_env("MEMBRANE_CLOUD_ENDPOINT","")
        }
        self.security_level = 1.0
        self.quarantine_dir = "membrane_quarantine"
        os.makedirs(self.quarantine_dir, exist_ok=True)
        self.encryption = EncryptionManager()
        self._stop = threading.Event()
        if self.config.get("auto_sync"):
            t = threading.Thread(target=self._auto_sync_loop, daemon=True)
            t.start()
        t2 = threading.Thread(target=self._decay_loop, daemon=True)
        t2.start()
        _log({"kind":"membrane_init","trusted_domains":self.config["trusted_domains"]})

    def _domain_allowed(self, url: str) -> bool:
        try:
            from urllib.parse import urlparse
            p = urlparse(url)
            host = p.netloc or p.path
            for d in self.config["trusted_domains"]:
                if d and d in host:
                    return True
            return False
        except Exception:
            return False

    def verify_permission(self, source: str) -> bool:
        if source.startswith("http"):
            ok = self._domain_allowed(source)
            _log({"kind":"verify","source":source,"allowed":ok})
            return ok
        if os.path.exists(source):
            lower = source.lower()
            if any(k in lower for k in ("core","configs","niblit","secret","key")):
                _log({"kind":"verify","source":source,"allowed":False,"reason":"protected"})
                return False
            return True
        _log({"kind":"verify","source":source,"allowed":False,"reason":"not_found"})
        return False

    def assess(self, data: bytes) -> float:
        try:
            size_mb = len(data)/(1024*1024)
            cap = max(0.1, float(self.config.get("max_upload_mb",5)))
            score = max(0.0, 1.0 - (size_mb / cap))
            try:
                txt = data.decode("utf-8", errors="ignore").strip()
                if txt.startswith("{") or txt.startswith("["):
                    score = min(1.0, score + 0.15)
            except Exception:
                pass
            score = score * (1.0/(1.0 + max(0, self.security_level - 1.0)))
            return float(max(0.0, min(1.0, score)))
        except Exception:
            return 0.0

    def is_sensitive(self, data: bytes) -> bool:
        try:
            txt = data.decode("utf-8", errors="ignore").lower()
            for t in ["password","private_key","secret","api_key","token","ssh-rsa"]:
                if t in txt:
                    return True
            return False
        except Exception:
            return True

    def membrane_filter(self, data: bytes) -> bool:
        v = self.assess(data)
        s = self.is_sensitive(data)
        allowed = (v > 0.5) and (not s)
        _log({"kind":"membrane_decision","value":v,"sensitive":s,"allowed":allowed,"security":self.security_level})
        return allowed

    def _quarantine(self, path:str):
        try:
            dest = os.path.join(self.quarantine_dir, f"{int(time.time())}_{os.path.basename(path)}")
            with open(path,"rb") as src, open(dest,"wb") as dst:
                dst.write(src.read())
            _log({"kind":"quarantine_file","file":path,"dest":dest})
        except Exception as e:
            _log({"kind":"quarantine_error","error":str(e)})

    def upload_data(self, file_path: str, destination_url: str) -> Optional[Dict[str,Any]]:
        if not os.path.exists(file_path):
            _log({"kind":"upload_attempt","file":file_path,"status":"missing"})
            return None
        if not self.verify_permission(file_path):
            _log({"kind":"upload_denied","file":file_path})
            return None
        raw = open(file_path,"rb").read()
        if self.is_sensitive(raw):
            self._quarantine(file_path)
            return None
        if not self.membrane_filter(raw):
            self._quarantine(file_path)
            return None
        payload = self.encryption.encrypt(raw)
        headers = {"X-Membrane-Security":str(self.security_level)}
        if not requests:
            _log({"kind":"upload_error","error":"requests_not_installed"})
            return None
        try:
            r = requests.post(destination_url, data=payload, headers=headers, timeout=30)
            _log({"kind":"upload","file":file_path,"url":destination_url,"status":r.status_code})
            return {"ok":r.ok,"status":r.status_code}
        except Exception as e:
            _log({"kind":"upload_error","error":str(e)})
            self._increase_security("upload_error")
            return None

    def download_data(self, source_url: str, save_path: str) -> Optional[str]:
        if not self.verify_permission(source_url):
            _log({"kind":"download_blocked","url":source_url})
            self._increase_security("download_blocked")
            return None
        if not requests:
            _log({"kind":"download_error","error":"requests_not_installed"})
            return None
        try:
            r = requests.get(source_url, timeout=30)
            if r.status_code != 200:
                _log({"kind":"download_failed","url":source_url,"code":r.status_code})
                return None
            raw = r.content
            if self.is_sensitive(raw):
                self._quarantine(source_url)
                return None
            if not self.membrane_filter(raw):
                self._quarantine_bytes(raw, "download_rejected")
                return None
            try:
                content = self.encryption.decrypt(raw)
            except Exception:
                content = raw
            os.makedirs(os.path.dirname(save_path) or ".", exist_ok=True)
            with open(save_path,"wb") as f:
                f.write(content)
            _log({"kind":"download_success","url":source_url,"saved":save_path})
            return save_path
        except Exception as e:
            _log({"kind":"download_error","error":str(e)})
            return None

    def _quarantine_bytes(self, data: bytes, tag: str):
        try:
            p = os.path.join(self.quarantine_dir, f"{int(time.time())}_{tag}.bin")
            with open(p,"wb") as f:
                f.write(data)
            _log({"kind":"quarantine_bytes","path":p,"tag":tag})
        except Exception as e:
            _log({"kind":"quarantine_error","error":str(e)})

    def _increase_security(self, ev:str, delta:float=0.5):
        old = self.security_level
        self.security_level = min(20.0, self.security_level + delta)
        _log({"kind":"security_increase","event":ev,"old":old,"new":self.security_level})
        if self.brain and hasattr(self.brain,"on_security_event"):
            try:
                self.brain.on_security_event(ev,self.security_level)
            except Exception:
                pass

    def _decay_loop(self):
        while True:
            time.sleep(60)
            if self.security_level > 1.0:
                old = self.security_level
                self.security_level = max(1.0, self.security_level - 0.1)
                _log({"kind":"security_decay","old":old,"new":self.security_level})

    def _auto_sync_loop(self):
        while True:
            try:
                ep = self.config.get("cloud_endpoint","")
                if ep and os.path.exists(getattr(self.brain,"memory_file","")):
                    self.sync_brain_memory(ep)
                time.sleep(self.config.get("sync_interval",300))
            except Exception as e:
                _log({"kind":"auto_sync_error","error":str(e)})
                time.sleep(10)

    def sync_brain_memory(self, destination_url: Optional[str] = None) -> bool:
        mem_path = getattr(self.brain, "memory_file", None)
        if not mem_path or not os.path.exists(mem_path):
            _log({"kind":"sync","status":"no_memory_file"})
            return False
        raw = open(mem_path,"rb").read()
        if not self.membrane_filter(raw):
            _log({"kind":"sync","status":"filtered_out"})
            return False
        dest = destination_url or self.config.get("cloud_endpoint","")
        if dest:
            res = self.upload_data(mem_path, dest)
            return bool(res)
        _log({"kind":"sync","status":"skipped_no_dest"})
        return False

# ---------- Niblit Brain (higher-level) ----------
class NiblitBrain:
    def __init__(self):
        self.memory_file = os.path.join(MEMORY_DIR,"niblit_memory.json")
        self.training_db = TrainingDB(self.memory_file)
        self.api = APIManager()
        self.encryption = EncryptionManager()
        self.bridge = Bridge(self.api)  # Bridge defined below
        self._start_reflection_loop()
        _log({"kind":"brain_init"})

    def chat(self, message: str) -> str:
        ml = message.lower().strip()
        # quick built-in replies
        for k in ["hello","hi","how are you","what is your name","bye","thank you"]:
            if k in ml:
                return {
                    "hello":"Hey there!",
                    "hi":"Hi! I'm Niblit.",
                    "how are you":"I'm learning and improving.",
                    "what is your name":"I'm Niblit, your AI assistant.",
                    "bye":"Goodbye — be safe!",
                    "thank you":"You're welcome!"
                }[k]
        # training DB lookup
        matches = self.training_db.find_matches(message)
        if matches:
            return matches[0][1]["response"]
        # fallback to bridge if available
        if self.bridge and self.bridge.can_call():
            try:
                return self.bridge.send_to_gpt(message)
            except Exception:
                pass
        # heuristic response and store
        resp = random.choice([
            "Interesting — tell me more.",
            "I will remember that.",
            "Could you clarify?",
            "That's a good point!"
        ])
        self.training_db.add_entry(message, resp, source="auto_reply")
        return resp

    def train(self, prompt: str, reply: str) -> str:
        self.training_db.add_entry(prompt, reply, source="manual")
        return f"Learned new reply for '{prompt}'."

    def review_memory(self, n=20):
        return self.training_db.review(n)

    def on_security_event(self, event_key: str, new_level: float):
        self.training_db.add_entry("[internal_security_event]", f"{event_key} level {new_level}", source="system")

    def _start_reflection_loop(self):
        def loop():
            while True:
                try:
                    # summarize last conversations and add as training example
                    last = self.training_db.review(10)
                    if len(last) >= 3:
                        summary = " | ".join([f"{e['input']} -> {e['response']}" for e in last[-5:]])
                        self.training_db.add_entry(f"reflection_{int(time.time())}", summary, source="reflection")
                        _log({"kind":"self_reflect","summary":summary})
                    time.sleep(600)
                except Exception:
                    time.sleep(60)
        t = threading.Thread(target=loop, daemon=True)
        t.start()

# ---------- Bridge (GPT / external) ----------
class Bridge:
    def __init__(self, api_manager: APIManager):
        self.api_manager = api_manager
        self.session_memory: List[Dict[str,str]] = []

    def can_call(self) -> bool:
        return bool(self.api_manager.get("openai")) and requests is not None

    def send_to_gpt(self, prompt: str) -> str:
        key = self.api_manager.get("openai")
        if not key or not requests:
            return "Bridge unavailable (no API key or requests)."
        try:
            url = "https://api.openai.com/v1/chat/completions"
            headers = {"Authorization": f"Bearer {key}", "Content-Type":"application/json"}
            payload = {"model":"gpt-4o-mini","messages":[{"role":"system","content":"You are Niblit AI."},{"role":"user","content":prompt}], "max_tokens": 512}
            r = requests.post(url, headers=headers, json=payload, timeout=20)
            jr = r.json()
            text = jr.get("choices",[{}])[0].get("message",{}).get("content","[no reply]")
            self.session_memory.append({"user":prompt,"assistant":text})
            return text
        except Exception as e:
            _log({"kind":"bridge_error","error":str(e)})
            return f"Bridge error: {e}"

    def summarize_memory(self):
        if not self.session_memory:
            return "No memory yet."
        return "\n".join([f"You: {m['user']}\nNiblit: {m['assistant']}" for m in self.session_memory[-5:]])

# ---------- Self-Healer ----------
class SelfHealer:
    def __init__(self, membrane: Membrane, brain: NiblitBrain):
        self.membrane = membrane
        self.brain = brain
        _log({"kind":"self_healer_init"})

    def check_and_heal(self):
        # check key modules & pip packages (best-effort)
        essentials = ["requests", "python-dotenv"]
        results = {}
        for m in essentials:
            try:
                __import__(m)
                results[m] = True
            except Exception:
                results[m] = False
                # try to pip install (best-effort)
                try:
                    import subprocess, sys
                    subprocess.check_call([sys.executable, "-m", "pip", "install", m])
                    results[m] = True
                except Exception as e:
                    results[m] = False
                    _log({"kind":"self_heal_install_failed","module":m,"error":str(e)})
        # check memory integrity
        try:
            self.brain.training_db._save()
        except Exception as e:
            _log({"kind":"self_heal_memory_save_failed","error":str(e)})
        _log({"kind":"self_heal_report","results":results})
        return results

    def safe_exec(self, cmd: str) -> str:
        ALLOWED = ["ls","pwd","whoami","id","cat"]
        if not any(cmd.strip().startswith(a) for a in ALLOWED):
            return "Command not allowed."
        try:
            import subprocess
            out = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, timeout=10)
            return out.decode(errors="ignore")
        except Exception as e:
            return f"Execution error: {e}"

# ---------- Draegtile Network ----------
class DraegtileNetwork:
    def __init__(self):
        self.db_path = "draegtile_network.json"
        self.modules = ["Education","Agriculture","Finance","Mobility","Infrastructure","Environment","Networking","I.T. & Security","Human Development"]
        self.data = {}
        self.sync_interval = 3600
        self._load()
        threading.Thread(target=self._auto_sync_loop, daemon=True).start()
        _log({"kind":"draegtile_init"})

    def _load(self):
        if os.path.exists(self.db_path):
            try:
                self.data = json.load(open(self.db_path,"r"))
            except Exception:
                self.data = {}
        for m in self.modules:
            self.data.setdefault(m, {"status":"active","resources":[],"last_update":None})
        self._save()

    def _save(self):
        try:
            open(self.db_path,"w").write(json.dumps(self.data, indent=2))
        except Exception:
            _log({"kind":"draegtile_save_error","err":traceback.format_exc()})

    def sync_module(self, module_name):
        try:
            if module_name == "Education" and requests:
                r = requests.get("https://api.publicapis.org/entries", timeout=10)
                if r.status_code == 200:
                    entries = r.json().get("entries", [])[:10]
                    self.data[module_name]["resources"] = [{"API":e.get("API"),"Desc":e.get("Description"),"Link":e.get("Link")} for e in entries]
            else:
                self.data[module_name]["resources"] = [{"info":"placeholder"}]
            self.data[module_name]["last_update"] = now_iso()
            self._save()
        except Exception as e:
            _log({"kind":"draegtile_sync_error","module":module_name,"error":str(e)})

    def sync_all(self):
        for m in self.modules:
            self.sync_module(m)

    def _auto_sync_loop(self):
        while True:
            try:
                self.sync_all()
                time.sleep(self.sync_interval)
            except Exception as e:
                _log({"kind":"draegtile_auto_sync_error","error":str(e)})
                time.sleep(10)

# ---------- System Manager & Diagnostics ----------
class SystemManager:
    def __init__(self):
        _log({"kind":"system_manager_init"})
    def diagnose(self):
        if not psutil:
            return {"error":"psutil_missing"}
        try:
            return {
                "cpu_percent": psutil.cpu_percent(interval=0.5),
                "memory_percent": psutil.virtual_memory().percent,
                "disk_percent": psutil.disk_usage("/").percent,
                "boot_time": psutil.boot_time()
            }
        except Exception as e:
            _log({"kind":"diagnose_error","error":str(e)})
            return {}

    def repair(self):
        # placeholder for repair steps: clear caches, compact memory, restart services
        _log({"kind":"system_repair","note":"performed_basic_checks"})
        return True

# ---------- CLI (fallback) ----------
def cli_loop(core):
    print("Niblit Pro V5 — CLI mode. Type /help")
    while True:
        try:
            cmd = input("> ").strip()
        except (KeyboardInterrupt, EOFError):
            print("Exiting.")
            break
        if not cmd:
            continue
        if cmd == "/help":
            print("/help /weather CITY /train prompt|reply /review /selfcheck /exit")
            continue
        if cmd.startswith("/weather"):
            parts = cmd.split(" ",1)
            city = parts[1] if len(parts)>1 else os.getenv("CITY","Cape Town")
            print(core.brain.chat(f"weather {city}"))
            continue
        if cmd.startswith("/train ") or cmd.startswith("/learn "):
            parts = cmd.split(" ",1)[1]
            if "|" not in parts:
                print("Usage: /train prompt|reply")
                continue
            p,r = parts.split("|",1)
            print(core.brain.train(p.strip(),r.strip()))
            continue
        if cmd == "/review":
            for e in core.brain.review_memory(10):
                print(e)
            continue
        if cmd == "/selfcheck":
            print("Running self-heal...")
            print(core.self_healer.check_and_heal())
            continue
        if cmd == "/exit":
            print("Bye.")
            break
        print("Niblit:", core.brain.chat(cmd))

# ---------- Dashboard (Tkinter) ----------
class DraegtileDashboardMobile:
    def __init__(self, root, core):
        self.root = root
        self.core = core
        self.root.title("Niblit Pro V5 Dashboard")
        self.root.geometry("480x800")
        self.root.configure(bg="#121212")
        self._build()
        threading.Thread(target=self._weather_loop, daemon=True).start()

    def _build(self):
        top = tk.Frame(self.root, bg="#1f1f1f")
        top.pack(fill="x")
        tk.Label(top, text="Niblit Pro V5", bg="#1f1f1f", fg="white", font=("Arial",14,"bold")).pack(pady=8)
        self.status_label = tk.Label(self.root, text="System Active", bg="#121212", fg="#4caf50", font=("Arial",12))
        self.status_label.pack(pady=6)
        # notebook
        nb = ttk.Notebook(self.root)
        nb.pack(fill="both", expand=True, padx=10, pady=10)
        # chat tab
        chat_tab = tk.Frame(nb, bg="#121212")
        train_tab = tk.Frame(nb, bg="#121212")
        mem_tab = tk.Frame(nb, bg="#121212")
        nb.add(chat_tab, text="Chat")
        nb.add(train_tab, text="Train")
        nb.add(mem_tab, text="Memory")
        # chat UI
        self.chat_display = scrolledtext.ScrolledText(chat_tab, height=20, bg="#1e1e1e", fg="white")
        self.chat_display.pack(fill="both", expand=True, padx=8, pady=8)
        self.chat_display.insert(tk.END, "Niblit: Hello — ask me anything.\n")
        self.chat_display.config(state=tk.DISABLED)
        self.chat_entry = tk.Entry(chat_tab, bg="#2b2b2b", fg="white")
        self.chat_entry.pack(fill="x", padx=8, pady=5)
        self.chat_entry.bind("<Return>", lambda e: self._send())
        tk.Button(chat_tab, text="Send", bg="#4caf50", fg="white", command=self._send).pack(pady=6)
        # training UI
        tk.Label(train_tab, text="Prompt").pack()
        self.train_prompt = tk.Entry(train_tab)
        self.train_prompt.pack(fill="x", padx=8, pady=4)
        tk.Label(train_tab, text="Response").pack()
        self.train_resp = tk.Entry(train_tab)
        self.train_resp.pack(fill="x", padx=8, pady=4)
        tk.Button(train_tab, text="Save Training", bg="#4caf50", fg="white", command=self._save_training).pack(pady=8)
        # memory viewer
        self.mem_view = scrolledtext.ScrolledText(mem_tab, height=20, bg="#111111", fg="white")
        self.mem_view.pack(fill="both", expand=True, padx=8, pady=8)
        tk.Button(mem_tab, text="Refresh Memory", command=self._refresh_memory).pack(pady=4)

    def _send(self):
        text = self.chat_entry.get().strip()
        if not text:
            return
        self.chat_entry.delete(0, "end")
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, f"You: {text}\n")
        self.chat_display.config(state=tk.DISABLED)
        def worker():
            try:
                reply = self.core.brain.chat(text)
            except Exception as e:
                reply = f"Error: {e}"
            self.chat_display.config(state=tk.NORMAL)
            self.chat_display.insert(tk.END, f"Niblit: {reply}\n\n")
            self.chat_display.see(tk.END)
            self.chat_display.config(state=tk.DISABLED)
        threading.Thread(target=worker, daemon=True).start()

    def _save_training(self):
        p = self.train_prompt.get().strip()
        r = self.train_resp.get().strip()
        if not p or not r:
            messagebox.showwarning("Empty", "Fill both fields.")
            return
        res = self.core.brain.train(p,r)
        messagebox.showinfo("Saved", res)
        self.train_prompt.delete(0,"end")
        self.train_resp.delete(0,"end")

    def _refresh_memory(self):
        entries = self.core.brain.review_memory(50)
        self.mem_view.config(state=tk.NORMAL)
        self.mem_view.delete("1.0","end")
        for e in entries:
            self.mem_view.insert(tk.END, json.dumps(e, indent=2) + "\n\n")
        self.mem_view.config(state=tk.DISABLED)

    def _weather_loop(self):
        while True:
            try:
                if hasattr(self.core.brain, "get_weather_status"):
                    w = self.core.brain.get_weather_status()
                else:
                    w = "Weather unavailable"
                self.status_label.config(text=w)
            except Exception:
                pass
            time.sleep(20)

# ---------- Visualizer ----------
class Visualizer:
    def __init__(self, db: TrainingDB):
        self.db = db
    def show_memory_window(self):
        if not tk:
            return "Tk missing"
        win = Toplevel()
        win.title("Memory Visualizer")
        st = scrolledtext.ScrolledText(win, width=90, height=40)
        st.pack(padx=8,pady=8)
        for item in self.db.review(200):
            st.insert(tk.END, f"{datetime.fromtimestamp(item['ts']).isoformat()} - {item['input']} -> {item['response']}\n")
        st.configure(state="disabled")

# ---------- Constructor / Trainer / Terminal utilities ----------
class Constructor:
    def add_module(self, name: str):
        try:
            __import__(name)
            return f"Module {name} loaded."
        except Exception as e:
            return f"Module load failed: {e}"
    def reload(self, name: str):
        try:
            mod = __import__(name)
            import importlib
            importlib.reload(mod)
            return f"Reloaded {name}"
        except Exception as e:
            return f"Reload failed: {e}"
    def write_file(self, path:str, content:str):
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        open(path,"w", encoding="utf-8").write(content)
        return f"Wrote {path}"

class Trainer:
    def train(self, brain: NiblitBrain, user_input:str, user_response:str):
        return brain.train(user_input, user_response)

class Terminal:
    def execute(self, cmd:str):
        ALLOWED = ["ls","pwd","whoami","id","cat"]
        if not any(cmd.strip().startswith(a) for a in ALLOWED):
            return "Not allowed"
        import subprocess
        try:
            return subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, timeout=10).decode(errors="ignore")
        except Exception as e:
            return f"Error: {e}"

# ---------- SLSA Generator ----------
def generate_basic_slsa(project_name: str, artifacts: List[str], builder: str = "niblit-builder/1.0"):
    import hashlib
    items = []
    for a in artifacts:
        h = None
        if os.path.exists(a):
            with open(a,"rb") as f:
                hobj = hashlib.sha256()
                while True:
                    b = f.read(8192)
                    if not b: break
                    hobj.update(b)
                h = hobj.hexdigest()
        items.append({"path":a,"sha256":h})
    prov = {
        "predicateType":"https://slsa.dev/provenance/v0.2",
        "builder":{"id":builder},
        "buildType":"niblit_local",
        "metadata":{"invocationTime":time.time(),"project":project_name},
        "materials":items
    }
    out = f"slsa_{project_name}_{int(time.time())}.json"
    open(out,"w").write(json.dumps(prov, indent=2))
    return out

# ---------- Master Core / Orchestrator ----------
class NiblitMaster:
    def __init__(self, gui_prefer=True):
        self.api = APIManager()
        self.brain = NiblitBrain()
        self.membrane = Membrane(brain_ref=self.brain)
        self.self_healer = SelfHealer(self.membrane, self.brain)
        self.draeg = DraegtileNetwork()
        self.sysmgr = SystemManager()
        self.visualizer = Visualizer(self.brain.training_db)
        self.constructor = Constructor()
        self.trainer = Trainer()
        self.terminal = Terminal()
        self.bridge = self.brain.bridge
        # background loops
        threading.Thread(target=self._self_train_loop, daemon=True).start()
        threading.Thread(target=self._alerter_loop, daemon=True).start()
        self.gui_prefer = gui_prefer
        _log({"kind":"master_init","gui_prefer":self.gui_prefer})

    def _self_train_loop(self):
        while True:
            try:
                # pick random small improvements: add trivial training to keep memory fresh
                self.brain.train("how are you", "I'm improving thanks to continuous learning.")
                _log({"kind":"self_train_cycle","result":"ok"})
                time.sleep(1800)
            except Exception:
                time.sleep(60)

    def _alerter_loop(self):
        while True:
            try:
                if psutil:
                    cpu = psutil.cpu_percent(interval=0.5)
                    if cpu > 95:
                        _log({"kind":"alerter","issue":"high_cpu","value":cpu})
                time.sleep(60)
            except Exception:
                time.sleep(60)

    def launch(self):
        # Try GUI first if available and desired
        if self.gui_prefer and tk:
            try:
                root = tk.Tk()
                # lightweight login
                from functools import partial
                def show_dashboard():
                    root.destroy()
                    mainwin = tk.Tk()
                    DraegtileDashboardMobile(mainwin, self)
                    mainwin.mainloop()
                login = tk.Tk()
                login.title("Niblit Login")
                login.geometry("360x500")
                login.configure(bg="#121212")
                tk.Label(login, text="Username:", fg="white", bg="#121212").pack(pady=5)
                u = tk.Entry(login)
                u.pack(pady=5)
                tk.Label(login, text="Password:", fg="white", bg="#121212").pack(pady=5)
                p = tk.Entry(login, show="*")
                p.pack(pady=5)
                def attempt():
                    if u.get()=="admin" and p.get()=="1234":
                        login.destroy()
                        show_dashboard()
                    else:
                        messagebox.showerror("Login", "Invalid")
                tk.Button(login, text="Login", bg="#4caf50", fg="white", command=attempt).pack(pady=20)
                login.mainloop()
                return
            except Exception as e:
                _log({"kind":"gui_launch_failed","error":str(e)})
                # fallthrough to CLI
        # otherwise fallback CLI
        cli_loop(self)

# ---------- Run ----------
def main():
    gm = NiblitMaster(gui_prefer=True)
    gm.launch()

if __name__ == "__main__":
    main()