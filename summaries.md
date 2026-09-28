# Riverbend Food Alliance — Task Summaries

---

**Email 1 — Inbox Triage Prompt Refactor**
The donate@ inbox was losing high-value food donation offers because the AI triage prompt was producing wrong outputs — vague replies, hallucinated attachments, and walls of prose instead of structured routing decisions. The task was to rewrite the prompt so it outputs clean JSON for every email, routes each message to the right person, and never promises something it can't deliver. The new prompt was tested live against 40 real inbox emails using Claude Haiku and iterated through four runs until all 40 passed with zero errors or hallucinations.

---

**Email 2 — Q1 Partner-Agency Allocation Memo**
The Executive Director drafted a board memo using AI and the numbers came out wrong. With a board meeting the next morning and a director specifically asking whether Ellis County is being underserved, the task was to pull the raw Q1 warehouse distribution logs and agency directory, fix the misspelled agency names in the data, recalculate every figure from scratch in lbs per family per month, and produce a corrected memo that is accurate enough to present to the board and honest about any data quality issues found along the way.

---

**Email 3 — Volunteer Confirmation Flow Architecture**
Every week, a staff member manually copies volunteer signups from a Google Sheet into Airtable and then hand-texts each confirmed volunteer the night before their shift. The task was to design an automated replacement — a single-page architecture diagram showing how the signup, roster, and SMS confirmation steps connect, where Claude and MCP fit in, and how the board gets a Monday morning report. The deliverable also included a draft reply to Priya with concrete time-saved numbers she could forward to Diane to get the project approved.

---

**Email 4 — Monthly API Cost Estimate**
Before the triage system from Email 1 can go live, Diane needs a dollar figure to approve. The task was to calculate the real monthly cost of running Claude Haiku on the donate@ inbox and draft a reply to Marcus with a number he can put in front of the Executive Director. Using measured token counts from the live test run in Email 1 — 1,252 input tokens and 94 output tokens per email on average — the actual cost works out to $0.86/month at 500 emails, under $1/month, with a recommended $5/month budget ceiling that covers roughly six times current volume.
