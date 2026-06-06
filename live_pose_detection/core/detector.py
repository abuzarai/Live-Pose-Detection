import os
import cv2
import numpy as np
from mediapipe import Image, ImageFormat
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

_MODEL_PATH = os.path.join(
    os.path.dirname(__file__), "..", "data", "models", "pose_landmarker_lite.task"
)

class PoseDetector:
    def __init__(self, min_detection_confidence=0.5, min_tracking_confidence=0.5, num_poses=1):
        options = vision.PoseLandmarkerOptions(
            base_options=python.BaseOptions(model_asset_path=str(_MODEL_PATH)),
            running_mode=vision.RunningMode.IMAGE,
            num_poses=num_poses,
            min_pose_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence,
        )
        self.detector = vision.PoseLandmarker.create_from_options(options)

    def detect(self, frame: np.ndarray):
        if frame is None:
            return None
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = Image(image_format=ImageFormat.SRGB, data=rgb)
        result = self.detector.detect(mp_image)
        if result.pose_landmarks:
            return result
        return None

    def close(self):
        if hasattr(self, "detector"):
            self.detector.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()
