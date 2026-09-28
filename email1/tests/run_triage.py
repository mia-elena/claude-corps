"""
Run all emails in inbox_sample.csv through the triage prompt via Claude Haiku.
Writes results to triage_results.json and triage_results.md.

Usage:
    python3 run_triage.py

Credentials are loaded from ../../../.env (repo root).
"""

import csv
import json
import os
import sys
import time
from pathlib import Path

# Load .env from repo root before importing anthropic
ENV_FILE = Path(__file__).parent.parent.parent / ".env"
if ENV_FILE.exists():
    from dotenv import load_dotenv
    load_dotenv(ENV_FILE)

import anthropic

# ── Paths ──────────────────────────────────────────────────────────────────────
ROOT        = Path(__file__).parent
PROMPT_FILE = ROOT.parent / "outputs" / "triage_prompt.md"
CSV_FILE    = ROOT.parent / "files" / "inbox_sample.csv"
OUT_JSON    = ROOT / "triage_results.json"
OUT_MD      = ROOT / "triage_results.md"

# ── Credentials ────────────────────────────────────────────────────────────────
# Prefer the workspace-scoped key; fall back to the admin key + workspace header.
WORKSPACE_KEY  = os.environ.get("ANTHROPIC_WORKSPACE_API_KEY", "")
ADMIN_KEY      = os.environ.get("ANTHROPIC_API_KEY", "")
WORKSPACE_ID   = os.environ.get("ANTHROPIC_WORKSPACE_ID", "")
MODEL          = os.environ.get("TRIAGE_MODEL", "claude-haiku-4-5-20251001")
MAX_TOKENS     = 512


# ── Build Anthropic client ─────────────────────────────────────────────────────
def build_client() -> anthropic.Anthropic:
    if WORKSPACE_KEY:
        # Workspace-scoped key — no extra header needed
        print(f"Using workspace-scoped key (workspace: {WORKSPACE_ID or 'default'})")
        return anthropic.Anthropic(api_key=WORKSPACE_KEY)
    elif ADMIN_KEY and WORKSPACE_ID:
        # Admin key — must pass workspace header
        print(f"Using admin key with workspace header ({WORKSPACE_ID})")
        return anthropic.Anthropic(
            api_key=ADMIN_KEY,
            default_headers={"anthropic-workspace-id": WORKSPACE_ID},
        )
    elif ADMIN_KEY:
        print("Using admin key (no workspace ID set — may fail if key requires one)")
        return anthropic.Anthropic(api_key=ADMIN_KEY)
    else:
        print("ERROR: No API key found. Set ANTHROPIC_API_KEY or ANTHROPIC_WORKSPACE_API_KEY in .env", file=sys.stderr)
        sys.exit(1)


# ── Load system prompt ─────────────────────────────────────────────────────────
def load_prompt() -> str:
    return PROMPT_FILE.read_text()


