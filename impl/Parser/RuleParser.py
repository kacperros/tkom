from Lexers.Lexer import Lexer
from Lexers.tokens import *
from Model.Cond.Condition import Condition
from Model.Cond.TrueCondition import TrueCondition
from Model.Cond.ComparisonCondition import ComparisonCondition
from Model.Cond.MasterCondition import MasterCondition
from Model.Cond.RuleExecCondition import RuleExecCondition
from Model.Cond.TrendCondition import TrendCondition
import Utils.DateConverter as dateConv
import math


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
        is_negated = False
        if token.token_type == TokenType.keyword or token.token_type == TokenType.number or (
                token.token_type == TokenType.logical_operator and token.token_value == '!'):
            if token.token_type == TokenType.logical_operator and token.token_value == '!':
                is_negated = True
            if token.token_value == 'currency' or token.token_value == 'stock' or token.token_type == TokenType.number:
                cond = _parse_comparison_cond(token, lexer, symbol_table, engine, is_negated)
                master.conditions.append(cond)
            if token.token_value == 'rule':
                cond = _parse_rule_cond(token, lexer, symbol_table, engine, is_negated)
                master.conditions.append(cond)
            if token.token_value == 'inc' or token.token_value == 'dec':
                cond = _parse_trend_cond(token, lexer, symbol_table, engine, is_negated)
                master.conditions.append(cond)
        elif token.token_type == TokenType.list_start:
            pass
        elif token.token_type == TokenType.logical_operator:
            pass
        elif token.token_type == TokenType.instr_end:
            break
    return master


def _parse_comparison_cond(token, lexer, symbol_table, engine, is_negated):
    access_method1, symbol_id1, date_str1, num1 = _get_numeric_comparison_argument(token, lexer, symbol_table, engine)
    operator = _get_comparison_operator(lexer)
    token = get_token_skipping_whitespace(lexer)
    access_method2, symbol_id2, date_str2, num2 = _get_numeric_comparison_argument(token, lexer, symbol_table, engine)
    return _build_comparison_condition(access_method1, symbol_id1, date_str1, num1, operator, access_method2,
                                       symbol_id2, date_str2, num2, is_negated)


def _get_numeric_comparison_argument(token, lexer, symbol_table, engine):
    if token.token_type == TokenType.number:
        return None, None, None, token.token_value
    if token.token_value == 'currency':
        expect_access_operator(lexer)
        symbol_id = symbol_table.get_currency(expect_given_name(lexer))
        expect_access_operator(lexer)
        token = lexer.get_token()
        if token.token_type == TokenType.keyword and token.token_value == 'rate':
            access_method = engine.world.get_currency_rate
            date_str = _get_date_arg(lexer, engine)
            return access_method, symbol_id, date_str, None
        elif token.token_type == TokenType.keyword and token.token_value == 'have':
            expect_access_operator(lexer)
            token = lexer.get_token()
            if token.token_type == TokenType.keyword and token.token_value == 'amount':
                access_method = engine.investor.has_currency
                return access_method, symbol_id, None, None
            else:
                raise ValueError("Forbidden token found, expected keyword amount " + str(token.token_value) + " ,Sir.")
        else:
            raise ValueError(
                "Forbidden token found, expected keywords rate or have found: " + str(token.token_value) + " ,Sir.")
    else:
        expect_access_operator(lexer)
        symbol_id = symbol_table.get_stock(expect_given_name(lexer))
        expect_access_operator(lexer)
        token = lexer.get_token()
        if token.token_type == TokenType.keyword and token.token_value == 'value':
            access_method = engine.world.get_stock_price
            date_str = _get_date_arg(lexer, engine)
            return access_method, symbol_id, date_str, None
        elif token.token_type == TokenType.keyword and token.token_value == 'have':
            expect_access_operator(lexer)
            token = lexer.get_token()
            if token.token_type == TokenType.keyword and token.token_value == 'amount':
                access_method = engine.investor.has_stock
                return access_method, symbol_id, None, None
            else:
                raise ValueError(
                    "Forbidden token found, expected keyword amount not " + str(token.token_value) + " ,Sir.")
        else:
            raise ValueError("Forbidden token found, expected keyword value or have keywords not " + str(
                token.token_value) + " ,Sir.")


def _get_date_arg(lexer, engine):
    token = lexer.get_token()
    if token.token_type != TokenType.list_start:
        if token.token_type == TokenType.whitespace:
            return dateConv.to_str(engine.world.current_day)
        else:
            raise ValueError(
                "Forbidden token found, expected whitespace or ( amount" + str(token.token_value) + " ,Sir.")
    else:
        token = get_token_skipping_whitespace(lexer)
        if token.token_type == TokenType.number:
            result = dateConv.get_date_back_x(dateConv.to_str(engine.world.current_day), math.fabs(token.token_value))
            token = get_token_skipping_whitespace(lexer)
            if token.token_type != TokenType.list_end:
                raise ValueError("Expected ) , found: " + str(token.token_value) + " ,Sir.")
            return result
        if token.token_type == TokenType.date:
            result = token.token_value
            token = get_token_skipping_whitespace(lexer)
            if token.token_type != TokenType.list_end:
                raise ValueError("Expected ) , found: " + str(token.token_value) + " ,Sir.")
            return result
        raise ValueError(" Expected Number or @date@, found neither, Sir")


def _get_comparison_operator(lexer):
    token = get_token_skipping_whitespace(lexer)
    if token.token_type != TokenType.relations_operator:
        raise ValueError("Relations operator expected, found: " + str(token.token_value) + " ,Sir.")
    return token.token_value


def _build_comparison_condition(access_method1, symbol_id1, date_str1, num1, operator, access_method2, symbol_id2,
                                date_str2, num2, is_negated):
    cond = ComparisonCondition(is_negated)
    cond.arg1_access_method = access_method1
    cond.arg1_method_symbol_id = symbol_id1
    cond.arg1_method_date_str = date_str1
    cond.arg1 = num1
    cond.chosen_oper = cond.comparison_opers[operator]
    cond.arg2_access_method = access_method2
    cond.arg2_method_date_str = date_str2
    cond.arg2_method_symbol_id = symbol_id2
    cond.arg2 = num2
    return cond


def _parse_rule_cond(token, lexer, symbol_table, engine, is_negated):
    pass


def _parse_trend_cond(token, lexer, symbol_table, engine, is_negated):
    pass


def get_actions(lexer, symbol_table):
    pass


def expect_given_name(lexer):
    token = lexer.get_token()
    if token.token_type != TokenType.given_name:
        raise ValueError("Given name expected [...], " + str(token.token_value) + " was found, Sir")
    return token.token_value


def expect_access_operator(lexer):
    token = lexer.get_token()
    if token.token_type != TokenType.access_operator:
        raise ValueError("Access operator expected, " + str(token.token_value) + " was found, Sir")


def get_token_skipping_whitespace(lexer):
    while True:
        token = lexer.get_token()
        if token.token_type == TokenType.whitespace:
            continue
        else:
            return token
