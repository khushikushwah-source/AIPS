class Company:
    def __init__(self, company_id=None, name=None, domain_ids=None, hiring_flow=None, logo_url=None):
        self.company_id = company_id
        self.name = name
        self.domain_ids = domain_ids or []
        self.hiring_flow = hiring_flow or []   # List of stages
        self.logo_url = logo_url

    def to_dict(self):
        return {
            "company_id": self.company_id,
            "name": self.name,
            "domain_ids": self.domain_ids,
            "hiring_flow": self.hiring_flow,
            "logo_url": self.logo_url
        }

    @staticmethod
    def from_dict(data):
        return Company(
            company_id=data.get("company_id"),
            name=data.get("name"),
            domain_ids=data.get("domain_ids", []),
            hiring_flow=data.get("hiring_flow", []),
            logo_url=data.get("logo_url")
        )
