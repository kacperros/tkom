from Lexers.tokens import *
from Lexers.abstractStateLexer import AbstractStateLexer
import string


class OtherCharLexer(AbstractStateLexer):
    def __init__(self, parsed_file):
        super().__init__(parsed_file)
        self.allowed_chars = list(string.punctuation)
        self.allowed_chars.remove('@')

    def is_applicable(self, starting_char):
        return starting_char in self.allowed_chars

    def get_token(self):
        curr_string = ""
        while True:
            curr_pos = self.parsed_file.tell()
            curr_char = self.parsed_file.read(1)
            if curr_char == '.':
                return Token(TokenType.access_operator, curr_char)
            if curr_char in self.allowed_chars:
                curr_string = curr_string + curr_char
            else:
                self.parsed_file.seek(curr_pos, 0)
                token = self.select_token(curr_string)
                if token.token_type == TokenType.error:
                    raise ValueError("My good Sir, no such tokens supported")
                if token.token_type == TokenType.comment_start:
                    while curr_char != "\n":
                        curr_char = self.parsed_file.read(1)
                    return token
                return token

    def select_token(self, curr_string):
        if curr_string == ".":
            return Token(TokenType.access_operator, curr_string)
        elif curr_string == ",":
            return Token(TokenType.list_separator, curr_string)
        elif curr_string == "{":
            return Token(TokenType.structure_operator_start, curr_string)
        elif curr_string == "}":
            return Token(TokenType.structure_operator_end, curr_string)
        elif curr_string in ["<=", ">=", "<", ">"]:
            return Token(TokenType.relations_operator, curr_string)
        elif curr_string in ["||", "&&", "!"]:
            return Token(TokenType.logical_operator, curr_string)
        elif curr_string in ["*", "/", "+", "-"]:
            return Token(TokenType.maths_operator, curr_string)
        elif curr_string == "(":
            return Token(TokenType.list_start, curr_string)
        elif curr_string == ")":
            return Token(TokenType.list_end, curr_string)
        elif curr_string == ":":
            return Token(TokenType.definition_operator, curr_string)
        elif curr_string == ";":
            return Token(TokenType.instr_end, curr_string)
        elif curr_string == "//":
            return Token(TokenType.comment_start, curr_string)
