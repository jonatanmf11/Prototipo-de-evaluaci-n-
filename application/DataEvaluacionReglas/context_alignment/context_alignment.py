from application.DataEvaluacionReglas.AbstractRuleEvaluator import (
    AbstractRuleEvaluator
)

from application.rules.organizational.context_alignment_rule import OrganizationalContextAlignmentRule


class contextalignmentEvaluator(
    AbstractRuleEvaluator
):

    def get_rule(self):

        return OrganizationalContextAlignmentRule()