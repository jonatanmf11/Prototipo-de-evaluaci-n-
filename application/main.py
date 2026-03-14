import json

from domain.enumType import EnumType
from application.loaders.json_loader import ProcessModelLoader
from domain.practice import Practice
from domain.role import Role
from domain.activity import Activity
from domain.context.project_context import ProjectContext
from domain.compability.compatibility_relation import CompatibilityRelation

from application.rules.rule_engine import RuleEngine

from application.rules.organizational.context_alignment_rule import (
    OrganizationalContextAlignmentRule
)
from application.rules.formal.has_required_rules_rule import (
    FormalHasRequiredRulesRule
)
from application.rules.functional.no_redundant_artifacts_rule import (
    FunctionalNoRedundantArtifactsRule
)
from application.rules.functional.no_role_conflict_rule import (
    FunctionalNoRoleConflictRule
)

from application.rules.formal.has_required_rules_rule import (
    FormalHasRequiredRulesRule
)

from application.rules.sequential.no_contradictory_dependencies_rule import (
    SequentialNoContradictoryDependenciesRule
)
from application.metrics.metric_engine import MetricEngine
from application.metrics.functional.ICF import ICF
from application.metrics.sequential.ICS import ICS
from application.metrics.organizational.NSR import NSR
from application.metrics.formal.CAF import CAF
from application.metrics.functional.mismatch import Mismatch
from application.metrics.formal.CPT import CPT 
from application.metrics.Global.IGC import IGC 



def main():
    print("Prueba AGATA ")

    # 1. Cargar modelo desde JSON
    process = ProcessModelLoader.load_from_file("data/AGATA_final.json")


    # 2. Inicializar Rule Engine
    engine = RuleEngine()
    engine.register_rule(OrganizationalContextAlignmentRule())
    engine.register_rule(FunctionalNoRedundantArtifactsRule())
    engine.register_rule(FunctionalNoRoleConflictRule())
    engine.register_rule(FormalHasRequiredRulesRule())
    engine.register_rule(SequentialNoContradictoryDependenciesRule())

    # 3. Evaluar reglas organizacionales
    violations = engine.evaluate(process)
    print(f"\nTotal de violaciones detectadas: {len(violations)}\n")
    # 4. Mostrar resultados
    if not violations:
      print("✅ No se detectaron violaciones")
    else:
        print("❌ Violaciones detectadas:\n")
        for v in violations:
            print(f"- Práctica: {v.practice_id}")
            print(f"  Regla: {v.rule_name}")
            print(f"  dimensión: {v.dimension}")
            print(f"  Descripción: {v.message}\n")

# 🔹 Leer JSON externo con los pares ICF desde carpeta data
    with open("data/artifactpairs.json", "r", encoding="utf-8") as file:
        icf_data = json.load(file)
    with open("data/caf_documentation.json", "r", encoding="utf-8") as f:
        caf_data = json.load(f)


    violations = engine.evaluate(process)

    metric_engine = MetricEngine()
    metric_engine.register_metric(ICS())
    metric_engine.register_metric(ICF(icf_data))
    metric_engine.register_metric(NSR())
    metric_engine.register_metric(CAF(caf_data))
    
     
    with open("data/mismatch.json", "r", encoding="utf-8") as f:
        mismatch_data = json.load(f)

    metric_engine.register_metric(Mismatch(mismatch_data, "agile"))
    metric_engine.register_metric(Mismatch(mismatch_data, "traditional"))
    metric_engine.register_metric(Mismatch(mismatch_data, "hybrid"))
    
    with open("data/cpt.json", "r", encoding="utf-8") as f:
        cpt_data = json.load(f)
    
    metric_engine.register_metric(CPT(cpt_data))
    
    results = metric_engine.evaluate(process, violations)
    
    results = metric_engine.evaluate(process, violations)
    print("\nResultados métricas:")

    for metric_name, data in results.items():
        value = data["value"]
        interpretation = data["interpretation"]

        print(f"{metric_name}: {value:.4f}")
        print(f"{interpretation}\n")
    
    
    

    igc_metric = IGC()

    igc_value = igc_metric.calculate(results)
    igc_interpretation = igc_metric.interpret(igc_value)

    print("IGC: {:.4f}".format(igc_value))
    print("  →", igc_interpretation)
   
    
if __name__ == "__main__":
    main()
  