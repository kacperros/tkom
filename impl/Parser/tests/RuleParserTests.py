import unittest
import Parser.RuleParser
from Model.SymbolsTable import SymbolsTable
from Lexers.Lexer import Lexer
from Engine.RealityController import RealityController


class EventParserTests(unittest.TestCase):

    def test_getCorrectEvents(self):
        symbol_table = SymbolsTable()
        symbol_table.add_currency('YUA')
        symbol_table.add_currency('USD')
        symbol_table.add_stock('CocaCola')
        symbol_table.add_stock('NukaCola')
        parsed_file = open("rule.txt")
        lexer = Lexer(parsed_file)
        controller = RealityController()
        Parser.RuleParser.parse_from_lexer(lexer, symbol_table, controller)


if __name__ == '__main__':
    unittest.main()