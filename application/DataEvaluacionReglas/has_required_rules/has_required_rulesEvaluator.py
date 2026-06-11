from application.DataEvaluacionReglas.AbstractRuleEvaluator import (
    AbstractRuleEvaluator
)

from application.rules.formal.has_required_rules_rule import FormalHasRequiredRulesRule


class hasRequiredRulesEvaluator(
    AbstractRuleEvaluator
):

    def get_rule(self):

        return FormalHasRequiredRulesRule()