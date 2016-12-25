from Model.Currency import Currency
import unittest


class CurrencyTests(unittest.TestCase):
    def setUp(self):
        self.currency = Currency('dolar amerykański', 'USD')
        self.currency.add_exchange_rate('2016.05.09', 20.0)
        self.currency.add_exchange_rate('2016.05.12', 25.0)

    def tearDown(self):
        self.currency = None

    def test_getCorrectDate(self):
        self.assertEqual(self.currency.get_exchange_rate('2016.05.09'), 20.0)

    def test_getDateUndefinedDataButInRange(self):
        self.assertEqual(self.currency.get_exchange_rate('2016.05.11'), 20.0)
        self.assertEqual(self.currency.get_exchange_rate('2016.06.12'), 25.0)

    def test_getDateUndefinedNotInRange(self):
        try:
            self.currency.get_exchange_rate('2015.05.11')
            self.assertEqual(1, 2)
        except ValueError:
            self.assertEqual(1, 1)

if __name__ == '__main__':
    unittest.main()