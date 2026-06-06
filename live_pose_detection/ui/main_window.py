import cv2
import numpy as np
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QComboBox, QLabel, QMessageBox, QFileDialog,
)
from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QImage, QPixmap

from live_pose_detection.core.detector import PoseDetector
from live_pose_detection.core.calculator import extract_landmark_array, get_joint_angles
from live_pose_detection.ui.overlay import PoseOverlay
from live_pose_detection.ui.panels import AnglePanel, StatsPanel
from live_pose_detection.features.exercise import SquatDetector, PushUpDetector
from live_pose_detection.features.recorder import SessionRecorder

EXERCISE_DETECTORS = {
    "Free": None,
    "Squat": SquatDetector,
    "Push-up": PushUpDetector,
}

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Live Pose Detection")
        self.setMinimumSize(1280, 720)
        self.detector = PoseDetector()
        self.overlay = PoseOverlay()
        self.recorder = SessionRecorder()
        self.capture = None
        self.timer = QTimer()
        self.timer.timeout.connect(self.process_frame)
        self.exercise_detector = None
        self._setup_ui()

    def _setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QHBoxLayout(central)

        left_layout = QVBoxLayout()
        self.cam_label = QLabel()
        self.cam_label.setMinimumSize(640, 480)
        self.cam_label.setStyleSheet("background-color: black;")
        left_layout.addWidget(self.cam_label)

        controls = QHBoxLayout()
        self.start_btn = QPushButton("Start Camera")
        self.start_btn.clicked.connect(self.toggle_camera)
        self.exercise_combo = QComboBox()
        self.exercise_combo.addItems(list(EXERCISE_DETECTORS.keys()))
        self.exercise_combo.currentTextChanged.connect(self._on_exercise_changed)
        self.record_btn = QPushButton("Record")
        self.record_btn.clicked.connect(self.toggle_recording)
        self.screenshot_btn = QPushButton("Screenshot")
        self.screenshot_btn.clicked.connect(self.take_screenshot)
        controls.addWidget(self.start_btn)
        controls.addWidget(self.exercise_combo)
        controls.addWidget(self.record_btn)
        controls.addWidget(self.screenshot_btn)
        left_layout.addLayout(controls)
        main_layout.addLayout(left_layout, stretch=2)

        right_layout = QVBoxLayout()
        self.angle_panel = AnglePanel()
        self.stats_panel = StatsPanel()
        right_layout.addWidget(self.angle_panel)
        right_layout.addWidget(self.stats_panel)
        right_layout.addStretch()
        main_layout.addLayout(right_layout, stretch=1)

    def _on_exercise_changed(self, mode: str):
        cls = EXERCISE_DETECTORS.get(mode)
        self.exercise_detector = cls() if cls else None
        self.stats_panel.update_stats(mode, 0, "--")

    def toggle_camera(self):
        if self.capture is not None:
            self.timer.stop()
            self.capture.release()
            self.capture = None
            self.start_btn.setText("Start Camera")
            self.cam_label.clear()
        else:
            self.capture = cv2.VideoCapture(0)
            if not self.capture.isOpened():
                QMessageBox.warning(self, "Error", "Cannot open camera")
                return
            self.timer.start(30)
            self.start_btn.setText("Stop Camera")

    def process_frame(self):
        ret, frame = self.capture.read()
        if not ret:
            return
        result = self.detector.detect(frame)
        angles = {}
        arr = None
        if result and result.pose_landmarks:
            landmarks_list = result.pose_landmarks[0]
            arr = extract_landmark_array(landmarks_list)
            frame = self.overlay.draw(frame, arr)
            angles = get_joint_angles(arr)
            self.angle_panel.update_angles(angles)
            if self.exercise_detector and "left_knee" in angles:
                ex_result = self.exercise_detector.update(
                    angles["left_knee"], left_knee=angles["left_knee"]
                )
                self.stats_panel.update_stats(
                    self.exercise_combo.currentText(), ex_result.reps, ex_result.feedback or "--"
                )
        if self.recorder.recording:
            self.recorder.write_frame(frame, arr, angles)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb.shape
        qimg = QImage(rgb.data, w, h, ch * w, QImage.Format_RGB888)
        self.cam_label.setPixmap(
            QPixmap.fromImage(qimg).scaled(
                self.cam_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
        )

    def toggle_recording(self):
        if not self.recorder.recording:
            frame = np.zeros((480, 640, 3), dtype=np.uint8)
            self.recorder.start(frame)
            self.record_btn.setText("Stop Recording")
        else:
            self.recorder.stop()
            self.record_btn.setText("Record")

    def take_screenshot(self):
        pixmap = self.cam_label.pixmap()
        if pixmap:
            path, _ = QFileDialog.getSaveFileName(
                self, "Save Screenshot", "", "PNG (*.png)"
            )
            if path:
                pixmap.save(path)

    def closeEvent(self, event):
        if self.capture:
            self.timer.stop()
            self.capture.release()
        if self.recorder.recording:
            self.recorder.stop()
        self.detector.close()
        event.accept()
