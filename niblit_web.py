from flask import Flask, request, jsonify
import threading
import time
from datetime import datetime
from niblit_core import NiblitCore

app = Flask(__name__)

# Initialize Niblit Core (headless)
niblit = NiblitCore()

# Background health tracker
uptime_start = time.time()

def health_loop():
    while True:
        uptime_s = int(time.time() - uptime_start)
        memory_entries = len(niblit.memory.data) if hasattr(niblit.memory, 'data') else 0
        app.config['HEALTH'] = {
            "uptime_s": uptime_s,
            "memory_entries": memory_entries,
            "network": getattr(niblit.network, 'status', 'offline'),
            "persona_tone": getattr(niblit, 'persona_tone', 'balanced'),
            "bridge": True
        }
        time.sleep(5)

threading.Thread(target=health_loop, daemon=True).start()

# -------------------- ROUTES --------------------

@app.route("/command", methods=["POST"])
def command():
    """
    Send a command to Niblit.
    JSON payload: {"text": "<your command>"}
    """
    data = request.get_json()
    text = data.get("text", "")
    if not text:
        return jsonify({"error": "No command provided"}), 400
    try:
        response = niblit.respond(text)
    except Exception as e:
        response = f"Error: {str(e)}"
    return jsonify({"response": response})

@app.route("/status", methods=["GET"])
def status():
    """Return core health and memory stats."""
    health = app.config.get('HEALTH', {})
    return jsonify(health)

@app.route("/memory", methods=["GET", "POST"])
def memory():
    """Get all memory entries or add new memory."""
    if request.method == "GET":
        mem = getattr(niblit.memory, 'data', {})
        return jsonify(mem)
    elif request.method == "POST":
        data = request.get_json()
        key = data.get("key")
        value = data.get("value")
        if not key or value is None:
            return jsonify({"error": "Provide both key and value"}), 400
        niblit.memory.set(key, value)
        return jsonify({"message": f"Remembered {key}"}), 200

@app.route("/health", methods=["GET"])
def health():
    """Return uptime and basic system health."""
    return jsonify(app.config.get('HEALTH', {}))

# -------------------- RUN SERVER --------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)