from unittest import TestCase
from copy import copy

from mortgage import Mortgage


class TestMortage(TestCase):

    loan_amount = 300_000
    loan_term = 30
    m = Mortgage(loan_amount, loan_term)
    m2 = copy(m)
    m2.next_month()
    m2.next_month()
    df = m2.schedule

    def test_initial_schedule(self):
        expected_list = [0, self.loan_amount, 0, 0, 0, 0]
        actual_list = self.m.schedule.values.tolist()[0]
        self.assertListEqual(actual_list, expected_list)

    def test_initial_total_paid(self):
        self.assertEqual(self.m.total_paid, 0)

    def test_initial_balance(self):
        self.assertEqual(self.m.balance, self.loan_amount)
    
    def test_balance(self):
        unique_values = len(self.df.balance.unique())
        self.assertEqual(unique_values, 3)
    
    def test_total_paid(self):
        unique_values = len(self.df.total_paid.unique())
        self.assertEqual(unique_values, 3)
    
    def test_principal_payment(self):
        unique_values = len(self.df.principal_payment.unique())
        self.assertEqual(unique_values, 2)
    
    def test_interest_payment(self):
        unique_values = len(self.df.interest_payment.unique())
        self.assertEqual(unique_values, 3)

    def _test(self):
        m = Mortgage(loan_amount, loan_term)
        m.schedule
        m.next_periods(360)
        m.next_month()
        m.schedule

