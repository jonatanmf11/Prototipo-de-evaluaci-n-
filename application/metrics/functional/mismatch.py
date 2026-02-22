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

        for characteristic in self.data["characteristics"]:

            project_value = characteristic["projectValue"]
            weight = characteristic.get("weight", 1)

            methodology_scores = characteristic["methodologies"]
            methodology_value = methodology_scores.get(self.methodology, 0)

            mismatch_score += weight * abs(project_value - methodology_value)

        return round(mismatch_score, 4)

    def interpret(self, value):
        return value