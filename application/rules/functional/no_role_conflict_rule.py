from typing import List, Dict, Set

from application.rules.base_rule import BaseRule
from application.rules.rule_violation import RuleViolation
from domain.hybrid_process_model import HybridProcessModel


class FunctionalNoRoleConflictRule(BaseRule):
    """
    OCL:
    context HybridProcessModel
    inv NoRoleConflict:
    A role must not participate in practices of different types.
    
    context HybridProcessModel
inv NoRoleConflict:
self.practices.roles->forAll(r |
    self.practices->select(p | p.roles->includes(r))
                   ->collect(p | p.type)
                   ->asSet()->size() = 1
)

    """

    def __init__(self):
        super().__init__(
            rule_id="F2",
            name="No Role Conflict",
            description=(
                "Verifica que un mismo rol no participe en prácticas "
                "de tipos funcionales diferentes"
            ),
            dimension="functional"
        )

    def evaluate(
        self,
        model: HybridProcessModel
    ) -> List[RuleViolation]:

        violations: List[RuleViolation] = []

        role_usage: Dict[str, Set[str]] = {}

        for practice in model.practices:
            for role in practice.roles:
                role_usage.setdefault(role.id, set()).add(practice.type.value)

        for role_id, practice_types in role_usage.items():
            if len(practice_types) > 1:
                violations.append(
                    RuleViolation(
                        practice_id="GLOBAL",
                        rule_id=self.rule_id,
                        rule_name=self.name,
                        dimension=self.dimension,
                        message=(
                            f"El rol '{role_id}' participa en prácticas "
                            f"de tipos incompatibles: {practice_types}"
                        )
                    )
                )

        return violations
