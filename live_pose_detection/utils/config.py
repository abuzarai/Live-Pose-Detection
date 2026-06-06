import json
import os

DEFAULT_CONFIG = {
    "camera_source": 0,
    "confidence_threshold": 0.5,
    "exercise_mode": "free",
    "show_skeleton": True,
    "show_keypoints": True,
}

class Config:
    def __init__(self, path: str = None):
        self.path = path or os.path.join(
            os.path.dirname(__file__), "..", "data", "config.json"
        )
        self.data = dict(DEFAULT_CONFIG)
        if os.path.exists(self.path):
            with open(self.path) as f:
                self.data.update(json.load(f))

    def get(self, key: str, default=None):
        return self.data.get(key, default)

    def set(self, key: str, value):
        self.data[key] = value

    def save(self):
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        with open(self.path, "w") as f:
            json.dump(self.data, f, indent=2)
