from enum import Enum


class TokenType(Enum):
    keyword = 1
    given_name = 2
    access_operator = 3
    relations_operator = 4
    logical_operator = 5
    maths_operator = 6
    number = 7
    structure_operator = 8
    definition_operator = 9
    list_separator = 10
    instr_end = 11
    group_operator = 12
    whitespace = 13


class Token:
    def __init__(self, token_type, token_value):
        self.token_type = token_type
        self.token_value = token_value
