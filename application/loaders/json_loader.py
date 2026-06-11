import json

from domain.practice import Practice
from domain.enumType import EnumType
from domain.role import Role
from domain.activity import Activity
from domain.artifact import Artifact
from domain.hybrid_process_model import HybridProcessModel
from domain.compability.compatibility_relation import CompatibilityRelation


class ProcessModelLoader:
    """
    Cargador del modelo de proceso híbrido desde JSON.
    """

    @staticmethod
    def load_from_file(path: str) -> HybridProcessModel:
        """
        Carga el modelo desde un archivo JSON.
        """
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        return ProcessModelLoader.load_from_dict(data)

    @staticmethod
    def load_from_dict(data: dict) -> HybridProcessModel:
        """
        Construye el modelo híbrido a partir de un diccionario.
        (Usado por API, tests o CLI)
        """

        practices = []

        # -----------------------------
        # Cargar prácticas
        # -----------------------------
        for p in data.get("practices", []):

            roles = [
                Role(
                    id=r["id"],
                    name=r.get("name", r["id"])
                )
                for r in p.get("roles", [])
            ]

            activities = [
                Activity(
                    id=a["id"],
                    name=a.get("name", a["id"]),
                    type=a.get("type", "agile"),
                    must_precede=a.get(
                        "mustPrecede",
                        []
                    )
                )
                for a in p.get("activities", [])
            ]

            artifacts = [
                Artifact(
                    id=ar["id"],
                    name=ar.get("name", ar["id"]),
                    category=ar.get(
                        "category",
                        "Document"
                    )
                )
                for ar in p.get("artifacts", [])
            ]

            practice = Practice(
                id=p["id"],
                name=p.get(
                    "name",
                    p["id"]
                ),
                type=EnumType(
                    p.get(
                        "type",
                        "agile"
                    ).lower()
                ),
                roles=roles,
                activities=activities,
                artifacts=artifacts,
                rules=p.get(
                    "rules",
                    []
                ),
                required_rules=p.get(
                    "requiredRules",
                    []
                ),
                context_requirements=p.get(
                    "contextRequirements",
                    []
                )
            )

            practices.append(practice)

        # -----------------------------
        # Crear mapa de prácticas
        # -----------------------------
        practice_map = {
            p.id: p
            for p in practices
        }

        # -----------------------------
        # Relaciones de compatibilidad
        # -----------------------------
        relations = []

        for r in data.get(
            "compatibilityRelations",
            []
        ):

            if (
                r["practiceA"] in practice_map
                and
                r["practiceB"] in practice_map
            ):

                relations.append(
                    CompatibilityRelation(
                        r["type"],
                        practice_map[
                            r["practiceA"]
                        ],
                        practice_map[
                            r["practiceB"]
                        ]
                    )
                )

        # -----------------------------
        # Construir modelo final
        # -----------------------------
        return HybridProcessModel(
            id=data.get(
                "id",
                "UNKNOWN"
            ),
            practices=practices,
            project_context=data.get(
                "projectContext",
                []
            ),
            compatibility_relations=relations
        )