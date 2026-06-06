import cv2
import numpy as np
import mediapipe as mp

class PoseDetector:
    def __init__(self, static_mode=False, model_complexity=1,
                 min_detection_confidence=0.5, min_tracking_confidence=0.5):
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(
            static_image_mode=static_mode,
            model_complexity=model_complexity,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence,
        )

    def detect(self, frame: np.ndarray):
        if frame is None:
            return None
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.pose.process(rgb)
        if results.pose_landmarks:
            return results.pose_landmarks
        return None

    def close(self):
        if hasattr(self, "pose"):
            self.pose.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()
