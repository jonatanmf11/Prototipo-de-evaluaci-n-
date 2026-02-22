class RuleViolation:

    def __init__(self, rule_id: str, rule_name: str, practice_id: str, message: str,dimension : str):
        self.rule_id = rule_id
        self.rule_name = rule_name
        self.practice_id = practice_id
        self.message = message
        self.dimension = dimension


    def __repr__(self):
        return (
            f"<RuleViolation rule={self.rule_name} "
            f"practice={self.practice_id}>"
        )
