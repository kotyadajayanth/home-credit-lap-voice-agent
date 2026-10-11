# test_rules.py
# Run from the project folder:  python -m unittest discover tests
import sys
import os
import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))
import rules
import demo


class TestRules(unittest.TestCase):

    def test_property_type(self):
        self.assertEqual(rules.check_property_type("residential"), "ok")
        self.assertEqual(rules.check_property_type("commercial"), "ok")
        self.assertEqual(rules.check_property_type("industrial"), "ok")
        self.assertEqual(rules.check_property_type("agricultural"), "fail")

    def test_ownership(self):
        self.assertEqual(rules.check_ownership("sole"), "ok")
        self.assertEqual(rules.check_ownership("joint"), "ok")

    def test_documents(self):
        self.assertEqual(rules.check_documents(True), "ok")
        self.assertEqual(rules.check_documents(False), "fail")

    def test_loan_amount(self):
        self.assertEqual(rules.check_loan_amount(5000000), "ok")
        self.assertEqual(rules.check_loan_amount(7500000), "ok")
        self.assertEqual(rules.check_loan_amount(9000000), "ask_max")

    def test_income(self):
        self.assertEqual(rules.check_income("salaried", "bank"), "ok")
        self.assertEqual(rules.check_income("self-employed", "bank"), "ok")
        self.assertEqual(rules.check_income("salaried", "cash"), "fail")
        self.assertEqual(rules.check_income("self-employed", "cash"), "fail")

    def test_tenure(self):
        self.assertEqual(rules.check_tenure(2), "fail")
        self.assertEqual(rules.check_tenure(3), "ok")
        self.assertEqual(rules.check_tenure(10), "ok")
        self.assertEqual(rules.check_tenure(15), "ok")
        self.assertEqual(rules.check_tenure(16), "fail")


class TestDemoExtraction(unittest.TestCase):

    def test_out_of_order_answers(self):
        state = {}
        demo.extract("It's a residential house worth about 1.2 crore, jointly owned with my wife",
                     state, "property_type")
        self.assertEqual(state["property_type"], "residential")
        self.assertEqual(state["ownership"], "joint")
        self.assertEqual(state["market_value"], 12000000)
        # next question should be documents, not ownership or market value
        self.assertEqual(demo.next_missing(state), "documents")

    def test_correction_latest_wins(self):
        state = {}
        demo.extract("it's residential... actually no, it's agricultural", state, "property_type")
        self.assertEqual(state["property_type"], "agricultural")
        self.assertIsNotNone(demo.find_problem(state))

    def test_transfer_detection(self):
        self.assertTrue(demo.is_transfer("I already have a loan on this property"))
        self.assertTrue(demo.is_transfer("I want to reduce my EMI"))
        self.assertFalse(demo.is_transfer("It is a residential flat"))

    def test_cash_income(self):
        state = {}
        demo.extract("I run a business and get paid in cash", state, "occupation")
        self.assertIsNotNone(demo.find_problem(state))


if __name__ == "__main__":
    unittest.main()
