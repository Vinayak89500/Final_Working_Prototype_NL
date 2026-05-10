import os
import json
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from dotenv import load_dotenv
import httpx

load_dotenv()

app = FastAPI(title="Claude Compass")

# Allow frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve index.html at root
_BASE_DIR = os.path.dirname(os.path.abspath(__file__))

@app.get("/", include_in_schema=False)
async def serve_index():
    return FileResponse(os.path.join(_BASE_DIR, "index.html"))

class TaskRequest(BaseModel):
    intent: str

SYSTEM_PROMPT = """
"role": "system", "content": 'You are Claude Compass. Analyze the user\'s task. Suggest "prompt" if factual/simple. Suggest "workflow" if multi-step, structured, or deterministic. Suggest "agent" for tasks requiring exploration, iteration, adaptation, or when scope is uncertain/dynamic...'
Modes to evaluate:
1. Simple Prompt: Single-turn, low complexity, direct answers.
2. Workflow: Structured, multi-step, recurring, predictable processes.
3. Agent: Open-ended, exploratory, iterative, adaptive, or requiring real-time decisions.

Calculate ROI based on estimated token density. Workflows save tokens by avoiding redundant context. Agents excel when tasks evolve or require multiple iterations.

Return ONLY raw JSON:
{
  "recommendation": "Workflow" | "Simple Prompt" | "Agent",
  "reasoning": "Context-specific rationale for this choice",
  "steps": [{"name": "Step Name", "desc": "Action", "tag": "Input|Process|Output", "tagClass": "tag-input|tag-process|tag-output"}],
  "complexity": "Description of structure and dependencies",
  "cards": [
    {
      "title": "Simple Prompt",
      "recommended": false,
      "rows": [
        {"label": "Fit Score", "val": "3/10", "bar": 30, "barColor": "#f87171", "valClass": "bad"},
        {"label": "Est. Tokens", "val": "15,000", "valClass": "bad"},
        {"label": "Verdict", "val": "Inefficient", "valClass": "bad"}
      ]
    },
    ... (repeat for Workflow and Agent)
  ],
  "savings": [
    {"val": "61%", "label": "Token Savings", "newNote": "vs. Serial Prompting"}
  ],
  "output_preview": "A simulated summary of what the result would look like"
}
"""

@app.post("/analyze")
async def analyze_task(request: TaskRequest):
    api_key = os.getenv("OPENROUTER_API_KEY")
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={"Authorization": f"Bearer {api_key}"},
            json={
                "model": "openai/gpt-4o-mini",
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": request.intent}
                ],
                "response_format": {"type": "json_object"}
            },
            timeout=60.0
        )
        
        if response.status_code != 200:
            err = response.json().get("error", {})
            raise HTTPException(
                status_code=500,
                detail=f"LLM error: {err.get('message', response.text)}"
            )

        data = response.json()
        raw_content = data["choices"][0]["message"]["content"]
        return json.loads(raw_content)

ANSWER_SYSTEM_PROMPT = """You are a knowledgeable, helpful AI assistant.
Answer the user's question or task clearly and concisely.
- For factual questions: give a direct, accurate answer with brief context.
- For task requests: provide a well-structured, actionable response.
- Use clear formatting with bullet points or short paragraphs where helpful.
- Keep the tone professional but conversational.
"""

@app.post("/answer")
async def answer_query(request: TaskRequest):
    """Return a direct LLM answer to the user's query."""
    api_key = os.getenv("OPENROUTER_API_KEY")

    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={"Authorization": f"Bearer {api_key}"},
            json={
                "model": "openai/gpt-4o-mini",
                "messages": [
                    {"role": "system", "content": ANSWER_SYSTEM_PROMPT},
                    {"role": "user", "content": request.intent}
                ]
            },
            timeout=60.0
        )

        if response.status_code != 200:
            err = response.json().get("error", {})
            raise HTTPException(
                status_code=500,
                detail=f"LLM error: {err.get('message', response.text)}"
            )

        data = response.json()
        return {"answer": data["choices"][0]["message"]["content"]}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
