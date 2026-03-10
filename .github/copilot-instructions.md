# Copilot Instructions for Niblit AI

## Project Overview

Niblit AI is a self-evolving, modular AI system designed for Android via KivyMD. It operates with local networking, UI, and sensor modules, and can optionally connect to external APIs. The system includes self-maintenance, sensor handling, data collection, training, and generation capabilities.

**Developer:** Riyaad Behardien  
**Project:** Symtium–Elysium Unified AI Initiative (Project One)

---

## Tech Stack

- **Language:** Python 3.10+
- **Android UI:** [KivyMD](https://kivymd.readthedocs.io/) (Material Design for Kivy)
- **APK Packaging:** [Buildozer](https://buildozer.readthedocs.io/)
- **Backend/API Layer:** [FastAPI](https://fastapi.tiangolo.com/) + [Uvicorn](https://www.uvicorn.org/)
- **Key Libraries:** `requests`, `psutil`, `cryptography`, `python-dotenv`, `plyer`, `SpeechRecognition`
- **Android Permissions:** INTERNET, RECORD_AUDIO, ACCESS_FINE_LOCATION, CAMERA, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE

---

## Repository Structure

```
Niblit-apk/
├── .github/
│   ├── copilot-instructions.md   # This file
│   └── workflows/
│       └── build-niblit-aios.yml # CI workflow (manual trigger)
├── NiblitProV5/                  # Main Android app source (KivyMD)
├── NiblitPro/                    # Earlier Pro variant
├── Niblit/                       # Core Niblit module
├── niblit-core/                  # Core logic package
├── modules/                      # Pluggable AI modules
├── data/                         # Training data and queues
├── niblit_memory/                # Persistent memory storage
├── main_refactor.py              # Main entry point (refactored)
├── niblit_core.py                # Core AI logic
├── niblit_network.py             # Network/internet handler
├── niblit_dashboard.py           # KivyMD dashboard UI
├── niblit_sensors.py             # Device sensor integration
├── niblit_voice.py               # Voice/speech recognition
├── niblit_web.py                 # Web interface
├── niblit_bridge.py              # Bridge module
├── niblit_memory.py              # Memory management
├── server.py                     # FastAPI server entry point
├── buildozer.spec                # Buildozer APK packaging config
├── requirements.txt              # Python dependencies
└── README.md
```

---

## Development Guidelines

### Code Style
- Follow [PEP 8](https://pep8.org/) for all Python code.
- Use descriptive variable and function names that reflect Niblit's AI module naming conventions (e.g., `niblit_`, `draegtile_`).
- Keep module responsibilities separated: each `niblit_*.py` file should handle a single concern (networking, UI, sensors, etc.).

### Adding a New Module
1. Create a new file named `niblit_<module_name>.py` at the project root or inside `modules/`.
2. Expose a main class or `init()` function that can be called from `main_refactor.py`.
3. Add any new dependencies to `requirements.txt` and `buildozer.spec` under `requirements`.
4. Document the module purpose at the top of the file with a docstring.

### Android / Buildozer
- Source extensions for APK build are: `py, kv, ttf, png, jpg, json` (see `buildozer.spec`).
- When adding new asset types, update `source.include_exts` in `buildozer.spec`.
- Target Android API: **33** (see CI workflow).
- Build tool version: **33.0.2**.

### API Server
- The FastAPI server is defined in `server.py`.
- Run locally with: `uvicorn server:app --reload`
- Environment variables should be placed in a `.env` file and loaded via `python-dotenv`. Never commit secrets.

### Testing
- There is no dedicated test suite currently. When adding tests, place them in a `tests/` directory and use `pytest`.
- Run checks with the existing shell script: `bash run_checks.sh`

---

## CI / Build

The CI workflow (`.github/workflows/build-niblit-aios.yml`) is triggered **manually** via `workflow_dispatch`. It:
1. Sets up Java 17 and Android SDK (API 33, build-tools 33.0.2).
2. Downloads the Niblit AIOS source archive.
3. Builds the APK with Gradle (`assembleArm7Release`).
4. Runs unit tests (`testArm7ReleaseUnitTest`).
5. Uploads the unsigned APK as an artifact.

To trigger: go to **Actions → build-niblit-aios → Run workflow**.

---

## Memory & Data Files
- `niblit_memory.json` / `niblit_memory/niblit_memory.json`: Persistent AI memory — do not manually edit these during a running session.
- `data/training_queue.json`: Training data queue consumed by the trainer module.
- `draegtile_network.json`: Draegtile network configuration.

---

## Security
- All AI decisions and network calls are sandboxed by design.
- The API bridge to external services (e.g., OpenAI) is **disabled by default**.
- Cloud functionality can be set to manual mode: `niblit_cloud.enable_manual_mode()`
- Do not commit `.env` files or API keys. Use environment variables or GitHub Secrets.
