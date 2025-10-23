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
