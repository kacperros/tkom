from Model.Cond.Condition import Condition


class TrueCondition(Condition):
    def __init__(self):
        super().__init__()

    def eval(self):
        return True
