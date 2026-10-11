# Test Scenarios

Fill the "Result" column after each real call on Retell / Bolna.
Say the lines like a real customer (fillers, full sentences, small mistakes).

| # | Scenario | What I say on the call | Expected result | Result (fill) |
|---|----------|------------------------|-----------------|---------------|
| 1 | Perfect customer | "Yes speaking... residential flat, my own, originals are at home, need 50 lakh, I'm salaried, salary comes to bank, worth around 1 crore, 10 years" | Qualified -> senior expert handoff | |
| 2 | Agricultural | "It's agricultural land actually" | Polite disqualify, call ends | |
| 3 | Cash income | "I run a small shop, mostly cash" | Polite disqualify, call ends | |
| 4 | No original documents | "I only have photocopies" | Polite disqualify, call ends | |
| 5 | Tenure too short | "Umm... 2 years" | Polite disqualify, call ends | |
| 6 | Tenure too long | "I want 20 years" | Polite disqualify, call ends | |
| 7 | Loan above limit | "I need 90 lakh" -> then "yes ok 75 lakh" | Agent explains 75 lakh limit, asks to proceed, continues | |
| 8 | Loan above limit, says no | "I need 90 lakh" -> then "no, then forget it" | Polite end of call | |
| 9 | Joint ownership | "It's jointly owned with my brother" | Continues (NOT disqualified) | |
| 10 | Existing loan | "I already have a loan on this property" | Transfer specialist message, call ends | |
| 11 | EMI reduction | "Actually I want to reduce my current EMI" | Transfer specialist message, call ends | |
| 12 | Out of order | "It's a residential house worth 1.2 crore, jointly owned with my wife" | Agent skips property, ownership, value. Asks documents next | |
| 13 | Busy customer | "I'm in a meeting right now" | Asks callback time, ends | |
| 14 | Interest rate diversion | "What is the interest rate?" (middle of checklist) | No made-up rate. Says expert will tell. Returns to next question | |
| 15 | Correction | "10 years... no wait, make it 12" | Uses 12 years | |
| 16 | Contradiction | "It's residential... actually no, agricultural" | Latest answer used -> disqualify | |
| 17 | Vague answer | "The papers are somewhere I think" | Agent asks clarifying question, does not assume yes | |
| 18 | Wrong person | "No, he is not here" | No offer details shared, polite end | |
| 19 | Hindi call (optional) | Set language_to_speak = Hindi, answer in Hindi | Agent stays in Hindi | |
| 20 | Skipped question | Ask a diversion question, don't answer one checklist item | Agent comes back and asks the skipped item before handoff | |
