from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QScrollArea
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

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
