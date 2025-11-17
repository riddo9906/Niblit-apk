import os
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from niblit_core_refactor import niblitcore
from modules.llm_adapter import LLMAdapter

# --- Initialize Niblit core and LLM ---
core = niblitcore()
llm = LLMAdapter(db=core.memory)

# --- FastAPI ---
app = FastAPI(title="NiblitProV5 Web API", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# --- Health endpoint ---
@app.get("/health")
async def health():
    return {
        "status": "alive",
        "uptime_s": (core.current_time_seconds() if hasattr(core, "current_time_seconds") else 0),
        "memory_entries": getattr(core.memory, "count", 0)
    }

# --- Query Niblit or LLM ---
@app.post("/query")
async def query(request: Request):
    data = await request.json()
    prompt = data.get("prompt", "")
    use_llm = data.get("llm", True)
    context = data.get("context", [])

    try:
        if use_llm and llm.is_available():
            resp = llm.query(prompt, context)
        else:
            resp = core.respond(prompt)
        return JSONResponse({"response": resp})
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

# --- Frontend placeholder ---
@app.get("/")
async def index():
    return {"message": "NiblitProV5 Web API running. POST to /query to interact."}

# --- Vercel entry point ---
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))