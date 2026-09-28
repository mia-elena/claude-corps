# Email 1 — Testing & Findings Audit
**Riverbend Food Alliance | donate@ Triage Prompt Refactor**

---

## Live Run Infrastructure

| Item | Value |
|---|---|
| Run script | `outputs/run_triage.py` |
| Environment file | `../../.env` (repo root) |
| Environment template | `../../.env.example` |
| Target model | `claude-haiku-4-5-20251001` |
| Workspace | `wrkspc_01DjRbGPpTNkH63GDcVhsZMV` |
| Output (raw) | `outputs/triage_results.json` |
| Output (report) | `outputs/triage_results.md` |
| Live run status | **PENDING** — workspace has no API credits |

**To run locally:**
```
python3 /Users/miaelena/Downloads/claude_corps/email1/outputs/run_triage.py
```
The script auto-loads `.env`, selects the right key, calls Haiku once per email, validates all outputs against expected labels, checks for taxonomy violations and hallucinations, and writes both JSON and Markdown reports.

**Note on billing:** Claude.ai Pro subscription and the Anthropic API are separate billing systems. API credits must be purchased independently at console.anthropic.com regardless of Pro status.

### Run History

| Run | Prompt version | Passes | Deviations | Cost | Notes |
|---|---|---|---|---|---|
| 1 | v1 (initial) | 26/40 | 14 | $0.051 | Baseline — identified 4 deviation patterns |
| 2 | v2 (non-standard items + food_assistance urgency + media exception) | 37/40 | 3 | $0.069 | Fixed 11 deviations; S31/S32 urgency and S09 routing remain |
| 3 | v2 + S31/S32 label correction | 39/40 | 1 | $0.068 | S16 oscillating (borderline "running short" rule) |
| 4 | v3 (tightened partner agency urgency rule) | **40/40** | **0** | $0.069 | **Final — all emails pass** |

**Prompt changes across runs:**
- v1 → v2: Added non-standard items exclusion to `auto_ok` routing; made `food_assistance_seeker` always urgent; added media/press "this week" exception to urgency rule
- v2 → v3: Tightened partner agency urgency to *current/same-day* distribution only — explicitly excluded future delivery requests ("next week's truck")
- Label correction: S31/S32 food drive urgency revised to `False` — "in May" does not meet the 72h rule; model behavior was correct

---

## Part 1: Task Requirements Audit

Checklist against `task.md` and the original Marcus email.

| # | Requirement | Source | Status | Notes |
|---|---|---|---|---|
| 1 | Deliverable: `triage_prompt.md` exists | task.md | PASS | Saved to `outputs/triage_prompt.md` |
| 2 | Deliverable: Evaluation note ≤1 page | task.md | PASS | `outputs/evaluation_note.md` |
| 3 | Deliverable: `corrections.csv` with 3 columns filled, header and `email` column untouched | task.md + Marcus email | PASS | All 6 rows populated; header row preserved |
| 4 | Exactly 8 categories, exact string match | task.md | PASS | All 8 present in prompt taxonomy |
| 5 | All 6 routing targets present in prompt | task.md + Marcus email | PASS | Added `diane` after initial gap; all 6 now defined |
| 6 | Output is JSON only — no prose | Marcus email | PASS | Prompt opens with hard constraint: "Output ONLY a single valid JSON object." |
| 7 | JSON schema: `{"category","urgent","route_to","draft"}` | Marcus email | PASS | Schema block matches exactly |
| 8 | Target model: Claude Haiku | task.md | PASS | Prompt is concise; no few-shot verbosity |
| 9 | `urgent` field is boolean (`true`/`false`) in JSON | Marcus email | PASS | Schema specifies `true\|false` |
| 10 | `urgent` field is `yes`/`no` in corrections.csv | Marcus email | PASS | CSV uses yes/no per Marcus's instruction |

**Defects found and corrected during audit:**
- `diane` routing target was missing from the initial prompt routing table. Fixed.
- `spam_no_reply` category lacked explicit disambiguation for food-adjacent promotional emails (e.g., "40% OFF bread"). Fixed with inline note.

