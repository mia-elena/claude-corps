# Email 4: Cost of donate@ Triage

## Objective
Calculate a concrete monthly cost estimate for running the automated `donate@` inbox triage system and provide the justification to Operations.

## Context
* **Current Issue:** Marcus needs to present the budget requirements for the automated triage system to Diane (Executive Director) for approval before it can be activated.
* **Goal:** Provide a specific dollar amount for the monthly operational cost of using the target AI model to process incoming emails, backed by clear, logical assumptions.

## Required Deliverables
1. **Email Reply Message**: A drafted response to Marcus that includes:
   * A specific estimated monthly cost in dollars.
   * A clear breakdown of the mathematical assumptions used to arrive at that number.

## Specific Requirements
* **Provide a Concrete Number:** You must explicitly state an estimated monthly dollar amount as requested ("Put a number on it").
* **State Assumptions Explicitly:** Clearly list the variables used in your calculation, such as:
  * Expected monthly email volume for the `donate@` inbox.
  * Average input tokens per email (prompt + email content).
  * Average output tokens per email (the JSON routing schema).
* **Target Model Pricing:** Base the calculation on the API cost for Claude Haiku (the model specified in Email 1 for this triage pipeline).

## Source Files (Attachments)
* *(No new files attached. Rely on context from the Email 1 task—such as the `inbox_sample.csv` and `triage_prompt.md`—to estimate realistic volume and token counts for the assumptions.)*