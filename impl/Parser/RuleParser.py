import Parser.ConditionParser as condParser
import Parser.ParserUtils as utils
from Lexers.Lexer import Lexer
from Lexers.tokens import *
from Model.Rule import Rule
from Model.Action import Action


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
        actions = get_actions(lexer, symbol_table, engine)
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


def get_actions(lexer, symbol_table, engine):
    last_was_action = False
    actions = []
    utils.expect_keyword(lexer, 'actions')
    utils.expect_otherchar(lexer, TokenType.definition_operator, ':')
    while True:
        if last_was_action:
            token = utils.get_token_skipping_whitespace(lexer)
            if token.token_value == TokenType.list_separator:
                last_was_action = False
                continue
            if token.token_value == TokenType.instr_end:
                break
        else:
            actions.append(parse_action(lexer, symbol_table, engine))
            last_was_action = True
    return actions


def parse_action(lexer, symbol_table, engine):
    is_buy = False
    is_stock = False
    token = utils.get_token_skipping_whitespace(lexer)
    if token.token_type != TokenType.keyword and token.token_value not in ['buy', 'sell']:
        raise ValueError('Buy or sell expected to start action, found something else, Sir')
    if token.token_value == 'buy':
        is_buy = True
    token = utils.get_token_skipping_whitespace(lexer)
    if token.token_type != TokenType.keyword and token.token_value not in ['stock', 'currency']:
        raise ValueError('An action requires you to choose either stock or currency, nothing else, Sir')
    if token.token_value == 'stock':
        is_stock = True
    utils.expect_access_operator(lexer)
    symbol_name = utils.expect_given_name(lexer)
    symbol_id = -1
    if is_stock:
        symbol_id = symbol_table.get_stock(symbol_name)
    else:
        symbol_id = symbol_table.get_currency(symbol_name)
    if not is_buy:
        token = utils.get_token_skipping_whitespace(lexer)
        if token.token_type == TokenType.keyword and token.token_value == 'amount':
            token = utils.get_token_skipping_whitespace(lexer)
            if token.token_type == TokenType.number:
                if token.token_value < 0:
                    raise ValueError("You can only sell a positive amount, Sir")
                return build_action(engine, is_buy, is_stock, symbol_id, amount=token.token_value)
            elif token.token_type == TokenType.keyword and token.token_value == 'ALL':
                return build_action(engine, is_buy, is_stock, symbol_id, amount='ALL')
            else:
                raise ValueError("Expecting a number or ALL keyword, found neither of them, Sir")
        elif token.token_type == TokenType.keyword and token.token_value == 'part':
            amount = utils.expect_number(lexer)
            if not 1 <= amount <= 100:
                raise ValueError("Part must be 1 to 100 no more no less, Sir")
            return build_action(engine, is_buy, is_stock, symbol_id, part=amount)
        elif token.token_type == TokenType.keyword and token.token_value == 'for':
            curr_amount = utils.expect_number(lexer)
            if curr_amount < 0:
                raise ValueError("You can only sell for a positive price, Sir")
            return build_action(engine, is_buy, is_stock, symbol_id, curr_amount=curr_amount)
        else:
            raise ValueError("Expecting either amount, part, for, none of those were found, Sir")
    else:
        token = utils.get_token_skipping_whitespace(lexer)
        if token.token_type != TokenType.keyword or token.token_value != 'amount':
            raise ValueError("Expecting keyword amount, Sir")
        token = utils.get_token_skipping_whitespace(lexer)
        buy_amount = 0
        if token.token_type == TokenType.keyword or token.token_value == 'MAX':
            buy_amount = 'MAX'
        elif token.token_type == TokenType.number:
            buy_amount = token.token_value
            if buy_amount < 0:
                raise ValueError("You can only buy a positive amount, Sir")
        else:
            raise ValueError("Unexpected Token, Sir")
        utils.expect_keyword(lexer, 'for')
        currency_used_id = None
        token = utils.get_token_skipping_whitespace(lexer)
        if token.token_type == TokenType.keyword or token.token_value == 'OWN':
            currency_used_id = 'OWN'
        elif token.token_type == TokenType.keyword or token.token_value == 'ANY':
            currency_used_id = 'ANY'
        elif token.token_type == TokenType.keyword or token.token_value == 'currency':
            utils.expect_access_operator(lexer)
            currency_name = utils.expect_given_name(lexer)
            currency_used_id = symbol_table.get_currency(currency_name)
        else:
            raise ValueError("Unexpected token, Sir")
        return build_action(engine, is_buy, is_stock, symbol_id, buy_amount=buy_amount, curr_used=currency_used_id)


def build_action(engine, is_buy, is_stock, symbol_id, amount=None, part=None, curr_amount=None, buy_amount=None,
                 curr_used=None):
    if is_buy:  # buy
        if is_stock:
            return Action(engine.buy_stock_amount, symbol_id, buy_amount, curr_used)
        else:
            return Action(engine.buy_currency_amount, symbol_id, buy_amount, curr_used)
    else:  # sell
        if not is_stock:
            raise ValueError("Currency can not be sold, Sir")
        if amount is not None:
            return Action(engine.sell_stock_amount, symbol_id, amount)
        elif part is not None:
            return Action(engine.sell_stock_part, symbol_id, part)
        elif curr_amount is not None:
            return Action(engine.sell_stock_for_currency)
        else:
            raise ValueError("Critical error, during construction, Sir")
