import pandas as pd
from datetime import date


class Mortgage():

    DEFAULT_WIBOR = 0.03
    DEFAULT_COMMISION = 0.02
    DEFAULT_INTEREST_RATE = DEFAULT_WIBOR + DEFAULT_COMMISION
    DEFAULT_START_DATE = pd.Timestamp.today().date()
    DEFAULT_START_DATE = DEFAULT_START_DATE.replace(
        month=DEFAULT_START_DATE.month + 1, day=1
        )

    def __init__(self, 
                 loan_amount,
                 loan_term,
                 start_date=DEFAULT_START_DATE,
                 interest_rate=DEFAULT_INTEREST_RATE,
                 ):
        self.loan_amount = loan_amount
        self.loan_term = loan_term
        self.start_date = start_date
        self.interest_rate = interest_rate
        self._set_initial_states()

    def __repr__(self):
        return (f"Mortgage("
                f"\n\tloan_amount={self.loan_amount},"
                f"\n\tloan_term={self.loan_term},"
                f"\n\tstart_date={self.start_date},"
                f"\n\tinterest_rate={self.interest_rate}\n)")

    def _set_initial_states(self):
        self.current_period = 0
        self.principal_payment = 0
        self.interest_payment = 0
        self.total_paid = 0
        self.balance = self.loan_amount
        self.date = self.start_date.replace(month=self.start_date.month + 1)
        self._create_schedule()

    def _create_schedule(self):
        columns = ['period', 'balance', 'payment', 'principal_payment',
                   'interest_payment', 'total_paid']
        self.schedule = pd.DataFrame(columns=columns)
        self._fill_schedule()

    def _fill_schedule(self):
        new_row = [self.current_period, self.balance, self.payment,
                   self.principal_payment, self.interest_payment,
                   self.total_paid]
        self.schedule.loc[len(self.schedule)] = new_row
        self.schedule.period = self.schedule.period.astype(int)

    @property
    def payment(self):
        return self.principal_payment + self.interest_payment

    @property
    def periods_left(self):
        total_periods = 12 * self.loan_term
        return total_periods - self.current_period

    def next_periods(self, n):
        for _ in range(n):
            self.next_month()

    def next_month(self):
        self.principal_payment = self._calculate_principal_payment()
        self.interest_payment = self._calculate_interest_payment()
        self.total_paid = self._calculate_total_paid()
        self.balance = self._calculate_balance()
        self.current_period += 1
        self._fill_schedule()

    def _calculate_total_paid(self):
        return self.total_paid + self.payment

    def _calculate_balance(self):
        return self.balance - self.principal_payment

    def _calculate_interest_payment(self):
        return (self.balance * self.interest_rate) / 12

    def _calculate_principal_payment(self):
        return self.balance / self.periods_left
