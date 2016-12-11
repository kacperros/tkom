from Lexers.abstractStateLexer import AbstractStateLexer
import string
from Lexers.tokens import *


class KeywordsStateLexer(AbstractStateLexer):
    def __init__(self, parsed_file):
        super().__init__(parsed_file)
        self.allowed_chars = list(string.ascii_letters)
        self.break_chars = [" ", "\t", "\n", ".", "/"]
        self.keywords = ["config", "events", "start", "rule", "id", "priority", "condition",
                         "have", "executed",
                         "currency", "rate", "amount"
                         "stock", "value", "globalValue", "amount",
                         "inc", "dec",
                         "actions", "sell", "buy", "part", "for", "ANY", "MAX", "OWN"]

    def get_token(self):
        curr_string = ""
        while True:
            curr_pos = self.parsed_file.tell()
            curr_char = self.parsed_file.read(1)
            if curr_char == -1 or curr_char == '':
                if curr_string in self.keywords:
                    return Token(TokenType.keyword, curr_string)
                else:
                    raise ValueError("Ran out of file and keyword was not matched, Sir.")
            if curr_char in self.break_chars:
                self.parsed_file.seek(curr_pos, 0)
                if curr_string in self.keywords:
                    return Token(TokenType.keyword, curr_string)
                else:
                    raise ValueError("Word completed but did not match any keywords, Sir.")
            elif curr_char in self.allowed_chars:
                curr_string = curr_string + curr_char
            else:
                raise ValueError("Horrendous characters detected, Sir.")
