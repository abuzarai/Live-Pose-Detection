from dataclasses import dataclass


@dataclass
class PostureResult:
    score: float
    feedback: list[str]

class PostureDetector:
    def __init__(self):
        self.history = []

    def update(self, metrics: dict) -> PostureResult:
        feedback = []
        score = 100.0

        fh = metrics.get("forward_head")
        if fh is not None:
            if fh > 30:
                score -= 25
                feedback.append("Forward head posture")
            elif fh > 20:
                score -= 10
                feedback.append("Slight forward head")

        slope = metrics.get("shoulder_slope", 0)
        if slope > 0.05:
            score -= 15
            feedback.append("Uneven shoulders")
        elif slope > 0.03:
            score -= 5

        sc = metrics.get("spine_curve", 0)
        if sc < 10:
            score -= 20
            feedback.append("Rounded upper back")
        elif sc < 15:
            score -= 10
            feedback.append("Mild spinal curve")

        nt = metrics.get("neck_tilt", 0)
        if nt > 25:
            score -= 15
            feedback.append("Excessive neck tilt")

        score = max(0, min(100, score))
        return PostureResult(score=score, feedback=feedback or ["Good posture"])
