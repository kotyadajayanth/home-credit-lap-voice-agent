# My Approach

## 1. How I understood the problem
The agent must call an existing customer, check a few eligibility points, and either
disqualify, transfer, or hand over to a senior loan expert. The hard part is not asking
questions, it is remembering answers and handling the unexpected.

## 2. Steps I followed
1. Read the assignment and wrote down every rule (property type, ownership, documents,
   loan amount, income, market value, tenure).
2. Marked the special cases: busy customer, existing loan / EMI reduction, loan above 75 lakh.
3. Wrote the rules as small Python functions (src/rules.py) so I could test them quickly.
4. Wrote the system prompt in sections (prompts/system_prompt.txt).
5. Wrote a small demo (src/demo.py) to check the "first missing question" logic.
6. Tested the prompt with different customer scenarios on the voice platform.
7. Fixed the prompt wherever the agent behaved wrongly.

## 3. Main design ideas in the prompt
- **First missing question:** after every reply the agent extracts all facts, checks rules,
  then asks only the first unanswered item. This handles out-of-order answers.
- **Immediate disqualification:** agricultural property, no original documents, cash income,
  tenure outside 3-15 years.
- **Loan above 75 lakh is not a fail:** the agent explains the limit and asks to proceed with 75 lakh.
- **Transfer switch:** existing loan on the same property or EMI reduction -> transfer message -> end.
- **Handoff gate:** no handoff until all 7 items are answered.
- **No made-up information:** no interest rate, no minimum market value (not in the assignment).
- **Voice style:** short replies, one question at a time, no markdown, amounts spoken naturally.
- **Variables:** every variable from the assignment is used, nothing is hard coded (name, gender, language).

## 4. Assumptions I made
- "Original documents available at home" counts as available.
- Occupation and income mode count as one checklist item (as in the assignment).
- A loan on a different property or product is not a transfer case.
- If a customer says "no" to the 75 lakh amount, the call ends politely.

## 5. Problems I faced and fixes
(Write your own here after testing. Example: "Agent asked ownership again after I already said
'jointly owned'. I added the EXTRACT and STORE steps to fix it.")

## 6. What I would improve with more time
- Test more Hindi calls.
- Add more examples for unclear answers.
- Connect real product knowledge using the RAG variable.
