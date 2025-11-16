# Niblit v5 – Unified AI Platform

**Author:** Riyaad Behardien  
**Version:** v5 (Unified from v1 → v5)  
**License:** Proprietary / All Rights Reserved (Registered by Riyaad Behardien)  

---

## Table of Contents
1. [Project Overview](#project-overview)  
2. [Key Features](#key-features)  
3. [System Requirements](#system-requirements)  
4. [Repository Structure](#repository-structure)  
5. [Installation & Setup](#installation--setup)  
6. [Usage](#usage)  
7. [Workflows & Automation](#workflows--automation)  
8. [Development Guidelines](#development-guidelines)  
9. [Contributing](#contributing)  
10. [Maintenance & Updates](#maintenance--updates)  
11. [Support & Contact](#support--contact)  

---

## Project Overview
Niblit v5 is a unified AI platform integrating all previous design versions (v1 → v5) into a single robust system. It provides local and cloud AI model access, modular development capabilities, and cross-device compatibility.  

The platform supports:  
- Standalone LLM access (OpenAI, MoonshotAI, Meta)  
- Modular design for quick prototyping and testing  
- Real-time integration with Android and desktop devices  

---

## Key Features
- **Unified Architecture:** Combines previous versions into a coherent structure.  
- **Independent AI Development:** Users can integrate their own AI models.  
- **Cross-Platform Ready:** Supports Android devices, desktop, and cloud environments.  
- **Automated Workflows:** GitHub Actions and Pylint-ready workflows for consistent builds.  
- **Secure API Management:** Supports storing multiple API keys for various data sources.  

---

## System Requirements
- **OS:** Android 9+ / Ubuntu 22.04+ / Windows 10+  
- **Python:** 3.11+  
- **Java:** 17+  
- **Gradle:** 8+  
- **Storage:** Minimum 1GB free for source and builds  
- **Network:** Required for API integration and workflow automation  

---

## Repository Structure
```text
Niblit-v5/
│
├─ .github/workflows/      # CI/CD and automation workflows
│   ├─ build.yml           # Android APK build workflow
│   └─ pylint.yml          # Linter workflow
│
├─ niblit_core/            # Core AI engine & modules
├─ designs/                # Standalone designs v1 → v5
├─ assets/                 # Models, datasets, API keys (encrypted or env)
├─ scripts/                # Utility scripts
├─ tests/                  # Unit and integration tests
├─ README.md               # Project documentation
└─ requirements.txt        # Python dependencies
