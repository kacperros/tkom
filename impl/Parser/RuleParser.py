from Lexers.Lexer import Lexer
from Lexers.tokens import *
from Model.Cond.Condition import Condition
from Model.Cond.TrueCondition import TrueCondition
from Model.Cond.ComparisonCondition import ComparisonCondition
from Model.Cond.MasterCondition import MasterCondition
from Model.Cond.RuleExecCondition import RuleExecCondition
from Model.Cond.TrendCondition import TrendCondition


def parse_from_lexer(lexer, symbol_table, engine):
    token = lexer.get_token()
    if token.token_type != TokenType.keyword or token.token_value != 'rule':
        raise ValueError("This error should not have occurred. rule keyword is expected, Sir")
    token = get_token_skipping_whitespace(lexer)
    if token.token_type == TokenType.given_name:
        parsed_file = open(token.token_value)
        new_lexer = Lexer(parsed_file)
        parse_from_lexer(new_lexer, symbol_table)
    elif token.token_type == TokenType.structure_operator_start:
        rid = get_id(lexer, symbol_table)
        prio = get_priority(lexer)
        condition = get_condition(lexer, symbol_table, engine)
        # actions = get_actions(lexer, symbol_table)
    else:
        raise ValueError("Either a given_name of a file containing a rule or { are expected, Sir")


def get_id(lexer, symbol_table):
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
    if symbol_table.is_rule_id_busy(rule_id):
        raise ValueError('Id' + str(rule_id) + 'for rule is already taken, Sir')
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


def get_condition(lexer, symbol_table, engine):
    token = get_token_skipping_whitespace(lexer)
    if token.token_type != TokenType.keyword or token.token_value != 'condition':
        raise ValueError("Keyword condition expected Sir. Found: " + str(token.token_value))
    token = get_token_skipping_whitespace(lexer)
    if token.token_type != TokenType.definition_operator:
        raise ValueError('Expected : ,found ' + str(token.token_value), " Sir.")
    token = get_token_skipping_whitespace(lexer)
    if token.token_type == TokenType.instr_end:
        return TrueCondition()
    elif token.token_type == TokenType.keyword or token.token_type == TokenType.list_start:
        return _build_conditions(token, lexer, symbol_table, engine)
    else:
        raise ValueError("Inappropriate token found " + str(token.token_value))


def _build_conditions(token, lexer, symbol_table, engine):
    master = MasterCondition()
    while True:
        if token.token_type == TokenType.keyword:
            if token.token_value == 'currency' or token.token_value == 'stock':
                pass
            if token.token_value == 'rule':
                pass
            if token.token_value == 'inc' or token.token_value == 'dec':
                pass
        elif token.token_type == TokenType.list_start:
            pass
        elif token.token_type == TokenType.instr_end:
            break
    return master


def get_actions(lexer, symbol_table):
    pass


def get_token_skipping_whitespace(lexer):
    while True:
        token = lexer.get_token()
        if token.token_type == TokenType.whitespace:
            continue
        else:
            return token
