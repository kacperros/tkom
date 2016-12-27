from Model.Cond.Condition import Condition


class ComparisonCondition(Condition):
    def __init__(self, is_negated):
        super().__init__()
        self.arg1 = None
        self.arg1_access_method = None
        self.arg1_method_symbol_id = None
        self.arg1_method_date_str = None
        self.arg2 = None
        self.arg2_access_method = None
        self.arg2_method_symbol_id = None
        self.arg2_method_date_str = None
        self.comparison_opers = {
            '<': self.les,
            '>': self.gr,
            '<=': self.leseq,
            '>=': self.greq
        }
        self.chosen_oper = None
        self.is_negated = is_negated

    def eval(self):
        arg1 = self.arg1
        arg2 = self.arg2
        if self.arg1 is None:
            if self.arg1_method_date_str is not None:
                arg1 = self.arg1_access_method(self.arg1_method_symbol_id, self.arg1_method_date_str)
            else:
                arg1 = self.arg1_access_method(self.arg1_method_symbol_id)
        if self.arg2 is None:
            if self.arg2_method_date_str is not None:
                arg2 = self.arg2_access_method(self.arg2_method_symbol_id, self.arg2_method_date_str)
            else:
                arg2 = self.arg2_access_method(self.arg2_method_symbol_id)
        if not self.is_negated:
            return self.chosen_oper(arg1, arg2)
        else:
            return not self.chosen_oper(arg1, arg2)

    def les(self, a, b):
        return a < b

    def gr(self, a, b):
        return a > b

    def leseq(self, a, b):
        return a <= b

    def greq(self, a, b):
        return a >= b
