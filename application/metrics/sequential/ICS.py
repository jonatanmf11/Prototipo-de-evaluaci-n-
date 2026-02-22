from application.metrics.base_metric import BaseMetric


class ICS(BaseMetric):
    """
    Índice de Compatibilidad de Secuencia (ICS)

    ICS = 1 - (conflictos_secuenciales / total_transiciones)
    """

    def __init__(self):
        super().__init__(
            metric_id="M_ICS",
            name="ICS",
            dimension="sequential"
        )

    def calculate(self, model, violations=None):

        # 🔹 1. Contar total de transiciones secuenciales
        total_transitions = sum(
            1
            for relation in model.compatibility_relations
            if relation.relation_type == "Sequential"
        )

        if total_transitions == 0:
            return 1.0

        # 🔹 2. Contar solo violaciones F3 (conflictos secuenciales)
        total_conflicts = 0

        if violations:
            total_conflicts = sum(
                1 for v in violations
                if v.rule_id == "F3"
            )

        # 🔹 3. Aplicar fórmula
        ics = 1 - (total_conflicts / total_transitions)

        return max(0.0, min(1.0, ics))
    
    def interpret(self, value: float) -> str:
        if value >= 0.85:
            return "Alta compatibilidad secuencial"
        elif value >= 0.70:
            return "Compatibilidad secuencial moderada"
        elif value >= 0.50:
            return "Compatibilidad secuencial baja"
        else:
            return "Compatibilidad secuencial crítica"

    def __repr__(self):
        return f"{self.__class__.__name__}(name='{self.name}')"