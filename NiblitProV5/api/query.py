# api/query.py
import asyncio
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

# Lazy-loading globals
core = None
llm = None

def get_core():
    global core
    if core is None:
        from niblit_core_refactor import niblitcore
        core = niblitcore()
    return core

def get_llm():
    global llm
    if llm is None:
        from modules.llm_adapter import LLMAdapter
        llm = LLMAdapter(db=get_core().memory)
    return llm

# FastAPI app
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/health")
async def health():
    c = get_core()
    return {
        "status": "alive",
        "uptime_s": getattr(c, "current_time_seconds", lambda: 0)(),
        "memory_entries": getattr(c.memory, "count", 0)
    }

@app.post("/query")
async def query(request: Request):
    data = await request.json()
    prompt = data.get("prompt", "")
    use_llm = data.get("llm", True)
    context = data.get("context", [])

    try:
        if use_llm:
            response = get_llm().query(prompt, context)
        else:
            response = get_core().respond(prompt)
        return JSONResponse({"response": response})
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)