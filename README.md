# Claude Corps — Riverbend Food Alliance

Four operational tasks for a fictional nonprofit food bank, each driven by a real incoming email and solved end-to-end using Claude. The work covers prompt engineering, data analysis, system design, and cost modeling — with live API tests and documented outputs for every task.

---

## Tasks

| # | Task | What was built |
|---|---|---|
| [Email 1](./email1/) | Inbox Triage Prompt Refactor | Rewrote a broken Claude prompt; tested 40 emails live via Haiku API; 40/40 passing |
| [Email 2](./email2/) | Q1 Board Memo Correction | Fact-checked an AI-generated memo against raw warehouse data; fixed numbers and agency name typos |
| [Email 3](./email3/) | Volunteer Confirmation Flow | Designed an automated signup → Airtable → SMS architecture; built the signup page and ROI draft |
| [Email 4](./email4/) | Monthly API Cost Estimate | Calculated real per-email token costs from live runs; $0.86/month at 500 emails |

---

## Repo Structure

```
claude_corps/
├── summaries.md          # One-paragraph plain-English summary of each task
├── email1/
│   ├── task.md           # Original task brief
│   ├── files/            # Source files (inbox sample, failure examples, etc.)
│   └── outputs/          # Deliverables + live test results
├── email2/
│   ├── task.md
│   ├── files/            # Raw distribution logs and agency directory
│   └── outputs/
├── email3/
│   ├── task.md
│   ├── files/            # Volunteer handbook and prototype page
│   └── outputs/
└── email4/
    ├── task.md
    └── outputs/
```

---

## Running the Email 1 Test Suite

The triage prompt can be tested live against all 40 inbox sample emails using Claude Haiku.

**Prerequisites**
```bash
pip3 install anthropic python-dotenv
```

**Setup** — copy `.env.example` to `.env` and fill in your credentials:
```
ANTHROPIC_API_KEY=sk-ant-...
ANTHROPIC_WORKSPACE_ID=wrkspc_...
ANTHROPIC_WORKSPACE_API_KEY=sk-ant-...
TRIAGE_MODEL=claude-haiku-4-5-20251001
```

**Run**
```bash
python3 email1/tests/run_triage.py
```

Expected: 40/40 clean passes, ~$0.069 per run, ~50s total.
