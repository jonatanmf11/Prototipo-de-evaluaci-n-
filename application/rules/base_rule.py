from abc import ABC, abstractmethod
from typing import List
from application.rules.rule_violation import RuleViolation
from domain.hybrid_process_model import HybridProcessModel


class BaseRule(ABC):
    """
    Regla abstracta del motor de reglas.
    """

    def __init__(self, rule_id: str, name: str, description: str, dimension: str):
        self.rule_id = rule_id
        self.name = name
        self.description = description
        self.dimension = dimension
        

    @abstractmethod
    def evaluate(self, model: HybridProcessModel) -> List[RuleViolation]:
        pass
