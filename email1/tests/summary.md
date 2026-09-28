# Email 1 — Process Summary & Repeatable Test Guide
**Riverbend Food Alliance | donate@ Triage Prompt Refactor**
**Date completed:** 2026-09-28 | **Model tested:** `claude-haiku-4-5-20251001`

---

## 1. What Was Built

A production-ready email triage system for Riverbend Food Alliance's `donate@` inbox, consisting of:

| File | Purpose |
|---|---|
| `triage_prompt.md` | System prompt for Claude Haiku; outputs strict JSON per email |
| `corrections.csv` | Re-triaged ground-truth labels for the 6 failure examples |
| `evaluation_note.md` | One-page testing strategy for ongoing prompt governance |
| `run_triage.py` | Python script that runs the full inbox sample through the live API |
| `tests.md` | Full findings audit: requirements checklist, edge case catalog, run history |
| `triage_results.json` | Raw API outputs for all 40 inbox sample emails (final run) |
| `triage_results.md` | Human-readable results report with deviation and cost tables |

---

## 2. Step-by-Step Process

### Step 1 — Read all source files

Four files drove every decision:

- **`current_prompt.md`** — the broken prompt that was generating wrong outputs
- **`failure_examples.md`** — 6 real email → output pairs showing exactly what went wrong
- **`inbox_sample.csv`** — 40 real inbox emails covering all category types
- **`corrections.csv`** — the template to fill in (header + `email` column pre-populated)

Reading all four before writing anything is essential. The failure examples reveal specific prompt deficiencies; the inbox sample reveals edge cases the failure examples don't cover.

### Step 2 — Diagnose the current prompt

Five distinct failure modes were identified in `current_prompt.md`:

| Failure | Root cause in old prompt |
|---|---|
| High-value corporate offer lost (Kevin) | No routing taxonomy; "forward to warehouse manager" was vague prose |
| Automated reply told Marcus to forward to Marcus (Pastor Dan) | No rule preventing "I'm forwarding to [name]" in drafts |
| Spam produced huge formatted prose summary | No JSON-only output constraint |
| Draft hallucinated a non-existent attachment (Jen) | No prohibition on unconfirmed actions |
| Reply asked for ID document not in policy (Ana) | No rule requiring `[FILL]` for unconfirmed operational details |

### Step 3 — Write `triage_prompt.md`

The new prompt was structured in five explicit sections:

1. **Output schema** — hard JSON-only constraint stated in the first line
2. **Categories** — table of 8 exact strings with one-line definitions, including explicit spam disambiguation for food-adjacent promos
3. **Routing** — table of 6 exact routing targets with `auto_ok` scoped narrowly to standard shelf-stable drop-offs
4. **Urgency rules** — four conditions using specific, unambiguous language (72h deadline, ≤14-day best-by, current distribution runout, food_assistance_seeker always urgent)
5. **Draft rules** — six numbered constraints eliminating every hallucination vector

Two few-shot examples were added: one corporate donation with a liquidation deadline, one spam email — chosen to cover the two hardest discriminations in the inbox sample.

### Step 4 — Fill `corrections.csv`

Applied the new prompt logic manually to each of the 6 failure emails:

| email | Logic applied |
|---|---|
| kevin | Corporate offer + Wednesday deadline → `corporate_food_donation`, `yes`, `marcus` |
| sarah | Simple canned goods drop-off → `individual_food_donation`, `no`, `auto_ok` |
| pastor_dan | Partner running out during active distribution → `partner_agency_request`, `yes`, `marcus` |
| spam | Automated marketing from grantstation.com → `spam_no_reply`, `no`, `no_reply` |
| jen | Group volunteer shift with May 15 deadline → `volunteer_inquiry`, `yes`, `priya` |
| ana | Household with 3 kids needing food → `food_assistance_seeker`, `yes`, `intake_line` |

### Step 5 — Write `evaluation_note.md`

Documented three things:
1. **Test set:** the 6 labeled examples as a regression baseline; the 40 inbox sample emails as an expanded benchmark
2. **Key metrics:** JSON parse rate, category/urgency/routing accuracy, hallucination rate, language match
3. **Red-team scenarios:** lookalike domains, multi-ask emails, spam with food-adjacent subjects, non-English emails

