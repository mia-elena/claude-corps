# Email 1: Inbox Triage Prompt Refactor

## Objective
Rewrite the email triage prompt for Riverbend Food Alliance's `donate@` inbox to eliminate operational errors, stop hallucinations, and streamline the volunteer workflow.

## Context
* **Current Issue:** High-value donation offers are getting lost. The current Claude Project prompt generates error-prone responses (e.g., promising unavailable inventory, sending inappropriate automated replies to corporate donors) and outputs unnecessary conversational prose.
* **Urgency:** Fix required for immediate presentation at tomorrow's board meeting under "operational risk."

## Required Deliverables
1. **`triage_prompt.md`**: The newly optimized prompt file.
2. **Evaluation Note**: A short document (max 1 page) detailing the evaluation strategy for the prompt.
3. **`corrections.csv`**: Re-triaged versions of the 6 failed examples from `failure_examples.md`. Populate the `correct_category`, `urgent` (yes/no), and `route_to` columns without altering the header or `email` columns.

## Prompt Requirements
* **Target Model:** Claude Haiku. (Optimize for cost and speed).
* **Output Format:** Strictly a JSON block. No conversational prose or introductory paragraphs.
* **JSON Schema:** 
  `{"category": "...", "urgent": true, "route_to": "...", "draft": "..."}`

## Allowed Taxonomies

**Categories (Exact match required):**
* `corporate_food_donation`
* `individual_food_donation`
* `partner_agency_request`
* `food_assistance_seeker`
* `volunteer_inquiry`
* `food_drive`
* `media_or_general_inquiry`
* `spam_no_reply`

**Routing Targets:**
* `marcus`
* `diane`
* `priya`
* `intake_line`
* `auto_ok` (Use when a draft is safe to send without manual review)
* `no_reply`

## Source Files (Attachments)
* `current_prompt.md`
* `failure_examples.md`
* `inbox_sample.csv`
* `corrections.csv`