# healer.py - simple restart / reload helpers
import importlib, sys

def heal_module(name):
    try:
        if name in sys.modules:
            importlib.reload(sys.modules[name])
        else:
            importlib.import_module(name)
        print('[Healer] Healed', name)
        return True
    except Exception as e:
        print('[Healer] Failed to heal', name, str(e))
        return False

def init():
    print('[Healer] Ready.')