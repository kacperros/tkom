from enum import Enum


class TokenType(Enum):
    keyword = 1
    given_name = 2
    access_operator = 3             # .
    relations_operator = 4          # >=, <=, <, >
    logical_operator = 5            # ||, &&, !
    maths_operator = 6              # +, -, /, *
    number = 7
    structure_operator_start = 8    # {
    structure_operator_end = 18     # }
    definition_operator = 9         # :
    list_start = 10                 # (
    list_end = 20                   # )
    instr_end = 11                  # ;
    list_separator = 12             # ,
    whitespace = 13
    comment_start = 14              # //
    error = 404


class Token:
    def __init__(self, token_type, token_value):
        self.token_type = token_type
        self.token_value = token_value
