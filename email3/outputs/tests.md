# Email 3 — Testing & Findings Audit

**Task:** Architecture for Volunteer Confirmation Flow  
**Outputs audited:** `architecture.html`, `email_reply.md`, `index.html`  
**Source files:** `task.md`, `handbook.md`, `index.html` (original prototype)  
**Audit date:** 2026-09-28

---

## 1. Deliverables Checklist

| # | Required Deliverable | Status | Notes |
|---|---|---|---|
| 1 | `architecture.html` produced | PASS | File present in `outputs/` |
| 2 | `email_reply.md` produced | PASS | File present in `outputs/` |
| 3 | `index.html` (optional) produced | PASS | File present in `outputs/` |

---

## 2. Architecture Diagram Requirements (task.md §Required Deliverables, item 1)

| Requirement | Status | Evidence |
|---|---|---|
| Shows where a volunteer signs up | PASS | `index.html → Google Form → Google Sheet` shown as intake layer |
| Shows where the roster lives | PASS | Airtable node shown as source of truth; fields: Name · Phone · Route · Shift · Status |
| Shows the mechanism sending texts | PASS | Twilio SMS MCP shown for outbound messages and inbound CANCEL webhook |
| Shows where Claude and MCP fit | PASS | 4 discrete Claude+MCP bots (Confirmation, Reminder, Cancellation Handler, Report Bot); MCP server table lists Airtable, Twilio, Slack connectors |
| Monday morning success report notification | PASS | Cron Mon 8AM → Claude+MCP Report Bot → Slack #volunteers |

---

## 3. Constraint Compliance (task.md §Constraints)

| Constraint | Status | Notes |
|---|---|---|
| Roster lives in Airtable (Name / Phone / Routes) | PASS | Airtable is the single source of truth; fields match. Minor: task specifies "Routes" (plural); architecture uses singular "Route" — functionally equivalent |
| Utilize existing Google Workspace | PASS | Google Form, Google Sheet, Google Apps Script — all existing, zero new spend |
| Utilize existing Slack | PASS | Slack MCP posts to #volunteers; Slack is listed as existing tool in handbook |
| SMS for confirmations (not email) | PASS | Twilio SMS used throughout; no email delivery to volunteers in any flow |
| New SaaS requires executive clearance | PASS | Twilio flagged as only net-new vendor with explicit "requires Diane sign-off" label in MCP table |

---

## 4. ROI Calculation Audit (`email_reply.md`)

All figures traced back to source material.

### 4a. Time Savings

| Step | Value | Source | Verdict |
|---|---|---|---|
| Current weekly hours (Priya) | 6 hrs/week | handbook.md: "call it six hours a week" | Verified ✓ |
| Hours retained post-automation | ~1 hr/week | Assumed (reviewing Monday report) | Editorial assumption — not in source; reasonable |
| Net hours saved | 5 hrs/week | Derived: 6 - 1 = 5 | Correct ✓ |
| Hourly rate | $33/hr | handbook.md: "Independent Sector rate (~$33/hr)" | Verified ✓ |
| Annual staff savings | ~$8,600/yr | 5 × $33 × 52 = $8,580 → rounds to $8,600 | Correct ✓ |

### 4b. No-Show Reduction

| Step | Value | Source | Verdict |
|---|---|---|---|
| Baseline no-show rate | ~35% | handbook.md: "anecdotally 30–40%" — midpoint used | Verified; flagged as anecdotal, not formally tracked |
| Total weekly shift slots | ~38 | index.html shift data: 8+6+8+12+4 = 38 | Verified ✓ |
| SMS reminder no-show reduction | 40–50% | External industry benchmark — not from handbook | **ASSUMPTION — source not cited in email** |
| Conservative reduction applied | 40% | Editorial choice (lower bound) | Reasonable; conservative |
| No-shows before | 38 × 0.35 = 13.3/week | Derived | Correct ✓ |
| Recovered appearances/week | 13.3 × 0.40 ≈ 5.3 | Derived | Email says "5–6" — correct ✓ |
| Value per volunteer-slot | 3 hrs × $33 = $99 | **Assumed average shift length — not in source files** | ASSUMPTION |
| Annual recovered capacity | 5.3 × $99 × 52 ≈ $27,300 | Derived | Email says "~$26,000" — slightly underestimates; conservative ✓ |

### 4c. Twilio Cost Estimate

| Step | Value | Source | Verdict |
|---|---|---|---|
| Unit cost per SMS | $0.0075 | Twilio standard rate | External reference; plausible |
| Weekly message volume | ~50 | Estimated: ~23 signups + ~23 reminders at ~60% fill rate | Reasonable estimate; not precisely sourced |
| Annual cost | $0.0075 × 50 × 52 = $19.50 | Derived | "Under $20/yr" claim is correct ✓ |

