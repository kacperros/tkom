from Model.Cond.Condition import Condition


class MasterCondition(Condition):
    def __init__(self):
        super().__init__()
        self.conditions = []
        self.operators = []
        self.logical_operators = {
            '||': self.log_or,
            '&&': self.log_and
        }

    def eval(self):
        if len(self.conditions) > 1:
            evaluated_conditions = []
            for cond in self.conditions:
                evaluated_conditions.append(cond.eval())
            result = evaluated_conditions[0]
            for i in range(1, len(evaluated_conditions)):
                result = self.logical_operators[self.operators[i - 1]](result, evaluated_conditions[i])
            return result
        elif len(self.conditions) == 1:
            return self.conditions[0].eval()
        else:
            return True

    def log_or(self, arg1, arg2):
        return arg1 or arg2

    def log_and(self, arg1, arg2):
        return arg1 and arg2