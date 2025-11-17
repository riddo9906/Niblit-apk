# auto_structure.py
import os, json

STRUCTURE = {
    "modules": [
        "analytics.py","antifraud.py","idea_generator.py","llm_adapter.py",
        "llm_module.py","reflect.py","storage.py","device_manager.py",
        "firmware.py","bios.py","bootloader.py","__init__.py"
    ],
    "__init__.py": "# Auto-generated to mark package\n",
    "main.py": "# main placeholder\n",
    "niblit_core.py": "# core placeholder\n",
    "niblit_memory.json": "{}",
    "niblit_net.py": "# net placeholder\n",
    "server.py": "# server placeholder\n",
    "auto_structure.py": "# auto-structure script\n"
}

DEFAULT_FILE_CONTENT = {
    "__init__.py": "# Auto-generated to mark package\n",
    "device_manager.py": "class DeviceManager:\n    pass\n",
    "firmware.py": "class Firmware:\n    pass\n",
    "bios.py": "class BIOS:\n    pass\n",
    "bootloader.py": "class Bootloader:\n    pass\n"
}

def ensure_structure(base_path: str):
    print(f"🔧 Checking Niblit directory: {base_path}")
    modules_path = os.path.join(base_path, "modules")
    os.makedirs(modules_path, exist_ok=True)
    for m in STRUCTURE["modules"]:
        fpath = os.path.join(modules_path, m)
        if not os.path.exists(fpath):
            print(f"📝 Creating module file: {fpath}")
            with open(fpath, "w", encoding="utf-8") as f:
                f.write(DEFAULT_FILE_CONTENT.get(m, f"# Auto-generated {m}\n"))
    for key, val in STRUCTURE.items():
        if key == "modules":
            continue
        path = os.path.join(base_path, key)
        if not os.path.exists(path):
            print(f"📝 Creating file: {path}")
            content = val if isinstance(val, str) else ""
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
    print("✅ Niblit structure verified & repaired.")
    return True

if __name__ == "__main__":
    BASE = os.path.dirname(os.path.abspath(__file__))
    ensure_structure(BASE)