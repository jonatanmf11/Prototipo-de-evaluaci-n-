
from application.metrics.base_metric import BaseMetric

class CPT(BaseMetric):
    
    def __init__(self, data: dict):
        self.data = data
        super().__init__(
            metric_id="M_CPT",
            name="CPT",
            dimension="formal"
        )


    def calculate(self, model=None, violations=None) -> float:

        agile_wp = set(self.data.get("agileWorkProducts", []))
        plan_wp = set(self.data.get("planDrivenWorkProducts", []))

        if not agile_wp and not plan_wp:
            return 0.0

        intersection = agile_wp.intersection(plan_wp)
        union = agile_wp.union(plan_wp)

        if not union:
            return 0.0

        return len(intersection) / len(union)

    def interpret(self, value: float) -> str:

        if value >= 0.70:
            return "Fuerte integración formal"
        elif value >= 0.40:
            return "Integración parcial"
        elif value >= 0.20:
            return "Segregación significativa de artefactos"
        else:
            return "Ausencia de integración formal"
        
    def __repr__(self):
        return f"{self.__class__.__name__}(name='{self.name}')"