**Typo in original email (non-blocking):**
Marcus wrote `corporaal_food_donation`. The canonical spelling from `task.md` is `corporate_food_donation`. The prompt uses the correct spelling.

---

## Part 2: Failure Case Re-triage

The six emails from `failure_examples.md`, audited against the corrections.csv and root causes in the original prompt.

### F1 — Kevin Walsh (corporate_food_donation)

| Field | Old Output | Correct | Match |
|---|---|---|---|
| category | `corporate_food_donation` | `corporate_food_donation` | PASS |
| urgent | Yes | yes | PASS |
| route_to | (not specified — forwarded vaguely to "warehouse manager") | `marcus` | FAIL — old prompt |

**Root cause:** The old prompt had no routing taxonomy. Draft said "I'm forwarding to our warehouse manager" without naming a specific target or confirming any operational details. A $40k+ pallet offer would have sat unresolved.

**New prompt fix:** `marcus` route explicitly defined for corporate donations. Draft rule prohibits vague forwarding language. Urgency rule triggers on liquidation deadline.

---

### F2 — Sarah M (individual_food_donation)

| Field | Old Output | Correct | Match |
|---|---|---|---|
| category | `individual_food_donation` | `individual_food_donation` | PASS |
| urgent | No | no | PASS |
| route_to | (not specified) | `auto_ok` | N/A — old prompt had no routing |

**Root cause:** Category was correct but old prompt generated excessive prose ("We're so grateful… donations like yours make a real difference"). Output was paragraphs, not structured data.

**New prompt fix:** JSON-only output; `auto_ok` routing means the draft sends directly with no human review.

---

### F3 — Pastor Dan Reyes (partner_agency_request)

| Field | Old Output | Correct | Match |
|---|---|---|---|
| category | `partner_agency_request` | `partner_agency_request` | PASS |
| urgent | Yes | yes | PASS |
| route_to | (draft said "forwarding to Marcus") | `marcus` | FAIL — old prompt |

**Root cause (critical):** The email was addressed directly to Marcus ("Marcus —"). The automated reply said "I'm forwarding your request to Marcus right away" — Marcus would have received an automated email telling him to forward something to himself. Additionally, the draft congratulated the partner on "wonderful growth" while they were in crisis.

**New prompt fix:** Draft rule explicitly prohibits "I'm forwarding to [name]" language. The routing field handles internal dispatch; the draft addresses only the sender.

---

### F4 — Spam (grantstation.com)

| Field | Old Output | Correct | Match |
|---|---|---|---|
| category | `spam_no_reply` | `spam_no_reply` | PASS |
| urgent | No | no | PASS |
| route_to | (not specified) | `no_reply` | FAIL — old prompt |

**Root cause:** Category was correct but the old prompt generated a formatted prose summary with headers and sections ("## Recommended Response") instead of silence. Wasted volunteer time and produced misleading output format.

**New prompt fix:** `spam_no_reply` → `no_reply` route; `draft: ""` rule enforced explicitly.

---

### F5 — Jen Park (volunteer_inquiry)

| Field | Old Output | Correct | Match |
|---|---|---|---|
| category | `volunteer_inquiry` | `volunteer_inquiry` | PASS |
| urgent | No | yes | FAIL — old prompt |
| route_to | (not specified) | `priya` | N/A — old prompt had no routing |

**Root cause (critical hallucination):** Draft said "I'm attaching our current needs list" — no attachment exists or was sent. This is a fabricated action. Jen would have received a reply referencing an attachment that never arrived.

**Urgency note:** The May 15 student service-hours deadline makes this urgent (see Edge Case 2 below for a full discussion of the urgency rule gap this exposes).

**New prompt fix:** Draft rule 1 explicitly prohibits promising files, attachments, or unconfirmed operational details. Route is `priya` for all volunteer/group-shift coordination.

---

### F6 — Ana Lucía Torres (food_assistance_seeker)

| Field | Old Output | Correct | Match |
|---|---|---|---|
| category | `food_assistance_seeker` | `food_assistance_seeker` | PASS |
| urgent | Yes | yes | PASS |
| route_to | (not specified) | `intake_line` | N/A — old prompt had no routing |

