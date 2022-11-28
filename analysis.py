from income import *
from outcome import *
from category import *
from budget import *
import datetime as dt
import matplotlib.pyplot as plt

class Analysis:
    def __init__(self, budget):
        if not isinstance(budget, Budget):
            raise TypeError("The argument budget_plan should be a Budget.")
        self.budget = budget

    def get_balance(self, date):
        return self.budget.check_balance(date)

    def get_planned_balance(self, date):
        balance = self.get_balance(date)
        for i in self.budget.incomes:
            if isinstance(i, ActualIncome) and i.get_start_date() <= date:
                balance += i.check_with_planned()
        for o in self.budget.outcomes:
            if isinstance(o, ActualOutcome) and o.get_start_date() <= date:
                balance += o.check_with_planned()
        return balance

    def plot_balance(self, start, end):
        if end < start:
            raise ValueError("Invalid value, end date before start date.")
        if not isinstance(start, dt.date):
            raise TypeError("The argument start should be a Date.")
        if not isinstance(end, dt.date):
            raise TypeError("The argument end should be a Date.")
        x = start
        balance_a = []
        balance_p = []
        date = []
        while x < end:
            balance_a.append(self.get_balance(x))
            balance_p.append(self.get_planned_balance(x))
            date.append(x)
            x += dt.timedelta(1)
        plt.plot(date, balance_a)
        plt.plot(date, balance_p, "--")
        plt.xlabel("Date")
        plt.ylabel("[zł]")
        plt.title("Balance for each day")
        plt.legend(["Actual Balance", "Planned Balance"])
        plt.show()