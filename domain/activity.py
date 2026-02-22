from domain.enumType import EnumType


class Activity:

    def __init__(
        self,
        id: str,
        name: str,
        type: str,
        must_precede=None
    ):
        self.id = id
        self.name = name
        self.type = type
        self.mustPrecede = must_precede or [] # referencia a otra actividad dentro de un proceso software

    def is_agile(self) -> bool:
        return self.type == EnumType.AGILE

    def is_traditional(self) -> bool:
        return self.type == EnumType.TRADITIONAL

    def __repr__(self):
        return f"<Activity {self.id} ({self.name}) - {self.type.value}>"
