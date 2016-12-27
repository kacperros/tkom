from Model.World import World
from Model.Event import Event
from Model.Event import EventType
from Model.SymbolsTable import SymbolsTable
import unittest


class WorldTests(unittest.TestCase):
    def setUp(self):
        self.world = World()
        self.world.add_currency('American Dolar', 'USD', 0)
        self.world.add_stock('CocaCola', 0, 0)
        self.world.set_start_date('2016.05.09')
        self.world.add_currency_rate(0, '2016.05.09', 150.0)
        self.world.add_currency_rate(0, '2016.05.10', 50.0)
        self.world.add_stock_price(0, '2016.05.09', 50.0)
        self.world.add_stock_price(0, '2016.05.10', 55.0)

    def tearDown(self):
        self.world = None

    def test_getCorrectCurrency(self):
        self.assertEqual(self.world.get_currency_rate_now(0), 150.0)
        self.assertEqual(self.world.get_currency_rate(0, '2016.05.09'), 150.0)

    def test_getNonExistingCurrency(self):
        try:
            self.world.get_currency_rate_now(1)
            self.fail()
        except ValueError:
            self.assertEqual(1, 1)

    def test_nextDay(self):
        self.world.next_day()
        self.assertEqual(self.world.get_currency_rate_now(0), 50.0)
        self.assertEqual(self.world.get_currency_rate(0, '2016.05.09'), 150.0)
        self.assertEqual(self.world.get_currency_rate(0, '2016.05.10'), 50.0)

    def test_getCorrectStock(self):
        self.assertEqual(self.world.get_stock_price_now(0), 50.0)
        self.assertEqual(self.world.get_stock_price(0, '2016.05.09'), 50.0)

    def test_getNonExistingStock(self):
        try:
            self.world.get_stock_price_now(1)
            self.fail()
        except ValueError:
            self.assertEqual(1, 1)

    def test_nextDayStock(self):
        self.world.next_day()
        self.assertEqual(self.world.get_stock_price_now(0), 55.0)
        self.assertEqual(self.world.get_stock_price(0, '2016.05.09'), 50.0)
        self.assertEqual(self.world.get_stock_price(0, '2016.05.10'), 55.0)


if __name__ == '__main__':
    unittest.main()
