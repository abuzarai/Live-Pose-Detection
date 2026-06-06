# Live Pose Detection

Real-time human pose estimation system for fitness and healthcare. Captures 33 full-body keypoints via webcam, computes joint angles, counts exercise reps, scores form quality, analyzes posture, and exports session data — all through a desktop UI.

## Features

- **Real-time pose tracking** — MediaPipe PoseLandmarker, 33-keypoint full-body, 30+ FPS on CPU
- **Exercise rep counting** — Squat and push-up detection with configurable angle thresholds
- **Form scoring** — Green/yellow/red skeleton overlay based on joint angle quality
- **Posture analysis** — Detects forward head, uneven shoulders, rounded upper back, neck tilt
- **Live angle timeline** — Real-time matplotlib chart of joint angles over the last 300 frames
- **Form guide overlay** — Semi-transparent reference skeleton for pose comparison
- **Video file input** — Load pre-recorded `.mp4` / `.avi` / `.mov` files in addition to live camera
- **Session recording** — Annotated MP4 video + raw keypoint data (CSV/JSON) per session
- **Multi-person support** — Up to 3 people tracked with proximity-based ID assignment
- **Desktop UI** — PySide6 with live camera feed, skeleton overlay, and tabbed stats panel

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Pose Engine | MediaPipe PoseLandmarker (BlazePose) |
| GUI | PySide6 |
| Computer Vision | OpenCV |
| Math | NumPy, SciPy |
| Analytics | Matplotlib, Pandas |
| Package Manager | uv |
| Testing | pytest |

## Quick Start

Requires Python 3.11+ and [uv](https://docs.astral.sh/uv/).

```bash
git clone git@github.com:abuzarai/Live-Pose-Detection.git
cd Live-Pose-Detection
make install
make run
```

### CLI Options

```
make help

--camera 2        Use external camera
--video demo.mp4  Analyze a recorded video
--exercise Posture Healthcare posture analysis mode
--show-guide      Display reference skeleton overlay
```

### Controls

| Button | Action |
|--------|--------|
| **Start Camera** | Opens webcam feed |
| **Open Video** | Load a video file for analysis |
| **Exercise dropdown** | Switch between Free / Squat / Push-up / Posture modes |
| **Record** | Save annotated MP4 + CSV/JSON to `data/sessions/` |
| **Screenshot** | Capture current frame as PNG |

## Project Structure

```
live_pose_detection/
├── main.py                    # CLI entry point
├── core/
│   ├── detector.py            # MediaPipe PoseLandmarker wrapper
│   ├── calculator.py          # Joint angle + posture calculations
│   └── tracker.py             # Multi-person ID + landmark smoothing
├── ui/
│   ├── main_window.py         # PySide6 window (camera, controls, tabbed panels)
│   ├── overlay.py             # Keypoint/skeleton drawing with form colors
│   └── panels.py              # Angle list, stats, posture feedback, timeline chart
├── features/
│   ├── exercise.py            # Squat/push-up detectors with rep counting
│   ├── posture.py             # Forward head, shoulder slope, spine curve analysis
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
make test
```

15 tests covering angle calculations, exercise detection logic, and config persistence.

## License

MIT
