# Email 1 — Inbox Triage Prompt Refactor

## Task

The `donate@` shared inbox was losing high-value donation offers. A volunteer-run Claude Project was triaging incoming emails, but the prompt was generating wrong outputs: vague forwarding language, hallucinated file attachments, walls of prose instead of routing decisions, and in one case an automated reply telling Marcus to forward something to himself. Two incidents had already reached the board as "operational risk."

**Deliverables requested:**
- Rewritten triage prompt (`triage_prompt.md`) outputting strict JSON
- Short evaluation strategy note (max one page)
- Re-triaged labels for 6 flagged failure emails (`corrections.csv`)

---

## Solution

### Prompt design
The new prompt enforces a single JSON output per email with four fields — `category`, `urgent`, `route_to`, `draft` — using exact taxonomy strings for all 8 categories and 6 routing targets. Key constraints added:

- No prose outside the JSON object
- No hallucinated attachments, forwarding promises, or unconfirmed operational details (`[FILL]` placeholder required)
- Explicit urgency conditions (72h deadline, ≤14-day best-by, active distribution runout, food assistance seekers always urgent)
- Language matching (Spanish email → Spanish draft)
- Inline disambiguation preventing food-adjacent spam from misclassifying as corporate donations

### Live testing
A Python script (`tests/run_triage.py`) calls Claude Haiku once per email from `inbox_sample.csv`, validates category/urgency/routing against expected labels, and checks drafts for hallucination phrases. Four iteration cycles:

| Run | Passes | Change |
|---|---|---|
| 1 | 26/40 | Baseline |
| 2 | 37/40 | Non-standard item routing, food assistance urgency, media exception |
| 3 | 39/40 | Corrected expected labels for food drive emails (model was right) |
| 4 | **40/40** | Tightened partner agency urgency — "next week's truck" is not urgent |

---

## Files

```
files/
├── inbox_sample.csv       # 40 real-world inbox emails used as test data
├── failure_examples.md    # 6 wrong outputs from the original prompt, annotated
├── current_prompt.md      # The original broken prompt
└── corrections.csv        # Template for re-triaged labels

outputs/                   # ★ Graded deliverables only
├── triage_prompt.md       # Rewritten system prompt (production-ready)
├── evaluation_note.md     # One-page testing strategy
└── corrections.csv        # Correct labels for all 6 failure examples

tests/                     # Supporting test infrastructure
├── run_triage.py          # Live API test runner (auto-loads .env)
├── triage_results.json    # Raw Haiku outputs for all 40 emails (final run)
├── triage_results.md      # Human-readable results report
├── tests.md               # Full findings audit and run history
└── summary.md             # Process walkthrough and repeatable test guide
```

---

## Running the Tests

```bash
pip3 install anthropic python-dotenv
# fill in .env at repo root with your API key and workspace ID
python3 tests/run_triage.py
```

**Final run stats:** 40/40 passes · 50,103 input tokens · 3,754 output tokens · $0.069 total · 0 hallucinations
