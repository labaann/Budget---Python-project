from income import *
from outcome import *
from category import *
import datetime as dt

class Budget:
    def __init__(self):
        self.incomes = []
        self.outcomes = []
        self.zarobki = Category("zarobki")
        self.kredyt = Category("kredyt")
        self.pozyczka = Category("pozyczka")
        self.czynsz = Category("czynsz", 1)
        self.zywność = Category("zywność", 1)
        self.rozrywka = Category("rozrywka", 2)
        self.inne = Category("inne", 2)
        self.o_categories = {self.czynsz: 2000, self.zywność: 800, self.rozrywka: 500, self.inne: 300}

    def show_incomes(self):
        print("PLANNED INCOMES:")
        for i in self.incomes:
            if i.get_start_date() > dt.date.today():
                print(i)
        print("")
        print("ACTUAL INCOMES:")
        for i in self.incomes:
            if i.get_start_date() <= dt.date.today():
                print(i)

    def show_outcomes(self):
        print("PLANNED OUTCOMES:")
        ctr = 0
        for o in self.outcomes:
            if o.get_start_date() > dt.date.today():
                print(o)
                ctr += 1
        print("")
        print("ACTUAL OUTCOMES:")
        for o in self.outcomes:
            if o.get_start_date() <= dt.date.today():
                print(o)

    def get_limit(self, category):
        if not isinstance(category, Category):
            raise TypeError("The argument category should be a Category.")
        return self.o_categories[category]
    
    def check_category(self, category):
        if not isinstance(category, Category):
            raise TypeError("The argument category should be a Category.")
        sum = 0
        for outcome in self.outcomes:
            if outcome.category == category:
                sum += outcome.value
        return sum
    
    def set_limit(self, category, limit):
        if not isinstance(category, Category):
            raise TypeError("The argument category should be a Category.")
        if limit < self.check_category(category):
            raise ValueError("The limit cannot be lower than the sum of expenses in this category.")
        self.o_categories[category] = limit

    def add_income(self, income):
        if not isinstance(income, PlannedIncome):
            raise TypeError("The argument income should be a PlannedIncome or ActualIncome.")

        if isinstance(income, ActualIncome):
            if income.get_planned() in self.incomes:
                self.del_income(income.get_planned())
        self.incomes.append(income)
               
    def add_outcome(self, outcome):
        if not isinstance(outcome, PlannedOutcome):
            raise TypeError("The argument outcome should be a PlannedOutcome or ActualOutcome.")
        
        if isinstance(outcome, ActualOutcome):
            if outcome.get_planned() in self.outcomes:
                self.del_outcome(outcome.get_planned())
                self.outcomes.append(outcome)
    
        else:
            latest_outcome = outcome.start_date
            for o in self.outcomes:
                if o.get_start_date() > latest_outcome:
                    latest_outcome = o.get_start_date()
            if self.check_balance(latest_outcome) - outcome.get_value() < 0:
                if outcome.get_priority() == 1:
                    needed_money = 0
                    o_to_del = []
                    for o in self.outcomes:
                        if needed_money < outcome.get_value():
                            if o.get_start_date() >= outcome.get_start_date() and o.get_priority() > 1:
                                needed_money += o.get_value()
                                o_to_del.append(o)
                    if needed_money >= outcome.get_value():
                        for o in o_to_del:
                            self.del_outcome(o)
                            print('WARNING! {} must have been deleted.'.format(o))
                    else:
                        raise ValueError("Insufficient funds!")
                else:      
                    raise ValueError("Insufficient funds!")
            else:
                if self.check_category(outcome.category) + outcome.get_value() > self.o_categories[outcome.category]:
                    raise ValueError("Limit in this category has been exceeded!")
            self.outcomes.append(outcome)
                    
    def del_income(self, income):
        if not isinstance(income, PlannedIncome):
            raise TypeError("The argument income should be a PlannedIncome or ActualIncome.")
        self.incomes.remove(income)
    
    def del_outcome(self, outcome):
        if not isinstance(outcome, PlannedOutcome):
            raise TypeError("The argument outcome should be a PlannedOutcome or ActualOutcome.")
        self.outcomes.remove(outcome)

    def check_balance(self, date):
        if not isinstance(date, dt.date):
            raise TypeError("The argument date should be a Date.")
        sum_incomes = 0
        sum_outcomes = 0
        for income in self.incomes:
            if income.start_date <= date:
                sum_incomes += income.value
        for outcome in self.outcomes:
            if outcome.start_date <= date:
                sum_outcomes += outcome.value
        return sum_incomes - sum_outcomes