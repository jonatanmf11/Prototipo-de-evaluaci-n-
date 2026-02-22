from abc import ABC, abstractmethod


class BaseMetric(ABC):
    """
    Clase abstracta base para todas las métricas del prototipo.
    """

    def __init__(self, metric_id: str, name: str, dimension: str):
        self.metric_id = metric_id
        self.name = name
        self.dimension = dimension

    @abstractmethod
    def calculate(self, model, violations=None):
        """
        Ejecuta el cálculo de la métrica.

        :param model: HybridProcessModel
        :param violations: Lista de RuleViolation (opcional)
        :return: dict serializable
        """
        pass
    
    @abstractmethod
    def interpret(self, value: float) -> str:
        """
        Devuelve la interpretación cualitativa del valor numérico
        """
        pass