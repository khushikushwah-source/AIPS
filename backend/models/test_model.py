class Test:
    def __init__(self, test_id=None, company_id=None, domain_id=None,
                 test_type=None, duration=None, question_ids=None, metadata=None):
        self.test_id = test_id
        self.company_id = company_id
        self.domain_id = domain_id
        self.test_type = test_type
        self.duration = duration
        self.question_ids = question_ids or []
        self.metadata = metadata or {}

    def to_dict(self):
        return {
            "test_id": self.test_id,
            "company_id": self.company_id,
            "domain_id": self.domain_id,
            "test_type": self.test_type,
            "duration": self.duration,
            "question_ids": self.question_ids,
            "metadata": self.metadata
        }

    @staticmethod
    def from_dict(data):
        return Test(
            test_id=data.get("test_id"),
            company_id=data.get("company_id"),
            domain_id=data.get("domain_id"),
            test_type=data.get("test_type"),
            duration=data.get("duration"),
            question_ids=data.get("question_ids", []),
            metadata=data.get("metadata", {})
        )
