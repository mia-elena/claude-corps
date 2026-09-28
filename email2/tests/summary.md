# Email 2 — Task Completion Report
## How the Fact-Check Was Done

---

## 1. What the task asked for

`task.md` required fact-checking `draft_memo.md` against two source files:

- `partner_agencies.csv` — 47 agencies with county, type, families served per month, and monthly planned allocation in lbs
- `distribution_log_q1.csv` — every Q1 delivery (date, agency name, lbs, truck ID) as exported from the warehouse inventory system

The deliverable was `memo_corrected.md`: same structure as the draft, correct numbers, data hygiene issues called out explicitly rather than papered over.

---

## 2. Step 1 — Ingest and audit source files

### partner_agencies.csv

Loaded all 47 rows. For each county, summed `families_served_monthly` and `monthly_allocation_lbs` to get the county-level baselines used in every subsequent calculation.

| County | Agencies | Total families/month | Total planned lbs/month |
|--------|:--------:|---------------------:|------------------------:|
| Harlan | 20 | 2,266 | 95,021 |
| Price | 16 | 1,795 | 70,962 |
| Ellis | 11 | 1,341 | 39,438 |

### distribution_log_q1.csv

Scanned every row for two categories of data hygiene issues before aggregating anything.

**a) Name variants** — agency names in the log are typed by whoever loaded the truck and do not always match the canonical names in the directory. Five variant forms were found and remapped:

| Raw name in log | Canonical name | Rows remapped |
|---|---|:---:|
| `St. Paul Food Shelf` | `St Paul Food Shelf` | 5 |
| `Mt. Zion Food Pantry` | `Mt Zion Food Pantry` | 6 |
| `Mount Zion Food Pantry` | `Mt Zion Food Pantry` | 4 |
| `Grace Fellowsihp` | `Grace Fellowship Church` | 3 |
| `Grace Fellowship` | `Grace Fellowship Church` | 1 |

Remapping was done before any aggregation so that all deliveries to the same physical agency were counted together.

**b) Exact duplicate rows** — rows were checked for identical combinations of `delivery_date + agency_name (canonical) + pounds + truck_id`. Any row that matched a previously seen combination was discarded. 18 duplicate rows were found and removed, totalling **12,356 lbs** that would otherwise have been double-counted.

**c) Unknown agency** — after name remapping, one agency name still had no match in the directory: `St Marks Pantry` (1 delivery, 2026-02-17, 812 lbs). This row was excluded from all metrics and flagged for follow-up.

---

## 3. Step 2 — Calculate county-level actuals

After cleaning, deliveries were aggregated by canonical agency name and calendar month (January = month 1, February = 2, March = 3). County-level monthly lbs were then summed from the agency totals.

**Raw county lbs (after de-duplication and name resolution):**

| County | January | February | March | Q1 Total |
|--------|--------:|---------:|------:|---------:|
| Harlan | 96,682 | 95,109 | 95,950 | 287,741 |
| Price | 71,731 | 69,585 | 71,852 | 213,168 |
| Ellis | 34,135 | 35,449 | 38,016 | 107,600 |
| **All** | **202,548** | **200,143** | **205,818** | **608,509** |

---

## 4. Step 3 — Convert to lbs per family per month

Every figure in the board table is expressed as **lbs per family per month**, not raw lbs. This makes counties comparable despite having different numbers of agencies and families.

**Formula:**

```
lbs/family/month = county_lbs_that_month ÷ county_total_families
```

**Planned** uses the same formula on planned lbs rather than actuals:

```
planned lbs/family/month = county_total_planned_lbs ÷ county_total_families
```

**Worked example — Ellis, January:**

```
34,135 lbs ÷ 1,341 families = 25.45 lbs/family  →  displayed as 25.5
```

**Worked example — Ellis, planned:**

```
39,438 lbs ÷ 1,341 families = 29.41 lbs/family  →  displayed as 29.4
```

**Full table (unrounded for % vs Plan; displayed values rounded to 1 decimal):**

| County | Planned | Jan | Feb | Mar | Q1 Avg | % vs Plan |
|--------|--------:|----:|----:|----:|-------:|----------:|
| Harlan | 41.93 | 42.67 | 41.97 | 42.34 | 42.33 | +0.9% |
| Price | 39.53 | 39.96 | 38.77 | 40.03 | 39.59 | +0.1% |
| Ellis | 29.41 | 25.45 | 26.43 | 28.35 | 26.75 | -9.1% |

**% vs Plan formula (applied to unrounded values to avoid rounding error):**

```
% vs Plan = (Q1 Avg − Planned) ÷ Planned × 100
```

Example — Harlan:

```
(42.33 − 41.93) ÷ 41.93 × 100 = +0.94% → +0.9%
```

