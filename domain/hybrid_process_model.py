class HybridProcessModel:

    def __init__(
        self,
        id: str,
        practices=None,
        project_context=None,
        compatibility_relations=None
    ):
        self.id = id
        self.practices = practices or []
        self.project_context = project_context or []
        self.compatibility_relations = compatibility_relations or []

    def __repr__(self):
        return (
            f"<HybridProcessModel {self.id} "
            f"practices={len(self.practices)} "
            f"relations={len(self.compatibility_relations)}>"
        )
