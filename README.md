# Z Cartridge

This cartridge defines a complete and reproducible environment for your projects.  It
includes a manifest that maps local directories to their upstream counterparts,
governance policies, environment definitions, cloud docking metadata and
documentation.  The contents of this tree are intentionally self‑describing so
that it can be plugged into any host and rehydrated into a development
environment without guesswork.

## AI Command-Line Interfaces

This repository includes scripts and documentation to help you install and configure common AI command-line interfaces.

### Supported AI CLIs

- **OpenAI CLI** - Python client for OpenAI's APIs (GPT-4, GPT-3.5, DALL-E, etc.)
- **Anthropic Claude** - Python client for Claude AI models
- **GitHub Copilot CLI** - Command-line interface for GitHub Copilot

### Installation

Run the installation script to set up all AI CLIs:

```bash
./scripts/install_ai_clis.sh
```

This script will:
1. Install Python dependencies from `requirements.txt` (OpenAI and Anthropic clients)
2. Install GitHub Copilot CLI via npm (if Node.js is available)
3. Check for GitHub CLI and provide setup instructions

### Prerequisites

- **Python 3.7+** with pip (for OpenAI and Anthropic clients)
- **Node.js and npm** (for GitHub Copilot CLI)
- **GitHub CLI** (optional, for enhanced Copilot integration)

### Configuration

After installation, configure your API keys:

```bash
# OpenAI API key
export OPENAI_API_KEY='your-openai-api-key'

# Anthropic API key
export ANTHROPIC_API_KEY='your-anthropic-api-key'
```

For GitHub Copilot, authenticate with:

```bash
gh auth login
```

### Usage Examples

**OpenAI (Python):**
```python
from openai import OpenAI
client = OpenAI()
response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Hello!"}]
)
```

**Anthropic Claude (Python):**
```python
from anthropic import Anthropic
client = Anthropic()
message = client.messages.create(
    model="claude-3-opus-20240229",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello!"}]
)
```

**GitHub Copilot CLI:**
```bash
# Get shell command suggestions
github-copilot-cli what-the-shell "list all files modified in the last week"

# Get git command suggestions
github-copilot-cli git-assist "undo last commit but keep changes"
```

### Manual Installation

If you prefer to install components individually:

**Python packages:**
```bash
pip install -r requirements.txt
```

**GitHub Copilot CLI:**
```bash
npm install -g @githubnext/github-copilot-cli
```
# AI Council System - Development Repository

## 🎯 Project Vision

A decentralized 24/7 live streaming platform where AI agents form organizational bodies to debate real-time events, with user participation through cryptocurrency mechanisms.

## 📋 Current Phase: Phase 1 - Foundation Architecture

### Project Status

- **Phase**: Foundation & Planning
- **Developer**: Solo (Swarm-Assisted)
- **Start Date**: October 14, 2025
- **Repository**: Development Prototype

## 🏗️ Architecture Overview

The AI Council System is designed as a modular, scalable "operating system" for decentralized AI collaboration. The core components are organized as follows:

```
ai-council-system/
├── swarm/                  # Swarm orchestration system
│   ├── orchestrator/       # Core orchestration logic
│   ├── roles/              # Role definitions and management
│   └── assemblies/         # Assembly definitions
├── ...                     # Other top-level directories for different system functions
```

For a detailed breakdown of the entire repository structure, please refer to the documentation in the `/docs` directory.

### Swarm Orchestration System

The `swarm` directory contains the core logic for the AI agent orchestration system. This system is responsible for coordinating multiple AI agents to perform complex tasks. It is built on three key concepts:

*   **Roles**: Define the responsibilities and capabilities of agents.
*   **Assemblies**: Define the workflows and success criteria for tasks.
*   **Orchestrator**: Manages the execution of assemblies, including agent assignment and result aggregation.

## 🚀 Getting Started

### Prerequisites

*   Python 3.9+
*   pip
*   virtualenv (recommended)

### Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/ai-council-system.git
    cd ai-council-system
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

### Usage

