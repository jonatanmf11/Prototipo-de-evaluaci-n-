from application.metrics.base_metric import BaseMetric


class Mismatch(BaseMetric):
    def __init__(self, mismatch_data: dict, methodology: str):
        super().__init__(
            metric_id=f"M_MISMATCH_{methodology.upper()}",
            name=f"MISMATCH_{methodology.upper()}",
            dimension="strategic"
        )
        self.data = mismatch_data
        self.methodology = methodology.lower()

    def calculate(self, model=None, violations=None):
        mismatch_score = 0
        max_possible = 0

        for characteristic in self.data["characteristics"]:
            project_value = characteristic["projectValue"]
            weight = characteristic.get("weight", 1)
            methodology_value = characteristic["methodologies"].get(self.methodology, 0)

            mismatch_score += weight * abs(project_value - methodology_value)
            max_possible += weight * 100

        if max_possible == 0:
            return 0.0

        normalized = 1 - (mismatch_score / max_possible)
        return round(normalized, 4)

    def interpret(self, value):
        if value >= 0.75:
            return "Alta compatibilidad: el proceso se ajusta bien al contexto"
        elif value >= 0.50:
            return "Compatibilidad moderada: existen desajustes en algunas características"
        else:
            return "Baja compatibilidad: desalineación severa entre proceso y contexto"