from category import *
import datetime as dt

class PlannedOutcome:
    def __init__(self, name, start_date, category, value=0):
        if not isinstance(category, Category):
            raise TypeError("The argument category should be a Category.")
        if not isinstance(start_date, dt.date):
            raise TypeError("The argument start_date should be a Date.")
        if value < 0:
            raise ValueError("Value cannot be less than zero.")
        self.name = name 
        self.start_date = start_date
        self.category = category
        self.value = value

    def __str__(self):
            return 'Outcome "{}", date: {}; category: {}; value: {} zł'.format(self.name, self.start_date, self.category.name, self.value)

    def get_start_date(self):
        return self.start_date

    def get_value(self):
        return self.value

    def get_category(self):
        return self.category
    
    def get_priority(self):
        return self.category.get_priority()
    
class ActualOutcome(PlannedOutcome):
    def __init__(self, name, start_date, category, value, planned=None):
        if start_date > dt.date.today():
            raise ValueError("Actual Outcome cannot be for a future date.")
        super().__init__(name, start_date, category, value=value)
        if not isinstance(planned, PlannedOutcome):
            raise TypeError("The argument planned should be a PlannedOutcome.")
        self.planned = planned
    
    def get_planned(self):
        return self.planned
    
    def check_with_planned(self):
        return self.planned.value - self.value