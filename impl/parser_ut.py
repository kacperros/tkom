import mainparser

tested_object = mainparser.MainParser("testFiles/only_config.txt")
tokens = ["config", "[", "example_config", ".", "xml", "]"]
counter = 0
while True:
    token = tested_object.get_token()
    if token == -1:
        break
    assert token == tokens[counter]
    counter += 1
print("Test 1 passed")

tested_object = mainparser.MainParser("testFiles/onlyRule.txt")
tokens = ["rule", "{", "id", ":", "1", ";", "}"]
counter = 0
while True:
    token = tested_object.get_token()
    if token == -1:
        break
    assert token == tokens[counter]
    counter += 1
print("test 2 passed")
