# AI Handoff User Summary – 2025‑10‑23

**Purpose:** This document captures your personal profile, AI interaction protocols, and an overview of your project architectures to facilitate smooth handoffs between AI assistants and maintain context across sessions.

## Personal Profile

### Background & Context
* **Primary Role:** Developer and system architect
* **Business Context:** Supporting father's business (Majestic Design) alongside personal projects
* **Technical Focus:** Python-based web applications, AI/ML projects, and business automation
* **Hosting Environment:** Microsoft-based business infrastructure with GoDaddy hosting [2025‑07‑15]

### Development Preferences
* **Editor:** VS Code with Python and Docker extensions
* **Version Control:** Git-based workflows
* **Containerization:** Docker Desktop configured for WSL 2 on Windows
* **Documentation Style:** Technical, structured, with cross-references (e.g., [AJP‑XX] notation)

## AI Interaction Protocols

### Communication Style
* **Tone:** Professional and technical
* **Detail Level:** Comprehensive documentation with practical examples
* **Format Preferences:** 
  - Markdown for documentation
  - Code blocks with appropriate syntax highlighting
  - Structured sections with clear headings
  - Cross-referenced components (AJP notation system)

### Project Context Management
* **Reference System:** Use [AJP‑XX] notation for cross-referencing related concepts
* **Date Stamping:** Include dates in brackets [YYYY‑MM‑DD] when referencing historical decisions
* **Architecture Layers:** Maintain separation between technical stack, user docs, and templates

## Project Architectures Overview

### Project Categories

#### 1. AI & Data Pipeline Projects
**Examples:** 
* "AI Council" [2025‑10‑13] – Multi-agent debate system
* "MET4morfoses/OS" [2025‑08‑24] – Unified Knowledge Pipeline

**Architecture Pattern:**
* Backend: Flask + Gunicorn for API serving
* AI Layer: OpenAI + LangChain for agent orchestration
* Data Processing: Pandas for data manipulation
* Real-time: Flask-SocketIO/WebSockets for streaming
* Containerization: Docker with service separation

#### 2. Interactive Web Applications
**Examples:**
* "Siddhartha" Journal [2025‑09‑17] – Personal journaling application
* "Buddhist Cosmology 3D Map" [2025‑10‑14] – 3D visualization web app

**Architecture Pattern:**
* Backend: Flask or Django with SQLAlchemy ORM
* Database: PostgreSQL (containerized)
* Authentication: Flask-Login + Flask-Bcrypt
* Frontend: JavaScript with Three.js for 3D rendering
* Static Assets: Served via Flask from `/static/js`

#### 3. Business Process & Utility Apps
**Examples:**
* Materials Management system
* Equipment Request forms
* Daily Reports [2025‑07‑11]
* Delay form for Nicholas [2025‑10‑09]

**Architecture Patterns (Dual Path):**

**Option A: Python Web App Path**
* Technology: Flask + SQLAlchemy
* Use Case: Internal web-based forms
* Deployment: Docker containers

**Option B: Microsoft Power Platform Path**
* Technology: Power Apps + Power Automate + SharePoint/Dataverse
* Use Case: Mobile/desktop business forms with approval workflows
* Environment: Microsoft 365 browser-based development

## Environment Setup Context

### Z Cartridge Structure
The repository follows a "Z Cartridge" pattern with:
* `$Z_ROOT` – Root directory
* `$Z_SCRIPTS` – Automation scripts (bootstrap, hydrate, verify)
* `$Z_WORKSPACE` – Working project area
* `$Z_CONTAINERS` – Container definitions
* `$Z_ENV` – Environment configurations
* `$Z_CLOUD` – Cloud integration metadata
* `$Z_DOCS` – Documentation (this file location)

### Bootstrap Workflow
1. Set environment variables (`$Z_*` paths)
2. Install prerequisites (Git, Python 3.10+, Docker Desktop, VS Code, pre-commit)
3. Run `bash Z:/scripts/bootstrap` for initial setup
4. Run `bash Z:/scripts/hydrate` to build containers and seed data
5. Run `bash Z:/scripts/verify` for validation (linters, secret scans, ADR checks)
6. Use `bash Z:/scripts/verify-archive` for snapshot validation

### Key Integration Points
* **Cloud Repos:** Mapped in `cloud/repo-map.yml`
* **Templates:** Available in `templates/` for quick project scaffolding
* **Secrets Management:** `.env` files (git-ignored) for API keys and credentials
* **Microsoft 365:** Sign-in required for Power Platform development

## Notes for AI Assistants

### Context Continuity
* Always reference the software stack deep dive (`docs/technical/software-stack-deep-dive_20251023.md`) for technical stack details
* Use templates from `templates/` directory as starting points for new projects
* Maintain the [AJP‑XX] reference system when adding new concepts
* Date-stamp significant architectural decisions

### Common Tasks
* **New Python Project:** Copy `templates/requirements.txt` and customize
* **New Service Stack:** Use `templates/docker-compose.yml` as starting point
* **Environment Config:** Base on `templates/env.example` with project-specific secrets
* **Documentation:** Follow existing structure in `docs/technical/` and `docs/user/`

### Security Considerations
* Never commit actual credentials to version control
* Ensure `.env` files are in `.gitignore`
* Use explicit placeholder values in examples (e.g., `CHANGE_THIS_TO_A_SECURE_RANDOM_STRING`)
* Avoid using real API key prefixes in documentation examples
