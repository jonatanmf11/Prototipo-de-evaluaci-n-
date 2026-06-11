from application.DataEvaluacionReglas.AbstractRuleEvaluator import (
    AbstractRuleEvaluator
)

from application.rules.functional.no_redundant_artifacts_rule import (
    FunctionalNoRedundantArtifactsRule
)


class NoRedundantArtifactsEvaluator(
    AbstractRuleEvaluator
):

    def get_rule(self):

        return FunctionalNoRedundantArtifactsRule()