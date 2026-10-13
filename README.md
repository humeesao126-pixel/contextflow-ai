
# ✦ ContextFlow AI

### Your ideas, in better context.

ContextFlow AI is a conversational AI chatbot built with Python,
Streamlit, and Google's Gemini API.

It maintains conversation context using session-based memory and a
configurable sliding-window mechanism. Chat histories are also
stored locally using SQLite.

Developed as part of the DecodeLabs Generative AI Industrial
Training Program — Project 1: Custom AI Chatbot with Memory.

## ✨ Features

- Google Gemini AI integration
- Real-time response streaming
- Sliding-window conversation memory
- SQLite-based persistent chat history
- Multiple chat conversations
- Create, switch, rename, and delete chats
- Memory Inspector dashboard
- Conversation export to TXT
- Offline Demo Mode with simulated responses
- Interactive suggested prompts
- Cloud Lilac Studio user interface
- API error handling and retry support

## 🛠️ Technologies

- Python
- Streamlit
- Google GenAI SDK
- SQLite
- HTML and CSS

## 📁 Project Structure

```text
contextflow-ai/
├── app.py
├── database.py
├── memory.py
├── demo.py
├── requirements.txt
├── README.md
├── .gitignore
└── .streamlit/
    └── config.toml
```

Private files such as API secrets, virtual environments, and the
local conversation database are excluded from Git.

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/contextflow-ai.git
cd contextflow-ai
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Gemini API

Create a file:

`.streamlit/secrets.toml`

Add:

```toml
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"
```

Do not commit this file to GitHub.

### 5. Run the application

```bash
streamlit run app.py
```

Open:

http://localhost:8501

## 🧠 Memory Architecture

ContextFlow AI combines two memory mechanisms:

**Session memory:** Streamlit Session State stores active
conversation messages in memory.

**Persistent storage:** SQLite saves conversations and messages
locally, allowing users to revisit saved conversations.

**Sliding-window memory:** The application sends recent chat
history to Gemini based on the selected context window size.

## 🧪 Offline Demo Mode

Demo Mode provides predefined simulated responses without
making Gemini API requests.

It is intended for interface demonstrations and testing.
It does not provide actual generative AI responses.

## ⚠️ Limitations

- Gemini API usage is subject to provider quotas and rate limits.
- SQLite is stored locally.
- Public multi-user deployment requires additional privacy,
  session-isolation, and persistent-storage considerations.
- Demo Mode responses are simulated.

## 👩‍💻 Developer

**Humeesa**

GitHub: https://github.com/humeesao126-pixel

## 📚 Project Context

DecodeLabs Generative AI Industrial Training Program

Project 1 — Custom AI Chatbot with Memory

## 📄 License

No license has been selected yet.
```
