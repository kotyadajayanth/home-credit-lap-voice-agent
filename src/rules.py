# rules.py
# Simple functions for the Home Credit LAP eligibility rules.
# Every function returns one of: "ok", "fail", or "ask_max" (only for loan amount)

MAX_LOAN = 7500000      # 75 lakh in rupees
MIN_TENURE = 3          # years
MAX_TENURE = 15         # years

ALLOWED_PROPERTY = ["residential", "commercial", "industrial"]
ALLOWED_OWNERSHIP = ["sole", "joint"]
ALLOWED_OCCUPATION = ["salaried", "self-employed"]


def check_property_type(property_type):
    # agricultural is the only one not allowed
    if property_type in ALLOWED_PROPERTY:
        return "ok"
    return "fail"


def check_ownership(ownership):
    # sole and joint are both fine
    if ownership in ALLOWED_OWNERSHIP:
        return "ok"
    return "fail"


def check_documents(has_original_documents):
    # True = original documents available, False = only photocopies / none
    if has_original_documents:
        return "ok"
    return "fail"


def check_loan_amount(amount):
    # more than 75 lakh is NOT a fail, agent should offer the max amount
    if amount <= MAX_LOAN:
        return "ok"
    return "ask_max"


def check_income(occupation, income_mode):
    if occupation not in ALLOWED_OCCUPATION:
        return "fail"
    if income_mode != "bank":
        return "fail"
    return "ok"


def check_tenure(years):
    if MIN_TENURE <= years <= MAX_TENURE:
        return "ok"
    return "fail"

# note: there is no rule for market value, the assignment gives no minimum