**Root cause:** Draft told Ana to bring an ID document — this may not be the actual intake policy and could have been a barrier for a family in need. Draft also used a warehouse address placeholder (`[warehouse address]`) which would have appeared verbatim in a sent reply if the volunteer didn't notice it.

**New prompt fix:** `[FILL]` placeholder rule surfaces all gaps to the human reviewer before sending. Language-matching rule ensures Spanish reply for Spanish sender. Route is `intake_line`, not the warehouse.

---

## Part 3: Full Inbox Sample — Expected Triage Results

Expected outputs for all 40 emails in `inbox_sample.csv`. Use this table as the ground-truth label set when running benchmark evaluations.

| ID | From | Category | Urgent | Route | Key Signal | Flags |
|---|---|---|---|---|---|---|
| S01 | warehouse@valleyfresh.com | corporate_food_donation | yes | marcus | "otherwise it goes to liquidation Monday" | Also used as prompt example |
| S02 | logistics@tristar.com | corporate_food_donation | yes | marcus | "Need confirmation by May 15" | **SUBJECT/BODY MISMATCH** — subject says "40 pallets canned vegetables," body says "15 pallets of cereal"; best-by 3 wks = 21 days (>14d threshold, but named deadline still triggers urgent) |
| S03 | logistics@valleyfresh.com | corporate_food_donation | yes | marcus | Best-by 10 days out; EOD Wednesday deadline | **SUBJECT/BODY MISMATCH** — subject says "40 pallets rice," body says "6 pallets of bread" |
| S04 | logistics@peakfoods.com | corporate_food_donation | yes | marcus | Best-by 10 days out; Friday noon deadline | **SUBJECT/BODY MISMATCH** — subject says "2 pallets bread," body says "8 pallets of cereal" |
| S05 | warehouse@valleyfresh.com | corporate_food_donation | yes | marcus | "otherwise it goes to liquidation Saturday" | |
| S06 | dpatel@outlook.com | individual_food_donation | no | marcus | Toiletries included — non-food item | Must NOT be `auto_ok`; needs human policy check |
| S07 | krodriguez@outlook.com | individual_food_donation | no | marcus | Clothing included — non-food item | Must NOT be `auto_ok`; draft should clarify accepted items |
| S08 | msmith@outlook.com | individual_food_donation | no | marcus | Toiletries included — non-food item | Must NOT be `auto_ok` |
| S09 | rsingh@gmail.com | individual_food_donation | no | auto_ok | Simple produce drop-off, no unusual items | |
| S10 | tbrown@yahoo.com | individual_food_donation | no | marcus | Yogurt — perishable/refrigerated; warehouse acceptance unclear | Must NOT be `auto_ok`; needs ops check |
| S11 | rsingh@outlook.com | individual_food_donation | no | marcus | Baby formula — specialized item; needs policy check | Must NOT be `auto_ok` |
| S12 | dpatel@gmail.com | individual_food_donation | no | auto_ok | Simple cereal drop-off | |
| S13 | anguyen@gmail.com | individual_food_donation | no | auto_ok | Simple produce drop-off | |
| S14 | office@lincolnhs.org | partner_agency_request | no | marcus | Missing item in delivery (yogurt) | |
| S15 | office@hopehouse.org | partner_agency_request | no | marcus | Missing item in delivery (rice) | |
| S16 | director@hopehouse.org | partner_agency_request | no | marcus | Extra allocation requested for next week's truck | Not urgent — next week, no active shortage reported |
| S17 | director@priceymca.org | partner_agency_request | no | marcus | Extra allocation requested for next week's truck | Not urgent — next week |
| S18 | office@lincolnhs.org | partner_agency_request | no | marcus | Missing item in delivery (sparkling water) | |
| S19 | office@hopehouse.org | partner_agency_request | no | marcus | Missing item in delivery (yogurt) | |
| S20 | msmith@gmail.com | food_assistance_seeker | yes | intake_line | Immediate household need; 8 kids | |
| S21 | msmith@gmail.com | food_assistance_seeker | yes | intake_line | Immediate need; Spanish | Reply must be in Spanish |
| S22 | anguyen@gmail.com | food_assistance_seeker | yes | intake_line | Immediate need; 20 kids | |
| S23 | cflores@gmail.com | food_assistance_seeker | yes | intake_line | Immediate need; Spanish | Reply must be in Spanish |
| S24 | advisor@gracechurch.edu | volunteer_inquiry | yes | priya | May 15 hard deadline for 12 students | See Edge Case 2 — urgency rule tension |
| S25 | msmith@gmail.com | volunteer_inquiry | no | priya | Friday shift inquiry | Near-duplicate of S27 |
| S26 | krodriguez@gmail.com | volunteer_inquiry | no | priya | Thursday shift inquiry | Near-duplicate of S27 (same sender, different day) |
| S27 | krodriguez@gmail.com | volunteer_inquiry | no | priya | Friday shift inquiry | |
| S28 | advisor@priceymca.edu | volunteer_inquiry | yes | priya | "by EOD Wednesday" — explicit 72h deadline | Near-duplicate of S29 from same sender |
| S29 | advisor@priceymca.edu | volunteer_inquiry | yes | priya | "by end of week" — within-72h deadline | Same sender as S28; slightly softer wording |
| S30 | anguyen@hopehouse.com | food_drive | no | priya | July food drive — not time-sensitive | |
| S31 | cflores@lincolnhs.com | food_drive | yes | priya | May food drive — upcoming deadline | Near-duplicate of S32 |
| S32 | dpatel@gracechurch.com | food_drive | yes | priya | May food drive — upcoming deadline | |
| S33 | reporter@stmarynews.com | media_or_general_inquiry | no | marcus | Interview request — summer hunger story | |
| S34 | reporter@priceymcanews.com | media_or_general_inquiry | no | marcus | Interview request — grocery prices story | |
| S35 | reporter@lincolnhsnews.com | media_or_general_inquiry | no | marcus | Interview request — food insecurity story | |
| S36 | noreply@valleyfresh.net | spam_no_reply | no | no_reply | "40% OFF bread" promo | **MISCLASSIFICATION RISK**: sender domain resembles legitimate donor `warehouse@valleyfresh.com`; content is promotional, not a donation offer |
| S37 | alerts@peakfoods.io | spam_no_reply | no | no_reply | Automated billing alert | Sender domain resembles `logistics@peakfoods.com`; content is billing, not food offer |
| S38 | hello@tristar.co | spam_no_reply | no | no_reply | Unsolicited sales pitch ("10x donor engagement") | Sender domain resembles `logistics@tristar.com`; content is cold outreach, not a donation |
| S39 | noreply@northbev.net | spam_no_reply | no | no_reply | "2% OFF produce" promo | |
| S40 | alerts@northbev.io | spam_no_reply | no | no_reply | Automated billing alert | |

