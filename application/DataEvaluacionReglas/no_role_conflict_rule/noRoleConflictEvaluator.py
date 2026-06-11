from application.DataEvaluacionReglas.AbstractRuleEvaluator import (
    AbstractRuleEvaluator
)

from application.rules.functional.no_role_conflict_rule import (
    FunctionalNoRoleConflictRule
)


class NoRoleConflictEvaluator(
    AbstractRuleEvaluator
):

    def get_rule(self):

        return FunctionalNoRoleConflictRule()