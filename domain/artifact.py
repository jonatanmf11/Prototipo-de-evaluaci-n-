class Artifact:

    def __init__(self, id: str, name: str, category: str):
        self.id = id
        self.name = name
        self.category = category

    def __repr__(self):
        return f"<Artifact {self.id} - {self.name} ({self.category})>"
