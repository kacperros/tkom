from Model.World import World
from Model.Event import Event
from Model.Event import EventType
from Model.SymbolsTable import SymbolsTable
import unittest


class WorldTests(unittest.TestCase):
    def setUp(self):
        symbol_table = SymbolsTable()
        self.world = World(symbol_table)
        self.world.add_currency('American Dolar', 'USD')
        self.world.add_stock('CocaCola', 'USD')
        self.world.set_start_date('2016.05.09')
        self.world.add_event(Event(EventType.STOCK, '2016.05.09', 'CocaCola', 50.0))
        self.world.add_event(Event(EventType.STOCK, '2016.05.10', 'CocaCola', 55.0))
        self.world.add_event(Event(EventType.CURRENCY, '2016.05.09', 'USD', 150.0))
        self.world.add_event(Event(EventType.CURRENCY, '2016.05.10', 'USD', 50.0))

    def tearDown(self):
        self.world = None

    def test_getCorrectCurrency(self):
        self.assertEqual(self.world.get_currency_rate_now('USD'), 150.0)
        self.assertEqual(self.world.get_currency_rate('USD', '2016.05.09'), 150.0)

    def test_getNonExistingCurrency(self):
        try:
            self.world.get_currency_rate_now('EUR')
            self.fail()
        except ValueError:
            self.assertEqual(1, 1)

    def test_nextDay(self):
        self.world.next_day()
        self.assertEqual(self.world.get_currency_rate_now('USD'), 50.0)
        self.assertEqual(self.world.get_currency_rate('USD', '2016.05.09'), 150.0)
        self.assertEqual(self.world.get_currency_rate('USD', '2016.05.10'), 50.0)

    def test_getCorrectStock(self):
        self.assertEqual(self.world.get_stock_price_now('CocaCola'), 50.0)
        self.assertEqual(self.world.get_stock_price('CocaCola', '2016.05.09'), 50.0)

    def test_getNonExistingStock(self):
        try:
            self.world.get_stock_price_now('NukaCola')
            self.fail()
        except ValueError:
            self.assertEqual(1, 1)

    def test_nextDayStock(self):
        self.world.next_day()
        self.assertEqual(self.world.get_stock_price_now('CocaCola'), 55.0)
        self.assertEqual(self.world.get_stock_price('CocaCola', '2016.05.09'), 50.0)
        self.assertEqual(self.world.get_stock_price('CocaCola', '2016.05.10'), 55.0)


if __name__ == '__main__':
    unittest.main()
