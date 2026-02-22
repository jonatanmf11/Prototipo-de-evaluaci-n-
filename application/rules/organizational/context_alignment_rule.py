from typing import List

from application.rules.base_rule import BaseRule
from application.rules.rule_violation import RuleViolation
from domain.hybrid_process_model import HybridProcessModel


class OrganizationalContextAlignmentRule(BaseRule):
    """
    OCL:
    context Practice
    inv Organizational_ContextAlignment:
    self.contextRequirements->forAll(req |
        self.projectContext->includes(req)
    )
    """

    def __init__(self):
        super().__init__(
            rule_id="O1",
            name="Organizational Context Alignment",
            description=(
                "Verifica que los requisitos contextuales de cada práctica "
                "estén alineados con el contexto del proyecto"
            ),
            dimension="organizational"
        )

    def evaluate(
        self,
        model: HybridProcessModel
    ) -> List[RuleViolation]:

        violations: List[RuleViolation] = []
        project_context = set(model.project_context)

        for practice in model.practices:
            for req in practice.context_requirements:
                if req not in project_context:
                    violations.append(
                        RuleViolation(
                            practice_id=practice.id,
                            rule_id=self.rule_id,
                            rule_name=self.name,
                            dimension=self.dimension,
                            message=(
                                f"El requisito contextual '{req}' "
                                f"no está presente en el contexto del proyecto"
                            )
                        )
                    )

        return violations
