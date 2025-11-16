# main_headless.py - Pydroid3 safe test script for NiblitCore
# Author: Riyaad Behardien

import sys, os, threading, time, traceback

# Ensure current folder is in Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from niblit_core import niblitcore
except ImportError:
    print("[Error] Could not import NiblitCore. Check filenames and folder structure.")
    sys.exit(1)


def run_headless():
    """Boot Niblit core in headless console mode"""
    print("[Niblit] Headless system startup initiated...")
    try:
        core = niblitcore()
        print("[Niblit] Core initialized successfully.")
    except Exception as e:
        print(f"[Error] Failed to initialize core: {e}")
        traceback.print_exc()
        return

    # Background loop to keep core services alive
    def core_loop():
        while True:
            try:
                core.update()  # If implemented, runs periodic tasks
            except Exception as e:
                print("[NiblitCore] Error in background loop:", e)
            time.sleep(2)

    threading.Thread(target=core_loop, daemon=True).start()
    print("[Niblit] Background services active. Type 'exit' to quit.")

    # Console interface for testing
    while True:
        try:
            cmd = input("You: ").strip()
            if cmd.lower() in ("exit", "quit"):
                print("[Niblit] Shutting down headless system...")
                try:
                    core.shutdown()
                except:
                    pass
                break
            response = core.respond(cmd)
            print("Niblit:", response)
        except KeyboardInterrupt:
            print("\n[Niblit] KeyboardInterrupt received. Exiting.")
            try:
                core.shutdown()
            except:
                pass
            break
        except Exception as e:
            print("[Error] Exception in console loop:", e)
            traceback.print_exc()


if __name__ == "__main__":
    run_headless()