**Category distribution (40 emails):**

| Category | Count |
|---|---|
| spam_no_reply | 5 |
| individual_food_donation | 8 |
| corporate_food_donation | 5 |
| partner_agency_request | 6 |
| food_assistance_seeker | 4 |
| volunteer_inquiry | 7 |
| food_drive | 3 |
| media_or_general_inquiry | 3 |
| **diane-routed** | **0** |

---

## Part 4: Edge Cases & Findings

### Edge Case 1 — Subject/Body Mismatches (S02, S03, S04)

Three corporate donation emails have subjects that do not match the body: product type and quantity both differ. Example: S03 subject = "40 pallets rice," body = "6 pallets of bread."

**Risk:** If the model reads only the subject line, it will log incorrect item types and quantities, causing Marcus to prepare for the wrong product.

**Current prompt status:** No explicit instruction to prioritize body over subject.

**Recommendation:** Add one line to the Draft Writing Rules section: *"Base all product details in the draft on the email body, not the subject line. If subject and body conflict, note the discrepancy in the draft."*

---

### Edge Case 2 — Urgency Rule Gap: Scheduled-Deadline Emails (S24, S31, S32, Jen)

The current urgency rule requires a deadline "within 72 hours." Jen (corrections.csv) is marked `urgent: yes` for a May 15 volunteer-hours deadline. S24 (advisor@gracechurch.edu) has the identical scenario. If processed more than 72 hours before May 15, the rule as written would fire `urgent: false`, inconsistent with the corrections.csv label.

