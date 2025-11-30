# self_researcher.py
import subprocess
import requests

class SelfResearcher:
    def __init__(self, db, modules=None):
        self.db = db
        self.modules = modules if modules else {}

        # Map internal Niblit commands → callable functions
        self.command_map = {
            "ideas": "ideas about",
            "reflect": "reflect",
            "analyze": "analyze",
            "memory": "!memory",
            "heal": "self-heal",
            "teach": "self-teach",
            "maintain": "self-maintenance",
            "impl": "self-idea-impl",
            "device": "device-info",
            "read": "read-file",
            "write": "write-file",
        }

    # ----------------------------------------
    # --- Main Entry ---
    # ----------------------------------------
    def handle_command(self, cmd, arg=None):
        cmd = cmd.lower().strip()

        # 1) Internal Commands
        if cmd in self.command_map:
            mapped = self.command_map[cmd]
            return f"[INTERNAL RESEARCH] → {mapped} {arg if arg else ''}".strip()

        # 2) Module-based Research
        if cmd == "module" and arg:
            return self.call_module(arg)

        # 3) Terminal Research
        if cmd == "terminal" and arg:
            return self.run_terminal(arg)

        # 4) Web Research
        if cmd in ("web", "web.run") or (arg is None and cmd):
            query = arg if arg else cmd
            return self.web_research(query)

        return "[RESEARCH ERROR] Unknown command or missing argument"

    # ----------------------------------------
    # --- Web Research (DuckDuckGo JSON API) ---
    # ----------------------------------------
    def web_research(self, query):
        try:
            url = "https://api.duckduckgo.com/"
            params = {"q": query, "format": "json", "no_html": 1, "skip_disambig": 1}
            resp = requests.get(url, params=params, timeout=8).json()

            results = []

            # Primary abstract
            if resp.get("AbstractText"):
                results.append(resp["AbstractText"])

            # Related topics (up to 3)
            if resp.get("RelatedTopics"):
                for item in resp["RelatedTopics"][:3]:
                    text = item.get("Text")
                    if text:
                        results.append(text)

            if results:
                return "[WEB RESEARCH RESULTS]\n" + "\n\n".join(results)
            return "[NO RESULTS FOUND]"

        except Exception as e:
            return f"[WEB RESEARCH ERROR] {e}"

    # ----------------------------------------
    # --- Module Calls ---
    # ----------------------------------------
    def call_module(self, text):
        """
        format examples:
            self-research module bios status
            self-research module fs_manager list /
        """
        if not text:
            return "[MODULE ERROR] Missing module command"

        parts = text.split(" ")
        module_name = parts[0].strip()
        action = " ".join(parts[1:]).strip()

        # Access module via runtime registry in db
        registry = self.db.runtime_registry if hasattr(self.db, "runtime_registry") else {}
        if module_name not in registry:
            return f"[MODULE ERROR] Module '{module_name}' not registered."

        target = registry[module_name]

        # Must expose public API
        if not hasattr(target, "api"):
            return f"[MODULE {module_name}] No callable API"

        try:
            return target.api(action)
        except Exception as e:
            return f"[MODULE ERROR] {e}"

    # ----------------------------------------
    # --- Terminal Commands ---
    # ----------------------------------------
    def run_terminal(self, cmd):
        if not cmd:
            return "[TERMINAL ERROR] Missing command"
        try:
            out = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
            return out.decode()
        except subprocess.CalledProcessError as e:
            return f"[TERMINAL ERROR] {e.output.decode()}"
