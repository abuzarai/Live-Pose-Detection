import numpy as np

LANDMARK_NAMES = {
    0: "nose", 11: "left_shoulder", 12: "right_shoulder",
    13: "left_elbow", 14: "right_elbow", 15: "left_wrist",
    16: "right_wrist", 23: "left_hip", 24: "right_hip",
    25: "left_knee", 26: "right_knee", 27: "left_ankle",
    28: "right_ankle",
}

def calculate_angle(a: tuple, b: tuple, c: tuple) -> float:
    a, b, c = np.array(a), np.array(b), np.array(c)
    ba = a - b
    bc = c - b
    norm_ba = np.linalg.norm(ba)
    norm_bc = np.linalg.norm(bc)
    if norm_ba < 1e-8 or norm_bc < 1e-8:
        return 0.0
    cosine = np.dot(ba, bc) / (norm_ba * norm_bc)
    return float(np.degrees(np.arccos(np.clip(cosine, -1.0, 1.0))))

def extract_landmark_array(landmarks: list) -> np.ndarray:
    if not landmarks:
        return np.empty((0, 4), dtype=np.float32)
    rows = []
    for lm in landmarks:
        rows.append([lm.x, lm.y, lm.z, lm.visibility])
    return np.array(rows, dtype=np.float32)

def get_joint_angles(landmark_array: np.ndarray) -> dict:
    angles = {}
    pairs = {
        "left_elbow": (11, 13, 15),
        "right_elbow": (12, 14, 16),
        "left_knee": (23, 25, 27),
        "right_knee": (24, 26, 28),
        "left_hip": (11, 23, 25),
        "right_hip": (12, 24, 26),
        "left_shoulder": (13, 11, 23),
        "right_shoulder": (14, 12, 24),
    }
    for name, (a, b, c) in pairs.items():
        p1 = landmark_array[a][:3]
        p2 = landmark_array[b][:3]
        p3 = landmark_array[c][:3]
        angles[name] = calculate_angle(p1, p2, p3)
    return angles
