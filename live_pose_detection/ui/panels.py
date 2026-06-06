from collections import deque

import numpy as np
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QLabel, QScrollArea, QVBoxLayout, QWidget


class ChartPanel(QWidget):
    def __init__(self, max_frames=300, parent=None):
        super().__init__(parent)
        self.max_frames = max_frames
        self.history = deque(maxlen=max_frames)
        layout = QVBoxLayout(self)
        title = QLabel("Angle Timeline")
        title.setFont(QFont("Arial", 14, QFont.Bold))
        layout.addWidget(title)
        self.fig = Figure(figsize=(3, 2.5), dpi=80)
        self.fig.subplots_adjust(bottom=0.2, left=0.2, right=0.95, top=0.9)
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasQTAgg(self.fig)
        layout.addWidget(self.canvas)

    def update_chart(self, angles: dict):
        self.history.append(angles)
        self.ax.clear()
        data = list(self.history)
        tracked = ["left_knee", "right_knee", "left_elbow", "right_elbow"]
        for key in tracked:
            vals = [f.get(key, 0) for f in data]
            if any(v != 0 for v in vals):
                self.ax.plot(vals, label=key.replace("_", " ").title(), linewidth=1)
        if data:
            self.ax.set_ylim(0, 180)
        self.ax.set_xlabel("Frame")
        self.ax.set_ylabel("Angle (°)")
        self.ax.legend(fontsize=7, loc="upper left")
        self.fig.tight_layout()
        self.canvas.draw_idle()


class AnglePanel(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.setLayout(layout)
        title = QLabel("Joint Angles")
        title.setFont(QFont("Arial", 14, QFont.Bold))
        layout.addWidget(title)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        self.info_widget = QWidget()
        self.info_layout = QVBoxLayout(self.info_widget)
        scroll.setWidget(self.info_widget)
        layout.addWidget(scroll)
        self.labels = {}

    def update_angles(self, angles: dict):
        for name, value in angles.items():
            if name not in self.labels:
                lbl = QLabel()
                self.info_layout.addWidget(lbl)
                self.labels[name] = lbl
            display = name.replace("_", " ").title()
            self.labels[name].setText(f"{display}: {value:.1f}°")


class StatsPanel(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.setLayout(layout)
        title = QLabel("Exercise Stats")
        title.setFont(QFont("Arial", 14, QFont.Bold))
        layout.addWidget(title)
        self.exercise_label = QLabel("Mode: Free")
        self.rep_label = QLabel("Reps: 0")
        self.score_label = QLabel("Form: --")
        layout.addWidget(self.exercise_label)
        layout.addWidget(self.rep_label)
        layout.addWidget(self.score_label)

    def update_stats(self, exercise: str, reps: int, score: str):
        self.exercise_label.setText(f"Mode: {exercise}")
        self.rep_label.setText(f"Reps: {reps}")
        self.score_label.setText(f"Form: {score}")


class PostureFeedbackPanel(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.setLayout(layout)
        title = QLabel("Posture Analysis")
        title.setFont(QFont("Arial", 14, QFont.Bold))
        layout.addWidget(title)
        self.metric_labels = {}
        self.feedback_label = QLabel("")
        self.feedback_label.setWordWrap(True)
        layout.addWidget(self.feedback_label)

    def update_metrics(self, metrics: dict, feedback: list[str]):
        for name, value in metrics.items():
            if name not in self.metric_labels:
                lbl = QLabel()
                self.layout().addWidget(lbl)
                self.metric_labels[name] = lbl
            display = name.replace("_", " ").title()
            self.metric_labels[name].setText(f"{display}: {value:.1f}")
        self.feedback_label.setText("\n".join(f"• {f}" for f in feedback))
