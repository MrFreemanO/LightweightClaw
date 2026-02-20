<div align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue.svg" alt="Python Version" />
  <img src="https://img.shields.io/badge/Local_LLM-Jan_AI-purple.svg" alt="Jan AI" />
  <img src="https://img.shields.io/badge/Memory-3--Layer_PiecesOS-green.svg" alt="Memory" />
  <img src="https://img.shields.io/badge/Status-Beta-orange.svg" alt="Status" />
</div>

<h1 align="center">🤖 LightweightClaw</h1>

<p align="center">
  <b>Ultra-lightweight autonomous AI agent.</b> Inspired by <i>OpenClaw</i> and <i>Nanobot</i> architectures, but rewritten for maximum simplicity, speed, and complete privacy. Executes commands on your PC and remembers context using a 3-layer memory system.
</p>

---

## ⚡ Features

- 🧠 **Three-Layer Memory Architecture**:
  - *Short-term* (Working memory, last 50 messages, auto-quantization).
  - *Mid-term* (Daily file-based memory, logged to disk).
  - *Long-term* (Context summarization system, similar to PiecesOS).
- 🎭 **Integrated Personas**:
  - **J.A.R.V.I.S.** — Strict, British AI for system tasks and code.
  - **Mira** — Quick-witted, lively assistant for trends and web searches.
- 🗣️ **Voice Engine (Local)**: 
  - Text-to-Speech (TTS) via **Piper**.
  - Speech-to-Text (STT) via **OpenAI Whisper**.
- 🛠️ **Real Tool Integrations**:
  - CoinGecko Market Data Parser.
  - Autonomous Web Search (DuckDuckGo parsing without API keys).
  - Host System Monitor (RAM, CPU, Disk).

*(Note: Memecoin Sniper module has been moved to a separate repository for security and modularity reasons).*

---

## 🛑 IMPORTANT: Security and Secrets (READ THIS FIRST)

This project is built for **local use**. All private keys, bot tokens, and API access MUST be stored ONLY in the `.env` file.

1. **Telegram Token:** Get it from `@BotFather`. Paste it only in your local `.env`.
2. **NEVER PUSH `.env` TO GITHUB!** A `.gitignore` file is included in the repository; make sure it is not deleted.

---

## 🚀 1-Minute Installation (Linux / ZorinOS / Mac)

```bash
# 1. Clone the repository
git clone https://github.com/MrFreemanO/LightweightClaw.git
cd LightweightClaw

# 2. Create the secrets file from the template (PASTE TOKENS HERE)
cp .env.example .env
nano .env

# 3. Install dependencies and run
bash scripts/deploy_all.sh
```

### Running the Agent:
```bash
source .venv/bin/activate
python main.py
```
Open your browser at: **http://localhost:8000**

---

## ⚙️ Integration with Local Models (Jan AI)

By default, the project is configured to work with **Jan AI** (an OpenAI-compatible local API).
1. Open Jan.
2. Download any GGUF model (e.g., Llama 3 8B, Mistral, Qwen).
3. Go to Jan settings and enable the **Local API Server** (usually runs on `http://127.0.0.1:1337`).
4. LightweightClaw will connect to it automatically.

---

## 📂 Project Structure

```text
lightweightclaw/
├── core/
│   ├── agent.py        # Core logic, LLM interaction, tool parsing
│   ├── memory.py       # 3-layer memory & quantization
│   ├── tools.py        # REAL functions: search, crypto, sys_info
│   └── security.py     # Task isolation (limits, timeouts)
├── channels/
│   ├── web_ui.py       # FastAPI WebSocket server
│   └── telegram_bot.py # Telegram integration
├── voice/
│   ├── stt.py          # Whisper integration 
│   └── tts.py          # Piper integration
├── config/
│   ├── config.yaml     # Main settings & router logic
│   ├── personas.yaml   # Prompts for Jarvis and Mira
│   └── tools.yaml      # Tool access management
├── memory/             # Local knowledge base (created on run)
└── main.py             # Entry point
```

---

## 🛡️ Disclaimer
*This project is provided as-is for educational and personal automation purposes. The author is not responsible for any actions executed by the autonomous agent on your local machine.*
