import pytest
import numpy as np
from live_pose_detection.core.calculator import (
    calculate_angle,
    extract_landmark_array,
    get_joint_angles,
    LANDMARK_NAMES,
)

def test_calculate_angle_right_angle():
    a = (0, 1, 0)
    b = (0, 0, 0)
    c = (1, 0, 0)
    angle = calculate_angle(a, b, c)
    assert angle == pytest.approx(90.0, abs=0.1)

def test_calculate_angle_straight():
    a = (0, 1, 0)
    b = (0, 0, 0)
    c = (0, -1, 0)
    angle = calculate_angle(a, b, c)
    assert angle == pytest.approx(180.0, abs=0.1)

def test_extract_landmark_array():
    landmarks = [
        type("LM", (), {"x": 0.1, "y": 0.2, "z": 0.3, "visibility": 0.9})(),
        type("LM", (), {"x": 0.4, "y": 0.5, "z": 0.6, "visibility": 0.8})(),
    ]
    result = extract_landmark_array(landmarks)
    assert result.shape == (2, 4)
    np.testing.assert_array_almost_equal(result[0], [0.1, 0.2, 0.3, 0.9])

def test_extract_landmark_array_empty():
    result = extract_landmark_array([])
    assert result.shape == (0, 4)

def test_calculate_angle_acute():
    a = (1, 1, 0)
    b = (0, 0, 0)
    c = (1, 0, 0)
    angle = calculate_angle(a, b, c)
    assert angle == pytest.approx(45.0, abs=0.1)

def test_calculate_angle_zero_vector():
    a = (0, 0, 0)
    b = (0, 0, 0)
    c = (1, 0, 0)
    angle = calculate_angle(a, b, c)
    assert angle == pytest.approx(0.0, abs=0.1)

def test_get_joint_angles():
    rng = np.random.default_rng(42)
    landmark_array = rng.random((33, 4)).astype(np.float32)
    angles = get_joint_angles(landmark_array)
    expected_keys = {
        "left_elbow", "right_elbow", "left_knee", "right_knee",
        "left_hip", "right_hip", "left_shoulder", "right_shoulder",
    }
    assert set(angles.keys()) == expected_keys
    for name, angle in angles.items():
        assert 0.0 <= angle <= 180.0, f"{name} angle {angle} out of range"

def test_get_joint_angles_known_pose():
    arr = np.zeros((33, 4), dtype=np.float32)
    arr[11] = [0, 1, 0, 1]
    arr[13] = [0, 0, 0, 1]
    arr[15] = [1, 0, 0, 1]
    angles = get_joint_angles(arr)
    assert angles["left_elbow"] == pytest.approx(90.0, abs=0.1)

def test_landmark_names_constant():
    assert LANDMARK_NAMES[0] == "nose"
    assert LANDMARK_NAMES[11] == "left_shoulder"
    assert LANDMARK_NAMES[28] == "right_ankle"
