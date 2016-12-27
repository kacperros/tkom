import unittest
import Parser.EventsParser as eP
from Model.SymbolsTable import SymbolsTable


class EventParserTests(unittest.TestCase):

    def test_getCorrectEvents(self):
        symbol_table = SymbolsTable()
        symbol_table.add_stock('CocaCola')
        result = eP.parse_file('events.xml', symbol_table)
        self.assertEqual(len(result), 1)


if __name__ == '__main__':
    unittest.main()