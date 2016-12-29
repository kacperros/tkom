from Engine.RealityController import RealityController
import Parser.ConfigParser as config_parser
import Parser.EventsParser as events_parser
import Parser.RuleParser as rule_parser
import Parser.StartParser as start_parser
from Lexers.tokens import TokenType
import Parser.ParserUtils as ut
from Lexers.Lexer import Lexer
from enum import Enum


class MainParser:
    def __init__(self, engine, lexer, symbol_table):
        self.engine = engine
        self.lexer = lexer
        self.symbol_table = symbol_table
        self.state_used = [False, False, False, False]

    def parse(self):
        state = 0  # 0 - config, 1 - events, 2 - start, 3 - rules, 4 - done
        while True:
            token = ut.get_token_skipping_whitespace(self.lexer)
            state = self.change_state_on_token(token, state)
            if state == 0:
                file_name = ut.expect_given_name(self.lexer)
                parse_results = config_parser.parse_file(file_name, self.symbol_table)
                currencies = parse_results['currencies']
                stocks = parse_results['stocks']
                for curr in currencies:
                    self.engine.add_currency(curr)
                for st in stocks:
                    self.engine.add_stock(st)
            elif state == 1:
                file_name = ut.expect_given_name(self.lexer)
                parse_results = events_parser.parse_file(file_name, self.symbol_table)
                for event in parse_results:
                    self.engine.add_event(event)
            elif state == 2:
                file_name = ut.expect_given_name(self.lexer)
                parse_results = start_parser.parse_file(file_name, self.symbol_table)
                currencies = parse_results['currencies']
                stocks = parse_results['stocks']
                for curr in currencies:
                    self.engine.add_start_cond(curr)
                for st in stocks:
                    self.engine.add_start_cond(st)
            elif state == 3:
                rule_parser.parse_from_lexer(self.lexer, self.symbol_table, self.engine, token)
            elif state == 4:
                return
            else:
                raise ValueError("Something went blood wrong, Sir")

    def change_state_on_token(self, token, state):
        if state == 0 and token.token_type == TokenType.keyword:
            if token.token_value == 'config':
                self.state_used[0] = True
                return 0
            elif token.token_value == 'events' and self.state_used[0]:
                self.state_used[1] = True
                return 1
            else:
                raise ValueError("At least one config file must appear")
        if state == 1 and token.token_type == TokenType.keyword:
            if token.token_value == 'events':
                self.state_used[1] = True
                return 1
            elif token.token_value == 'start' and self.state_used[1]:
                self.state_used[2] = True
                return 2
            else:
                raise ValueError("At least one events file must appear")
        if state == 2 and token.token_type == TokenType.keyword:
            if token.token_value == 'start':
                self.state_used[2] = True
                return 2
            elif token.token_value == 'rule':
                self.state_used[3] = True
                return 3
            else:
                raise ValueError("At least one start file must appear")
        if state == 3 and token.token_type == TokenType.keyword:
            if token.token_value == 'rule':
                return 3
            else:
                raise ValueError("Only rules allowed")
        if token.token_type == TokenType.eof and self.state_used[3]:
            return 4
