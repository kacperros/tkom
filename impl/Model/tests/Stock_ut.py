from Model.Stock import Stock
import unittest


class StockTests(unittest.TestCase):
    def setUp(self):
        self.stock = Stock('Amerykańska Coca Cola', 'Coke', 'USD')
        self.stock.add_exchange_price('2016.05.09', 20.0)
        self.stock.add_exchange_price('2016.05.12', 25.0)

    def tearDown(self):
        self.currency = None

    def test_getCorrectDate(self):
        self.assertEqual(self.stock.get_exchange_price('2016.05.09'), 20.0)

    def test_getDateUndefinedDataButInRange(self):
        self.assertEqual(self.stock.get_exchange_price('2016.05.11'), 20.0)
        self.assertEqual(self.stock.get_exchange_price('2016.06.12'), 25.0)

    def test_getDateUndefinedNotInRange(self):
        try:
            self.stock.get_exchange_price('2015.05.11')
            self.assertEqual(1, 2)
        except ValueError:
            self.assertEqual(1, 1)

if __name__ == '__main__':
    unittest.main()