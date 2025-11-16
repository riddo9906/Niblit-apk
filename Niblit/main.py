# main.py
from niblit_core import NiblitCore

def run():
    niblit = NiblitCore()

    print("Starting Niblit...")
    print("Checking LLM availability...")
    print("LLM Online:", niblit.llm.is_available())

    print("\n--- Chat Session ---")
    print("Type 'exit' to quit.\n")

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ["exit", "quit"]:
            break

        response = niblit.handle(user_input)
        print(f"Niblit: {response}")

    print("\nSaving memory and chat logs...")
    niblit.save_all()
    print("Done.")

if __name__ == "__main__":
    run()
