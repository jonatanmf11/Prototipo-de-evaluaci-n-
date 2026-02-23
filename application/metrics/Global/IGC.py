from application.metrics.base_metric import BaseMetric


class IGC(BaseMetric):
    """
    Índice Global de Consistencia

    IGC = α·DF + β·DO + γ·DS + δ·DFo

    α = 0.30 (Funcional)
    β = 0.30 (Organizacional)
    γ = 0.20 (Secuencial)
    δ = 0.20 (Formal)
    """

    def __init__(self):
        super().__init__(
            metric_id="M_IGC",
            name="IGC",
            dimension="global"
        )

        self.alpha = 0.30  # Funcional
        self.beta = 0.30   # Organizacional
        self.gamma = 0.20  # Secuencial
        self.delta = 0.20  # Formal

    def calculate(self, metric_results: dict) -> float:
        """
        metric_results debe ser el diccionario que devuelve MetricEngine.evaluate()
        """

        
        # Dimensión Funcional (DF)
        
        icf = metric_results.get("ICF", {}).get("value", 0)
        # Dimensión Funcional (DF)

        icf = metric_results.get("ICF", {}).get("value", 0)

        #se toma el mejor ajuste (menor mismatch)
        mismatch_agile = metric_results.get("MISMATCH_AGILE", {}).get("value", 0)
        mismatch_traditional = metric_results.get("MISMATCH_TRADITIONAL", {}).get("value", 0)
        mismatch_hybrid = metric_results.get("MISMATCH_HYBRID", {}).get("value", 0)

        raw_mismatch = min(mismatch_agile, mismatch_traditional, mismatch_hybrid)

        # normalizacion mismatch
        max_possible = 600
        normalized_mismatch = 1 - (raw_mismatch / max_possible)

        DF = (icf + normalized_mismatch) / 2
#
        
        # 2Dimensión Organizacional (DO)
       
        DO = metric_results.get("NSR", {}).get("value", 0)

        
        # 3Dimensión Secuencial (DS)
        
        DS = metric_results.get("ICS", {}).get("value", 0)

       
        # 4Dimensión Formal (DFo)
        
        caf = metric_results.get("CAF", {}).get("value", 0) / 100
        cpt = metric_results.get("CPT", {}).get("value", 0)

        DFo = (caf + cpt) / 2 if (caf or cpt) else 0

       
        # 5Cálculo final ponderado
        
        igc = (
            self.alpha * DF +
            self.beta * DO +
            self.gamma * DS +
            self.delta * DFo
        )

        return max(0, min(1, igc))

    def interpret(self, value: float) -> str:

        if value >= 0.80:
            return "Proceso híbrido altamente consistente y equilibrado"
        elif value >= 0.60:
            return "Consistencia moderada con áreas de mejora"
        elif value >= 0.40:
            return "Consistencia baja; existen desalineaciones relevantes"
        else:
            return "Proceso híbrido inconsistente y con alto riesgo estructural"

    def __repr__(self):
        return f"{self.__class__.__name__}(name='{self.name}')"