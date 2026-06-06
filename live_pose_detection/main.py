import argparse
import sys

import cv2
from PySide6.QtWidgets import QApplication

from live_pose_detection.core.detector import PoseDetector
from live_pose_detection.ui.main_window import MainWindow


def main():
    parser = argparse.ArgumentParser(
        description="Real-time human pose detection for fitness and healthcare"
    )
    parser.add_argument(
        "--camera", type=int, default=0,
        help="Camera source index (default: 0)",
    )
    parser.add_argument(
        "--video", type=str, default=None,
        help="Path to video file (overrides --camera)",
    )
    parser.add_argument(
        "--exercise", choices=["Free", "Squat", "Push-up", "Posture"], default="Free",
        help="Initial exercise mode (default: Free)",
    )
    parser.add_argument(
        "--confidence", type=float, default=0.5,
        help="Detection confidence threshold 0-1 (default: 0.5)",
    )
    parser.add_argument(
        "--show-guide", action="store_true",
        help="Show reference pose overlay",
    )
    args = parser.parse_args()

    app = QApplication(sys.argv)
    window = MainWindow()
    if args.video:
        window.load_video(args.video)
    elif args.camera is not None:
        window.open_camera(args.camera)
    if args.exercise:
        idx = window.exercise_combo.findText(args.exercise)
        if idx >= 0:
            window.exercise_combo.setCurrentIndex(idx)
    if args.show_guide:
        window.overlay.show_guide = True
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
