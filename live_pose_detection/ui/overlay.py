import cv2
import numpy as np

KEYPOINT_COLOR = (0, 255, 0)
SKELETON_COLOR = (255, 255, 255)
TEXT_COLOR = (255, 255, 255)
GREEN = (0, 255, 0)
YELLOW = (0, 255, 255)
RED = (0, 0, 255)

SKELETON_CONNECTIONS = [
    (11, 12), (12, 24), (24, 26), (26, 28),
    (11, 23), (23, 25), (25, 27),
    (12, 14), (14, 16), (11, 13), (13, 15),
    (23, 24),
]

def _form_color(score: float | None) -> tuple:
    if score is None:
        return SKELETON_COLOR
    if score >= 70:
        return GREEN
    if score >= 40:
        return YELLOW
    return RED

class PoseOverlay:
    def __init__(self, show_keypoints=True, show_skeleton=True):
        self.show_keypoints = show_keypoints
        self.show_skeleton = show_skeleton

    def draw(self, frame: np.ndarray, landmark_array: np.ndarray,
             angles: dict = None, person_id: int = None,
             fps: float = None, form_score: float = None) -> np.ndarray:
        h, w = frame.shape[:2]
        color = _form_color(form_score)
        if self.show_skeleton:
            for start, end in SKELETON_CONNECTIONS:
                if start >= len(landmark_array) or end >= len(landmark_array):
                    continue
                p1 = (int(landmark_array[start][0] * w), int(landmark_array[start][1] * h))
                p2 = (int(landmark_array[end][0] * w), int(landmark_array[end][1] * h))
                if landmark_array[start][3] > 0.5 and landmark_array[end][3] > 0.5:
                    cv2.line(frame, p1, p2, color, 2)
        if self.show_keypoints:
            for lm in landmark_array:
                if lm[3] > 0.5:
                    cx, cy = int(lm[0] * w), int(lm[1] * h)
                    cv2.circle(frame, (cx, cy), 4, color, -1)
        if person_id is not None:
            cv2.putText(frame, f"ID: {person_id}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, TEXT_COLOR, 2)
        if fps is not None:
            cv2.putText(frame, f"{fps:.0f} FPS", (w - 120, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, TEXT_COLOR, 2)
        return frame
