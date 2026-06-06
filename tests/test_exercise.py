import numpy as np
from live_pose_detection.features.exercise import SquatDetector, PushUpDetector

def test_squat_detector_counts_reps():
    detector = SquatDetector()
    assert detector.rep_count == 0
    angles = [170, 160, 140, 120, 90, 85, 90, 120, 140, 160, 170]
    for angle in angles:
        detector.update(angle, left_knee=angle)
    assert detector.rep_count == 1

def test_pushup_detector_counts_reps():
    detector = PushUpDetector()
    elbows = [170, 160, 140, 110, 90, 110, 140, 160, 170]
    for angle in elbows:
        detector.update(angle)
    assert detector.rep_count == 1

def test_squat_detector_no_rep_on_partial():
    detector = SquatDetector()
    angles = [170, 150, 120, 150, 170]
    for angle in angles:
        detector.update(angle)
    assert detector.rep_count == 0

def test_pushup_detector_multiple_reps():
    detector = PushUpDetector()
    pattern = [170, 160, 140, 110, 90, 110, 140, 160, 170] * 3
    for angle in pattern:
        detector.update(angle)
    assert detector.rep_count == 3