### Step 6 — Run live API tests

The Python script `run_triage.py`:
1. Loads `.env` from the repo root (API key + workspace ID)
2. Reads `triage_prompt.md` as the system prompt
3. Reads all 40 rows from `inbox_sample.csv`
4. For each email, calls `client.messages.create()` with `model=claude-haiku-4-5-20251001`
5. Parses the JSON response
6. Compares `category`, `urgent`, and `route_to` against the `EXPECTED` labels dict
7. Checks drafts for hallucination phrases
8. Checks category and route values against the allowed taxonomy
9. Writes `triage_results.json` (raw) and `triage_results.md` (report)

### Step 7 — Iterate on deviations

Three prompt revision cycles were needed:

**Run 1 → Run 2 (26/40 → 37/40):** Three prompt fixes applied in one pass:
- Non-standard individual donations (`auto_ok` → `marcus`): added explicit exclusion list for toiletries, clothing, refrigerated items, specialty items
- Food assistance seekers always urgent: changed condition from "household in immediate food need" (requires inference) to "`food_assistance_seeker` — always `urgent: true`" (declarative)
- Media "this week" false positives: added explicit exception that press requests with "this week/soon" are not urgent unless a specific publication date is named

**Run 2 → Run 3 (37/40 → 39/40):**
- S31/S32 expected labels corrected from `urgent: true` to `urgent: false` — "in May" does not meet the 72h rule, and the model's behavior was correct; our expected labels were wrong

**Run 3 → Run 4 (39/40 → 40/40):**
- S16 was oscillating between runs (non-deterministic on "running short" + "next week's truck"). Fixed by tightening the partner agency urgency condition to *current or same-day* distribution only, with an explicit parenthetical: "next week's truck is NOT urgent"

---

## 3. How Token Costs Were Calculated

All token counts are **measured directly** from the Anthropic API response's `usage` field — not estimated.

```python
resp = client.messages.create(model=..., system=..., messages=[...])
input_tokens  = resp.usage.input_tokens   # tokens consumed by system prompt + user message
output_tokens = resp.usage.output_tokens  # tokens generated in the response
```

### Final run measurements (40 emails, `claude-haiku-4-5-20251001`)

| Metric | Value |
|---|---|
| Total input tokens | 50,103 |
| Total output tokens | 3,754 |
| Average input tokens / email | 1,252 |
| Average output tokens / email | 94 |
| Min input (shortest email) | 1,238 |
| Max input (longest email) | 1,275 |
| Min output (spam, empty draft) | 38 |
| Max output (longest draft) | 136 |

**Why input tokens are ~1,252 per email:**
The `triage_prompt.md` system prompt alone is ~1,150–1,200 tokens (it includes two tables, 4 rule sections, and 2 few-shot examples — roughly 3.9 KB of text). Each email payload adds 40–100 tokens for the From/Subject/Body fields. Total: ~1,250 tokens per call.

**Why output tokens are ~94 per email:**
The JSON object has fixed structural overhead (~20 tokens). Spam emails produce `"draft": ""` — only ~38 tokens total. Non-spam emails produce a draft reply of 50–100 words (~65–136 tokens). Weighted average across the 40-email mix: 94 tokens.

### Cost formula

```
input_cost  = total_input_tokens  / 1,000,000 × $1.00
output_cost = total_output_tokens / 1,000,000 × $5.00
total_cost  = input_cost + output_cost
```

**Pricing used:** Claude Haiku 4.5 (`claude-haiku-4-5-20251001`) — $1.00/M input, $5.00/M output (September 2025).

### Per-email cost

```
(1,252 × $1.00/M) + (94 × $5.00/M)
= $0.001252 + $0.000470
= $0.001722 per email
```

### Monthly cost at various volumes

| Monthly volume | Monthly cost |
|---|---|
| 200 emails/month | $0.34 |
| 500 emails/month | $0.86 |
| 1,000 emails/month | $1.72 |
| 2,900 emails/month (≈$5 ceiling) | $4.99 |

---

## 4. Repeatable Test Steps

These steps reproduce the entire test run from scratch.

