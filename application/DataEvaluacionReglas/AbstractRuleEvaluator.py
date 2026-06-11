from abc import ABC, abstractmethod
import json
import csv

from sklearn.metrics import (
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix
)

from application.loaders.json_loader import ProcessModelLoader
from application.rules.rule_engine import RuleEngine


class AbstractRuleEvaluator(ABC):

    def __init__(
        self,
        json_path: str,
        csv_path: str,
        output_path: str
    ):
        self.json_path = json_path
        self.csv_path = csv_path
        self.output_path = output_path

        self.expected = []
        self.predicted = []

        self.results = []

    # ---------------------------------------------------
    # Cargar valores esperados
    # ---------------------------------------------------

    def load_expected_from_csv(self):

        with open(
            self.csv_path,
            newline="",
            encoding="utf-8"
        ) as f:

            reader = csv.DictReader(
                f,
                delimiter=";"
            )

            self.expected = [
                int(row["Violaciones detectadas"])
                for row in reader
            ]

    # ---------------------------------------------------
    # Ejecutar regla sobre JSON
    # ---------------------------------------------------

    def evaluate_models_from_json(self):

        with open(
            self.json_path,
            "r",
            encoding="utf-8"
        ) as f:

            data = json.load(f)

        if isinstance(data, dict):
            models = data.get("models", [data])

        elif isinstance(data, list):
            models = data

        else:
            raise ValueError(
                "Formato JSON no soportado"
            )

        engine = RuleEngine()
        engine.register_rule(
            self.get_rule()
        )

        self.predicted = []
        self.results = []

        for index, model_data in enumerate(models):

            process = (
                ProcessModelLoader
                .load_from_dict(model_data)
            )

            violations = engine.evaluate(
                process
            )

            detected = (
                1 if len(violations) > 0
                else 0
            )

            self.predicted.append(
                detected
            )

            expected = (
                self.expected[index]
                if index < len(self.expected)
                else None
            )

            self.results.append({
                "Caso": index + 1,
                "Esperado": expected,
                "Predicho": detected,
                "CantidadViolaciones":
                    len(violations)
            })

    # ---------------------------------------------------
    # Guardar resultados detallados
    # ---------------------------------------------------

    def save_results(self):

        with open(
            self.output_path,
            mode="w",
            newline="",
            encoding="utf-8"
        ) as f:

            writer = csv.DictWriter(
                f,
                fieldnames=[
                    "Caso",
                    "Esperado",
                    "Predicho",
                    "CantidadViolaciones"
                ],
                delimiter=";"
            )

            writer.writeheader()

            for row in self.results:
                writer.writerow(row)

    # ---------------------------------------------------
    # Calcular métricas
    # ---------------------------------------------------

    def calculate_metrics(self):

        precision = precision_score(
            self.expected,
            self.predicted,
            zero_division=0
        )

        recall = recall_score(
            self.expected,
            self.predicted,
            zero_division=0
        )

        f1 = f1_score(
            self.expected,
            self.predicted,
            zero_division=0
        )

        tn, fp, fn, tp = confusion_matrix(
            self.expected,
            self.predicted
        ).ravel()

        print("\n=== RESULTADOS ===")
        print("Precision:", precision)
        print("Recall:", recall)
        print("F1:", f1)

        print("\n=== MATRIZ DE CONFUSIÓN ===")
        print("TP:", tp)
        print("TN:", tn)
        print("FP:", fp)
        print("FN:", fn)

        return {
            "precision": precision,
            "recall": recall,
            "f1": f1,
            "tp": tp,
            "tn": tn,
            "fp": fp,
            "fn": fn
        }

    # ---------------------------------------------------
    # Ejecución completa
    # ---------------------------------------------------

    def run(self):

        self.load_expected_from_csv()

        self.evaluate_models_from_json()

        self.save_results()

        return self.calculate_metrics()

    @abstractmethod
    def get_rule(self):
        pass