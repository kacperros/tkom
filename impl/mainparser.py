class MainParser:
    def __init__(self, file_name):
        self.parsed_file = open(file_name, 'r+')
        self.breaking_chars = [" ", "\n", "\t"]
        self.key_chars = [".", ",", "<", ">", ";", ":",
                          "(", ")", "/", "/", "*",
                          "{", "}", "[", "]", "=",
                          "|", "&", "!"]
        self.key_words = ["config", "events", "start",
                          "rule", "id", "priority", "condition", "actions",
                          "currency", "stock",
                          "rate", "value", "amount", "have", "executed",
                          "part", "for", "ANY", "MAX",
                          "buy", "sell"]

    def get_token(self):
        current_string = ""
        while True:
            current_position = self.parsed_file.tell()
            current_character = self.parsed_file.read(1)
            if current_character == "":
                if current_string == "":
                    return -1
                elif current_string == "":
                    return current_string
            if current_character in self.breaking_chars:
                if current_string == "":
                    continue
                else:
                    return current_string
            if current_character in self.key_chars:
                if current_string != "":
                    self.parsed_file.seek(current_position, 0)
                    return current_string
                else:
                    return current_character
            current_string += current_character
