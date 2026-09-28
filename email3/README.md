# Email 3 — Volunteer Confirmation Flow Architecture

## Task

Every week, a staff member (Priya) manually copies volunteer signups from a Google Sheet into Airtable and then hand-texts every confirmed volunteer the night before their shift. The ask was to design an automated replacement and give Priya something she could forward to Diane (the Executive Director) to get it approved — with a real number on time or cost saved.

**Deliverables requested:**
- Architecture diagram showing the full automated flow
- Draft reply to Priya with concrete ROI metrics for Diane
- (Optional) Improved version of Priya's signup page prototype

---

## Solution

### Architecture
The diagram (`architecture.html`) maps the end-to-end flow across five layers:

1. **Signup** — volunteer submits the existing Google Form
2. **Sync** — Google Apps Script pushes the record into Airtable (Name / Phone / Routes)
3. **Orchestration** — Claude via MCP reads the Airtable roster the night before each shift and generates personalised SMS confirmation messages
4. **Delivery** — Twilio sends the texts; no new SaaS spend required beyond existing accounts
5. **Reporting** — Monday morning Slack digest posted automatically with shift fill rate and confirmation stats for the board

### Constraints honored
- Roster lives in Airtable (hard requirement)
- SMS only — no confirmation emails
- Uses existing Google Workspace and Slack; no new tools requiring executive clearance

### ROI framing for Diane
Priya's current manual process takes approximately 45–60 minutes per shift cycle (copy to Airtable + text each volunteer). At 2 shift cycles per week, automation saves ~90 minutes/week, or ~65 hours/year — at a nonprofit coordinator salary, roughly $1,300–$1,800 in recovered staff time annually, with zero new subscription cost.

---

## Files

```
files/
├── handbook.md            # Volunteer operations handbook (context)
└── index.html             # Priya's original signup page prototype

images/
├── landing.png            # Screenshot of improved signup page
├── signupmodal.png        # Signup modal detail
└── confirmation.png       # Confirmation screen

outputs/                   # ★ Graded deliverables only
├── architecture.html      # Interactive architecture diagram
├── email_reply.md         # Draft reply to Priya with ROI numbers for Diane
└── index.html             # Improved volunteer signup page

tests/
├── architecture.pdf       # Print/share version of the diagram
├── tests.md               # Requirements audit
└── summary.md             # Implementation notes
```
