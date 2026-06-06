from dataclasses import dataclass

@dataclass
class ExerciseResult:
    reps: int
    stage: str
    score: float
    feedback: str

class SquatDetector:
    def __init__(self, threshold_down=100, threshold_up=150):
        self.threshold_down = threshold_down
        self.threshold_up = threshold_up
        self.stage = "standing"
        self.rep_count = 0
        self.min_angle = 180

    def update(self, knee_angle: float, **kwargs) -> ExerciseResult:
        self.min_angle = min(self.min_angle, knee_angle)
        if knee_angle < self.threshold_down and self.stage == "standing":
            self.stage = "squatting"
        elif knee_angle > self.threshold_up and self.stage == "squatting":
            self.stage = "standing"
            self.rep_count += 1
            depth_score = max(0, min(100, 100 * (1 - self.min_angle / 180)))
            self.min_angle = 180
            feedback = "Good depth" if depth_score > 70 else "Go deeper"
            return ExerciseResult(self.rep_count, self.stage, depth_score, feedback)
        return ExerciseResult(self.rep_count, self.stage, 0, "")

class PushUpDetector:
    def __init__(self, threshold_down=100, threshold_up=150):
        self.threshold_down = threshold_down
        self.threshold_up = threshold_up
        self.stage = "up"
        self.rep_count = 0

    def update(self, elbow_angle: float, **kwargs) -> ExerciseResult:
        if elbow_angle < self.threshold_down and self.stage == "up":
            self.stage = "down"
        elif elbow_angle > self.threshold_up and self.stage == "down":
            self.stage = "up"
            self.rep_count += 1
            depth_score = max(0, min(100, 100 * (1 - elbow_angle / 180)))
            return ExerciseResult(self.rep_count, self.stage, depth_score, "Good form")
        return ExerciseResult(self.rep_count, self.stage, 0, "")