# ── Load emails ────────────────────────────────────────────────────────────────
def load_emails() -> list[dict]:
    with open(CSV_FILE, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


# ── Build user message ─────────────────────────────────────────────────────────
def build_user_message(email: dict) -> str:
    return (
        f"From: {email['from']}\n"
        f"Subject: {email['subject']}\n"
        f"Body: {email['body']}"
    )


# ── Call Haiku ─────────────────────────────────────────────────────────────────
def triage_email(client: anthropic.Anthropic, system: str, email: dict) -> dict:
    resp = client.messages.create(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        system=system,
        messages=[{"role": "user", "content": build_user_message(email)}],
    )
    usage = resp.usage
    text  = resp.content[0].text.strip()

    # Strip markdown code fences if the model wraps output
    if text.startswith("```"):
        lines = text.splitlines()
        text  = "\n".join(l for l in lines if not l.startswith("```")).strip()

    try:
        parsed = json.loads(text)
    except json.JSONDecodeError:
        parsed = {"_parse_error": True, "_raw": text}

    return {
        "id":             email["id"],
        "from":           email["from"],
        "subject":        email["subject"],
        "body":           email["body"],
        "input_tokens":   usage.input_tokens,
        "output_tokens":  usage.output_tokens,
        "result":         parsed,
    }


# ── Expected labels (from tests.md) ───────────────────────────────────────────
EXPECTED = {
    "S01": ("corporate_food_donation",  True,  "marcus"),
    "S02": ("corporate_food_donation",  True,  "marcus"),
    "S03": ("corporate_food_donation",  True,  "marcus"),
    "S04": ("corporate_food_donation",  True,  "marcus"),
    "S05": ("corporate_food_donation",  True,  "marcus"),
    "S06": ("individual_food_donation", False, "marcus"),
    "S07": ("individual_food_donation", False, "marcus"),
    "S08": ("individual_food_donation", False, "marcus"),
    "S09": ("individual_food_donation", False, "auto_ok"),
    "S10": ("individual_food_donation", False, "marcus"),
    "S11": ("individual_food_donation", False, "marcus"),
    "S12": ("individual_food_donation", False, "auto_ok"),
    "S13": ("individual_food_donation", False, "auto_ok"),
    "S14": ("partner_agency_request",   False, "marcus"),
    "S15": ("partner_agency_request",   False, "marcus"),
    "S16": ("partner_agency_request",   False, "marcus"),
    "S17": ("partner_agency_request",   False, "marcus"),
    "S18": ("partner_agency_request",   False, "marcus"),
    "S19": ("partner_agency_request",   False, "marcus"),
    "S20": ("food_assistance_seeker",   True,  "intake_line"),
    "S21": ("food_assistance_seeker",   True,  "intake_line"),
    "S22": ("food_assistance_seeker",   True,  "intake_line"),
    "S23": ("food_assistance_seeker",   True,  "intake_line"),
    "S24": ("volunteer_inquiry",        True,  "priya"),
    "S25": ("volunteer_inquiry",        False, "priya"),
    "S26": ("volunteer_inquiry",        False, "priya"),
    "S27": ("volunteer_inquiry",        False, "priya"),
    "S28": ("volunteer_inquiry",        True,  "priya"),
    "S29": ("volunteer_inquiry",        True,  "priya"),
    "S30": ("food_drive",               False, "priya"),
    "S31": ("food_drive",               False, "priya"),
    "S32": ("food_drive",               False, "priya"),
    "S33": ("media_or_general_inquiry", False, "marcus"),
    "S34": ("media_or_general_inquiry", False, "marcus"),
    "S35": ("media_or_general_inquiry", False, "marcus"),
    "S36": ("spam_no_reply",            False, "no_reply"),
    "S37": ("spam_no_reply",            False, "no_reply"),
    "S38": ("spam_no_reply",            False, "no_reply"),
    "S39": ("spam_no_reply",            False, "no_reply"),
    "S40": ("spam_no_reply",            False, "no_reply"),
}

VALID_CATS   = {
    "corporate_food_donation", "individual_food_donation",
    "partner_agency_request",  "food_assistance_seeker",
    "volunteer_inquiry",       "food_drive",
    "media_or_general_inquiry","spam_no_reply",
}
VALID_ROUTES = {"marcus", "diane", "priya", "intake_line", "auto_ok", "no_reply"}
HALLUC_PHRASES = [
    "i'm forwarding", "i will forward", "forwarding to",
    "i'm attaching", "see attachment", "attached please find",
]


# ── Main ───────────────────────────────────────────────────────────────────────
def main():
    client  = build_client()
    system  = load_prompt()
    emails  = load_emails()
    results = []

    total = len(emails)
    print(f"Model : {MODEL}")
    print(f"Emails: {total}\n")

    for i, email in enumerate(emails, 1):
        print(f"  [{i:02d}/{total}] {email['id']}  {email['subject'][:55]}")
        try:
            row = triage_email(client, system, email)
        except Exception as exc:
            row = {
                "id":            email["id"],
                "from":          email["from"],
                "subject":       email["subject"],
                "body":          email["body"],
                "input_tokens":  0,
                "output_tokens": 0,
                "result":        {"_api_error": str(exc)},
            }
        results.append(row)
        time.sleep(0.25)

    # ── Save raw JSON ──────────────────────────────────────────────────────────
    OUT_JSON.write_text(json.dumps(results, indent=2))

    # ── Token / cost tallies ───────────────────────────────────────────────────
    total_in  = sum(r["input_tokens"]  for r in results)
    total_out = sum(r["output_tokens"] for r in results)
    # Claude Haiku 4.5 pricing: $1.00/M input, $5.00/M output
    cost_in   = total_in  / 1_000_000 * 1.00
    cost_out  = total_out / 1_000_000 * 5.00
    cost_run  = cost_in + cost_out

    # ── Classify each result ───────────────────────────────────────────────────
    api_errors    = []
    parse_errors  = []
    tax_violations = []
    hallucinations = []
    deviations    = []
    passes        = []

    for r in results:
        eid = r["id"]
        res = r["result"]

        if "_api_error" in res:
            api_errors.append(eid)
            continue
        if "_parse_error" in res:
            parse_errors.append((eid, res.get("_raw", "")))
            continue

        cat   = res.get("category",  "")
        urg   = res.get("urgent")
        route = res.get("route_to",  "")
        draft = (res.get("draft") or "").lower()

        # Taxonomy check
        if cat not in VALID_CATS:
            tax_violations.append((eid, f"invalid category '{cat}'"))
        if route not in VALID_ROUTES:
            tax_violations.append((eid, f"invalid route '{route}'"))

        # Hallucination check
        for phrase in HALLUC_PHRASES:
            if phrase in draft:
                hallucinations.append((eid, phrase))

        # Deviation vs expected
        if eid in EXPECTED:
            exp_cat, exp_urg, exp_route = EXPECTED[eid]
            diffs = []
            if cat   != exp_cat:   diffs.append(f"category  expected={exp_cat} got={cat}")
            if urg   != exp_urg:   diffs.append(f"urgent    expected={exp_urg} got={urg}")
            if route != exp_route: diffs.append(f"route_to  expected={exp_route} got={route}")
            if diffs:
                deviations.append((eid, diffs))
            else:
                passes.append(eid)

    # ── Build Markdown report ──────────────────────────────────────────────────
    lines = [
        "# Triage Run Results",
        "",
        f"**Model:** `{MODEL}`  ",
        f"**Date:** 2026-09-28  ",
        f"**Emails processed:** {total}  ",
        "",
        "## Run Health",
        "",
        f"| Check | Count |",
        f"|---|---|",
        f"| API errors | {len(api_errors)} |",
        f"| JSON parse errors | {len(parse_errors)} |",
        f"| Taxonomy violations | {len(tax_violations)} |",
        f"| Hallucinations detected | {len(hallucinations)} |",
        f"| Label deviations vs expected | {len(deviations)} |",
        f"| Clean passes | {len(passes)} / {len(EXPECTED)} |",
        "",
        "---",
        "",
        "## Full Results",
        "",
        "| ID | Category | Urgent | Route | Flags |",
        "|---|---|---|---|---|",
    ]

    for r in results:
        eid = r["id"]
        res = r["result"]

        if "_api_error" in res:
            lines.append(f"| {eid} | — | — | — | **API ERROR:** {res['_api_error'][:80]} |")
            continue
        if "_parse_error" in res:
            lines.append(f"| {eid} | — | — | — | **PARSE ERROR:** `{res.get('_raw','')[:60]}` |")
            continue

        cat   = res.get("category",  "—")
        urg   = str(res.get("urgent", "—")).lower()
        route = res.get("route_to",  "—")
        draft = (res.get("draft") or "").lower()

        flags = []
        if cat   not in VALID_CATS:   flags.append(f"BAD CAT: `{cat}`")
        if route not in VALID_ROUTES: flags.append(f"BAD ROUTE: `{route}`")
        for phrase in HALLUC_PHRASES:
            if phrase in draft:       flags.append(f"HALLUC: '{phrase}'")

        if eid in EXPECTED:
            exp_cat, exp_urg, exp_route = EXPECTED[eid]
            if cat   != exp_cat:   flags.append(f"cat? expected `{exp_cat}`")
            if urg   != str(exp_urg).lower(): flags.append(f"urgent? expected `{exp_urg}`")
            if route != exp_route: flags.append(f"route? expected `{exp_route}`")

        flag_str = " / ".join(flags) if flags else "PASS"
        lines.append(f"| {eid} | `{cat}` | {urg} | `{route}` | {flag_str} |")

    # ── Deviations detail ──────────────────────────────────────────────────────
    lines += ["", "---", "", "## Deviations Detail", ""]
    if deviations:
        for eid, diffs in deviations:
            lines.append(f"**{eid}**")
            for d in diffs:
                lines.append(f"- {d}")
            lines.append("")
    else:
        lines.append("No deviations — all labeled emails match expected outputs.")

    # ── Hallucinations detail ──────────────────────────────────────────────────
    lines += ["", "---", "", "## Hallucinations Detected", ""]
    if hallucinations:
        for eid, phrase in hallucinations:
            lines.append(f"- **{eid}:** triggered phrase `\"{phrase}\"`")
    else:
        lines.append("None detected.")

    # ── Token & cost table ─────────────────────────────────────────────────────
    lines += [
        "",
        "---",
        "",
        "## Token & Cost Summary",
        "",
        "| Metric | Value |",
        "|---|---|",
        f"| Model | `{MODEL}` |",
        f"| Emails processed | {total} |",
        f"| Total input tokens | {total_in:,} |",
        f"| Total output tokens | {total_out:,} |",
        f"| Avg input tokens / email | {total_in // max(total,1):,} |",
        f"| Avg output tokens / email | {total_out // max(total,1):,} |",
        f"| Input cost (\\$1.00 / M) | \\${cost_in:.5f} |",
        f"| Output cost (\\$5.00 / M) | \\${cost_out:.5f} |",
        f"| **Total run cost** | **\\${cost_run:.5f}** |",
        "",
        "> Pricing: Claude Haiku 4.5 — \\$1.00/M input, \\$5.00/M output.",
        "> Monthly cost extrapolation: multiply per-email cost by estimated monthly volume.",
    ]

    OUT_MD.write_text("\n".join(lines))

    # ── Console summary ────────────────────────────────────────────────────────
    print(f"\n{'─'*55}")
    print(f"Results saved:")
    print(f"  {OUT_JSON}")
    print(f"  {OUT_MD}")
    print(f"\nHealth summary:")
    print(f"  API errors      : {len(api_errors)}")
    print(f"  Parse errors    : {len(parse_errors)}")
    print(f"  Taxonomy issues : {len(tax_violations)}")
    print(f"  Hallucinations  : {len(hallucinations)}")
    print(f"  Label deviations: {len(deviations)}")
    print(f"  Clean passes    : {len(passes)}/{len(EXPECTED)}")
    print(f"\nTokens  : {total_in:,} in / {total_out:,} out")
    print(f"Run cost: ${cost_run:.5f}")


if __name__ == "__main__":
    main()