### Prerequisites

```bash
# Python 3.9+
python3 --version

# Install dependencies
pip3 install anthropic python-dotenv
```

### Environment setup

Create `/Users/miaelena/Downloads/claude_corps/.env`:

```
ANTHROPIC_API_KEY=<your-admin-key>
ANTHROPIC_WORKSPACE_ID=wrkspc_01DjRbGPpTNkH63GDcVhsZMV
ANTHROPIC_WORKSPACE_API_KEY=<your-workspace-key>
TRIAGE_MODEL=claude-haiku-4-5-20251001
```

The workspace must have API credits. Add them at: console.anthropic.com → select workspace → Settings → Billing.

### Run the test

```bash
python3 /Users/miaelena/Downloads/claude_corps/email1/outputs/run_triage.py
```

### What to expect

```
Using workspace-scoped key (workspace: wrkspc_...)
Model : claude-haiku-4-5-20251001
Emails: 40
  [01/40] S13  donation
  ...
  [40/40] S36  🔥 40% OFF bread — this week only!

Health summary:
  API errors      : 0
  Parse errors    : 0
  Taxonomy issues : 0
  Hallucinations  : 0
  Label deviations: 0
  Clean passes    : 40/40

Tokens  : ~50,000 in / ~3,700 out
Run cost: ~$0.069
```

**A clean run produces:** 0 API errors, 0 parse errors, 0 taxonomy violations, 0 hallucinations, 0 label deviations, 40/40 passes.

### Interpreting output files

| File | What to check |
|---|---|
| `triage_results.md` | **Flags column** — any non-PASS entry needs investigation |
| `triage_results.md` | **Deviations Detail** section — lists exactly which field was wrong and what value was expected |
| `triage_results.md` | **Hallucinations Detected** section — any entry here is a prompt failure requiring immediate fix |
| `triage_results.json` | Raw model outputs per email — useful for debugging specific cases |

### How to test a single email manually

```python
import anthropic, json
from pathlib import Path

client = anthropic.Anthropic(api_key="sk-ant-...")
system = Path("triage_prompt.md").read_text()

resp = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=512,
    system=system,
    messages=[{"role": "user", "content": "From: test@example.com\nSubject: donation\nBody: I have canned goods to donate."}]
)
print(json.loads(resp.content[0].text))
```

### How to add a new test case

1. Add a row to `inbox_sample.csv` with a new `id`, `from`, `subject`, `body`
2. Add the expected label to the `EXPECTED` dict in `run_triage.py`:
   ```python
   "S41": ("individual_food_donation", False, "auto_ok"),
   ```
3. Re-run `run_triage.py` — the new email is automatically included

### How to update the prompt and re-test

1. Edit `triage_prompt.md`
2. Run `python3 run_triage.py`
3. Check `triage_results.md` for regressions against all 40 expected labels
4. If deviations appear, fix and repeat

**The `EXPECTED` dict in `run_triage.py` is the regression baseline.** Any prompt change that breaks a previously-passing email is a regression. Update the expected labels only when you've verified the model's new output is actually correct (as was done for S31/S32 in Run 3).

---

## 5. Key Findings

| Finding | Impact |
|---|---|
| System prompt dominates token cost (1,200/1,252 tokens per call) | Cost scales almost entirely with email volume, not email length |
| Non-standard items need explicit enumeration to avoid `auto_ok` misrouting | Model defaults to the most permissive routing without a clear exclusion list |
| Declarative urgency rules outperform inferential ones | "food_assistance_seeker — always urgent" was 100% reliable; "household in immediate need" was 0% reliable |
| Borderline partner agency urgency (S16) required explicit counter-example in the rule text | "next week's truck is NOT urgent" in parentheses resolved the oscillation |
| Media "this week" genuinely ambiguous — model was defensible | Final resolution: media not urgent unless specific date named; this is a judgment call, not a model error |
| Real input tokens (1,252) are 79% higher than the pre-run estimate (700) | Cost estimates based on assumed prompt size significantly undercount — always measure |
| Real output tokens (94) are 37% lower than the pre-run estimate (150) | Partly offsets the input undercount; net effect is ~18% higher cost than original estimate |
