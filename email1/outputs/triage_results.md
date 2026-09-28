# Triage Run Results

**Model:** `claude-haiku-4-5-20251001`  
**Date:** 2026-09-28  
**Emails processed:** 40  

## Run Health

| Check | Count |
|---|---|
| API errors | 0 |
| JSON parse errors | 0 |
| Taxonomy violations | 0 |
| Hallucinations detected | 0 |
| Label deviations vs expected | 0 |
| Clean passes | 40 / 40 |

---

## Full Results

| ID | Category | Urgent | Route | Flags |
|---|---|---|---|---|
| S13 | `individual_food_donation` | false | `auto_ok` | PASS |
| S27 | `volunteer_inquiry` | false | `priya` | PASS |
| S14 | `partner_agency_request` | false | `marcus` | PASS |
| S16 | `partner_agency_request` | false | `marcus` | PASS |
| S25 | `volunteer_inquiry` | false | `priya` | PASS |
| S08 | `individual_food_donation` | false | `marcus` | PASS |
| S09 | `individual_food_donation` | false | `auto_ok` | PASS |
| S24 | `volunteer_inquiry` | true | `priya` | PASS |
| S30 | `food_drive` | false | `priya` | PASS |
| S29 | `volunteer_inquiry` | true | `priya` | PASS |
| S28 | `volunteer_inquiry` | true | `priya` | PASS |
| S17 | `partner_agency_request` | false | `marcus` | PASS |
| S23 | `food_assistance_seeker` | true | `intake_line` | PASS |
| S21 | `food_assistance_seeker` | true | `intake_line` | PASS |
| S10 | `individual_food_donation` | false | `marcus` | PASS |
| S12 | `individual_food_donation` | false | `auto_ok` | PASS |
| S22 | `food_assistance_seeker` | true | `intake_line` | PASS |
| S18 | `partner_agency_request` | false | `marcus` | PASS |
| S05 | `corporate_food_donation` | true | `marcus` | PASS |
| S19 | `partner_agency_request` | false | `marcus` | PASS |
| S01 | `corporate_food_donation` | true | `marcus` | PASS |
| S33 | `media_or_general_inquiry` | false | `marcus` | PASS |
| S02 | `corporate_food_donation` | true | `marcus` | PASS |
| S20 | `food_assistance_seeker` | true | `intake_line` | PASS |
| S11 | `individual_food_donation` | false | `marcus` | PASS |
| S32 | `food_drive` | false | `priya` | PASS |
| S06 | `individual_food_donation` | false | `marcus` | PASS |
| S15 | `partner_agency_request` | false | `marcus` | PASS |
| S34 | `media_or_general_inquiry` | false | `marcus` | PASS |
| S03 | `corporate_food_donation` | true | `marcus` | PASS |
| S35 | `media_or_general_inquiry` | false | `marcus` | PASS |
| S04 | `corporate_food_donation` | true | `marcus` | PASS |
| S40 | `spam_no_reply` | false | `no_reply` | PASS |
| S31 | `food_drive` | false | `priya` | PASS |
| S07 | `individual_food_donation` | false | `marcus` | PASS |
| S37 | `spam_no_reply` | false | `no_reply` | PASS |
| S38 | `spam_no_reply` | false | `no_reply` | PASS |
| S39 | `spam_no_reply` | false | `no_reply` | PASS |
| S26 | `volunteer_inquiry` | false | `priya` | PASS |
| S36 | `spam_no_reply` | false | `no_reply` | PASS |

---

## Deviations Detail

No deviations — all labeled emails match expected outputs.

---

## Hallucinations Detected

None detected.

---

## Token & Cost Summary

| Metric | Value |
|---|---|
| Model | `claude-haiku-4-5-20251001` |
| Emails processed | 40 |
| Total input tokens | 50,103 |
| Total output tokens | 3,754 |
| Avg input tokens / email | 1,252 |
| Avg output tokens / email | 93 |
| Input cost (\$1.00 / M) | \$0.05010 |
| Output cost (\$5.00 / M) | \$0.01877 |
| **Total run cost** | **\$0.06887** |

> Pricing: Claude Haiku 4.5 — \$1.00/M input, \$5.00/M output.
> Monthly cost extrapolation: multiply per-email cost by estimated monthly volume.