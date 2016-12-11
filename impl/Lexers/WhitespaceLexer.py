from Lexers.abstractStateLexer import AbstractStateLexer
import string
from decimal import *
from Lexers.tokens import *


class WhitespaceLexer(AbstractStateLexer):
    def __init__(self, parsed_file):
        super().__init__(parsed_file)
        self.allowed_chars = list(string.whitespace)

    def is_applicable(self, starting_char):
        return starting_char in self.allowed_chars

    def get_token(self):
        curr_string = ""
        while True:
            curr_pos = self.parsed_file.tell()
            curr_char = self.parsed_file.read(1)
            if curr_char == -1 or curr_char == '':
                return Token(TokenType.whitespace, curr_string)
            if curr_char in self.allowed_chars:
                curr_string = curr_string + curr_char
            else:
                self.parsed_file.seek(curr_pos, 0)
                return Token(TokenType.whitespace, curr_string)