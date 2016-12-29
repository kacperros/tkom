class Rule:
    def __init__(self, rid, priority, condition, actions):
        self.rule_id = rid
        self.priority = priority
        self.condition = condition
        self.actions = actions
        self.executed = False

    def execute(self):
        if self.condition.eval():
            self.executed = True
            for action in self.actions:
                action.perform()