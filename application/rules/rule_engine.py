class RuleEngine:
    def __init__(self):
        self.rules = []

    def register_rule(self, rule):
        self.rules.append(rule)

    def evaluate(self, model):
        violations = []
        for rule in self.rules:
            violations.extend(rule.evaluate(model))
        return violations
