import numpy as np
from collections import deque

class PoseTracker:
    def __init__(self, smoothing_window=5, distance_threshold=0.3):
        self.history = {}
        self.next_id = 0
        self.smoothing_window = smoothing_window
        self.distance_threshold = distance_threshold

    def assign_ids(self, detections: list) -> list[tuple[int, np.ndarray]]:
        assigned = []
        for landmarks in detections:
            arr = np.array([[lm.x, lm.y] for lm in landmarks.landmark])
            centroid = np.mean(arr, axis=0)
            best_id = None
            best_dist = self.distance_threshold
            for pid, history in self.history.items():
                last = np.mean(history[-1][:, :2], axis=0)
                dist = np.linalg.norm(centroid - last)
                if dist < best_dist:
                    best_dist = dist
                    best_id = pid
            if best_id is None:
                best_id = self.next_id
                self.next_id += 1
            self.history.setdefault(best_id, deque(maxlen=self.smoothing_window))
            landmarks_array = np.array([[lm.x, lm.y, lm.z, lm.visibility] for lm in landmarks.landmark])
            self.history[best_id].append(landmarks_array)
            assigned.append((best_id, landmarks_array))
        return assigned

    def get_smoothed(self, person_id: int) -> np.ndarray | None:
        if person_id not in self.history:
            return None
        return np.mean(self.history[person_id], axis=0)
