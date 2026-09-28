# Email 4 — Monthly API Cost Estimate

## Task

The triage system built in Email 1 is ready to deploy, but Marcus needs a dollar figure to present to Diane (Executive Director) for budget approval. The ask was simple: put a number on it, show the math, and make it something Diane can act on.

**Deliverables requested:**
- Draft reply to Marcus with a specific monthly cost estimate and clear assumptions

---

## Solution

Rather than estimating token counts from first principles, the cost figures were derived directly from the live API run conducted in Email 1 — 40 emails processed through Claude Haiku with usage measured from the API response.

### Measured token counts (40-email live run)

| Metric | Value |
|---|---|
| Average input tokens / email | 1,252 |
| Average output tokens / email | 94 |
| Per-email cost | $0.001722 |

The high input token count (1,252 vs an initial estimate of 700) is explained by the triage system prompt being ~1,150 tokens — it includes two taxonomy tables, urgency rules, draft constraints, and two few-shot examples. Email content itself adds only ~100 tokens per call.

### Monthly cost

```
At 500 emails/month:
  Input:  500 × 1,252 × $1.00/M = $0.626
  Output: 500 ×    94 × $5.00/M = $0.235
  Total:  $0.861/month
```

**Recommended budget ceiling: $5/month** — covers ~2,900 emails/month, roughly 6× estimated current volume, with no pricing cliff.

### Pricing
Model: `claude-haiku-4-5-20251001` — $1.00/M input tokens, $5.00/M output tokens (September 2025)

---

## Files

```
outputs/              # ★ Graded deliverables only
└── reply_to_marcus.md   # Draft reply with cost breakdown and budget recommendation

tests/
└── tests.md             # Arithmetic verification and assumption audit
```

---

## Relationship to Email 1

This task has no source files of its own — all inputs come from Email 1. The token counts in `reply_to_marcus.md` are sourced from `email1/tests/triage_results.json` (the final 40/40 test run). The prompt referenced is `email1/outputs/triage_prompt.md`.
