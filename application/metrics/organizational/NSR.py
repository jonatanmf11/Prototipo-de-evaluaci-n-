from application.metrics.base_metric import BaseMetric


class NSR(BaseMetric):

    def __init__(self):
        super().__init__(
            
            metric_id="M_NSR",
            name="NSR",
            dimension="organizational"
        )

    def calculate(self, model, violations=None):

        total_responsibilities = sum(
            len(practice.roles)
            for practice in model.practices
        )

        if total_responsibilities == 0:
            return 1.0

        overlapped = 0

        if violations:
            overlapped = sum(
                1 for v in violations
                if v.rule_id == "F2"
            )

        return 1 - (overlapped / total_responsibilities)

    def interpret(self, value: float) -> str:

        if value > 0.85:
            return "Roles bien definidos y baja probabilidad de conflictos"

        elif value >= 0.70:
            return "Claridad aceptable con solapamientos menores"

        else:
            return "Fuerte ambigüedad y alto riesgo de conflictos"