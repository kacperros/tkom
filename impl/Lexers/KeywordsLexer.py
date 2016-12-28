from Lexers.abstractStateLexer import AbstractStateLexer
from Lexers.tokens import *
import string


class KeywordsLexer(AbstractStateLexer):
    def __init__(self, parsed_file):
        super().__init__(parsed_file)
        self.break_chars = [" ", "\t", "\n", ".", "/", ":", "("]
        self.keywords = ["config", "events", "start", "rule", "id", "priority", "condition",
                         "have", "executed",
                         "currency", "rate", "amount",
                         "stock", "value", "globalValue", "amount",
                         "inc", "dec", "by", "in",
                         "actions", "sell", "buy", "part", "for", "ANY", "MAX", "OWN"]
        self.allowed_chars = list(string.ascii_letters)
        self.first_chars = self.__get_first_chars()
        self.max_length = self.__get_max_length()

    def __get_first_chars(self):
        result = []
        for keyword in self.keywords:
            result.append(keyword[0])
        return result

    def __get_max_length(self):
        max_len = 0
        for keyword in self.keywords:
            max_len = max(max_len, len(keyword))
        return max_len

    def is_applicable(self, starting_char):
        return starting_char in self.first_chars

    def get_token(self):
        curr_string = ""
        while True:
            curr_pos = self.parsed_file.tell()
            curr_char = self.parsed_file.read(1)
            if len(curr_string) > self.max_length:
                raise ValueError("Attempting to read a keyword that is too long, Sir.")
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
