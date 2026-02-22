from application.metrics.base_metric import BaseMetric


class ICF(BaseMetric):

    def __init__(self, artifact_pairs=None):
        super().__init__(
            metric_id="M_ICF",
            name="ICF",
            dimension="functional"
        )
        self.artifact_pairs = artifact_pairs or []

    def calculate(self, model, violations=None):

        if not self.artifact_pairs:
            return 0.0

        total_equivalence = sum(
            max(0.0, min(1.0, pair.get("equivalence", 0.0)))
            for pair in self.artifact_pairs
        )

        return total_equivalence / len(self.artifact_pairs)

    
    def interpret(self, value: float) -> str:
        if value >= 0.80:
            return "Alta equivalencia funcional"
        elif value >= 0.65:
            return "Equivalencia funcional moderada"
        elif value >= 0.50:
            return "Equivalencia funcional baja"
        else:
            return "Equivalencia funcional débil"
    
    
    def __repr__(self):
        return f"{self.__class__.__name__}(name='{self.name}')"