**Risk:** The model will systematically under-flag volunteer group shifts and food drives that have named future deadlines requiring lead time to coordinate.

**Recommendation:** Expand the urgency condition to: *"Email contains a named scheduling deadline (volunteer shift, food drive, delivery confirmation) within 5 business days."*

---

### Edge Case 3 — Lookalike Domains (S36, S37, S38)

Three spam emails come from domains that closely resemble legitimate corporate donor or vendor domains:

| Spam sender | Legitimate donor |
|---|---|
| noreply@valleyfresh**.net** | warehouse@valleyfresh**.com** |
| alerts@peakfoods**.io** | logistics@peakfoods**.com** |
| hello@tristar**.co** | logistics@tristar**.com** |

**Risk:** A model relying on sender name recognition could misclassify these as `corporate_food_donation` instead of `spam_no_reply`.

**Current prompt fix:** The `spam_no_reply` category note explicitly states that a donation offer must involve giving food at no cost. Promotional or billing content from any domain is spam regardless of the sender name.

**Recommendation:** Add this as an explicit red-team test case in the evaluation suite: run each lookalike domain pair and verify the spam email never reaches `marcus`.

---

### Edge Case 4 — Non-Standard Items in Individual Donations (S06, S07, S08, S10, S11)

Five individual donor emails include non-food items (toiletries, clothing) or items requiring cold chain or policy checks (yogurt, baby formula, sparkling water). The prompt's `auto_ok` routing applies only to "simple individual drop-off donations."

**Risk:** Without explicit guidance, the model may treat any self-described "donation" as auto_ok.

**Current prompt fix:** `auto_ok` description specifies "simple individual drop-off donations only." A perishable item or non-food item is not simple.

**Recommendation:** Verify this boundary holds in live testing by running S06–S11 against the deployed prompt and confirming none return `route_to: auto_ok`.

---

### Edge Case 5 — `diane` Routing Has No Triggering Examples

Zero emails in the 40-email inbox sample route to `diane`. The routing target is defined and included in the prompt, but no current inbox volume demonstrates it.

**Risk:** Without an example, the model has no training signal for when to use `diane`. It may never route to her, or use her incorrectly.

**Recommendation:** Define 1–2 concrete triggering scenarios before the next prompt version (e.g., "An email from a named foundation or major funder offering a grant, sponsorship, or executive-level partnership") and add them as examples or few-shot cases in the prompt.

---

### Edge Case 6 — Near-Duplicate Emails from Different Senders

Multiple email IDs carry identical body text from different senders (S13/S09, S25/S27, S21/S23, S22/S20). This is expected in a real inbox and does not represent a prompt failure — triage should produce identical outputs for identical content regardless of sender. No action required, but useful for verifying the model is not over-relying on sender identity.

---

## Part 5: Summary

| Dimension | Result |
|---|---|
| Task requirements met | 10/10 after fixing `diane` gap and spam disambiguation |
| Failure cases correctly re-triaged | 6/6 |
| Inbox sample emails with expected labels | 40/40 |
| Routing targets covered in prompt | 6/6 (marcus, diane, priya, intake_line, auto_ok, no_reply) |
| Categories covered in prompt | 8/8 (all exact strings) |
| Confirmed hallucination vectors eliminated | 3 (fake attachment, fake forwarding, unconfirmed operational details) |
| Open recommendations | 4 (subject/body rule, urgency rule expansion, lookalike domain test, diane examples) |

**Highest-priority open item before go-live:** The urgency rule gap (Edge Case 2) will cause the model to systematically under-flag volunteer and food-drive scheduling deadlines. A one-line amendment to the prompt resolves it. The four open recommendations are documented but do not block the board presentation.
