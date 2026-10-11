# Home Credit - LAP Qualification Voice Agent

An AI voice agent prompt for **Home Credit** that calls existing customers about a
pre-approved **Loan Against Property (LAP)** offer (up to Rs 75 Lakh), checks 7 eligibility
points, and hands qualified customers to a senior loan expert.

This was built for the **SalesAgents AI - AI Intern (Prompt Engineer)** assignment.

## What the agent does

1. Greets and verifies the customer (asks a callback time if busy)
2. Presents the offer as a reward for loyalty
3. Detects existing-loan / EMI-reduction cases and moves them to a transfer specialist
4. Collects 7 eligibility points (remembers answers given out of order)
5. Disqualifies politely and immediately when a rule fails
6. Hands off to a senior loan expert only after all 7 points are done

## Eligibility rules

| # | Item | Rule |
|---|------|------|
| 1 | Property type | Residential / Commercial / Industrial OK. Agricultural = not eligible |
| 2 | Ownership | Sole or Joint both OK |
| 3 | Documents | Original documents must be available |
| 4 | Loan amount | Up to Rs 75,00,000. Above that, offer the max amount |
| 5 | Occupation + income | Salaried or Self-employed OK, income must be in Bank (Cash = not eligible) |
| 6 | Market value | Just noted, no minimum |
| 7 | Tenure | 3 to 15 years |

## Project structure

```
home-credit-lap-voice-agent/
├── README.md
├── requirements.txt
├── .env.example
├── .gitignore
├── prompts/
│   └── system_prompt.txt        <- MAIN DELIVERABLE (paste into Retell / Bolna)
├── src/
│   ├── rules.py                 <- eligibility rules as simple functions
│   ├── demo.py                  <- offline demo of the question logic
│   └── chat_with_prompt.py      <- optional text chat with the prompt (needs API key)
├── tests/
│   └── test_rules.py            <- unit tests
├── test_scenarios/
│   └── scenarios.md             <- 20 call scenarios + expected results
├── audio/                       <- call recordings
├── transcripts/                 <- call transcripts (template inside)
└── docs/
    └── approach.md              <- my approach and learnings
```

## How to run

You need Python 3.9 or above.

```bash
# 1. open the folder in VS Code, then open the terminal
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # Mac / Linux

pip install -r requirements.txt
```

**Run the unit tests (no API key needed):**
```bash
python -m unittest discover tests
```

**Run the offline demo (no API key needed):**
```bash
python src/demo.py
```
Try typing: `It's a residential house worth 1.2 crore, jointly owned with my wife`
and see that it skips those questions and asks about documents next.

**Chat with the real prompt in the terminal (optional):**
```bash
copy .env.example .env         # then add your API key inside .env
python src/chat_with_prompt.py
```

## How to test the voice agent

1. Create a free account on Retell AI or Bolna and make a new agent.
2. Copy everything from `prompts/system_prompt.txt` into the agent instructions.
3. Set the variables (`company_name`, `customer_name`, `agent_name`, `agent_gender`,
   `language_to_speak`, etc.).
4. Choose a professional voice that matches `agent_gender`.
5. Call the agent and test each scenario in `test_scenarios/scenarios.md`.
6. Save the recording to `audio/` and the transcript to `transcripts/`.

## Key prompt ideas

- **Extract -> check -> store -> ask the first missing question.** This is how the agent
  handles answers that come out of order.
- **Latest answer wins** when the customer corrects themselves.
- **No guessing:** vague answers get a clarifying question.
- **No made-up data:** interest rate goes to the senior expert, and no minimum property value is invented.
- **Voice friendly:** short replies, one question at a time, no markdown.

## Test results

| # | Scenario | Passed? |
|---|----------|---------|
| 1 | Eligible customer | |
| 2 | Agricultural property | |
| 3 | Cash income | |
| 4 | No original documents | |
| 5 | Tenure too short / too long | |
| 6 | Loan above 75 lakh | |
| 7 | Existing loan / EMI reduction | |
| 8 | Busy customer | |
| 9 | Out-of-order answers | |

(Fill after your real calls. Full list is in `test_scenarios/scenarios.md`.)

## Limitations

- `src/demo.py` uses simple keyword matching, so it is only a demo of the logic. The real
  language understanding is done by the LLM through the system prompt.
- Call quality (voice, delay) depends on the voice platform used.

## Author

Jayanth
