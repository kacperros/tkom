from Lexers.tokens import *


def expect_given_name(lexer):
    token = get_token_skipping_whitespace(lexer)
    if token.token_type != TokenType.given_name:
        raise ValueError("Given name expected [...], " + str(token.token_value) + " was found, Sir")
    return token.token_value


def expect_access_operator(lexer):
    token = get_token_skipping_whitespace(lexer)
    if token.token_type != TokenType.access_operator:
        raise ValueError("Access operator expected, " + str(token.token_value) + " was found, Sir")


def expect_keyword(lexer, word):
    token = get_token_skipping_whitespace(lexer)
    if token.token_type != TokenType.keyword or token.token_value != word:
        raise ValueError("Keyword " + word + " expected, but found " + str(token.token_value) + " , Sir")


def expect_number(lexer):
    token = get_token_skipping_whitespace(lexer)
    if token.token_type != TokenType.number:
        raise ValueError("Given number, " + str(token.token_value) + " was found, Sir")
    return token.token_value


def get_token_skipping_whitespace(lexer):
    while True:
        token = lexer.get_token()
        if token == -1:
            return Token(TokenType.eof, -1)
        if token.token_type == TokenType.whitespace:
            continue
        else:
            print(token.token_value)
            return token


def expect_otherchar(lexer, otherchar_type, other_char_value):
    token = get_token_skipping_whitespace(lexer)
    if token.token_type != otherchar_type or token.token_value != other_char_value:
        raise ValueError("Given number, " + str(token.token_value) + " was found, Sir")
    return token.token_value
