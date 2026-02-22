from typing import List

from application.rules.base_rule import BaseRule
from application.rules.rule_violation import RuleViolation
from domain.hybrid_process_model import HybridProcessModel


class SequentialNoContradictoryDependenciesRule(BaseRule):
    """
    OCL:
    context CompatibilityRelation
    inv Sequential_NoContradictoryDependencies:
    self.relationType = 'Sequential' implies
    not (a.mustPrecede = b and b.mustPrecede = a)
    """

    def __init__(self):
        super().__init__(
            rule_id="F3",
            name="Sequential No Contradictory Dependencies",
            description=(
                "Verifica que las dependencias temporales secuenciales "
                "no generen ciclos contradictorios entre actividades"
            ),
            dimension="functional"
        )

    def evaluate(
        self,
        model: HybridProcessModel
    ) -> List[RuleViolation]:

        violations: List[RuleViolation] = []

        # 🔹 Iteramos sobre las relaciones del modelo
        for relation in model.compatibility_relations:

            # 🔹 Solo aplica a relaciones secuenciales
            if relation.relation_type != "Sequential":
                continue

            practice_a = relation.practice_a
            practice_b = relation.practice_b

            for act_a in practice_a.activities:
                for act_b in practice_b.activities:

                    if (
                        act_b.id in act_a.mustPrecede and
                        act_a.id in act_b.mustPrecede
                    ):
                        violations.append(
                            RuleViolation(
                                rule_id=self.rule_id,
                                rule_name=self.name,
                                dimension=self.dimension,
                                practice_id="GLOBAL",
                                message=(
                                    f"Dependencia temporal contradictoria: "
                                    f"'{act_a.name}' debe preceder a "
                                    f"'{act_b.name}' y viceversa"
                                )
                            )
                        )

        return violations
