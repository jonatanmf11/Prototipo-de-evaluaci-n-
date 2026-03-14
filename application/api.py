from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json

from application.loaders.json_loader import ProcessModelLoader
from application.rules.rule_engine import RuleEngine
from application.metrics.metric_engine import MetricEngine

from application.rules.organizational.context_alignment_rule import OrganizationalContextAlignmentRule
from application.rules.formal.has_required_rules_rule import FormalHasRequiredRulesRule
from application.rules.functional.no_redundant_artifacts_rule import FunctionalNoRedundantArtifactsRule
from application.rules.functional.no_role_conflict_rule import FunctionalNoRoleConflictRule
from application.rules.sequential.no_contradictory_dependencies_rule import SequentialNoContradictoryDependenciesRule

from application.metrics.functional.ICF import ICF
from application.metrics.sequential.ICS import ICS
from application.metrics.organizational.NSR import NSR
from application.metrics.formal.CAF import CAF
from application.metrics.functional.mismatch import Mismatch
from application.metrics.formal.CPT import CPT
from application.metrics.Global.IGC import IGC

app = FastAPI()

# -----------------------------
# CORS
# -----------------------------

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# CARGAR MODELO BASE
# -----------------------------

@app.get("/model/base")
def get_base_model():

    with open("data/AGATA.json", "r", encoding="utf-8") as f:
        model = json.load(f)

    return model


# -----------------------------
# ICF DATA
# -----------------------------

@app.get("/icf/pairs")
def get_icf_pairs():

    with open("data/artifactpairs.json", "r", encoding="utf-8") as f:
        pairs = json.load(f)

    return pairs


# -----------------------------
# CAF DATA
# -----------------------------

@app.get("/caf/documentation")
def get_caf_documentation():

    with open("data/caf_documentation.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    return data


# -----------------------------
# CPT DATA
# -----------------------------

@app.get("/cpt/work-products")
def get_cpt_work_products():

    with open("data/cpt.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    return data


# -----------------------------
# MISMATCH DATA
# -----------------------------

@app.get("/mismatch/characteristics")
def get_mismatch_characteristics():

    with open("data/mismatch.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    return data


# -----------------------------
# EVALUAR SOLO REGLAS
# -----------------------------

@app.post("/evaluate/model")
def evaluate_model(model: dict):

    process = ProcessModelLoader.load_from_dict(model)

    engine = RuleEngine()

    engine.register_rule(OrganizationalContextAlignmentRule())
    engine.register_rule(FunctionalNoRedundantArtifactsRule())
    engine.register_rule(FunctionalNoRoleConflictRule())
    engine.register_rule(FormalHasRequiredRulesRule())
    engine.register_rule(SequentialNoContradictoryDependenciesRule())

    violations = engine.evaluate(process)

    return {
        "violations_count": len(violations),
        "violations": [
            {
                "practice_id": v.practice_id,
                "rule": v.rule_name,
                "dimension": v.dimension,
                "message": v.message
            }
            for v in violations
        ]
    }


# -----------------------------
# EVALUAR SOLO MÉTRICAS
# -----------------------------

@app.post("/evaluate/metrics")
def evaluate_metrics(model: dict):

    process = ProcessModelLoader.load_from_dict(model)

    metric_engine = MetricEngine()

    with open("data/artifactpairs.json", "r", encoding="utf-8") as f:
        icf_data = json.load(f)

    with open("data/caf_documentation.json", "r", encoding="utf-8") as f:
        caf_data = json.load(f)

    with open("data/mismatch_project_characteristics.json", "r", encoding="utf-8") as f:
        mismatch_data = json.load(f)

    with open("data/cpt.json", "r", encoding="utf-8") as f:
        cpt_data = json.load(f)

    metric_engine.register_metric(ICS())
    metric_engine.register_metric(ICF(icf_data))
    metric_engine.register_metric(NSR())
    metric_engine.register_metric(CAF(caf_data))
    metric_engine.register_metric(Mismatch(mismatch_data, "agile"))
    metric_engine.register_metric(Mismatch(mismatch_data, "traditional"))
    metric_engine.register_metric(Mismatch(mismatch_data, "hybrid"))
    metric_engine.register_metric(CPT(cpt_data))

    results = metric_engine.evaluate(process, [])

    return {
        "metrics": results
    }


# -----------------------------
# EVALUACIÓN COMPLETA
# -----------------------------

@app.post("/evaluate/full")
def evaluate_full(payload: dict):

    model_data = payload.get("model")
    icf_pairs = payload.get("icf_pairs", [])
    caf_data = payload.get("caf_documentation")
    cpt_data = payload.get("cpt_data")
    mismatch_data = payload.get("mismatch_data")

    if not model_data:
        raise ValueError("Model data not received")

    process = ProcessModelLoader.load_from_dict(model_data)

    # -----------------------------
    # RULE ENGINE
    # -----------------------------

    rule_engine = RuleEngine()

    rule_engine.register_rule(OrganizationalContextAlignmentRule())
    rule_engine.register_rule(FunctionalNoRedundantArtifactsRule())
    rule_engine.register_rule(FunctionalNoRoleConflictRule())
    rule_engine.register_rule(FormalHasRequiredRulesRule())
    rule_engine.register_rule(SequentialNoContradictoryDependenciesRule())

    violations = rule_engine.evaluate(process)

    # -----------------------------
    # METRIC ENGINE
    # -----------------------------

    metric_engine = MetricEngine()

    # ICF

    if icf_pairs and len(icf_pairs) > 0:
        icf_data = icf_pairs
    else:
        with open("data/artifactpairs.json", "r", encoding="utf-8") as f:
            icf_data = json.load(f)

    # CAF

    if not caf_data:
        with open("data/caf_documentation.json", "r", encoding="utf-8") as f:
            caf_data = json.load(f)

    # CPT

    if not cpt_data:
        with open("data/cpt.json", "r", encoding="utf-8") as f:
            cpt_data = json.load(f)

    # MISMATCH

    if not mismatch_data:
        with open("data/mismatch_project_characteristics.json", "r", encoding="utf-8") as f:
            mismatch_data = json.load(f)

    # REGISTER METRICS

    metric_engine.register_metric(ICS())
    metric_engine.register_metric(ICF(icf_data))
    metric_engine.register_metric(NSR())
    metric_engine.register_metric(CAF(caf_data))
    metric_engine.register_metric(Mismatch(mismatch_data, "agile"))
    metric_engine.register_metric(Mismatch(mismatch_data, "traditional"))
    metric_engine.register_metric(Mismatch(mismatch_data, "hybrid"))
    metric_engine.register_metric(CPT(cpt_data))

    results = metric_engine.evaluate(process, violations)

    # -----------------------------
    # GLOBAL INDEX
    # -----------------------------

    igc_metric = IGC()
    igc_value = igc_metric.calculate(results)

    return {
        "violations_count": len(violations),
        "violations": [
            {
                "practice_id": v.practice_id,
                "rule": v.rule_name,
                "dimension": v.dimension,
                "message": v.message
            }
            for v in violations
        ],
        "metrics": results,
        "IGC": igc_value
    }