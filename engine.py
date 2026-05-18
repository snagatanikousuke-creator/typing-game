import time

class GameEngine:
    def __init__(self, time_limit: int = 60):
        self.time_limit = time_limit
        self.score = 0
        self.correct_count = 0
        self.miss_count = 0
        self.results: list[dict] = []
        self.start_time: float = 0.0

    def start(self):
        self.start_time = time.time()

    def time_left(self) -> float:
        return max(0.0, self.time_limit - (time.time() - self.start_time))

    def is_time_over(self) -> bool:
        return self.time_left() <= 0

    def record_correct(self, word: str):
        self.score += 10
        self.correct_count += 1
        self.results.append({"word": word, "result": "correct"})

    def record_miss(self, word: str):
        self.score = max(0, self.score - 3)
        self.miss_count += 1
        self.results.append({"word": word, "result": "miss"})

    def get_summary(self) -> dict:
        total = self.correct_count + self.miss_count
        accuracy = self.correct_count / total * 100 if total > 0 else 0.0
        return {
            "score": self.score,
            "correct": self.correct_count,
            "miss": self.miss_count,
            "accuracy": accuracy,
        }
