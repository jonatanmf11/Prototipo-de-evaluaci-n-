class MetricEngine:

    def __init__(self):
        self.metrics = []

    def register_metric(self, metric):
        self.metrics.append(metric)

    def evaluate(self, model, violations=None):
        results = {}

        for metric in self.metrics:
            try:
                value = metric.calculate(model, violations)
            except TypeError:
                value = metric.calculate(model)

            results[metric.name] = {
                "value": value,
                "interpretation": metric.interpret(value)
            }

        return results