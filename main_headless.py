# main_headless.py (FULLY OPTIMIZED)

import sys, os, threading, time, traceback
from dotenv import load_dotenv

# Ensure current folder in path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Load environment variables
load_dotenv()

# Import core
try:
    from niblit_core_refactor import niblitcore
except ImportError:
    print("[Error] Could not import NiblitCore.")
    sys.exit(1)

def run_headless():
    print("[Niblit] Headless mode starting...")

    # Initialize core
    try:
        core = niblitcore()
    except Exception as e:
        print("[Error] Core failed to initialize:", e)
        traceback.print_exc()
        return

    # Background loop (updates sensors, memory, training, etc.)
    def background_loop():
        while core.running:
            try:
                core.update()
            except Exception as e:
                print("[NiblitCore] Update cycle error:", e)
            time.sleep(2)  # Update interval

    threading.Thread(target=background_loop, daemon=True).start()

    print("[Niblit] Ready. Type 'exit' to stop.")

    # Interactive loop
    try:
        while True:
            cmd = input("You: ").strip()
            
            if cmd.lower() in ("exit", "quit"):
                print("[Niblit] Shutting down...")
                core.shutdown()
                break

            # Respond and only print interaction outputs
            try:
                response = core.respond(cmd)
                print("Niblit:", response)
            except Exception as e:
                print("[Console ERROR] Response failed:", e)
                traceback.print_exc()

    except KeyboardInterrupt:
        print("\n[Niblit] KeyboardInterrupt received. Shutting down...")
        core.shutdown()
    except Exception as e:
        print("[Console ERROR] Unexpected error:", e)
        traceback.print_exc()

if __name__ == "__main__":
    run_headless()