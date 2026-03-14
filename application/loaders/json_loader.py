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

        #Cargar prácticas
        for p in data.get("practices", []):

            roles = [
                Role(id=r["id"], name=r["name"])
                for r in p.get("roles", [])
            ]

            activities = [
                Activity(
                    id=a["id"],
                    name=a["name"],
                    type=a["type"],
                    must_precede=a.get("mustPrecede", [])
                )
                for a in p.get("activities", [])
            ]

            artifacts = [
                Artifact(
                    id=ar["id"],
                    name=ar["name"],
                    category=ar["category"]
                )
                for ar in p.get("artifacts", [])
            ]

            practice = Practice(
                id=p["id"],
                name=p["name"],
                type=EnumType(p["type"]),
                roles=roles,
                activities=activities,
                artifacts=artifacts,
                rules=p.get("rules", []),
                required_rules=p.get("requiredRules", []),
                context_requirements=p.get("contextRequirements", [])
            )

            practices.append(practice)

        #Crear mapa de prácticas (para relaciones)
        practice_map = {p.id: p for p in practices}

        #Cargar relaciones de compatibilidad
        relations = []
        for r in data.get("compatibilityRelations", []):
            relations.append(
                CompatibilityRelation(
                    r["type"],
                    practice_map[r["practiceA"]],
                    practice_map[r["practiceB"]]
                )
            )

        #Construir modelo final
        return HybridProcessModel(
            id=data["id"],
            practices=practices,
            project_context=data.get("projectContext", []),
            compatibility_relations=relations
        )