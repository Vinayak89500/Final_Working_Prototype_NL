import asyncio, httpx, os, json
from dotenv import load_dotenv
load_dotenv()

SYSTEM_PROMPT = """
You are the Claude Compass Decision Intelligence Engine. Your goal is to solve the 'Decision Architecture' problem.
Analyze the user's intent and return a JSON object with a dynamic task decomposition and mode comparison.

Modes to evaluate:
1. Simple Prompt: Single-turn, low complexity.
2. Workflow: Structured, multi-step, recurring.
3. Agent: Open-ended, unpredictable, high autonomy.

Calculate ROI based on estimated token density. A Workflow typically saves tokens by avoiding redundant context.

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

async def test():
    async with httpx.AsyncClient() as client:
        r = await client.post(
            'https://openrouter.ai/api/v1/chat/completions',
            headers={'Authorization': f'Bearer {os.getenv("OPENROUTER_API_KEY")}'},
            json={
                'model': 'openai/gpt-4o-mini',
                'messages': [
                    {'role': 'system', 'content': SYSTEM_PROMPT},
                    {'role': 'user', 'content': 'Analyze 50 customer feedback emails, categorize sentiment, and create a weekly report'}
                ],
                'response_format': {'type': 'json_object'}
            },
            timeout=60.0
        )
        data = r.json()
        content = data['choices'][0]['message']['content']
        parsed = json.loads(content)
        print(json.dumps(parsed, indent=2))
        print("\n\n=== TOP-LEVEL KEYS ===")
        print(list(parsed.keys()))

asyncio.run(test())
