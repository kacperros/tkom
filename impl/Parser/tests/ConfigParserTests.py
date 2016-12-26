import unittest
import Parser.ConfigParser as cp


class CurrencyTests(unittest.TestCase):

    def test_getCorrectDate(self):
        result = cp.parse_file('config.xml')
        currencies = result['currencies']
        stocks = result['stocks']
        self.assertEqual(len(currencies), 3)
        self.assertEqual(currencies[0].name, 'yuan')
        self.assertEqual(currencies[0].abbreviation, 'YUA')
        self.assertEqual(len(stocks), 1)


if __name__ == '__main__':
    unittest.main()