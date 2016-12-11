from Lexers.NumberLexer import NumberLexer
from Lexers.tokens import *
from decimal import *

file = open("../testFiles/numLexTF.txt", 'r+')
tested_object = NumberLexer(file)
token = tested_object.get_token()
assert (token.token_value == 1000)
assert (token.token_type == TokenType.number)
file.close()
print("Test 1 passed")

file = open("../testFiles/numLexTF2.txt", 'r+')
tested_object = NumberLexer(file)
token = tested_object.get_token()
assert (token.token_value.compare(Decimal('1000.15')) == 0)
assert (token.token_type == TokenType.number)
file.close()
print("Test 2 passed")

file = open("../testFiles/numLexTF3.txt", 'r+')
tested_object = NumberLexer(file)
try:
    token = tested_object.get_token()
    assert (1 == 2)
except ValueError:
    assert (1 == 1)
file.close()
print("Test 3 passed")