The primary entry point for interacting with the swarm orchestration system is the `SwarmCoordinator` class, located in `swarm/orchestrator/coordinator.py`.

**Basic Example:**

```python
from swarm.orchestrator.coordinator import SwarmCoordinator, Agent
from swarm.assemblies.assembly_loader import get_assembly

# Initialize the coordinator
coordinator = SwarmCoordinator()

# Register an agent
agent = Agent(
    agent_id="007",
    name="James Bond",
    capabilities=["espionage", "seduction", "mixology"]
)
coordinator.register_agent(agent)

# Load an assembly
assembly = get_assembly("example_mission")

# Execute the assembly
if assembly:
    result = coordinator.execute_assembly(assembly, {"mission_briefing": "Infiltrate the secret lair."})
    print(result)
```

## 🚀 Development Phases

### Phase 1: Foundation (Current)

- [x] Project setup
- [x] README update
- [ ] Core architecture definition
- [ ] Swarm orchestrator implementation
- [ ] Basic AI agent framework
- [ ] Event ingestion prototype

### Phase 2: Prototyping

- [ ] Website launch
- [ ] Twitter presence
- [ ] Token creation (pump.fun)
- [ ] Basic live stream setup

### Phase 3: Core Implementation

- [ ] AI council debates
- [ ] Blockchain RNG integration
- [ ] User interaction mechanics
- [ ] Cryptocurrency rewards

### Phase 4: Advanced Features

- [ ] Generative visuals
- [ ] Advanced betting mechanics
- [ ] Governance implementation
- [ ] Multi-chain support

### Phase 5: Launch & Scale

- [ ] Public beta
- [ ] Community building
- [ ] 24/7 operations
- [ ] Platform expansion

## ⚠️ Legal & Ethical Considerations

### Immediate Concerns

1. **Gambling Regulations**: Betting mechanics require compliance with UIGEA, state laws
2. **Securities Law**: Token may be classified as security (Howey Test)
3. **Content Liability**: NSFW content creates platform risks
4. **International Compliance**: EU AI Act, GDPR, etc.

### Mitigation Strategy

- Start with entertainment-focused MVP (no gambling)
- Implement robust content moderation
- Consult legal counsel before token launch
- Build compliance frameworks from day one

## 🛠️ Technology Stack

### Core Technologies

- **AI/LLM**: Claude, GPT-4, Grok (via APIs)
- **Blockchain**: Ethereum + Solana hybrid
- **RNG**: Chainlink VRF, Pyth Entropy, Quantum (future)
- **Streaming**: OBS, RTMP, Twitch/YouTube APIs
- **Frontend**: Next.js, React, TailwindCSS
- **Backend**: Node.js, Python (FastAPI)
- **Database**: PostgreSQL, Redis (caching)

### Development Tools

- **Version Control**: Git/GitHub
- **CI/CD**: GitHub Actions
- **Testing**: Jest, Pytest, Hardhat
- **Monitoring**: Prometheus, Grafana

## 📊 Key Metrics & Data Points

### Market Context (October 2025)

- Bitcoin: $102,000 (from $123,000 peak)
- Liquidations: $19 billion
- Memecoin failure rate: 97-99%
- Pump.fun successes: 293 tokens >$1M profit

### Target Metrics

- Stream uptime: 99.9% (24/7)
- Concurrent viewers: 1,000+ (Phase 5)
- Token holders: 10,000+ (Phase 5)
- Daily transactions: 5,000+ (Phase 5)

## 🤝 Contributing

Solo developer project with swarm-assisted development. Contact via GitHub issues.

## 📄 License

TBD - Pending legal review

## 🔗 Links

- Website: TBD
- Twitter: TBD
- Discord: TBD
- Token: TBD

---

**Last Updated**: October 24, 2025
**Version**: 0.1.1-alpha

## 📚 Z Cartridge Foundation

This repository is built on the Z Cartridge framework, providing:
- Reproducible development environments
- Governance policies and standards
- Documentation architecture
- Container definitions
- Workspace management

See `/docs` for detailed cartridge documentation.
