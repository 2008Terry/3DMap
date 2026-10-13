"""On-device, single-hand MediaPipe inference on a dedicated QThread."""

from __future__ import annotations

import sys
import threading
import time
from pathlib import Path

import cv2
from PySide6.QtCore import Property, QThread, Signal, Slot


GESTURE_LABELS = {
    "Open_Palm": "张开手掌",
    "Thumb_Up": "拇指向上",
    "Thumb_Down": "拇指向下",
    "Victory": "胜利手势",
    "Pointing_Up": "食指指向",
    "Closed_Fist": "握拳",
}


class GestureWorker(QThread):
    gesture_changed = Signal(str, str, float, object)
    status_changed = Signal(str)
    runningChanged = Signal()

    def __init__(self, model_path: Path, parent=None):
        super().__init__(parent)
        self._model_path = Path(model_path)
        self._stop_event = threading.Event()

    @Property(bool, notify=runningChanged)
    def running(self) -> bool:
        return self.isRunning()

    @Slot()
    def start(self, priority=QThread.Priority.InheritPriority):
        if self.isRunning():
            return
        self._stop_event.clear()
        super().start(priority)
        self.runningChanged.emit()

    @Slot()
    def stop(self):
        if self.isRunning():
            self._stop_event.set()
            self.requestInterruption()
            self.wait(5000)
        self.status_changed.emit("Gesture camera stopped")
        self.runningChanged.emit()

    def run(self):
        recognizer = None
        capture = None
        try:
            self.status_changed.emit("Loading local gesture model")
            if not self._model_path.is_file():
                raise FileNotFoundError(f"Local gesture model not found: {self._model_path}")

            # TensorFlow is optional for MediaPipe Tasks; it is only imported for API docs.
            previous_tensorflow = sys.modules.get("tensorflow", ...)
            sys.modules["tensorflow"] = None
            try:
                import mediapipe as mp
            finally:
                if previous_tensorflow is ...:
                    sys.modules.pop("tensorflow", None)
                else:
                    sys.modules["tensorflow"] = previous_tensorflow

            options = mp.tasks.vision.GestureRecognizerOptions(
                base_options=mp.tasks.BaseOptions(model_asset_path=str(self._model_path)),
                running_mode=mp.tasks.vision.RunningMode.VIDEO,
                num_hands=1,
                min_hand_detection_confidence=0.5,
                min_hand_presence_confidence=0.5,
                min_tracking_confidence=0.5,
            )
            recognizer = mp.tasks.vision.GestureRecognizer.create_from_options(options)

            capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)
            capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            if not capture.isOpened():
                self.status_changed.emit("Camera unavailable; mouse controls remain available")
                return
            self.status_changed.emit("Camera active · local CPU recognition")

            last_inference = 0.0
            last_timestamp_ms = 0
            frame_interval = 1.0 / 15.0
            while not self._stop_event.is_set() and not self.isInterruptionRequested():
                now = time.monotonic()
                remaining = frame_interval - (now - last_inference)
                if remaining > 0:
                    self._stop_event.wait(remaining)
                    continue

                ok, frame = capture.read()
                if not ok:
                    self.status_changed.emit("Camera frame unavailable; mouse controls remain available")
                    break
                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
                timestamp_ms = max(last_timestamp_ms + 1, int(time.monotonic() * 1000))
                result = recognizer.recognize_for_video(image, timestamp_ms)
                last_timestamp_ms = timestamp_ms
                last_inference = time.monotonic()

                if result.gestures and result.gestures[0]:
                    category = result.gestures[0][0]
                    landmarks = [(float(point.x), float(point.y)) for point in result.hand_landmarks[0]]
                    key = category.category_name
                    self.gesture_changed.emit(key, GESTURE_LABELS.get(key, key), float(category.score), landmarks)
                else:
                    self.gesture_changed.emit("", "No hand detected", 0.0, [])
        except Exception as error:
            self.status_changed.emit(f"Gesture recognition unavailable: {error}; mouse controls remain available")
        finally:
            if capture is not None:
                capture.release()
            if recognizer is not None:
                recognizer.close()
            self.runningChanged.emit()
