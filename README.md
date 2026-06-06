# Live Pose Detection

Real-time human pose estimation system for fitness and healthcare applications. Captures 33 full-body keypoints via webcam, computes joint angles, counts exercise reps, scores form quality, and exports session data.

## Features

- **Real-time pose tracking** — MediaPipe PoseLandmarker, 33-keypoint full-body, 30+ FPS on CPU
- **Exercise rep counting** — Squat and push-up detection with configurable angle thresholds
- **Form scoring** — Green/yellow/red feedback on joint angles relative to ideal ranges
- **Healthcare/rehab mode** — Range of Motion tracking, left-right symmetry analysis, CSV export
- **Session recording** — Annotated MP4 video + raw keypoint data (CSV/JSON) per session
- **Multi-person support** — Up to 3 people tracked with proximity-based ID assignment
- **Desktop UI** — PySide6 with live camera feed, skeleton overlay, and real-time stats panel

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Pose Engine | MediaPipe PoseLandmarker (BlazePose) |
| GUI | PySide6 |
| Computer Vision | OpenCV |
| Math | NumPy, SciPy |
| Analytics | Matplotlib, Pandas |
| Package Manager | uv |

## Installation

Requires Python 3.11+ and [uv](https://docs.astral.sh/uv/).

```bash
git clone git@github.com:abuzarai/Live-Pose-Detection.git
cd Live-Pose-Detection
uv sync
```

## Usage

```bash
uv run python live_pose_detection/main.py
```

Controls:
- **Start Camera** — Opens webcam feed
- **Exercise dropdown** — Select Free, Squat, or Push-up mode
- **Record** — Saves annotated video + CSV/JSON keypoint data to `data/sessions/`
- **Screenshot** — Captures current frame as PNG

## Project Structure

```
live_pose_detection/
├── main.py                    # Application entry point
├── core/
│   ├── detector.py            # MediaPipe pose inference wrapper
│   ├── calculator.py          # Joint angle calculations
│   └── tracker.py             # Multi-person ID + landmark smoothing
├── ui/
│   ├── main_window.py         # PySide6 main window (camera + controls + panels)
│   ├── overlay.py             # Keypoint/skeleton drawing on frames
│   └── panels.py              # Right panel: joint angles, exercise stats
├── features/
│   ├── exercise.py            # Squat/push-up detectors with rep counting
│   └── recorder.py            # Session recording (MP4 + CSV/JSON export)
├── utils/
│   └── config.py              # JSON settings loader/saver
└── data/
    ├── config.json            # Persistent settings
    ├── models/                # MediaPipe model files
    └── sessions/              # Recorded session output
```

## Testing

```bash
uv run pytest tests/ -v
```

15 tests covering angle calculations, exercise detection logic, and config persistence.

## License

MIT
