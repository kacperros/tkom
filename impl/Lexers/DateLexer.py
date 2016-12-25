from Lexers.abstractStateLexer import AbstractStateLexer
from datetime import datetime
from Lexers.tokens import *


class DateLexer(AbstractStateLexer):
    def __init__(self, parsed_file):
        super().__init__(parsed_file)
        self.start_char = "@"
        self.end_char = "@"

    def is_applicable(self, starting_char):
        return starting_char == self.start_char

    def get_token(self):
        curr_string = ""
        waiting_for_close = False
        while True:
            curr_pos = self.parsed_file.tell()
            curr_char = self.parsed_file.read(1)
            if curr_char == self.start_char and waiting_for_close == False:
                waiting_for_close = True
                continue
            if curr_char == -1 or curr_char == '':
                if waiting_for_close:
                    raise ValueError("Ran out of file and no closing @ found, Sir.")
                else:
                    raise ValueError("No opening ever encountered. Very grave Sir.")
            if curr_char == self.end_char and waiting_for_close:
                if curr_string == "":
                    raise ValueError("Date can not be empty, Sir.")
                else:
                    try:
                        date_parts = curr_string.split(".")
                        if len(date_parts) < 3:
                            raise ValueError
                        got_date = datetime.strptime(curr_string, "%Y.%m.%d").date()
                    except ValueError:
                        raise ValueError("Incorrect date format, Sir.")
                    return Token(TokenType.date, curr_string)
            curr_string = curr_string + curr_char
