import unittest
import Parser.RuleParser
import Utils.DateConverter as dC
from Model.SymbolsTable import SymbolsTable
from Model.Currency import Currency
from Model.Stock import Stock
from Model.Event import Event
from Model.Event import EventType
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
        controller.world.current_day = dC.to_date('2016.05.16')
        controller.world.add_currency(Currency('yuan', 'YUA', 0))
        controller.world.add_currency(Currency('usa dollar', 'USD', 1))
        controller.add_event(Event(EventType.CURRENCY, '2016.05.16', 0, 500))
        Parser.RuleParser.parse_from_lexer(lexer, symbol_table, controller)


if __name__ == '__main__':
    unittest.main()