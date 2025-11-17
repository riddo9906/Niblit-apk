
🧠 NIBLIT AI SYSTEM (V5)

Developer: Riyaad Behardien

Project: Symtium–Elysium Unified AI Initiative (Project One)


---

📘 OVERVIEW

Niblit AI is a self-evolving, modular AI system designed for Android (via KivyMD).
It operates independently from external AI services (e.g. OpenAI), with local networking, UI, and sensor modules — but can later connect to APIs when enabled.
This version initializes Niblit as its own autonomous AI environment with self-maintenance, sensors, learning, and data collection.


---

🗂️ FILE STRUCTURE

NiblitProV5/
│
├── main.py                # Core bootloader, integrates all modules on startup
├── niblit_dashboard.py    # KivyMD-based visual dashboard (green/black theme)
├── niblit_network.py      # Internet connection handler + network monitor
├── niblit_selfmaintenance.py # CPU/RAM monitor and healing module
├── niblit_membrane.py     # Simulated digital membrane (AI awareness boundary)
├── niblit_collector.py    # Data collector module (environment, user, and network)
├── niblit_trainer.py      # AI training/learning logic for self-improvement
├── niblit_generator.py    # Creative logic & pattern generator module
├── assets/                # Textures, icons, UI sounds, and visual assets
│   ├── logo.png
│   ├── bg_texture.jpg
│   ├── icons/
│   └── sounds/
└── README.md              # This file


---

⚙️ SETUP GUIDE

1. 📱 Run Environment

You’ll need:

Pydroid 3 (Android) or PC Python 3.10+

Kivy and KivyMD installed:

pip install kivy kivymd requests psutil


2. 📦 Running Niblit

1. Open Pydroid 3 or your Python IDE.


2. Navigate to the NiblitProV5 directory.


3. Run:

python main.py


4. Niblit will boot with:

Network connection

Sensors initialization

Dashboard interface

Self-maintenance and training systems active





---

🌐 INTERNET & CLOUD SYSTEM

Niblit connects directly to the internet via the Niblit Network module.
A local cloud (self-hosted simulation) can be initialized later for:

Data backup and learning archives

Shared module updates

Real-time synchronization



---

💠 MODULE OVERVIEW

Module	Purpose

main.py	Boots and integrates all subsystems, starts dashboard
niblit_network.py	Connects Niblit to the internet
niblit_dashboard.py	Green/Black ChatGPT-style visual UI
niblit_selfmaintenance.py	Monitors system health and repairs functions
niblit_membrane.py	Creates digital “barrier” for awareness and self-organization
niblit_collector.py	Gathers data from network, user input, and sensors
niblit_trainer.py	Updates and retrains Niblit models with new info
niblit_generator.py	Creates new text, ideas, and patterns from input



---

🔋 SELF MAINTENANCE

The healer module monitors CPU, RAM, and system usage.
It automatically:

Clears unused memory

Adjusts refresh cycles

Logs performance data



---

🧬 DEVELOPMENT ROADMAP

Stage	Description

✅ Phase 1	Local execution + dashboard boot
🔄 Phase 2	Cloud integration + remote synchronization
🧩 Phase 3	Hybrid API connectivity (optional OpenAI / Meta)
🌌 Phase 4	Sentient AI foundation — Niblit Autonomous Core



---

💾 PACKAGING INTO APK

To package the project into an Android APK:

1. Install Buildozer or use Pydroid 3 Premium Plugin.


2. Include all assets in /assets.


3. Set app name: Niblit AI


4. Build command:

buildozer android debug


5. Output APK will appear in /bin.




---

🧠 Notes for Developer

All AI decisions and network calls are sandboxed for safety.

Cloud functionality can be switched to manual mode using:

niblit_cloud.enable_manual_mode()

The API bridge remains disabled by default until reactivated.



---

🪙 LEGAL & RIGHTS

All project rights, assets, and AI intellectual property belong to
© 2025 Riyaad Behardien — All Rights Reserved