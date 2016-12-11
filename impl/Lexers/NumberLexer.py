from Lexers.abstractStateLexer import AbstractStateLexer
import string
from decimal import *
from Lexers.tokens import *


class NumberLexer(AbstractStateLexer):
    def __init__(self, parsed_file):
        super().__init__(parsed_file)
        self.allowed_chars = list(string.digits)
        self.allowed_chars.append(".")
        self.allowed_chars.append("-")

    def is_applicable(self, starting_char):
        return starting_char in self.allowed_chars

    def get_token(self):
        curr_string = ""
        decimal_found = False
        while True:
            curr_pos = self.parsed_file.tell()
            curr_char = self.parsed_file.read(1)
            if curr_char == "." and not decimal_found:
                decimal_found = True
            elif curr_char == "." and decimal_found:
                raise ValueError("Sir, I am afraid two decimal points is one two many")
            if curr_char == -1 or curr_char == '':
                return Token(TokenType.number, self.to_number(curr_string, decimal_found))
            if curr_char in self.allowed_chars:
                curr_string = curr_string + curr_char
            else:
                self.parsed_file.seek(curr_pos, 0)
                return Token(TokenType.number, self.to_number(curr_string, decimal_found))

    def to_number(self, converted_val, decimal_present):
        if decimal_present:
            return Decimal(converted_val)
        else:
            return int(converted_val)