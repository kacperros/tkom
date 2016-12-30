from Engine.RealityController import RealityController
from Lexers.Lexer import Lexer
from Model.SymbolsTable import SymbolsTable
from Parser.MainParser import MainParser
import Engine.RealityPrinter as printer


class Engine:
    def __init__(self, date_start, date_end, parsed_file):
        self.start_date = date_start
        self.end_date = date_end
        self.parsed_file = parsed_file
        self.reality_control = None
        self.symbol_table = None

    def invest(self):
        lexer = Lexer(self.parsed_file)
        self.reality_control = RealityController()
        self.symbol_table = SymbolsTable()
        self.reality_control.world.set_start_date(self.start_date)
        parser = MainParser(self.reality_control, lexer, self.symbol_table)
        parser.parse()
        self.reality_control.run_reality(self.start_date, self.end_date)
        printer.print_reality(self.reality_control, self.symbol_table)
