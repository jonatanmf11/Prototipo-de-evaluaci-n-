from application.DataEvaluacionReglas.AbstractRuleEvaluator import (
    AbstractRuleEvaluator
)

from application.rules.sequential.no_contradictory_dependencies_rule import (
    SequentialNoContradictoryDependenciesRule
)


class NoContradictoryDependenciesEvaluator(
    AbstractRuleEvaluator
):

    def get_rule(self):

        return SequentialNoContradictoryDependenciesRule()