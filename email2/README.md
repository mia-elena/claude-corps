# Email 2 — Q1 Partner-Agency Allocation Memo

## Task

The Executive Director used Claude to draft a board summary of Q1 food distribution across partner agencies. The numbers were likely wrong. With a board meeting the next morning and a director specifically asking whether Ellis County is being underserved relative to need, the memo needed to be fact-checked and corrected — fast.

**Deliverables requested:**
- Corrected memo (`memo_corrected.md`) with recalculated figures, fixed agency names, and a lbs-per-family-per-month data table

---

## Solution

### Data sources
- `partner_agencies.csv` — directory of 47 partner agencies with county, type, families served/month, and planned monthly allocation in lbs
- `distribution_log_q1.csv` — raw warehouse delivery logs for January through March

### Data hygiene
The warehouse export contained misspelled agency names (the memo calls these "creative" spellings). Each name in the distribution log was matched to the official agency directory by fuzzy comparison, resolved manually, and called out transparently in the corrected memo rather than silently fixed.

### Calculations
All figures were recalculated from scratch in **lbs per family per month** using the formula:

```
lbs per family = total lbs delivered ÷ families served
```

The corrected table includes: Planned · Jan Actuals · Feb Actuals · Mar Actuals · Q1 Average · % vs Plan · Q1 Grand Total (lbs)

The Ellis County underservice question was answered directly using the same per-family metric across county lines.

---

## Files

```
files/
├── draft_memo.md             # Original AI-drafted memo (with errors)
├── partner_agencies.csv/.xlsx  # Agency directory (47 agencies)
└── distribution_log_q1.csv/.xlsx  # Raw Q1 delivery logs

outputs/
├── memo_corrected.md         # ★ Fact-checked memo ready for the board
└── summary.md                # Notes on methodology and data hygiene findings
```
