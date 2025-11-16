# run.py
from niblit_core import NiblitCore
from model_adapters import EchoAdapter, OpenAIAdapter, LlamaCppAdapter
import os

def pick_adapter():
    # Auto-detect a simple environment variable to pick adapter
    # Set NIBLIT_LLAMA_MODEL to path to use Llama adapter.
    llama_model = os.environ.get("NIBLIT_LLAMA_MODEL")
    if llama_model:
        print("Using local Llama adapter with model:", llama_model)
        return LlamaCppAdapter(binary_path=os.environ.get("NIBLIT_LLAMA_BIN","llama"), model_path=llama_model)
    openai_key = os.environ.get("OPENAI_API_KEY")
    if openai_key:
        print("Using OpenAI adapter.")
        return OpenAIAdapter(api_key=openai_key)
    print("No model configured — using fallback echo adapter.")
    return EchoAdapter()

def main():
    adapter = pick_adapter()
    n = NiblitCore(adapter=adapter, session_id="main")
    print("Niblit core running. Commands: !remember key: value  |  !forget key  |  !memory  | Ctrl-C to quit")
    try:
        while True:
            user = input("\nYou: ").strip()
            if not user:
                continue
            if user == "!memory":
                facts = n.review_memory()
                if not facts:
                    print("[No facts saved yet]")
                else:
                    for k,v,tags,ts in facts:
                        print(f"- {k}: {v} (tags={tags})")
                continue
            resp = n.ingest_user_message(user)
            print("\nNiblit:", resp)
    except KeyboardInterrupt:
        print("\nBye.")
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    main()