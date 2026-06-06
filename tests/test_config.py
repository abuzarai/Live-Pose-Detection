import json
import tempfile
import os
from live_pose_detection.utils.config import Config

def test_config_load_and_save():
    data = {"camera_source": 1, "confidence_threshold": 0.7}
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump(data, f)
        path = f.name
    cfg = Config(path)
    assert cfg.get("camera_source") == 1
    cfg.set("camera_source", 2)
    cfg.save()
    with open(path) as f:
        loaded = json.load(f)
    assert loaded["camera_source"] == 2
    os.unlink(path)

def test_config_defaults():
    cfg = Config("nonexistent.json")
    assert cfg.get("missing", 42) == 42