### 4d. Total ROI

| Claim | Derived value | Output value | Verdict |
|---|---|---|---|
| Total annual ROI | $8,580 + ~$27,300 = ~$35,880 | "~$34,000" | Slight understatement; conservative rounding acceptable ✓ |

**Flagged assumptions in ROI section (not labeled as such in the email):**
1. The "40–50% no-show reduction from SMS reminders" is an industry benchmark with no cited source.
2. The "3 hrs/shift" average for recovered volunteer-slot value is not in any source file.
3. The retained 1 hr/week for report review is editorial.

These are reasonable estimates but the email presents them as facts. For Diane's purposes this is low-risk; for a grant report it would require citations.

---

## 5. Technical Findings — `architecture.html`

### 5a. Rendering

| Check | Status | Detail |
|---|---|---|
| Mermaid.js dependency | WARN | Loaded via CDN (`cdn.jsdelivr.net`). Diagram will not render offline. Acceptable for a prototype/internal doc; should be noted for production use. |
| Single-page requirement | PASS | All content on one HTML page ✓ |
| Color legend present | PASS | 6 categories: existing Google tools, Airtable, Claude+MCP, SMS, Slack, cron ✓ |
| MCP server table | PASS | Lists all 3 servers, operations, and SaaS status ✓ |

### 5b. Flow Correctness

| Check | Status | Detail |
|---|---|---|
| Signup → Airtable path | PASS | index.html → Google Form → Sheet → Apps Script → Airtable ✓ |
| Confirmation SMS on new record | PASS | Airtable "new record added" trigger → Confirmation Bot → SMS ✓ |
| Day-before reminder timing | PASS | Cron labeled "Thu for Fri/Sat; Mon for Tue" — correctly accounts for different shift days ✓ |
| CANCEL reply handling | PARTIAL | CANCEL is shown as a reply to `SMS2` (the reminder). A volunteer who wants to cancel after the *initial confirmation* SMS has no defined path. The CANCEL flow should accept replies to any outbound SMS, not just reminders. **Gap.** |
| Monday morning report | PASS | Cron Mon 8AM → Claude → Airtable rollup → Slack ✓ |

### 5c. Infrastructure Gaps

| Gap | Severity | Detail |
|---|---|---|
| Cron platform unspecified | MEDIUM | Architecture shows cron triggers but names no platform. Google Apps Script time-driven triggers are free and fit the "use what we have" constraint — should be specified to avoid ambiguity at implementation. |
| Twilio webhook hosting | MEDIUM | Receiving inbound CANCEL texts requires a publicly accessible HTTPS endpoint. No hosting or deployment mechanism is mentioned. Options (e.g., Google Cloud Run, Cloudflare Workers) would need Diane's approval if they incur cost. |
| Duplicate submission handling | LOW | If a volunteer submits the Google Form twice, Apps Script would attempt to create two Airtable records. An upsert-by-phone strategy should be noted. |
| Apps Script → Airtable credentials | LOW | Architecture note says "Airtable API key from Marcus" but does not address where the key is stored for the Apps Script (e.g., script properties). Implementation detail, not a design flaw. |

---

## 6. Technical Findings — `index.html` (updated prototype)

### 6a. Functional Tests

| Test | Status | Detail |
|---|---|---|
| Shift list renders on load | PASS | `render()` called on script init ✓ |
| Shift 2 (Tuesday 1pm-4pm) shows as Full | PASS | `taken:6 === need:6`; button disabled, "Full" badge shown ✓ |
| Sign up button opens modal | PASS | `openModal(id)` called correctly from button; `selectedShift` set ✓ |
| Modal backdrop click closes modal | PASS | Event listener checks `e.target === this` ✓ |
| Cancel button closes modal | PASS | `onclick="closeModal()"` ✓ |
| Name validation (blank) | PASS | Shows "Please enter your name." error ✓ |
| Email validation (no @) | PASS | `!email.includes('@')` catches missing domain ✓ |
| Phone validation (< 10 digits) | PASS | `phone.replace(/\D/g,'').length < 10` strips formatting before counting ✓ |
| Waiver checkbox required | PASS | Shows error if unchecked ✓ |
| Age checkbox required for mobile pantry | PASS | Shift 4 (Ellis mobile): `ageOk = !selectedShift.mobile \|\| (ageEl && ageEl.checked)`; null-safe ✓ |
| Age checkbox absent for non-mobile shifts | PASS | `ageEl` is null for non-mobile; `!selectedShift.mobile` short-circuits to true ✓ |
| Confirmation screen renders post-submit | PASS | innerHTML replaced with confirm-screen; includes name, shift, phone ✓ |
| Spot count decrements after signup | PASS | `selectedShift.taken += 1`; `render()` called; spot count updates ✓ |
| Spot count resets on page refresh | PASS (by design) | Prototype behavior; noted in proto-note ✓ |

