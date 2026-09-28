# Triage Prompt Evaluation Strategy
**Riverbend Food Alliance — donate@ Inbox | Version 1.0**

---

## Strategy Overview

Evaluate on two axes: **structural correctness** (does the output parse as valid JSON with all required fields?) and **semantic correctness** (are category, urgency, routing, and draft accurate?).

---

## Test Set

**Ground-truth labeled set (6 emails):** The `corrections.csv` file provides confirmed labels for the six failure cases from `failure_examples.md`. These serve as the regression baseline — any prompt change must pass all six.

**Expanded test set (41 emails):** The `inbox_sample.csv` provides a broader unlabeled set. Label these manually once (one-time ~1 hour effort) to create a full 47-email benchmark. This covers edge cases not in the six labeled examples: delivery issues, multi-ask emails, near-duplicate senders, short-dated high-volume corporate offers.

---

## Key Metrics

| Metric | Target |
|---|---|
| JSON parse success rate | 100% — any failure is a blocker |
| Category accuracy | ≥95% on labeled set |
| Urgency accuracy | ≥95% on labeled set |
| Routing accuracy | ≥95% on labeled set |
| Draft hallucination rate | 0% (no invented attachments, inventory, addresses, or named staff) |
| Draft language match | 100% (Spanish input → Spanish draft) |

---

## Red-Team Scenarios to Explicitly Test

1. **Email addressed directly to a staff member** (e.g., "Marcus —"): system must still route correctly; draft should not say "forwarding to Marcus."
2. **Multi-ask emails** (e.g., Jen Park's volunteer + food drive): primary category captured; both asks addressed in draft.
3. **Non-English emails**: Spanish, Portuguese — verify language match in draft.
4. **Spam with food-adjacent subject lines** (e.g., "40% OFF bread promo"): must not misclassify as `corporate_food_donation`.
5. **Short-dated corporate offers with tight deadlines**: verify `urgent: true` and `route_to: marcus`.
6. **Individual donation with unusual items** (e.g., toiletries, clothing): must not be `auto_ok`; needs human review.

---

## Maintenance

Run the full 47-email benchmark before any prompt revision is deployed. Log failures with the email ID, expected vs. actual field, and the triggering prompt change. Expand the test set whenever a new failure pattern reaches production.

**Owner:** Marcus (routing/category decisions), Priya (volunteer-related edge cases).
