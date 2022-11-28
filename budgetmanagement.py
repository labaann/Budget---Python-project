from income import *
from outcome import *
from category import *
from budget import *
from analysis import *
import datetime as dt
import matplotlib.pyplot as plt

class BudgetManagement():
    def __init__(self, access_path):
        self.ap = access_path
        self.budget = Budget()
        self.analysis = Analysis(self.budget)
    
    def decoder(self):
        catoutcomes = {"1": self.budget.czynsz, "2": self.budget.zywność, "3": self.budget.rozrywka, "4": self.budget.inne}
        catincomes = {"1": self.budget.zarobki, "2": self.budget.kredyt, "3": self.budget.pozyczka, "4": self.budget.inne}
        with open(self.ap, 'r', encoding='utf8') as f:
        
            for line in f.readlines():
                line = line.split()
                if line[0] == "set_limit":
                    self.budget.set_limit(catoutcomes[line[1]], float(line[2]))
                if line[0] == "add_income_N":
                    self.budget.add_income(PlannedIncome(line[1], dt.date(int(line[2]), int(line[3]), int(line[4])), catincomes[line[5]], float(line[6])))
                if line[0] == "add_income_Y":
                    self.budget.add_income(ActualIncome(line[1], dt.date(int(line[2]), int(line[3]), int(line[4])), self.budget.incomes[int(line[6])].category, float(line[5]), self.budget.incomes[int(line[6])])) 
                if line[0] == "add_outcome_N":
                    self.budget.add_outcome(PlannedOutcome(line[1], dt.date(int(line[2]), int(line[3]), int(line[4])), catoutcomes[line[5]], float(line[6])))
                if line[0] == "add_outcome_Y":
                    self.budget.add_outcome(ActualOutcome(line[1], dt.date(int(line[2]), int(line[3]), int(line[4])), self.budget.outcomes[int(line[6])].category, float(line[5]), self.budget.outcomes[int(line[6])]))
                if line[0] == "del_income":
                    self.budget.del_income(self.budget.incomes[int(line[1])])
                if line[0] == "del_outcome":
                    self.budget.del_outcome(self.budget.outcomes[int(line[1])])
    
    def initialize(self):
        catoutcomes = {"1": self.budget.czynsz, "2": self.budget.zywność, "3": self.budget.rozrywka, "4": self.budget.inne}
        catincomes = {"1": self.budget.zarobki, "2": self.budget.kredyt, "3": self.budget.pozyczka, "4": self.budget.inne}
        self.decoder()
        with open(self.ap, 'a', encoding='utf8') as f:
            while True:
                print('''
    ----------------------------------------
    SELECT OPERATION:
    ----------------------------------------
    1. check limits
    2. set limit
    3. show incomes
    4. show outcomes
    5. add income
    6. add outcome
    7. delete income
    8. delete outcome
    9. check balance for the indicated day
    10. show balance on a chart
    11. end
    ----------------------------------------
                ''')
                
                action = input()

                if action == "1":
                    print("Spending limits in each category:")
                    for cat in self.budget.o_categories:
                        print("{}: {}".format(cat.name, self.budget.o_categories[cat]))

                if action == "2":
                    print('''
        SELECT CATEGORY TO CHANGE LIMIT:
        1. czynsz
        2. zywność
        3. rozrywka
        4. inne
                    ''')
                    c = input()
                    l = float(input("New limit: "))
                    while l < 0:
                        print("The limit value cannot be negative.")
                        l = float(input("New limit: "))
                    self.budget.set_limit(catoutcomes[c], l)
                    f.write("set_limit {} {}\n".format(c, l))

                if action == "3":
                    self.budget.show_incomes()
                    
                if action == "4":
                    self.budget.show_outcomes()
                    
                if action == "5":
                    print("do you want to update a previously added income because actually it has a different value?")
                    x = input("Y - yes / N - no: ")
                    if x == "N":
                        print('''
    SELECT CATEGORY FOR NEW INCOME:
    1. zarobki
    2. kredyt
    3. pozyczka
    4. inne
                        ''')
                        c = input()
                    
                        n = input("Enter name: ")
                        print("Enter date: ")
                        y = int(input("Year: "))
                        m = int(input("Month: "))
                        day = int(input("Day: "))
                        d = dt.date(y, m, day)
                        v = input("Enter value: ")
                        income = PlannedIncome(n, d, catincomes[c], int(v))                        
                        self.budget.add_income(income)
                        f.write("add_income_N {} {} {} {} {} {} \n".format(n, y, m, day, c, v))

                    if x == "Y":
                        print("SELECT INCOME YOU WANT TO UPDATE:")
                        licznik = 0
                        for i in self.budget.incomes:
                            print("{}. {}".format(licznik, i))
                            licznik+=1
                        previous = input()
                        n = self.budget.incomes[int(previous)].name
                        d = self.budget.incomes[int(previous)].get_start_date()
                        v = input("Enter value: ")
                        date = str(dt.date(2021, 6, 10)).split("-")
                        income = ActualIncome(n, d, self.budget.incomes[int(previous)].category, int(v), self.budget.incomes[int(previous)])
                        self.budget.add_income(income)
                        f.write("add_income_Y {} {} {} {} {} {} \n".format(n, date[0], date[1], date[2], v, previous))
                        
                if action == "6":
                    print("Do you want to update a previously added outcome because actually it has a different value?")
                    x = input("Y - yes / N - no: ")
                    if x == "N":
                        print('''
        SELECT CATEGORY FOR NEW OUTCOME:
        1. czynsz
        2. zywność
        3. rozrywka
        4. inne
                        ''')
                        c = input()

                        n = input("Name: ")
                        y = int(input("Year: "))
                        m = int(input("Month: "))
                        day = int(input("Day: "))
                        d = dt.date(y, m, day)
                        v = input("Value: ")
                        outcome = PlannedOutcome(n, d, catoutcomes[c], int(v))                        
                        self.budget.add_outcome(outcome)
                        f.write("add_outcome_N {} {} {} {} {} {} \n".format(n, y, m, day, c, v))
                        

                    if x == "Y":
                        print("SELECT OUTCOME YOU WANT TO UPDATE:")
                        n = 0
                        for i in self.budget.outcomes:
                            print("{}. {}".format(n, i))
                            n+=1
                        previous = input()
                        n = self.budget.outcomes[int(previous)].name
                        d = self.budget.outcomes[int(previous)].get_start_date()
                        v = input("Enter value: ")
                        date = str(dt.date(2021, 6, 10)).split("-")
                        outcome = ActualOutcome(n, d, self.budget.outcomes[int(previous)].category, int(v), self.budget.outcomes[int(previous)])                   
                        self.budget.add_outcome(outcome)
                        f.write("add_outcome_Y {} {} {} {} {} {} \n".format(n, date[0], date[1], date[2], v, previous))
                        
                if action == "7":
                    print("SELECT INCOME YOU WANT TO DELETE:")
                    n = 0
                    for i in self.budget.incomes:
                        print("{}. {}".format(n, i))
                        n+=1
                    d = input()
                    self.budget.del_income(self.budget.incomes[int(d)])
                    f.write("del_income {} \n".format(d))
                
                if action == "8":
                    print("SELECT OUTCOME YOU WANT TO DELETE:")
                    n = 0
                    for i in self.budget.outcomes:
                        print("{}. {}".format(n, i))
                        n+=1
                    d = input()
                    self.budget.del_outcome(self.budget.outcomes[int(d)])
                    f.write("del_outcome {} \n".format(d))

                if action == "9":
                    print("Enter date: ")
                    y = int(input("Year: ")) 
                    m = int(input("Month: "))
                    day = int(input("Day: "))
                    d = dt.date(y, m, day)
                    print("Balance for {} is: {}.".format(d, self.analysis.get_planned_balance(d)))
                
                if action == "10":
                    print("Enter start date: ")
                    y1 = int(input("Year: ")) 
                    m1 = int(input("Month: "))
                    day1 = int(input("Day: "))
                    d1 = dt.date(y1, m1, day1)
                    print("Enter end date: ")
                    y2 = int(input("Year: ")) 
                    m2 = int(input("Month: "))
                    day2 = int(input("Day: "))
                    d2 = dt.date(y2, m2, day2)
                    self.analysis.plot_balance(d1, d2)
                
                if action == "11":
                    print("Thank you for today :)")
                    break


if __name__=="__main__":
    Budzet2021 = BudgetManagement('/Users/ania/Desktop/Python 2/Projekt/budzetANIA.txt')
    print(Budzet2021.initialize())