> **Why +0.9% and not +1.0%:** An earlier pass rounded the monthly actuals to one decimal before averaging, then computed the percentage from the rounded average. This introduced 0.1% of rounding error. The correct approach is to carry full precision through all intermediate steps and round only the final display value. The audit confirmed +0.9% using unrounded values throughout.

---

## 5. Step 4 — Grand total reconciliation

**Verified total: 608,509 lbs**

The draft stated 621,677 lbs. The 13,168 lb gap is fully accounted for:

| Source of inflation | lbs |
|---|---:|
| 18 exact-duplicate delivery rows | 12,356 |
| Delivery to `St Marks Pantry` (not in directory) | 812 |
| **Total** | **13,168** |

621,677 − 13,168 = **608,509** ✓

---

## 6. Step 5 — Agency-level vs-plan rankings

For each of the 47 agencies, Q1 actual lbs (sum of all cleaned deliveries) was compared to Q1 planned lbs (monthly allocation × 3):

```
% vs Plan = (Q1 actual − Q1 planned) ÷ Q1 planned × 100
```

Agencies were sorted ascending by this percentage. The three furthest below plan:

| Agency | County | Q1 Actual | Q1 Planned | % vs Plan |
|--------|--------|----------:|-----------:|----------:|
| Ellis Senior Center | Ellis | 11,861 | 20,886 | -43.2% |
| New Hope Shelter | Ellis | 4,264 | 5,652 | -24.6% |
| Southside Church Pantry | Ellis | 4,777 | 6,279 | -23.9% |

**Mt Zion Food Pantry fact-check:** The draft claimed Mt Zion received only 2,919 lbs (-61.9% vs plan). After resolving all three name variants (`Mt Zion`, `Mt. Zion`, `Mount Zion`) and summing deliveries, Mt Zion's Q1 actual was **8,154 lbs** against a planned 7,653 lbs — **+6.5% over plan**. The draft figure was a hallucination with no basis in the source data.

---

## 7. Step 6 — Hub agency identification

Hub agencies were identified as the largest agency by `families_served_monthly` per county, taken directly from `partner_agencies.csv`.

| County | #1 Agency | Families |
|--------|-----------|:--------:|
| Ellis | Ellis Rescue Mission | 312 |
| Harlan | First Baptist Pantry | 314 |
| Price | Price Head Start | 338 |

The draft named Open Door Mission as Ellis's hub (118 families, third-largest in Ellis), Northgate Church Pantry for Price (it is a Harlan agency), and Bethel AME Food Ministry for Harlan/Price (138 families in Harlan, ninth-largest in that county).

---

## 8. Step 7 — Narrative audit

Each claim in the draft's prose was checked against the computed numbers:

| Draft claim | Verdict | Corrected fact |
|---|:---:|---|
| "Ellis is slightly over plan" | Wrong | Ellis is 9.1% under plan |
| "The board chair's concern doesn't show up in Q1" | Wrong | It is fully supported |
| "March was the strongest month for all three counties" | Wrong | January was Harlan's strongest; Price was flat (Jan = Mar); only Ellis peaked in March |
| "Ellis serves 1,890 families" | Wrong | 1,341 families (direct sum from directory) |
| "Prioritize St Marks Pantry" | Unfounded | St Marks Pantry is not in the official agency directory |

---

## 9. Summary of all corrections

| Item | Draft value | Corrected value |
|---|---|---|
| Q1 Grand Total | 621,677 lbs | **608,509 lbs** |
| Harlan % vs Plan | -1.4% | **+0.9%** |
| Price % vs Plan | -2.3% | **+0.1%** |
| Ellis % vs Plan | +1.4% | **-9.1%** |
| Strongest month (Harlan) | March | **January** |
| Strongest month (Price) | March | **January = March (tied)** |
| Mt Zion Q1 lbs | 2,919 | **8,154** |
| Mt Zion % vs Plan | -61.9% | **+6.5%** |
| Most-underserved agency | Mt Zion Food Pantry | **Ellis Senior Center (-43.2%)** |
| Ellis hub agency | Open Door Mission | **Ellis Rescue Mission** |
| Harlan hub agency | Northgate Church Pantry | **First Baptist Pantry** |
| Price hub agency | Bethel AME Food Ministry | **Price Head Start** |
| Ellis total families | 1,890 | **1,341** |
| Recommended priority | St Marks Pantry (not in directory) | **Ellis Senior Center** |

---

## 10. Files produced

```
email2/
├── task.md                          ← instructions (unchanged)
├── files/
│   ├── draft_memo.md                ← original draft (unchanged)
│   ├── partner_agencies.csv/.xlsx   ← source data (unchanged)
│   └── distribution_log_q1.csv/.xlsx← source data (unchanged)
└── outputs/
    ├── memo_corrected.md            ← fact-checked board memo
    └── summary.md                   ← this file
```
