import argparse
import sys
from PySide6.QtWidgets import QApplication
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
        "--exercise", choices=["Free", "Squat", "Push-up"], default="Free",
        help="Initial exercise mode (default: Free)",
    )
    parser.add_argument(
        "--confidence", type=float, default=0.5,
        help="Detection confidence threshold 0-1 (default: 0.5)",
    )
    args = parser.parse_args()

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