### 6b. Policy Compliance (handbook.md cross-reference)

| Policy | Status | Detail |
|---|---|---|
| Mobile pantry 18+ minimum (insurance constraint) | PASS | Age gate banner + required age checkbox in modal for Shift 4 ✓ |
| Liability waiver on arrival (not pre-signed) | PASS | Global notice banner states "sign a one-page liability waiver on arrival at their first shift — no pre-sign required" ✓ |
| No gatekeeping (income/immigration/docs) | PASS | Form collects name, email, phone only — no qualifying questions ✓ |
| Background check for route liaisons | N/A | Not required for single mobile-pantry days per handbook ✓ (correctly omitted) |

### 6c. Gaps in Prototype

| Gap | Severity | Detail |
|---|---|---|
| Warehouse sort minimum age not enforced | MEDIUM | Handbook: warehouse sort is 14+ with parental consent, 16+ unaccompanied. Form does not ask age for non-mobile shifts. An acknowledgment checkbox ("I am 16 or older, or attending with a parent/guardian who has signed a consent form") would close this. |
| Signup page is English-only | MEDIUM | Handbook explicitly states any wide-audience communication "should work in both English and Spanish." A Spanish language toggle or bilingual labels are missing. |
| No data persistence | LOW (prototype) | Noted in proto-note text; expected for current stage. Airtable integration is the defined next step in architecture. |
| Group signup path absent | LOW | Handbook notes groups are coordinated by email with Priya and capped per shift. No group field or routing path exists in the form. Out of scope for prototype but worth noting. |
| Email validation is shallow | LOW | `includes('@')` does not catch `user@` or `@domain`. Acceptable for prototype; should use regex or the `type="email"` constraint more strictly at production. |

---

## 7. Source File Cross-Reference — Edge Cases Checked

| Item | Checked | Finding |
|---|---|---|
| T-99 test slot in inventory system | Yes | Not relevant to volunteer flow; correctly omitted ✓ |
| Major donors table (internal-only) | Yes | Not referenced in any output — correct ✓ |
| Ellis County Spanish-speaking population | Yes | Wide-audience signup form is English-only — flagged above as gap ⚠️ |
| Hub agencies forwarding to satellites | Yes | Not relevant to volunteer flow ✓ |
| Marcus / Diane sign-off boundaries | Yes | Twilio correctly routed to Diane for approval; Airtable API correctly noted as "from Marcus" ✓ |
| Jordan Lee (part-time MWF) | Yes | $33/hr rate sourced from handbook; Jordan's schedule not relevant ✓ |
| Priya's wishlist cancellation banner | Yes | Addressed in architecture Design Notes: weather cancellations can trigger bulk SMS from Marcus's Slack post ✓ |
| Pantry Manager API | Yes | Exists, relevant to warehouse inventory only — correctly excluded from volunteer flow ✓ |

---

## 8. Summary

### What passed cleanly
- All three required deliverables produced and placed in `outputs/`.
- Every mandatory architecture element from the task is present and correctly wired.
- All four system constraints (Airtable, Google Workspace, Slack, SMS-not-email) are satisfied.
- ROI arithmetic is correct and conservative; handbook figures used where available.
- New SaaS (Twilio) correctly identified and flagged for executive clearance.
- index.html fixes the two highest-priority gaps from the original prototype: the 18+ insurance constraint and the missing liability waiver acknowledgment.

### What needs attention before production

| Priority | Issue | File |
|---|---|---|
| HIGH | CANCEL reply should be accepted after any outbound SMS, not only the day-before reminder | `architecture.html` |
| HIGH | English-only signup page conflicts with handbook bilingual requirement | `index.html` |
| HIGH | Cron hosting platform must be specified; Twilio webhook requires a public endpoint — both carry potential cost and need Diane's awareness | `architecture.html` |
| MEDIUM | Warehouse sort minimum age (14+/16+) not enforced in signup form | `index.html` |
| MEDIUM | "40-50% no-show reduction" statistic should be labeled as an industry estimate | `email_reply.md` |
| LOW | "3 hrs/shift" value assumption should be labeled as an estimate | `email_reply.md` |
| LOW | Duplicate Google Form submission handling (upsert logic) not addressed in architecture | `architecture.html` |
