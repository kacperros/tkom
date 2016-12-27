import unittest
import Parser.RuleParser
from Model.SymbolsTable import SymbolsTable
from Lexers.Lexer import Lexer


class EventParserTests(unittest.TestCase):

    def test_getCorrectEvents(self):
        parsed_file = open("rule.txt")
        lexer = Lexer(parsed_file)
        Parser.RuleParser.parse_from_lexer(lexer)


if __name__ == '__main__':
    unittest.main()