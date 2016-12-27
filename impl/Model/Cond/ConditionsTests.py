from Model.Cond.ComparisonCondition import ComparisonCondition
from Model.Cond.MasterCondition import MasterCondition
from Model.Cond.TrendCondition import TrendCondition
import unittest

from Model.World import World
from Model.Currency import Currency
from Model.Stock import Stock
from Model.Investor import Investor


class WorldTests(unittest.TestCase):
    def setUp(self):
        self.world = World()
        self.world.add_currency(Currency('American Dolar', 'USD', 0))
        self.world.add_stock(Stock('CocaCola', 0, 0))
        self.world.set_start_date('2016.05.09')
        self.world.add_currency_rate(0, '2016.05.09', 150.0)
        self.world.add_currency_rate(0, '2016.05.10', 250.0)
        self.world.add_currency_rate(0, '2016.05.11', 255.0)
        self.world.add_currency_rate(0, '2016.05.12', 275.0)
        self.world.add_stock_price(0, '2016.05.09', 50.0)
        self.world.add_stock_price(0, '2016.05.10', 55.0)
        self.investor = Investor()
        self.investor.add_currency(0, 500)
        self.investor.add_stock(0, 300)

    def test_comparisonCond(self):
        self.world.next_day()
        cond = ComparisonCondition(False)
        cond.chosen_oper = cond.comparison_opers['<']
        cond.arg1_access_method = self.world.get_currency_rate
        cond.arg1_method_symbol_id = 0
        cond.arg1_method_date_str = '2016.05.09'
        cond.arg2_access_method = self.world.get_currency_rate_now
        cond.arg2_method_symbol_id = 0
        result = cond.eval()
        self.assertTrue(result)

    def test_comparisonCond2(self):
        self.world.next_day()
        cond = ComparisonCondition(False)
        cond.chosen_oper = cond.comparison_opers['<']
        cond.arg1 = 15
        cond.arg2_access_method = self.world.get_currency_rate_now
        cond.arg2_method_symbol_id = 0
        result = cond.eval()
        self.assertTrue(result)

    def test_masterCond(self):
        self.world.next_day()
        cond1 = ComparisonCondition(False)
        cond1.chosen_oper = cond1.comparison_opers['<']
        cond1.arg1_access_method = self.world.get_currency_rate
        cond1.arg1_method_symbol_id = 0
        cond1.arg1_method_date_str = '2016.05.09'
        cond1.arg2_access_method = self.world.get_currency_rate_now
        cond1.arg2_method_symbol_id = 0

        cond = ComparisonCondition(False)
        cond.chosen_oper = cond.comparison_opers['>']
        cond.arg1_access_method = self.world.get_currency_rate
        cond.arg1_method_symbol_id = 0
        cond.arg1_method_date_str = '2016.05.09'
        cond.arg2_access_method = self.world.get_currency_rate_now
        cond.arg2_method_symbol_id = 0

        master = MasterCondition()
        master.conditions = [cond1, cond]
        master.operators = ['&&']
        result = master.eval()
        self.assertFalse(result)
        master.operators = ['||']
        result = master.eval()
        self.assertTrue(result)

    def test_trendCond(self):
        self.world.next_day()
        self.world.next_day()
        self.world.next_day()
        cond = TrendCondition(self.world)
        cond.accessor_method = self.world.get_currency_rate
        cond.symbol_id = 0
        cond.number_of_days = 2
        cond.is_inc = True
        cond.growth_percent = 5
        res = cond.eval()
        self.assertTrue(res)
