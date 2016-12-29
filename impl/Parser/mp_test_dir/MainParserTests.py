import unittest

from Engine.RealityController import RealityController
from Lexers.Lexer import Lexer
from Model.SymbolsTable import SymbolsTable
from Parser.MainParser import MainParser


class MainParserTests(unittest.TestCase):

    def test_getCorrectProgram(self):
        parsed_file = open('program.txt')
        lexer = Lexer(parsed_file)
        engine = RealityController()
        symbol_table = SymbolsTable()
        engine.world.set_start_date('2016.05.11')
        parser = MainParser(engine, lexer, symbol_table)
        parser.parse()
        print("Done")


if __name__ == '__main__':
    unittest.main()