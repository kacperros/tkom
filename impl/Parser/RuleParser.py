import Parser.ConditionParser as condParser
import Parser.ParserUtils as utils
from Lexers.Lexer import Lexer
from Lexers.tokens import *
from Model.Rule import Rule


def parse_from_lexer(lexer, symbol_table, engine):
    token = lexer.get_token()
    if token.token_type != TokenType.keyword or token.token_value != 'rule':
        raise ValueError("This error should not have occurred. rule keyword is expected, Sir")
    token = utils.get_token_skipping_whitespace(lexer)
    if token.token_type == TokenType.given_name:
        parsed_file = open(token.token_value)
        new_lexer = Lexer(parsed_file)
        parse_from_lexer(new_lexer, symbol_table)
    elif token.token_type == TokenType.structure_operator_start:
        rid = get_id(lexer, symbol_table)
        prio = get_priority(lexer)
        condition = condParser.get_condition(lexer, symbol_table, engine)
        condition.eval()
        actions = get_actions(lexer, symbol_table)
        rule = Rule(rid, prio, condition, actions)
        symbol_table.add_rule_id(rid)
        engine.rules[rid] = rule

    else:
        raise ValueError("Either a given_name of a file containing a rule or { are expected, Sir")


def get_id(lexer, symbol_table):
    token = utils.get_token_skipping_whitespace(lexer)
    if token.token_type != TokenType.keyword or token.token_value != 'id':
        raise ValueError('Expected id keyword, Sir. Found ' + str(token.token_value))
    token = utils.get_token_skipping_whitespace(lexer)
    if token.token_type != TokenType.definition_operator:
        raise ValueError('Expected : ,found ' + str(token.token_value), " Sir.")
    token = utils.get_token_skipping_whitespace(lexer)
    if token.token_type != TokenType.number:
        raise ValueError('Rule id must be a number, found ' + str(token.token_value))
    rule_id = token.token_value
    if symbol_table.is_rule_id_busy(rule_id):
        raise ValueError('Id' + str(rule_id) + 'for rule is already taken, Sir')
    token = utils.get_token_skipping_whitespace(lexer)
    if token.token_type != TokenType.instr_end:
        raise ValueError('Expected ; found ' + str(token.token_value) + " ,Sir.")
    return rule_id


def get_priority(lexer):
    token = utils.get_token_skipping_whitespace(lexer)
    if token.token_type != TokenType.keyword or token.token_value != 'priority':
        raise ValueError('Expected priority keyword, Sir. Found ' + str(token.token_value))
    token = utils.get_token_skipping_whitespace(lexer)
    if token.token_type != TokenType.definition_operator:
        raise ValueError('Expected : ,found ' + str(token.token_value), " Sir.")
    token = utils.get_token_skipping_whitespace(lexer)
    if token.token_type != TokenType.number:
        raise ValueError('Rule id must be a number, found ' + str(token.token_value))
    rule_id = token.token_value
    token = utils.get_token_skipping_whitespace(lexer)
    if token.token_type != TokenType.instr_end:
        raise ValueError('Expected ; found ' + str(token.token_value) + " ,Sir.")
    return rule_id



def get_actions(lexer, symbol_table):
    pass


