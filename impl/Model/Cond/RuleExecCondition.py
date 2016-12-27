from Model.Cond.Condition import Condition


class RuleExecCondition(Condition):
    def __init__(self, rule, is_negated):
        super().__init__()
        self.rule = rule
        self.is_negated = is_negated

    def eval(self):
        if self.is_negated:
            return self.rule.executed
        else:
            return not self.rule.executed
