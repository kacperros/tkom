from Lexers.GivenNameLexer import GivenNameLexer
from Lexers.tokens import *


file = open("../testFiles/givenNamesLexTF.txt", 'r+')
tested_object = GivenNameLexer(file)
token = tested_object.get_token()
assert (token.token_value == "Oh some blood $ long s*** ")
assert (token.token_type == TokenType.given_name)
file.close()
print("Test 1 passed")

file = open("../testFiles/givenNamesLexTF2.txt", 'r+')
tested_object = GivenNameLexer(file)
try:
    token = tested_object.get_token()
    assert (1 == 2)
except ValueError:
    assert (1 == 1)
file.close()
print("Test 2 passed")
