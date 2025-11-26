class Domain:
    def __init__(self, domain_id=None, name=None, description=None, tags=None):
        self.domain_id = domain_id
        self.name = name
        self.description = description
        self.tags = tags or []

    def to_dict(self):
        return {
            "domain_id": self.domain_id,
            "name": self.name,
            "description": self.description,
            "tags": self.tags
        }

    @staticmethod
    def from_dict(data):
        return Domain(
            domain_id=data.get("domain_id"),
            name=data.get("name"),
            description=data.get("description"),
            tags=data.get("tags", [])
        )
