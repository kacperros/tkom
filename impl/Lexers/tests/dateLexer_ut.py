from Lexers.DateLexer import DateLexer
from Lexers.tokens import *


file = open("../testFiles/bad_date.txt", 'r+')
tested_object = DateLexer(file)
try:
    token = tested_object.get_token()
    assert(1 == 0)
except ValueError:
    assert (1 == 1)
file.close()
print("Test 1 passed")

file = open("../testFiles/bad_date.txt", 'r+')
tested_object = DateLexer(file)
try:
    token = tested_object.get_token()
    assert(1 == 0)
except ValueError:
    assert (1 == 1)
file.close()
print("Test 2 passed")

file = open("../testFiles/date.txt", 'r+')
tested_object = DateLexer(file)
try:
    token = tested_object.get_token()
    assert(token.token_type == TokenType.date)
    assert(token.token_value == '2016.09.15')
except ValueError:
    assert (1 == 0)
file.close()
print("Test 3 passed")
