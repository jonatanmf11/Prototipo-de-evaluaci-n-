from typing import List

from application.rules.base_rule import BaseRule
from application.rules.rule_violation import RuleViolation
from domain.hybrid_process_model import HybridProcessModel


class FormalHasRequiredRulesRule(BaseRule):
    """
    OCL:
    context Practice
    inv Formal_HasRequiredRules:
    self.rules->size() >= self.requiredRules->size()
    """

    def __init__(self):
        super().__init__(
            rule_id="F1",
            name="Formal Has Required Rules",
            description=(
                "Verifica que cada práctica tenga definidas al menos "
                "las reglas formales mínimas requeridas"
            ),
            dimension="formal"
        )

    def evaluate(
        self,
        model: HybridProcessModel
    ) -> List[RuleViolation]:

        violations: List[RuleViolation] = []

        for practice in model.practices:
            if len(practice.rules) < len(practice.required_rules):
                violations.append(
                    RuleViolation(
                        practice_id=practice.id,
                        rule_id=self.rule_id,
                        rule_name=self.name,
                        dimension=self.dimension,
                        message=(
                            f"La práctica define {len(practice.rules)} reglas, "
                            f"pero requiere al menos {len(practice.required_rules)}"
                        )
                    )
                )

        return violations
