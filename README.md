# 🧭 Claude Compass — AI-Native Decision Intelligence

Claude Compass analyzes your task intent and recommends the optimal Claude execution mode — **Simple Prompt**, **Workflow**, or **Agent**. It also fetches a live AI answer to your query via OpenRouter.

## ✨ Features

- **7-screen guided flow** — Intent → Analysis → Decomposition → Scorecard → Handoff → Results → Feedback
- **Capability Scorecard** — Compares Simple Prompt, Workflow, and Agent with fit scores, token estimates, and verdicts
- **Task Decomposition** — Breaks your task into structured Input / Process / Output steps
- **Live AI Response card** — Fetches a real LLM answer to your query on the results screen
- **Progress tracker** — Animated dot indicator across all screens
- **Copy to clipboard** — One-click copy of the live AI response

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Vanilla HTML + CSS + JS |
| Backend | Python + FastAPI |
| LLM Provider | OpenRouter (gpt-4o-mini) |
| Server | Uvicorn |

## 🚀 Running Locally

### 1. Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/claude-compass.git
cd claude-compass
```

### 2. Create a virtual environment & install deps
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate

pip install -r requirements.txt
```

### 3. Set up your API key
```bash
# Copy the example file and add your key
cp .env.example .env
```
Then open `.env` and replace `your-openrouter-api-key-here` with your real key.  
Get a free key at 👉 https://openrouter.ai/keys

### 4. Run the server
```bash
python main.py
```

Open **http://localhost:8000** in your browser.

## 📁 Project Structure

```
claude-compass/
├── main.py          # FastAPI backend — /analyze and /answer endpoints
├── index.html       # Full frontend (single-file, no build step)
├── requirements.txt # Python dependencies
├── .env.example     # Template for your API key
└── .gitignore
```

## 🔌 API Endpoints

| Method | Path | Description |
|---|---|---|
| `GET` | `/` | Serves the frontend |
| `POST` | `/analyze` | Analyzes intent → returns JSON scorecard, steps, savings |
| `POST` | `/answer` | Returns a direct LLM answer to the user's query |

## ☁️ Deploying to the Web

This app has a Python backend so you need a service that runs Python:

| Platform | Free Tier | Deploy Command |
|---|---|---|
| [Render](https://render.com) | ✅ Yes | Connect GitHub repo, set env var |
| [Railway](https://railway.app) | ✅ Yes (limited) | `railway up` |
| [Fly.io](https://fly.io) | ✅ Yes | `fly launch` |

**For Render:** Set the Start Command to `python main.py` and add `OPENROUTER_API_KEY` as an Environment Variable in the dashboard.

## ⚠️ Important

Never commit your `.env` file — it contains your API key. The `.gitignore` already excludes it.
