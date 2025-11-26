class Attempt:
    def __init__(self, attempt_id=None, user_id=None, test_id=None,
                 started_at=None, finished_at=None, score=None,
                 answers=None, media_urls=None):
        self.attempt_id = attempt_id
        self.user_id = user_id
        self.test_id = test_id
        self.started_at = started_at
        self.finished_at = finished_at
        self.score = score
        self.answers = answers or []   # List of: {q_id, response, score}
        self.media_urls = media_urls or []  # Uploaded media (audio/video)

    def to_dict(self):
        return {
            "attempt_id": self.attempt_id,
            "user_id": self.user_id,
            "test_id": self.test_id,
            "started_at": self.started_at,
            "finished_at": self.finished_at,
            "score": self.score,
            "answers": self.answers,
            "media_urls": self.media_urls
        }

    @staticmethod
    def from_dict(data):
        return Attempt(
            attempt_id=data.get("attempt_id"),
            user_id=data.get("user_id"),
            test_id=data.get("test_id"),
            started_at=data.get("started_at"),
            finished_at=data.get("finished_at"),
            score=data.get("score"),
            answers=data.get("answers", []),
            media_urls=data.get("media_urls", [])
        )
