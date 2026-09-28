# Email Reply: donate@ Triage System — Monthly API Cost Estimate

**To:** Marcus
**Subject:** RE: donate@ Triage System — Monthly API Cost Estimate

---

Marcus,

The estimated monthly API cost to run the automated `donate@` triage pipeline is **approximately $0.86/month** at 500 emails/month — under $1/month.

This figure is based on **measured token counts from a live test run** of the triage prompt against 40 inbox sample emails using `claude-haiku-4-5-20251001`, not estimated assumptions.

---

**Model:** Claude Haiku 4.5 (`claude-haiku-4-5-20251001`)
**Pricing:** $1.00 per million input tokens / $5.00 per million output tokens

### Measured Variables (from live API run, 40 emails)

| Variable | Measured Value | Notes |
|---|---|---|
| Average input tokens per email | **1,252 tokens** | System prompt (~1,150 tokens) + email content (~100 tokens) |
| Average output tokens per email | **94 tokens** | JSON object + draft reply; spam emails produce only ~38 tokens |
| Per-email API cost | **$0.001722** | (1,252 × $1/M) + (94 × $5/M) |

### Monthly Cost at Various Volumes

| Monthly email volume | Monthly API cost |
|---|---|
| 200 emails/month | **$0.34** |
| **500 emails/month (planning baseline)** | **$0.86** |
| 1,000 emails/month | $1.72 |
| 2,900 emails/month ($5 ceiling) | $4.99 |

**Monthly cost math at 500 emails:**
- Input: 500 × 1,252 tokens = 626,000 tokens → $0.626
- Output: 500 × 94 tokens = 47,000 tokens → $0.235
- **Total: $0.861/month**

---

### Budget Recommendation for Diane

I'd recommend presenting Diane with a ceiling of **$5/month**, which covers up to approximately 2,900 emails per month — roughly 6× our current estimated volume. The cost scales linearly; there is no pricing cliff.

**ROI framing:** At under $1/month in operational cost, this system eliminates manual triage time on every incoming email and eliminates the risk class we're currently in — where a pallet offer worth $40k can sit unseen for three days. The API cost is immaterial relative to a single volunteer hour, let alone a missed donation.

---

### Note on Prior Estimate

A pre-run estimate of $0.73/month was calculated using assumed token counts (700 input / 150 output). The measured values differ:

| | Pre-run estimate | Measured actuals | Delta |
|---|---|---|---|
| Input tokens/email | 700 | 1,252 | +79% |
| Output tokens/email | 150 | 94 | −37% |
| Monthly cost at 500 emails | $0.73 | $0.86 | +18% |

The gap is explained by the system prompt being longer than assumed (the triage prompt includes two taxonomy tables, urgency rules, draft rules, and two few-shot examples — approximately 1,150 tokens vs the assumed 600). The higher input cost is partially offset by the compact JSON output being shorter than assumed. The net real cost is 18% above the initial estimate — still well under $1/month and well within any reasonable budget threshold.

The 500 emails/month volume assumption remains the variable with the most uncertainty. If you have actual 30-day inbox counts, substituting the real number will sharpen this further.

---

*Methodology: Token counts measured from Anthropic API `usage.input_tokens` / `usage.output_tokens` fields during a live run of `run_triage.py` against `inbox_sample.csv` (40 emails). Pricing confirmed for `claude-haiku-4-5-20251001` at $1.00/M input, $5.00/M output as of September 2025.*
