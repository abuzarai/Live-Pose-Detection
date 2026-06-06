.PHONY: run help test install clean

run:
	uv run python live_pose_detection/main.py

help:
	uv run python live_pose_detection/main.py --help

test:
	uv run pytest tests/ -v

install:
	uv sync
