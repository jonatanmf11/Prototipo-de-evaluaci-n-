from typing import List, Dict

from application.rules.base_rule import BaseRule
from application.rules.rule_violation import RuleViolation
from domain.hybrid_process_model import HybridProcessModel


class FunctionalNoRedundantArtifactsRule(BaseRule):
    """
    OCL:
    context HybridProcessModel
    inv NoRedundantArtifacts:
    self.practices.artifacts->isUnique(name)
    """

    def __init__(self):
        super().__init__(
            rule_id="F1",
            name="No Redundant Artifacts",
            description=(
                "Verifica que no existan artefactos funcionalmente redundantes "
                "entre prácticas del modelo"
            ),
            dimension="functional"
        )

    def evaluate(
        self,
        model: HybridProcessModel
    ) -> List[RuleViolation]:

        violations: List[RuleViolation] = []
        artifact_registry: Dict[str, str] = {}

        for practice in model.practices:
            for artifact in practice.artifacts:
                if artifact.name in artifact_registry:
                    violations.append(
                        RuleViolation(
                            practice_id=practice.id,
                            rule_id=self.rule_id,
                            rule_name=self.name,
                            dimension = self.dimension,
                            message=(
                                f"El artefacto '{artifact.name}' "
                                f"ya fue definido en la práctica "
                                f"'{artifact_registry[artifact.name]}'"
                            )
                        )
                    )
                else:
                    artifact_registry[artifact.name] = practice.id

        return violations
