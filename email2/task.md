# Email 2: Board Ask — Q1 Partner-Agency Allocations

## Objective
Fact-check and correct the draft board memo regarding Q1 partner-agency allocations against the raw distribution and agency data. 

## Context
* **Current Issue:** The Executive Director (Diane) used Claude to draft a board summary from raw data, but the generated numbers and details are likely inaccurate. Additionally, the warehouse distribution log contains data hygiene issues (e.g., misspelled agency names).
* **Urgency:** The corrected memo is needed for a board meeting tomorrow at 9 AM. One director specifically wants data to see if Ellis County is underserved relative to need.

## Required Deliverables
1. **`memo_corrected.md`**: The fact-checked and corrected version of the memo.

## Specific Requirements
* **Preserve Structure:** Keep the original structure of `draft_memo.md` while fixing any incorrect numbers, agency names, or narrative points.
* **Table Metrics:** The data table must be calculated and presented in **lbs per family per month**. Include the following columns:
  * Planned
  * January Actuals
  * February Actuals
  * March Actuals
  * Q1 Average
  * % vs Plan
  * Q1 Grand Total (in pounds)
* **Data Hygiene:** Manually resolve the "creative" spelling of agency names from the warehouse export to match the official agency directory.
* **Transparency:** Explicitly call out any data hygiene issues directly in the memo rather than papering over them.

## Source Files (Attachments)
* `draft_memo.md` - *The draft to be corrected*
* `partner_agencies.xlsx` / `.csv` - *Directory of 47 partner agencies, county, type, families served/month, and planned standard monthly allocation (lbs).*
* `distribution_log_q1.xlsx` / `.csv` - *Raw Q1 (Jan-Mar) delivery logs from the inventory system.*