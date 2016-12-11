class AbstractStateLexer:
    def __init__(self, parsed_file):
        self.parsed_file = parsed_file

    def get_token(self):
        pass

    def is_applicable(self, starting_char):
        pass
