class Practice:
    def __init__(
        self,
        id: str,
        name: str,
        type,
        roles=None,
        activities=None,
        artifacts=None,
        rules=None,
        required_rules=None,
        context_requirements=None
    ):
        self.id = id
        self.name = name
        self.type = type
        self.roles = roles or []
        self.activities = activities or []
        self.artifacts = artifacts or []
        self.rules = rules or []
        self.required_rules = required_rules or []
        self.context_requirements = context_requirements or []
