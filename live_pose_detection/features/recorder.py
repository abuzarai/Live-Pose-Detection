import cv2
import csv
import json
import os
from datetime import datetime
import numpy as np

class SessionRecorder:
    def __init__(self, output_dir: str = None):
        self.output_dir = output_dir or os.path.join(
            os.path.dirname(__file__), "..", "data", "sessions"
        )
        self.video_writer = None
        self.keypoints_log = []
        self.session_id = None
        self.recording = False

    def start(self, frame: np.ndarray):
        os.makedirs(self.output_dir, exist_ok=True)
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        h, w = frame.shape[:2]
        video_path = os.path.join(self.output_dir, f"{self.session_id}.mp4")
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        self.video_writer = cv2.VideoWriter(video_path, fourcc, 30.0, (w, h))
        self.keypoints_log = []
        self.recording = True

    def write_frame(self, frame: np.ndarray, landmarks: np.ndarray = None, angles: dict = None):
        if not self.recording:
            return
        self.video_writer.write(frame)
        if landmarks is not None:
            self.keypoints_log.append({
                "frame": len(self.keypoints_log),
                "landmarks": landmarks.tolist(),
                "angles": angles,
            })

    def stop(self):
        if not self.recording:
            return
        self.recording = False
        if self.video_writer:
            self.video_writer.release()
            self.video_writer = None
        if self.keypoints_log:
            csv_path = os.path.join(self.output_dir, f"{self.session_id}.csv")
            json_path = os.path.join(self.output_dir, f"{self.session_id}.json")
            with open(json_path, "w") as f:
                json.dump(self.keypoints_log, f, indent=2)
            if self.keypoints_log:
                with open(csv_path, "w", newline="") as f:
                    writer = csv.writer(f)
                    first = self.keypoints_log[0]
                    if first["angles"]:
                        writer.writerow(["frame"] + list(first["angles"].keys()))
                        for entry in self.keypoints_log:
                            row = [entry["frame"]] + list(entry["angles"].values())
                            writer.writerow(row)
