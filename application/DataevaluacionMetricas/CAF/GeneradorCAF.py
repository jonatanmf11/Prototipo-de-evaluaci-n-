import json
import random

NUM_CASOS = 200

ACTIVITIES = [
    "A_REU_REQ", "A_ID_ATTR_CAL", "A_DEF_HU", "A_ATTR_DD",
    "A_QA_ATT_WKS", "A_ID_TAC_ARQ", "A_DIB_PERF_ARQ",
    "A_EV_ARQ_DLLO", "A_SPR_PLAN_MEET", "A_PRD_BACK_ORG",
    "A_IT_PLANNING", "A_EFF_ESTIMATION", "A_PRJ_VELOCITY_CALC",
    "A_DELIVERY_PLAN_DEF", "A_DAILY_SPR_MEET", "A_SPR_REVIEW",
    "A_SPR_RETROSPECTIVE", "A_INTEG_CONTINUA",
    "A_INCRE_VALIDATION", "A_TEST_DRIVEN_DEV",
    "A_REFACTORING", "A_SIMPLE_DESIGN",
    "A_SYST_MET_APP", "A_COLLECTIVE_CODE_OWN",
    "A_CODE_CONVENTIONS"
]

RULES = [
    "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8"
]

ROLES = [
    "R_SRCUM_XP",
    "R_SCRUM_XA",
    "R_PO",
    "R_AGATA_MASTER"
]

ARTIFACTS = [
    "AR_REQ_DOC",
    "USER_STORIES",
    "QUALITY_ATTR",
    "AR_ARCH_HISTORY",
    "AR_ARCH_DRAFT",
    "PRODUCT_BACKLOG",
    "SPRINT_BACKLOG",
    "AR_Plan_Delivery",
    "PRODUCT_INCREMENT",
    "RETRO_ACTIONS",
    "SOURCE_CODE",
    "UNIT_TESTS",
    "ACCEPTANCE_TESTS",
    "ARCH_REFACTOR_LOG"
]

METRICS = [
    "ICF",
    "ICS",
    "NSR",
    "CAF",
    "CPT",
    "MISMATCH"
]

SEQUENCES = [
    ("P01", "P02"),
    ("P02", "P03"),
    ("P03", "P04"),
    ("P04", "P05"),
    ("P05", "P06"),
    ("P06", "P07"),
    ("P07", "P08"),
    ("P08", "P09")
]


def generar_items(catalogo):

    cantidad = random.randint(0, len(catalogo))

    seleccionados = random.sample(
        catalogo,
        cantidad
    )

    return [
        {
            "id": item,
            "documented": random.choice(
                [True, False]
            )
        }
        for item in seleccionados
    ]


def generar_secuencias():

    cantidad = random.randint(
        0,
        len(SEQUENCES)
    )

    seleccionados = random.sample(
        SEQUENCES,
        cantidad
    )

    return [
        {
            "practiceA": a,
            "practiceB": b,
            "documented": random.choice(
                [True, False]
            )
        }
        for a, b in seleccionados
    ]


def calcular_expected_caf(caso):

    weights = {
        "activities": 0.30,
        "rules": 0.20,
        "roles": 0.15,
        "artifacts": 0.20,
        "sequence": 0.10,
        "metrics": 0.05
    }

    scores = {}

    for categoria in weights:

        total = len(caso[categoria])

        if total == 0:
            scores[categoria] = 1
            continue

        documentados = sum(
            1
            for elemento in caso[categoria]
            if elemento["documented"]
        )

        scores[categoria] = (
            documentados / total
        )

    caf = sum(
        scores[k] * weights[k]
        for k in weights
    )

    return round(caf * 100, 6)


casos = []

for i in range(1, NUM_CASOS + 1):

    caso = {
        "id": i,
        "activities": generar_items(ACTIVITIES),
        "rules": generar_items(RULES),
        "roles": generar_items(ROLES),
        "artifacts": generar_items(ARTIFACTS),
        "sequence": generar_secuencias(),
        "metrics": generar_items(METRICS)
    }

    caso["expectedCAF"] = calcular_expected_caf(
        caso
    )

    casos.append(caso)


with open(
    "application/DataevaluacionMetricas/CAF/dataCAF.json",
    "w",
    encoding="utf-8"
) as archivo:

    json.dump(
        casos,
        archivo,
        indent=2,
        ensure_ascii=False
    )

print(
    f"Se generaron {NUM_CASOS} casos para CAF."
)