"""
evaluate_prototype.py
---------------------
Evaluation script for the Claude Compass prototype.
Tests the /analyze endpoint against a golden set of 15 labelled examples
covering all three capabilities: Simple Prompt, Workflow, and Agent.

Usage:
    python evaluate_prototype.py [--url URL]

Default URL: https://final-working-prototype-nl.onrender.com
"""

import asyncio
import argparse
import httpx

# ---------------------------------------------------------------------------
# Golden test set  (5 per category)
# ---------------------------------------------------------------------------
GOLDEN_SET = [
    # ── Simple Prompt ────────────────────────────────────────────────────────
    {
        "intent": "What is the capital of France?",
        "expected": "Simple Prompt",
        "rationale": "Single-turn factual question — no steps, no tools needed.",
    },
    {
        "intent": "Summarize the following paragraph: [paste of 200-word text]",
        "expected": "Simple Prompt",
        "rationale": "Fixed-context summarization; no external data required.",
    },
    {
        "intent": "Review this email draft for grammar and tone: [paste of email]",
        "expected": "Simple Prompt",
        "rationale": "Text review on fixed context; purely single-turn.",
    },
    {
        "intent": "Translate 'Good morning' into Spanish, French, and German.",
        "expected": "Simple Prompt",
        "rationale": "Simple factual lookup, single response.",
    },
    {
        "intent": "Explain the difference between supervised and unsupervised learning.",
        "expected": "Simple Prompt",
        "rationale": "Explanatory Q&A — no iteration or external tools needed.",
    },

    # ── Workflow ──────────────────────────────────────────────────────────────
    {
        "intent": "Every Monday morning, pull last week's sales data from our CRM, "
                  "format it into a standard report, and email it to the team.",
        "expected": "Workflow",
        "rationale": "Recurring, deterministic, fixed steps — classic workflow.",
    },
    {
        "intent": "When a new customer signs up, send a welcome email, create a "
                  "CRM record, and notify the sales team on Slack.",
        "expected": "Workflow",
        "rationale": "Event-triggered, structured, predictable multi-step sequence.",
    },
    {
        "intent": "Convert all uploaded PDFs to text, extract invoice totals, "
                  "and append them to a Google Sheet.",
        "expected": "Workflow",
        "rationale": "Structured ETL pipeline — same steps every time.",
    },
    {
        "intent": "Each night at midnight, back up the database, compress the file, "
                  "and upload it to S3.",
        "expected": "Workflow",
        "rationale": "Scheduled, repeatable, deterministic steps.",
    },
    {
        "intent": "When a GitHub PR is merged, run the test suite, build the Docker "
                  "image, and deploy to staging.",
        "expected": "Workflow",
        "rationale": "CI/CD pipeline — fixed, deterministic sequence.",
    },

    # ── Agent ─────────────────────────────────────────────────────────────────
    {
        "intent": "Research the top 5 competitors in the EV market, analyse their "
                  "pricing strategies, and recommend where we should position our product.",
        "expected": "Agent",
        "rationale": "Requires web browsing, iteration, and adaptive decision-making.",
    },
    {
        "intent": "Debug this production outage — investigate logs, identify the root "
                  "cause, and propose a fix.",
        "expected": "Agent",
        "rationale": "Exploratory, open-ended; scope is unknown upfront.",
    },
    {
        "intent": "Find the best flight and hotel combo for a trip to Tokyo next month "
                  "within a $2,000 budget.",
        "expected": "Agent",
        "rationale": "Requires real-time data fetching, comparison, and iteration.",
    },
    {
        "intent": "Autonomously test our checkout flow, identify any UX issues, "
                  "and suggest improvements.",
        "expected": "Agent",
        "rationale": "Requires browser navigation, observation, and adaptive reasoning.",
    },
    {
        "intent": "Monitor our Twitter mentions in real time and respond to customer "
                  "complaints as they come in.",
        "expected": "Agent",
        "rationale": "Continuous, real-time, requires dynamic decision-making.",
    },
]

# ---------------------------------------------------------------------------
# Evaluation logic
# ---------------------------------------------------------------------------

async def run_eval(base_url: str) -> None:
    url = base_url.rstrip("/") + "/analyze"
    print(f"\n{'='*60}")
    print(f"  Claude Compass Evaluation")
    print(f"  Endpoint: {url}")
    print(f"  Test cases: {len(GOLDEN_SET)}")
    print(f"{'='*60}\n")

    passed = 0
    failed = 0
    errors = 0
    results = []

    async with httpx.AsyncClient(timeout=60.0) as client:
        for i, case in enumerate(GOLDEN_SET, 1):
            try:
                resp = await client.post(url, json={"intent": case["intent"]})
                resp.raise_for_status()
                data = resp.json()
                got = data.get("recommendation", "").strip()
                ok = got.lower() == case["expected"].lower()

                status = "✅ PASS" if ok else "❌ FAIL"
                if ok:
                    passed += 1
                else:
                    failed += 1

                results.append({
                    "id": i,
                    "status": status,
                    "expected": case["expected"],
                    "got": got,
                    "intent": case["intent"][:70],
                    "rationale": case["rationale"],
                })

            except Exception as exc:
                errors += 1
                results.append({
                    "id": i,
                    "status": "⚠️  ERROR",
                    "expected": case["expected"],
                    "got": f"ERROR: {exc}",
                    "intent": case["intent"][:70],
                    "rationale": case["rationale"],
                })

    # ── Print results ──────────────────────────────────────────────────────
    for r in results:
        print(f"[{r['id']:02d}] {r['status']}")
        print(f"     Intent   : {r['intent']}...")
        print(f"     Expected : {r['expected']}")
        print(f"     Got      : {r['got']}")
        if "FAIL" in r['status'] or "ERROR" in r['status']:
            print(f"     Rationale: {r['rationale']}")
        print()

    total = len(GOLDEN_SET)
    score = passed / total * 100
    print(f"{'='*60}")
    print(f"  Results : {passed}/{total} passed  ({score:.1f}%)")
    if errors:
        print(f"  Errors  : {errors} request(s) failed")
    print(f"{'='*60}\n")

    if score == 100.0:
        print("  🎉 Perfect score! Prototype is ready.")
    elif score >= 80.0:
        print("  👍 Good — minor issues remain. Review FAILed cases above.")
    else:
        print("  🔧 Needs work — review the FAIL pattern and tighten the prompt.")
    print()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Evaluate Claude Compass prototype.")
    parser.add_argument(
        "--url",
        default="https://final-working-prototype-nl.onrender.com",
        help="Base URL of the running prototype (default: Render deployment).",
    )
    args = parser.parse_args()
    asyncio.run(run_eval(args.url))
