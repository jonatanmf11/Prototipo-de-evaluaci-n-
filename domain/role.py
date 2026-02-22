class Role:
    def __init__(self, id: str, name: str):
        self.id = id
        self.name = name
        self._incompatible_roles = set()

    def add_incompatible_role(self, role: "Role"):
        """
        Declara que este rol es incompatible con otro rol
        """
        self._incompatible_roles.add(role.id)

    def is_incompatible_with(self, role: "Role") -> bool:
        return role.id in self._incompatible_roles

    def is_incompatible_with_any(self, roles: list) -> bool:
        """
        Retorna True si este rol es incompatible con alguno de los roles dados
        """
        return any(self.is_incompatible_with(r) for r in roles)

    def __repr__(self):
        return f"<Role {self.id} - {self.name}>"
