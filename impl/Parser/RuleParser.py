from Lexers.Lexer import Lexer
from Lexers.tokens import *


def parse_from_lexer(lexer):
    token = lexer.get_token()
    if token.token_type != TokenType.keyword or token.token_value != 'rule':
        raise ValueError("This error should not have occurred. rule keyword is expected, Sir")
    token = get_token_skipping_whitespace(lexer)
    if token.token_type == TokenType.given_name:
        parsed_file = open(token.token_value)
        new_lexer = Lexer(parsed_file)
        parse_from_lexer(new_lexer)
    elif token.token_type == TokenType.structure_operator_start:
        rid = get_id(lexer)
        prio = get_priority(lexer)
        print(prio)
        # condition = get_condition(lexer)
        # actions = get_actions(lexer)
    else:
        raise ValueError("Either a given_name of a file containing a rule or { are expected, Sir")


def get_id(lexer):
    token = get_token_skipping_whitespace(lexer)
    if token.token_type != TokenType.keyword or token.token_value != 'id':
        raise ValueError('Expected id keyword, Sir. Found ' + str(token.token_value))
    token = get_token_skipping_whitespace(lexer)
    if token.token_type != TokenType.definition_operator:
        raise ValueError('Expected : ,found ' + str(token.token_value), " Sir.")
    token = get_token_skipping_whitespace(lexer)
    if token.token_type != TokenType.number:
        raise ValueError('Rule id must be a number, found ' + str(token.token_value))
    rule_id = token.token_value
    token = get_token_skipping_whitespace(lexer)
    if token.token_type != TokenType.instr_end:
        raise ValueError('Expected ; found ' + str(token.token_value) + " ,Sir.")
    return rule_id


def get_priority(lexer):
    token = get_token_skipping_whitespace(lexer)
    if token.token_type != TokenType.keyword or token.token_value != 'priority':
        raise ValueError('Expected priority keyword, Sir. Found ' + str(token.token_value))
    token = get_token_skipping_whitespace(lexer)
    if token.token_type != TokenType.definition_operator:
        raise ValueError('Expected : ,found ' + str(token.token_value), " Sir.")
    token = get_token_skipping_whitespace(lexer)
    if token.token_type != TokenType.number:
        raise ValueError('Rule id must be a number, found ' + str(token.token_value))
    rule_id = token.token_value
    token = get_token_skipping_whitespace(lexer)
    if token.token_type != TokenType.instr_end:
        raise ValueError('Expected ; found ' + str(token.token_value) + " ,Sir.")
    return rule_id


def get_condition(lexer):
    pass


def get_actions(lexer):
    pass


def get_token_skipping_whitespace(lexer):
    while True:
        token = lexer.get_token()
        if token.token_type == TokenType.whitespace:
            continue
        else:
            return token
