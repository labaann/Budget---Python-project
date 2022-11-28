from income import *
from outcome import *
from category import *
from budget import *
from analysis import *
import datetime as dt
import unittest as ut

class TestCategory(ut.TestCase):
    def setUp(self):
        self.values = Category("zakupy", 3)
    
    def test_get_priority(self):
        self.assertEqual(self.values.get_priority(), 3)
        self.assertIsInstance(self.values.get_priority(), int)
       
    def test_set_priority(self):
        self.values.set_priority(4)
        self.assertEqual(self.values.get_priority(), 4)


class TestIncome(ut.TestCase):
    def setUp(self):
        self.values_p = PlannedIncome("wypłata01", dt.date(2020,1,3), Category("praca"), 1800)
        self.values_a = ActualIncome("wypłata01", dt.date(2020,1,3), Category("praca"), 2000, self.values_p)

    def test_check_with_planned(self):
        self.assertEqual(self.values_a.check_with_planned(), -200)
    

class TestOutcome(ut.TestCase):
    def setUp(self):
        self.values_p = PlannedOutcome("prąd", dt.date(2020,5,12), Category("czynsz"), 700)
        self.values_a = ActualOutcome("prąd", dt.date(2020,5,12), Category("czynsz"), 650, self.values_p)

    def test_check_with_planned(self):
        self.assertEqual(self.values_a.check_with_planned(), 50)
    

class TestBudget(ut.TestCase):
    def setUp(self):
        self.values = Budget()
        self.values.set_limit(self.values.inne, 1500)
        self.values.add_income(PlannedIncome("prezent", dt.date(2020,2,11), self.values.inne, 400))
        self.values.add_income(PlannedIncome("wypłata", dt.date(2020,1,10), self.values.zarobki, 1800))
        self.values.add_outcome(PlannedOutcome("urodziny", dt.date(2020,2,16), self.values.rozrywka, 360))
    
    def test_set_limit(self):
        self.assertEqual(self.values.o_categories[self.values.inne], 1500)
        self.assertFalse(self.values.o_categories[self.values.inne] == 0)

    def test_get_limit(self):
        self.assertEqual(self.values.get_limit(self.values.inne), 1500)
    
    def test_check_category(self):
        self.assertEqual(self.values.check_category(self.values.rozrywka), 360)

    def test_add_income(self):
        with self.assertRaises(TypeError):
            self.values.add_income("prezent od babci")
        
    def test_add_outcome(self):
        with self.assertRaises(ValueError):
            self.values.add_outcome(PlannedOutcome("spa", dt.date(2020,12,4), self.values.inne, 2000)) 
        with self.assertRaises(TypeError):
            self.values.add_outcome("spa")
    
    def test_del_income(self):
        with self.assertRaises(TypeError):
            self.values.del_income("hhh")
        with self.assertRaises(ValueError):
            self.values.del_income(PlannedIncome("bigos_sprzedaz",dt.date(2020,1,3),self.values.zywność, 100))

    def test_del_outcome(self):
        with self.assertRaises(TypeError):
            self.values.del_outcome("jjj")
        with self.assertRaises(ValueError):
            self.values.del_outcome(PlannedOutcome("jajka",dt.date(2020,1,3),self.values.zywność, 10))

    def test_check_balance(self):
        self.assertEqual(self.values.check_balance(dt.date(2021,12,31)), 1840)
        self.assertFalse(self.values.check_balance(dt.date(2021,12,31)) == 0)

class TestAnalysis(ut.TestCase):
    def setUp(self):
        self.values = Budget()
        self.analysis = Analysis(self.values)
        self.p_income = PlannedIncome("sprzedaz_krowy", dt.date(2021, 4, 30), self.values.inne, 3000)
        self.values.add_income(self.p_income)
        self.values.add_income(ActualIncome("sprzedaz_krowy", dt.date(2021, 4, 30), self.values.inne, 2500, self.p_income))

    def test_get_balance(self):
        self.assertEqual(self.analysis.get_balance(dt.date(2021, 4, 30)), 2500)
    
    def test_get_planned_balance(self):
        self.assertEqual(self.analysis.get_planned_balance(dt.date(2021,4,30)), 3000)


if __name__=="__main__":
    ut.main()