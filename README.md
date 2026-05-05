# Claude Compass 🧭

> An AI-native decision intelligence layer that helps users decide *when* to use a Workflow vs. a Simple Prompt vs. an Agent — before execution.

🔗 **Live Demo:** [final-working-prototype-nl.onrender.com](https://final-working-prototype-nl.onrender.com/)

---

## The Problem

As Claude evolved into Skills, Workflows, and Agents, users stopped struggling with **what** Claude can do — and started struggling with **how** to use it. ~35% of tasks qualify for a Workflow, but only ~5% of users actually adopt one. The result: token waste, trial-and-error fatigue, and abandoned advanced capabilities.

This isn't a skill gap. It's **decision anxiety**.

## What Compass Does

Compass intercepts user intent *before* execution and recommends the optimal Claude mode with rationale.

1. **Task Decomposition** — breaks a raw task into Input, Process, and Output steps
2. **Capability Scorecard** — evaluates the task across all Claude execution modes (Simple Prompt / Workflow / Agent) and recommends the best fit
3. **Token Efficiency Proof** — shows side-by-side token cost, output quality, and runtime so users understand *why* one mode wins

## Built For

The NextLeap Product Management Fellowship graduation project (2026 cohort), submitted in the **Workflows** capability track.

## Tech Stack

- **Backend:** FastAPI (Python)
- **Frontend:** Vanilla HTML / CSS / JS (single-page)
- **AI:** OpenRouter API (calling Claude models)
- **Hosting:** Render

## Project Structure

```
Final_Working_Prototype_NL/
├── index.html          # Single-page frontend (Compass UI)
├── main.py             # FastAPI backend — handles /analyze and /execute endpoints
├── test_api.py         # Decision Intelligence Engine — system prompt + classifier logic
├── requirements.txt    # Python dependencies
├── .env.example        # Template for environment variables
├── .gitignore
└── README.md
```

## Run Locally

### Prerequisites
- Python 3.9+
- An [OpenRouter API key](https://openrouter.ai/keys)

### Setup

```bash
# 1. Clone the repo
git clone https://github.com/Vinayak89500/Final_Working_Prototype_NL.git
cd Final_Working_Prototype_NL

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate     # macOS / Linux
# OR
venv\Scripts\activate        # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up environment variables
cp .env.example .env
# Then open .env and add your OPENROUTER_API_KEY

# 5. Run the server
uvicorn main:app --reload

# 6. Open your browser
# http://localhost:8000
```

## How It Works

```
User input
    ↓
Frontend (index.html) — captures task description
    ↓
POST /analyze → main.py
    ↓
test_api.py — Decision Intelligence Engine
    • Step-count parser (verbs, "then", lists)
    • Recurrence detector (weekly, every, recurring)
    • Determinism scorer (structured vs creative output)
    • Token estimator + confidence gate (<70% → ask 1 clarifying question)
    ↓
JSON Scorecard returned to frontend
    • Recommended mode + rationale
    • Token cost across all 3 modes
    • Step-by-step decomposition
    ↓
User reviews → executes → rates result
```

## Project Context

This repository is the prototype layer of a complete product strategy. The full project includes:

- 📑 **10-slide pitch deck** — problem, research, personas, solution, GTM, metrics
- 🎙️ **User research** — in-depth interviews + survey of Claude power users
- 📈 **Product strategy** — North Star metric (Workflow Activation Rate), four-signal classifier, embedded in-product GTM
- 🎬 **90-second demo video**

## What I'd Do Differently

A few things I'd change if taking this from prototype to production:

- **Larger sample size for research.** The qualitative signal was strong, but the survey size was exploratory. A v2 would target n=200+ with stratified sampling across user behaviour segments.
- **Effort estimate was optimistic.** I scoped this at 4–6 weeks. A real implementation — with proper classifier ML, persistence, and Anthropic plan-tier integration — is closer to 12–16 weeks for a small team.
- **The classifier is rule-based, not learned.** The four-signal heuristic works for the demo, but a production version should fine-tune on labelled task → optimal-mode pairs as users interact.
- **No team mode yet.** The "Reluctant Team Coordinator" persona was identified but not solved in MVP. A shared Workflow library is the natural v2.

## Built By

Vinayak — aspiring APM, NextLeap Fellowship 2026.

[GitHub](https://github.com/Vinayak89500)

---

*Built as part of the NextLeap PM Fellowship graduation requirement. Not affiliated with Anthropic.*
