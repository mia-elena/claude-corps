# Email 3 — Summary Report

**Task:** Architecture for Volunteer Confirmation Flow  
**Date:** 2026-09-28  
**Outputs produced:** `architecture.html`, `email_reply.md`, `index.html`, `tests.md`

---

## Part 1: Process — How the Task Was Completed

### Step 1 — Ingest source files

Two source files were provided: `handbook.md` and `index.html` (Priya's original prototype). Both were read in full before any output was drafted.

`handbook.md` was the primary operational reference. Key facts extracted:

- Priya's current volunteer workflow: Google Form → Google Sheet → manual Airtable entry → hand-texting every confirmed volunteer the night before their shift. Total time estimated in the handbook at approximately six hours per week, split across Mondays and Thursdays.
- No automated reminder system exists. No-show rate is anecdotally 30–40% and is not formally tracked.
- Independent Sector volunteer valuation rate: approximately $33/hr. This is the rate the organization reports to funders, making it the appropriate internal measure for valuing volunteer time.
- Tools currently in use: Google Workspace (Forms, Sheets, Apps Script), Airtable, Slack, and a Claude Team plan. All are existing tools with no marginal cost.
- Minimum age rules: mobile pantry routes are 18+ only due to an insurance constraint. Warehouse sort is 14+ with parental consent, 16+ unaccompanied. These constraints are binding and needed to appear in any redesigned signup form.
- Bilingual requirement: the handbook states explicitly that any wide-audience material — which a public-facing signup form qualifies as — must work in both English and Spanish. Ellis County's Spanish-speaking population is the fastest-growing segment served.
- Approval boundaries: any new SaaS vendor requires executive (Diane) clearance. Corporate and pallet-scale decisions route through Marcus. Airtable API credentials are held by Marcus.
- The cancellation banner for volunteer weather cancellations has been on Priya's wishlist for over a year and has never been built.

`index.html` (original prototype) was read to understand what already existed before drafting the updated version. Key observations:

- Five shifts hardcoded: Tuesday 9am–12pm, Tuesday 1pm–4pm, Thursday 9am–12pm, Saturday 8am–11am (mobile pantry Ellis), Saturday 9am–1pm (drop-off). Total capacity: 38 spots across the week.
- The signup modal collected name, email, and phone, but contained a developer comment: `// TODO: this doesn't actually save anywhere yet!` The form was entirely client-side with no persistence.
- No age verification existed for the mobile pantry shift despite the 18+ insurance constraint.
- No liability waiver acknowledgment was present, despite the handbook noting all volunteers must sign one on their first shift.
- No field validation beyond a name-blank check.

### Step 2 — Identify the deliverables and constraints

From `task.md`, the required outputs were:

1. An architecture diagram showing: signup entry point, roster location, SMS mechanism, Claude and MCP position in the pipeline, and a Monday morning reporting mechanism.
2. An email reply to Priya with concrete ROI metrics — specifically framed so she can forward it directly to Diane.
3. Optionally, an improved version of the signup page prototype.

The hard constraints were:
- Volunteer roster must live in Airtable (Name, Phone, Routes).
- Must use existing Google Workspace and Slack.
- Volunteer confirmations must use SMS, not email.
- No new SaaS spend without Diane's approval.

### Step 3 — Plan the architecture

The architecture was designed in four layers, chosen to map cleanly onto the existing tool stack and introduce the minimum number of new dependencies.

**Layer 1 — Intake (all existing tools)**  
The existing Google Form → Sheet flow was kept as the intake surface. This avoids any change to the experience for volunteers signing up and requires no new infrastructure. A Google Apps Script `onFormSubmit` trigger was chosen to sync new rows to Airtable automatically, replacing Priya's manual entry step entirely. Apps Script is part of Google Workspace, so it costs nothing additional.

**Layer 2 — Roster (Airtable)**  
Airtable was designated the single source of truth as required by the task. The Sheet becomes a transient staging layer only. Fields mapped to the task requirement: Name, Phone, Route, Shift, Status.

**Layer 3 — Claude and MCP automation**  
Four discrete Claude-driven bots were defined, each triggered by a different event:

- Confirmation Bot: fires when Airtable receives a new record. Reads the volunteer's details via Airtable MCP and sends an immediate confirmation SMS via Twilio MCP.
- Reminder Bot: fires on a schedule (the evening before each shift day). Queries Airtable for the next day's confirmed roster and sends personalized day-before reminders via Twilio.
- Cancellation Handler: fires when a volunteer replies CANCEL to an SMS. Twilio delivers the inbound message to a webhook. Claude updates the volunteer's Airtable status to Cancelled and posts an alert to Slack.
- Report Bot: fires every Monday at 8am. Pulls the previous week's data from Airtable, generates a summary, and posts it to the #volunteers Slack channel.

Claude's role in this pipeline is text generation and routing, not data storage. It personalizes message content (correct shift time, location, cancellation instruction) and decides what to surface to Slack. All actual data read/write operations go through MCP connectors.

Twilio was chosen as the SMS provider because it is the industry standard for programmatic SMS, has a Twilio MCP server available, and costs approximately $0.0075 per message — under $20 per year at current volume. It is the only net-new vendor in the entire architecture. The decision to flag it explicitly for Diane's sign-off came directly from the handbook's instruction that any new SaaS requires executive clearance.

**Layer 4 — Reporting (Slack)**  
The Monday morning report was wired to Slack because Slack is already in use and the board can read it there without any additional tooling. Diane and Priya both have access.

### Step 4 — Draft the email reply

The task asked for "a number or two" estimating time or cost saved. Rather than a single figure, the reply was structured around two distinct value categories — direct staff time and recovered volunteer capacity — because these map to different budget arguments Diane would care about:

- Staff time savings is an operating cost argument (Priya's hours have real value at the rate reported to funders).
- Volunteer capacity recovery is a mission-impact argument (more volunteers showing up means more food distributed).

Both figures were derived from handbook data and the shift capacity data in the prototype. The calculations are detailed in Part 2 below.

The total ROI claim was kept conservative by using the low end of the no-show reduction range and slightly understating the recovered capacity figure.

### Step 5 — Update the prototype

The original prototype was improved by addressing the most operationally significant gaps identified during source file review:

- Added the 18+ age gate for the mobile pantry shift (Shift 4), visible both as a badge on the shift card and as a required acknowledgment checkbox inside the modal.
- Added a liability waiver acknowledgment checkbox for all shifts, matching the handbook requirement.
- Added phone number and email validation.
- Replaced the `alert()` confirmation with an inline confirmation screen that shows the volunteer their shift details and instructs them to reply CANCEL if plans change — setting the expectation for the SMS workflow.
- Moved modal content injection into a stable `modal-body` div rather than replacing parent-level innerHTML, which was a latent bug in the original approach.
- Kept the prototype disclaimer visible so no one mistakes the form for a live system.

### Step 6 — Write the tests file

After all outputs were written, each deliverable was audited against the task requirements, the handbook constraints, and the original prototype. The tests file recorded: a requirements checklist, a constraint compliance table, a line-by-line ROI verification, technical findings per file, and a prioritized gap list.

---

## Part 2: Calculations — How Every Number Was Derived

### Calculation 1 — Direct staff time savings ($8,600/year)

**Source data:**
- Handbook: "Between the form, the sheet, and the texts it's most of her Mondays and a chunk of Thursday — call it six hours a week."
- Handbook: "We report volunteer hours to funders at the Independent Sector rate (~$33/hr)."

**Assumption:**
After automation, Priya retains approximately one hour per week to review the Monday morning Slack report and handle any exceptions. This is an editorial estimate — the handbook does not specify a residual time figure.

**Calculation:**
```
Hours saved per week  = 6 hrs - 1 hr = 5 hrs
Weekly staff savings  = 5 hrs × $33/hr = $165/week
Annual staff savings  = $165 × 52 weeks = $8,580/year ≈ $8,600/year
```

**Confidence: HIGH.** Both inputs (6 hrs/week, $33/hr) are direct quotes from the handbook. The only assumption is the 1-hour residual, which is conservative (if anything it overstates the retained time).

---

### Calculation 2 — Recovered volunteer capacity ($26,000/year)

This calculation has more layers and two assumptions that are not sourced from the handbook.

**Source data:**
- Handbook: "No-show rate is anecdotally 30–40%; we don't track it formally."
- index.html prototype shift data: 5 shifts with capacities of 8, 6, 8, 12, and 4 spots.

**Step 1 — Establish baseline no-show rate**

The handbook gives a range of 30–40%. The midpoint, 35%, was used as the baseline. Because no formal tracking exists, this figure has inherent uncertainty.

```
Baseline no-show rate = (30% + 40%) / 2 = 35%
```

**Step 2 — Establish total weekly shift capacity**

The shift data in the prototype was treated as representative of a typical week:

```
Shift 1 (Tue 9am)  =  8 spots
Shift 2 (Tue 1pm)  =  6 spots
Shift 3 (Thu 9am)  =  8 spots
Shift 4 (Sat 8am)  = 12 spots
Shift 5 (Sat 9am)  =  4 spots
                     --------
Total capacity     = 38 spots/week
```

Note: the prototype may not reflect the full operation. If the actual weekly capacity is larger, the recovered-capacity figure scales proportionally.

**Step 3 — Calculate weekly no-shows before automation**

```
No-shows per week (before) = 38 spots × 35% = 13.3 volunteer-slots lost/week
```

**Step 4 — Apply SMS reminder reduction rate**

This is the first external assumption. Automated SMS day-before reminders reducing no-show rates by 40–50% is an industry benchmark for volunteer and appointment-based programs. This figure is not sourced from the handbook — it is general industry knowledge. The conservative end of the range (40%) was applied.

```
No-show reduction = 40%
No-shows prevented per week = 13.3 × 40% = 5.3 additional volunteer-appearances/week
```

**Step 5 — Value each recovered volunteer-slot**

This is the second external assumption. The handbook gives the Independent Sector rate of $33/hr for volunteer time but does not specify average shift length. A three-hour average shift was assumed, which is consistent with the shift durations shown in the prototype (3-hour morning warehouse sorts; 3-hour drop-off shift; 3-hour mobile pantry shift).

```
Value per recovered slot = 3 hrs × $33/hr = $99
```

**Step 6 — Annual recovered capacity value**

```
Weekly recovered value  = 5.3 slots × $99/slot = $524.70/week
Annual recovered value  = $524.70 × 52 weeks = $27,284/year ≈ $26,000–$27,000/year
```

The email states "about $26,000/year" — this is a slight underestimate of the derived figure. The conservative round-down was intentional to avoid overpromising.

**Confidence: MEDIUM.** The 40–50% no-show reduction benchmark and the 3-hour average shift length are assumptions, not Riverbend-specific data. Both are reasonable but should be labeled as estimates in any formal proposal.

---

### Calculation 3 — Twilio SMS cost (under $20/year)

**Source data:**
- Twilio standard rate for US SMS: approximately $0.0075 per message (outbound). This is a publicly available rate from Twilio's pricing page, not from the handbook.
- Shift capacity data: 38 total spots per week.

**Step 1 — Estimate weekly message volume**

Two SMS events occur per confirmed volunteer: one immediate confirmation (on signup) and one day-before reminder.

```
Estimated fill rate    ≈ 60% (Shifts 1–5 at various stages of capacity)
Signups per week       = 38 × 60% ≈ 23
Confirmations sent     = 23
Reminder texts sent    = 23
Total messages/week    ≈ 46, rounded to ~50 to account for cancellations/re-signups
```

**Step 2 — Annual cost**

```
Annual messages = 50/week × 52 weeks = 2,600 messages/year
Annual cost     = 2,600 × $0.0075   = $19.50/year
```

Stated in the email as "under $20/year." Correct.

**Confidence: HIGH for the math; MEDIUM for the 60% fill rate assumption.** If fill rates are higher, message volume increases but cost remains negligible (at 100% fill: 38 × 2 × 52 × $0.0075 = $29.64/year — still under $30/year).

---

### Calculation 4 — Total ROI (~$34,000/year)

```
Staff time savings         = $8,580/year
Recovered volunteer value  = $27,284/year  (derived; email uses $26,000)
                             ----------
Total                      = $35,864/year  (email states "~$34,000")
```

The email understates the total by approximately $1,900, consistent with the conservative rounding applied throughout. The claim of "~$34,000" is defensible and not misleading.

---

## Part 3: Assumptions Register

All assumptions used in the outputs, consolidated for transparency.

| # | Assumption | Used In | Sourced From | Confidence |
|---|---|---|---|---|
| 1 | Priya retains ~1 hr/week post-automation (for report review) | ROI time savings | Editorial estimate | Medium |
| 2 | Baseline no-show rate = 35% (midpoint of 30–40%) | No-show reduction | handbook.md (anecdotal range) | Medium |
| 3 | Automated SMS reminders reduce no-shows by 40–50% | No-show reduction | Industry benchmark, not Riverbend data | Medium |
| 4 | Conservative 40% reduction applied (low end of range) | No-show reduction | Editorial choice | High (conservative) |
| 5 | Average shift length = 3 hours | Volunteer slot valuation | Derived from prototype shift durations | Medium |
| 6 | index.html shift data (38 spots) is representative of a typical week | No-show reduction, Twilio cost | index.html prototype | Medium |
| 7 | ~60% average fill rate across all shifts | Twilio cost estimate | Derived from prototype taken/need ratios | Medium |
| 8 | Twilio rate = $0.0075/message | Twilio cost estimate | External (Twilio pricing) | High |
| 9 | Claude API usage is covered under existing Claude Team plan | Cost model | handbook.md (Claude Team plan listed as existing) | High |

---

## Part 4: Files Produced

| File | Description |
|---|---|
| `architecture.html` | Single-page Mermaid architecture diagram showing the automated volunteer confirmation flow, MCP server table, and design notes |
| `email_reply.md` | Drafted reply to Priya with ROI framing for forwarding to Diane; includes staff savings, volunteer capacity recovery, and Twilio cost estimate |
| `index.html` | Updated signup page prototype with 18+ age gate, waiver acknowledgment, field validation, and inline confirmation screen |
| `tests.md` | Full audit of all three outputs against task requirements, constraints, ROI math, technical correctness, and handbook policy |
| `summary.md` | This file — process narrative and calculation documentation |
