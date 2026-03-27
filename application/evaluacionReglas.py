import json
from application.loaders.json_loader import ProcessModelLoader
from application.rules.rule_engine import RuleEngine
from application.rules.functional.no_redundant_artifacts_rule import (
    FunctionalNoRedundantArtifactsRule
)
import csv
from sklearn.metrics import precision_score, recall_score, f1_score

def main():
    path = "application/DataEvaluacionReglas/no_redundant_artifacts_rule/modelosPruebas.json"
    ruta_entrada = "application/DataEvaluacionReglas/no_redundant_artifacts_rule/noredundantrulesCalculados.csv"
    ruta_salida = "application/DataEvaluacionReglas/no_redundant_artifacts_rule/noredundantrulesResultados.csv"
    calculados = [] 
    
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    
    if isinstance(data, dict):
        if "models" in data:
            models = data["models"]
        else:
            
            models = [data]
    elif isinstance(data, list):
        models = data
    else:
        raise ValueError("Formato de JSON no soportado")

    engine = RuleEngine()
    engine.register_rule(FunctionalNoRedundantArtifactsRule())

    total_violations = 0

    for model_data in models:
        #print("=" * 50)
        #print(f"Evaluando modelo: {model_data['id']} - {model_data['name']}")

        process = ProcessModelLoader.load_from_dict(model_data)

        violations = engine.evaluate(process)
        resultado = 1 if len(violations) > 0 else 0
        calculados.append(resultado)


    print("\n RESULTADOS DE LA EVALUACION:")
    print(calculados)





    violaciones_entrada= []

    with open(ruta_entrada, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=";")
        
        for row in reader:
            violaciones_entrada.append(int(row["Violaciones detectadas"]))

    print(violaciones_entrada)


    precision = precision_score(violaciones_entrada, calculados)
    recall = recall_score(violaciones_entrada, calculados)
    f1 = f1_score(violaciones_entrada, calculados)

    print("Precision:", precision)
    print("Recall:", recall)
    print("F1-score:", f1)
if __name__ == "__main__":
    main()