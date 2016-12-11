from Lexers.KeywordsLexer import *
from Lexers.GivenNameLexer import *
from Lexers.NumberLexer import *
from Lexers.OtherCharLexer import *
from Lexers.WhitespaceLexer import *


class Lexer:
    def __init__(self, parsed_file):
        self.parsed_file = parsed_file
        self.lexers = [KeywordsLexer(self.parsed_file),
                       GivenNameLexer(self.parsed_file),
                       NumberLexer(self.parsed_file),
                       OtherCharLexer(self.parsed_file),
                       WhitespaceLexer(self.parsed_file)]

    def get_token(self):
        while True:
            curr_pos = self.parsed_file.tell()
            curr_char = self.parsed_file.read(1)
            if curr_char == "" or curr_char == -1:
                return -1
            else:
                selected_lexer = self.choose_lexer(curr_char)
                self.parsed_file.seek(curr_pos, 0)
                return selected_lexer.get_token()

    def choose_lexer(self, curr_char):
        for lexer in self.lexers:
            if lexer.is_applicable(curr_char):
                return lexer
        raise ValueError("Blood Hell, Sir, no lexers found!!!")

