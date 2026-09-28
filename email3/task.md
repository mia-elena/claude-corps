# Email 3: Architecture for Volunteer Confirmation Flow

## Objective
Design a simple, single-page architecture diagram outlining an automated flow for volunteer signups, roster management, and SMS confirmations to replace the current manual process.

## Context
* **Current Issue:** The volunteer confirmation process is highly manual. Signups go from a Google Form to a Sheet, are manually entered into Airtable, and require hand-texting every confirmed volunteer the night before their shift. 
* **Goal:** Automate the flow to consolidate sign-up lists, provide visibility/dashboards for the board, and eliminate manual texting. 

## Required Deliverables
1. **`architecture.html`** (or `.svg` / `.mmd`): An architecture diagram detailing the new flow. Must include:
   * Where a volunteer signs up.
   * Where the roster lives.
   * The mechanism sending the texts.
   * Where Claude and MCP (Model Context Protocol) fit into the pipeline.
   * A notification mechanism for Monday morning success reports.
2. **Email Reply Message**: A drafted reply to Priya containing concrete ROI metrics ("a number or two" estimating time or cost saved) that she can forward directly to Diane to justify the project.
3. *(Optional)* **`index.html`**: An updated, improved version of Priya's initial signup page prototype.

## Constraints & System Requirements
* **Data Storage:** The volunteer roster (Name / Phone / Routes) must live in Airtable.
* **Existing Tooling:** Utilize existing Google Workspace and Slack integrations. 
* **Communication:** System must use SMS text messaging (not email) for volunteer shift confirmations.
* **Budget:** "Use what we have." Any new SaaS spending requires executive clearance.

## Source Files (Attachments)
* `handbook.md` 
* `index.html` - *Priya's initial prototype page*