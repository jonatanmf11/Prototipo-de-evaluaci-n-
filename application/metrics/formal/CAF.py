from application.metrics.base_metric import BaseMetric

class CAF(BaseMetric):

    def __init__(self, documentation_data: dict):
        super().__init__(
            metric_id="M_CAF",
            name="CAF",
            dimension="formal"
        )

        self.documentation_data = documentation_data

        self.weights = {
            "activities": 0.30,
            "rules": 0.20,
            "roles": 0.15,
            "artifacts": 0.20,
            "sequence": 0.10,
            "metrics": 0.05
        }

    def calculate(self, model, violations=None):

        # -----------------------------
        # Totales desde el modelo
        # -----------------------------

        total_activities = sum(len(p.activities) for p in model.practices)
        total_rules = len(model.practices)
        total_roles = sum(len(p.roles) for p in model.practices)
        total_artifacts = sum(len(p.artifacts) for p in model.practices)
        total_sequence = len(model.compatibility_relations)
        total_metrics = 1  # asumimos al menos el sistema métrico existe

        # -----------------------------
        # Documentados desde JSON externo
        # -----------------------------

        documented_activities = len([
            a for a in self.documentation_data.get("activities", [])
            if a.get("documented", False)
        ])

        documented_rules = len([
            r for r in self.documentation_data.get("rules", [])
            if r.get("documented", False)
        ])

        documented_roles = len([
            r for r in self.documentation_data.get("roles", [])
            if r.get("documented", False)
        ])

        documented_artifacts = len([
            a for a in self.documentation_data.get("artifacts", [])
            if a.get("documented", False)
        ])

        documented_sequence = len([
            s for s in self.documentation_data.get("sequence", [])
            if s.get("documented", False)
        ])

        documented_metrics = len([
            m for m in self.documentation_data.get("metrics", [])
            if m.get("documented", False)
        ])

        # -----------------------------
        # Cálculo normalizado por categoría
        # -----------------------------

        scores = {}

        scores["activities"] = (
            documented_activities / total_activities
            if total_activities > 0 else 1
        )

        scores["rules"] = (
            documented_rules / total_rules
            if total_rules > 0 else 1
        )

        scores["roles"] = (
            documented_roles / total_roles
            if total_roles > 0 else 1
        )

        scores["artifacts"] = (
            documented_artifacts / total_artifacts
            if total_artifacts > 0 else 1
        )

        scores["sequence"] = (
            documented_sequence / total_sequence
            if total_sequence > 0 else 1
        )

        scores["metrics"] = (
            documented_metrics / total_metrics
            if total_metrics > 0 else 1
        )

        # -----------------------------
        # Ponderación
        # -----------------------------

        caf = sum(
            scores[k] * self.weights[k]
            for k in self.weights
        )

        return caf * 100

    def interpret(self, value: float) -> str:

        if value > 80:
            return "Alta cobertura formal, proceso maduro y replicable"
        elif value >= 60:
            return "Cobertura moderada, existen áreas de mejora"
        else:
            return "Baja formalización, alto riesgo de dependencia informal"