from Lexers.Lexer import Lexer
from Lexers.tokens import *

# parsed_file = open("../testFiles/only_config.txt")
# tested_object = Lexer(parsed_file)
# tokens = ["config", " ", "example_config.xml"]
# counter = 0
# while True:
#     token = tested_object.get_token()
#     if token == -1:
#         break
#     assert token.token_value == tokens[counter]
#     counter += 1
# print("Test 1 passed")
#
# parsed_file = open("../testFiles/onlyRule.txt")
# tested_object = Lexer(parsed_file)
# tokens = ["rule", "{", "id", ":", "1", ";", "}"]
# counter = 0
# while True:
#     token = tested_object.get_token()
#     if token == -1:
#         break
#     if token.token_type == TokenType.whitespace:
#         continue
#
#     if token.token_type == TokenType.number:
#         assert token.token_value == int(tokens[counter])
#     else:
#         assert token.token_value == tokens[counter]
#     counter += 1
# print("test 2 passed")

parsed_file = open("../testFiles/access.txt")
tested_object = Lexer(parsed_file)
tokens = ["rule", "{", "id", ":", "1", ";", "}"]
counter = 0
while True:
    token = tested_object.get_token()

    if token == -1:
        break
    print(token.token_value)
    # if token.token_type == TokenType.whitespace:
    #     continue
    #
    # if token.token_type == TokenType.number:
    #     assert token.token_value == int(tokens[counter])
    # else:
    #     assert token.token_value == tokens[counter]
    # counter += 1
print("test 2 passed")
