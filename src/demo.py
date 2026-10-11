# demo.py
# A very small offline demo of the LOGIC behind my system prompt.
# It is NOT the voice agent. It only shows the "first missing question" idea:
#   extract -> check disqualify -> check transfer -> ask first unanswered item
# Run:  python src/demo.py

import re
import rules

QUESTIONS = {
    "property_type": "What type of property is it - residential, commercial or industrial?",
    "ownership": "Is the property solely owned by you, or jointly owned?",
    "documents": "Do you have the original property documents available for verification?",
    "loan_amount": "How much loan amount are you looking for?",
    "occupation": "Are you salaried or self-employed?",
    "income_mode": "And is your income received in your bank account or in cash?",
    "market_value": "Approximately what is the current market value of the property?",
    "tenure": "In how many years would you like to repay the loan?",
}

# order of the checklist (occupation + income_mode count as one item in the assignment)
ORDER = ["property_type", "ownership", "documents", "loan_amount",
         "occupation", "income_mode", "market_value", "tenure"]


def get_amount(text):
    # reads things like "50 lakh", "1.2 crore", "90 lakhs"
    match = re.search(r"(\d+(\.\d+)?)\s*(lakh|lakhs|crore|crores|cr|l)\b", text)
    if not match:
        return None
    number = float(match.group(1))
    unit = match.group(3)
    if unit.startswith("c"):
        return int(number * 10000000)
    return int(number * 100000)


def extract(text, state, asked):
    # pull out every fact we can find in the customer's sentence
    text = text.lower()

    # property type (latest mention wins, so check agricultural last)
    for p in ["residential", "commercial", "industrial", "agricultural"]:
        if p in text:
            state["property_type"] = p
    if "house" in text or "flat" in text:
        state["property_type"] = "residential"
    if "shop" in text or "office" in text:
        state["property_type"] = "commercial"
    if "factory" in text:
        state["property_type"] = "industrial"

    # ownership
    if "joint" in text or "wife" in text or "husband" in text or "brother" in text:
        state["ownership"] = "joint"
    elif "sole" in text or "my own" in text or "only me" in text:
        state["ownership"] = "sole"

    # documents
    if "photocopy" in text or "photocopies" in text or "no documents" in text:
        state["documents"] = False
    elif "original" in text:
        state["documents"] = True

    # occupation and income
    if "self-employed" in text or "self employed" in text or "business" in text:
        state["occupation"] = "self-employed"
    elif "salaried" in text or "job" in text:
        state["occupation"] = "salaried"
    if "cash" in text:
        state["income_mode"] = "cash"
    elif "bank" in text:
        state["income_mode"] = "bank"

    # amounts: if the text says "worth"/"value" it is market value,
    # otherwise use whatever question we just asked
    amount = get_amount(text)
    if amount is not None:
        if "worth" in text or "value" in text or asked == "market_value":
            state["market_value"] = amount
        else:
            state["loan_amount"] = amount

    # tenure
    match = re.search(r"(\d+)\s*(year|years|yrs|yr)", text)
    if match:
        state["tenure"] = int(match.group(1))


def find_problem(state):
    # returns a message if something fails, else None
    if "property_type" in state and rules.check_property_type(state["property_type"]) == "fail":
        return "The property is not eligible type."
    if "documents" in state and rules.check_documents(state["documents"]) == "fail":
        return "Original documents are needed."
    if "income_mode" in state and state["income_mode"] == "cash":
        return "Income must come to the bank."
    if "tenure" in state and rules.check_tenure(state["tenure"]) == "fail":
        return "Tenure must be between 3 and 15 years."
    return None


def is_transfer(text):
    words = ["existing loan", "already have a loan", "reduce my emi",
             "reduce emi", "lower emi", "balance transfer", "already have loan"]
    text = text.lower()
    for w in words:
        if w in text:
            return True
    return False


def next_missing(state):
    for key in ORDER:
        if key not in state:
            return key
    return None


def main():
    print("Agent: Hello, am I speaking with the customer? Is this a good time to talk?")
    state = {}
    asked = None
    busy = input("You: ").lower()
    if "busy" in busy or "meeting" in busy or "later" in busy:
        print("Agent: Sure, what time should I call you back?")
        input("You: ")
        print("Agent: Noted, thank you. Bye!")
        return

    print("Agent: We have a special Loan Against Property offer of up to 75 lakhs for you.")
    print("Agent: Let me ask a few quick questions.")

    while True:
        # ask the first missing item
        asked = next_missing(state)
        if asked is None:
            break
        print("Agent:", QUESTIONS[asked])
        text = input("You: ")

        if is_transfer(text):
            print("Agent: A loan transfer specialist will contact you shortly. Thank you!")
            return

        extract(text, state, asked)

        problem = find_problem(state)
        if problem:
            print("Agent: Sorry, you do not meet the criteria for this offer at this time. Thank you!")
            print("(reason for testing:", problem + ")")
            return

        # loan more than 75 lakh -> offer max amount
        if "loan_amount" in state and rules.check_loan_amount(state["loan_amount"]) == "ask_max":
            print("Agent: The offer is up to 75 lakhs. Would you like to go ahead with 75 lakhs?")
            answer = input("You: ").lower()
            if "yes" in answer or "ok" in answer or "haan" in answer:
                state["loan_amount"] = rules.MAX_LOAN
            else:
                print("Agent: No problem, thank you for your time!")
                return

    print("Agent: Thank you! A senior loan expert will call you back shortly with exact interest rates.")
    print("(collected data:", state, ")")


if __name__ == "__main__":
    main()
