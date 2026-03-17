# **Gemma AI Helper**

A lightweight CLI chat application powered by Google Gemini API.

## Features
* **Context Memory:** Maintains conversation flow using `collections.deque` for efficient history management.
* **Persistent Storage:** Automatically saves chat history to JSON format for future sessions.
* **Cross-Platform:** Full support for both Windows and Linux.
* **OS-Standard Paths:** Securely stores API keys in standard directories: `~/.config` for Linux and `AppData/Roaming` for Windows.
* **OOP Architecture:** Built with clean, Object-Oriented principles to ensure code scalability.

## Tech Stack
* **Python 3.14+**
* **Google Generative AI SDK** (Gemma)
* **JSON** (for local data persistence)
* **Git** (Conventional Commits style)

## Quick Start
1. **Clone the repo:**
   `git clone https://github.com/dmitrovskii/gemma-ai-helper.git`
2. **Install requirements:**
   `pip install -r requirements.txt`
3. **Setup API Key:**
   Save your API key in key.txt within the configuration paths mentioned above.
4. **Launch:**
   `python main.py`

## Roadmap
- **[ ]** Add data validation via Pydantic.
- **[ ]** Support for multiple concurrent chat sessions.
- **[ ]** Implement `asyncio` for non-blocking I/O.
- **[ ]** Integrate a Vector Database for long-term RAG memory.

---
**Author:** Dmitry (@dmitrovskii)