from Lexers.keywordsStateLexer import KeywordsStateLexer
from Lexers.tokens import *


file = open("../testFiles/keywordsStateLexerTF.txt", 'r+')
tested_object = KeywordsStateLexer(file)
token = tested_object.get_token()
assert (token.token_value == "config")
assert (token.token_type == TokenType.keyword)
file.close()
print("Test 1 passed")

file = open("../testFiles/keywordsStateLexerTF2.txt", 'r+')
tested_object = KeywordsStateLexer(file)
try:
    token = tested_object.get_token()
    assert (1 == 2)
except ValueError:
    assert (1 == 1)
file.close()
print("Test 2 passed")
