class Condition:
    def __init__(self):
        self.logical_operators = {
            '!': self.negate,
            '||': self.log_or,
            '&&': self.log_and
        }
        self.children = []
        self.parent = None

    def eval(self):
        return False

    def negate(self):
        return not self.eval()

    def log_or(self, cond2):
        return self.eval() or cond2.eval()

    def log_and(self, cond2):
        return self.eval() and cond2.eval()
