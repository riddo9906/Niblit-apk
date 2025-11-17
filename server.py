# server.py
import os, logging, time, json
from flask import Flask, request, jsonify
from modules.niblit_bridge import Bridge

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')
log = logging.getLogger("niblit-server")

app = Flask(__name__)
BRIDGE = Bridge()

@app.route("/status", methods=["GET"])
def status():
    return jsonify({
        "ok": True,
        "llm_available": BRIDGE.can_call(),
        "time": time.time()
    })

@app.route("/chat", methods=["POST"])
def chat():
    payload = request.json or {}
    text = payload.get("text") or payload.get("message") or ""
    prefer = payload.get("prefer","openai")
    if not text:
        return jsonify({"error":"no text provided"}), 400
    try:
        reply = BRIDGE.send_to_llm(text, prefer=prefer)
        # ensure string
        if isinstance(reply, (dict,list)):
            reply = json.dumps(reply)
        return jsonify({"ok": True, "reply": reply})
    except Exception as e:
        log.exception("chat error")
        return jsonify({"ok": False, "error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)