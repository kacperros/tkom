from Lexers.abstractStateLexer import AbstractStateLexer
import string
from Lexers.tokens import *


class GivenNameLexer(AbstractStateLexer):
    def __init__(self, parsed_file):
        super().__init__(parsed_file)
        self.start_char = "["
        self.end_char = "]"

    def is_applicable(self, starting_char):
        return starting_char == self.start_char

    def get_token(self):
        curr_string = ""
        waiting_for_close = False
        while True:
            curr_pos = self.parsed_file.tell()
            curr_char = self.parsed_file.read(1)
            if curr_char == self.start_char:
                waiting_for_close = True
                continue
            if curr_char == -1 or curr_char == '':
                if waiting_for_close:
                    raise ValueError("Ran out of file and no closing ] found, Sir.")
                else:
                    raise ValueError("No opening ever encountered. Very grave Sir.")
            if curr_char == self.end_char and waiting_for_close:
                if curr_string == "":
                    raise ValueError("Given name can not be empty, Sir.")
                else:
                    return Token(TokenType.given_name, curr_string)
            curr_string = curr_string + curr_char
