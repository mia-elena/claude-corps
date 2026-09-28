# Q1 Distribution — Board Summary (CORRECTED)

*Diane Okafor — for board chair review*

We distributed **608,509 lbs** across 47 partner agencies in Q1.

## By county — lbs per family per month

| County | Planned | Jan | Feb | Mar | Q1 avg | % vs Plan | Q1 Grand Total (lbs) |
|---|---:|---:|---:|---:|---:|---:|---:|
| Harlan | 41.9 | 42.7 | 42.0 | 42.3 | 42.3 | +0.9% | 287,741 |
| Price | 39.5 | 40.0 | 38.8 | 40.0 | 39.6 | +0.1% | 213,168 |
| Ellis | 29.4 | 25.5 | 26.4 | 28.3 | 26.7 | **-9.1%** | 107,600 |

Ellis is **9.1% under plan** — the board chair's concern is fully supported by the Q1 data. January was Harlan's strongest month; Price ran flat with January and March tied; Ellis showed an upward trend through the quarter (25.5 → 26.4 → 28.3 lbs/family), which is a positive signal but does not close the gap to plan.

## Agencies furthest under allocation

| Agency | vs plan |
|---|---:|
| Ellis Senior Center | -43.2% |
| New Hope Shelter | -24.6% |
| Southside Church Pantry | -23.9% |

Ellis Senior Center received only **11,861 lbs** all quarter against a planned **20,886 lbs** — less than 57% of its Q1 allocation. All three agencies furthest under plan are in Ellis County.

## Hub agencies

Our largest partners by families served — Ellis: **Ellis Rescue Mission** (312 families). Harlan: **First Baptist Pantry** (314 families). Price: **Price Head Start** (338 families).

## Recommended actions

1. Prioritize **Ellis Senior Center** for an immediate allocation review — it is down 43.2% on Q1, and New Hope Shelter and Southside Church Pantry compound the Ellis shortfall.
2. Ask Priya to audit the Ellis delivery routes — the county-level data confirms a systemic gap, not isolated agency-level variation.
3. Note for the formula review: Ellis serves **1,341 families** on the lowest per-family allocation of the three counties.

*Context: Ellis is our highest Spanish-speaking-share county. Routes and truck schedules are owned by Priya.*

## Data hygiene

The warehouse export contained issues that required resolution before calculating any figures above. All metrics are based on the cleaned data.

| Issue | Rows affected | lbs impact |
|---|---:|---:|
| 18 exact-duplicate delivery rows (identical date / agency / lbs / truck) | 18 | +12,356 inflated |
| `Mt. Zion Food Pantry` and `Mount Zion Food Pantry` → `Mt Zion Food Pantry` | 10 | name only |
| `Grace Fellowsihp` and `Grace Fellowship` → `Grace Fellowship Church` | 4 | name only |
| `St. Paul Food Shelf` → `St Paul Food Shelf` | 5 | name only |
| `St Marks Pantry` — not in official agency directory | 1 | 812 lbs excluded |

The 13,168 lb difference between the draft total (621,677) and the verified total (608,509) is fully accounted for by the duplicate rows (12,356 lbs) and the unrecognized agency (812 lbs). **St Marks Pantry requires follow-up** — it is not among our 47 partner agencies and should not appear in delivery logs.

---
*Corrected from `partner_agencies.xlsx` + `distribution_log_q1.xlsx`. All figures independently verified.*
