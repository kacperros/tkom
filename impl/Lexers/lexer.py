class Lexer:
    def __init__(self, file_name):
        self.parsed_file = open(file_name, 'r+')
        self.whitespace_chars = ["\t", " "]
        self.opt_whitespace_chars = ["", "\t", " "]
        self.given_name_start = "["
        self.given_name_end = "]"

    def get_token(self):
        state = 0
        start = self.parsed_file.tell()
        current_string = ""
        while True:
            current_position = self.parsed_file.tell()
            current_character = self.parsed_file.read(1)
            if state == 0:
                state = self.determine_state(current_character, current_string)

