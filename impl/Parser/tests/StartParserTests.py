import unittest
import Parser.StartParser as sP
from Model.SymbolsTable import SymbolsTable


class StartParserTests(unittest.TestCase):

    def test_getCorrectEvents(self):
        symbol_table = SymbolsTable()
        symbol_table.add_stock('CocaCola')
        symbol_table.add_currency('USD')
        result = sP.parse_file('start.xml', symbol_table)
        self.assertEqual(len(result), 2)


if __name__ == '__main__':
    unittest.main()