from application.DataEvaluacionReglas.no_redundant_artifacts_rule.NoRedundantArtifactsEvaluator import NoRedundantArtifactsEvaluator
from application.DataEvaluacionReglas.no_role_conflict_rule.noRoleConflictEvaluator import NoRoleConflictEvaluator
from application.DataEvaluacionReglas.has_required_rules.has_required_rulesEvaluator import hasRequiredRulesEvaluator
from application.DataEvaluacionReglas.context_alignment.context_alignment import contextalignmentEvaluator
from application.DataEvaluacionReglas.no_contradictory_dependencies.no_contradictory_dependenciesEvaluator import (
    NoContradictoryDependenciesEvaluator
)
def main():
     
     #evaluar No_redundant_artifacts
     
    json_NRA = (
        "application/DataEvaluacionReglas/"
        "no_redundant_artifacts_rule/"
        "modelosPruebas.json"
    )

    csv_NRA = (
        "application/DataEvaluacionReglas/"
        "no_redundant_artifacts_rule/"
        "noredundantrulesCalculados.csv"
    )

    output_NRA = (
        "application/DataEvaluacionReglas/"
        "no_redundant_artifacts_rule/"
        "resultadosEvaluacion.csv"
    )

    evaluatorNRA = NoRedundantArtifactsEvaluator(
        json_NRA,
        csv_NRA,
        output_NRA
    )

    evaluatorNRA.run()
    
    #Evaluar no role conflict
    
    json_NRC = (
        "application/DataEvaluacionReglas/no_role_conflict_rule/"
        "NRC.json"
    )

    csv_NRC = (
        "application/DataEvaluacionReglas/no_role_conflict_rule/"
        "NRC.csv"
    )

    output_NRC = (
        "application/DataEvaluacionReglas/"
        "no_redundant_artifacts_rule/"
        "resultadosEvaluacionNRC.csv"
    )

    evaluatorNRC = NoRoleConflictEvaluator(
        json_NRC,
        csv_NRC,
        output_NRC
    )
    

    evaluatorNRC.run()
    
    
    #Evaluar has required rules
    
    
    json_HRR = (
        "application/DataEvaluacionReglas/has_required_rules/HRR.json"
    )

    csv_HRR = (
        "application/DataEvaluacionReglas/has_required_rules/HRRCalculados.csv"
    )

    output_HRR = (
        "application/DataEvaluacionReglas/has_required_rules/HRRResultadoss.csv"
    )

    evaluator_HRR = hasRequiredRulesEvaluator(
        json_HRR,
        csv_HRR,
        output_HRR
    )
    

    evaluator_HRR.run()

#Evaluar context alignment
    
    
    json_CA = (
        "application/DataEvaluacionReglas/context_alignment/CA.json"
    )

    csv_CA = (
        "application/DataEvaluacionReglas/context_alignment/CACalculados.csv"
    )

    output_CA = (
        "application/DataEvaluacionReglas/context_alignment/CAResultados.csv"
    )

    evaluator_CA = contextalignmentEvaluator(
        json_CA,
        csv_CA,
        output_CA
    )
    

    evaluator_CA.run()
    
    #Evaluar no contradictory dependencies 
  
    json_NCD = (
        "application/DataEvaluacionReglas/no_contradictory_dependencies/NCD.json"
    )

    csv_NCD = (
        "application/DataEvaluacionReglas/no_contradictory_dependencies/NCDCalculado.csv"
    )

    output_NCD = (
        "application/DataEvaluacionReglas/no_contradictory_dependencies/NCDResultados.csv"
    )

    evaluator_NCD = NoContradictoryDependenciesEvaluator(
        json_NCD,
        csv_NCD,
        output_NCD
    )
    

    evaluator_NCD.run()
    
    
if __name__ == "__main__":
    main()