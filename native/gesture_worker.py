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
    "ILoveYou": "手势未绑定",
}


class GestureWorker(QThread):
    gesture_changed = Signal(str, str, float, object)
    status_changed = Signal(str)
    runningChanged = Signal()
    metricsChanged = Signal()
    cameraIndexChanged = Signal()

    def __init__(self, model_path: Path, parent=None):
        super().__init__(parent)
        self._model_path = Path(model_path)
        self._stop_event = threading.Event()
        self._lock = threading.Lock()
        self._latest = None
        self._camera_index = 0
        self._last_delivery = 0.0
        self._result_count = 0
        self._inference_ms = 0.0
        self._metrics = {}
        self._metric_at = time.monotonic()
        self._metric_count = 0
        self.finished.connect(self.runningChanged)

    @Property(int, notify=cameraIndexChanged)
    def camera_index(self):
        return self._camera_index

    @Slot(int)
    def set_camera_index(self, index):
        if not self.isRunning() and 0 <= index <= 5:
            self._camera_index = index
            self.cameraIndexChanged.emit()

    @Property("QVariantMap", notify=metricsChanged)
    def metrics(self):
        return self._metrics

    @Slot()
    def poll_latest(self):
        """GUI pulls a single latest observation, never a backlog of gestures."""
        now = time.monotonic()
        with self._lock:
            latest, self._latest = self._latest, None
            count, latency = self._result_count, self._inference_ms
        if not self.isRunning() or self._stop_event.is_set():
            latest = None
            self._last_delivery = 0.0
        if latest is not None and now - latest[0] < 0.25:
            self._last_delivery = now
            self.gesture_changed.emit(*latest[1:])
        elif self._last_delivery and now - self._last_delivery > 0.25:
            self._last_delivery = 0.0
            self.gesture_changed.emit("", "没有新手部观测", 0.0, [])
        if now - self._metric_at >= 0.5:
            self._metrics = {"fps": round((count - self._metric_count) / (now - self._metric_at), 1),
                             "latencyMs": round(latency, 1)}
            self._metric_count, self._metric_at = count, now
            self.metricsChanged.emit()

    @Property(bool, notify=runningChanged)
    def running(self) -> bool:
        return self.isRunning()

    @Slot()
    def start(self, priority=QThread.Priority.InheritPriority):
        if self.isRunning():
            return
        self._stop_event.clear()
        with self._lock:
            self._latest = None
            self._result_count = 0
            self._inference_ms = 0.0
        self._metric_count = 0
        self._metric_at = time.monotonic()
        super().start(priority)
        self.runningChanged.emit()

    @Slot()
    def stop(self):
        if self.isRunning():
            self._stop_event.set()
            self.requestInterruption()
            self.wait(5000)
        self.status_changed.emit("Gesture camera stopped")
        self._last_delivery = 0.0
        with self._lock:
            self._latest = None
        self.gesture_changed.emit("", "已停止", 0.0, [])
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

            def receive_result(result, _image, timestamp_ms):
                if self._stop_event.is_set():
                    return
                key, label, confidence, landmarks = "", "未识别姿态", 0.0, []
                if result.hand_landmarks:
                    landmarks = [(float(p.x), float(p.y), float(p.z)) for p in result.hand_landmarks[0]]
                    if result.gestures and result.gestures[0]:
                        category = result.gestures[0][0]
                        key, confidence = category.category_name, float(category.score)
                        label = GESTURE_LABELS.get(key, key)
                captured_at = timestamp_ms / 1000.0
                latency = (time.monotonic() - captured_at) * 1000
                with self._lock:
                    self._latest = (captured_at, key, label, confidence, landmarks)
                    self._result_count += 1
                    self._inference_ms += 0.2 * (latency - self._inference_ms)

            options = mp.tasks.vision.GestureRecognizerOptions(
                base_options=mp.tasks.BaseOptions(model_asset_path=str(self._model_path)),
                running_mode=mp.tasks.vision.RunningMode.LIVE_STREAM,
                result_callback=receive_result,
                num_hands=1,
                min_hand_detection_confidence=0.55,
                min_hand_presence_confidence=0.65,
                min_tracking_confidence=0.55,
            )
            recognizer = mp.tasks.vision.GestureRecognizer.create_from_options(options)

            capture = cv2.VideoCapture(self._camera_index, cv2.CAP_DSHOW)
            if not capture.isOpened():
                capture.release()
                capture = cv2.VideoCapture(self._camera_index, cv2.CAP_MSMF)
            capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            capture.set(cv2.CAP_PROP_FPS, 30)
            capture.set(cv2.CAP_PROP_BUFFERSIZE, 1)
            if not capture.isOpened():
                self.status_changed.emit("Camera unavailable; mouse controls remain available")
                return
            self.status_changed.emit("摄像头已开启 · 本地识别 · 等待手势")

            last_capture = 0.0
            last_timestamp_ms = 0
            frame_interval = 1.0 / 30.0
            while not self._stop_event.is_set() and not self.isInterruptionRequested():
                now = time.monotonic()
                remaining = frame_interval - (now - last_capture)
                if remaining > 0:
                    self._stop_event.wait(remaining)
                    continue

                last_capture = time.monotonic()
                ok, frame = capture.read()
                if not ok:
                    self.status_changed.emit("Camera frame unavailable; mouse controls remain available")
                    break
                # Use the actual frame dimensions assumed by the geometry rules.
                if frame.shape[:2] != (480, 640):
                    frame = cv2.resize(frame, (640, 480))
                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
                timestamp_ms = max(last_timestamp_ms + 1, int(time.monotonic() * 1000))
                recognizer.recognize_async(image, timestamp_ms)
                last_timestamp_ms = timestamp_ms
        except Exception as error:
            self.status_changed.emit(f"Gesture recognition unavailable: {error}; mouse controls remain available")
        finally:
            self._stop_event.set()
            if capture is not None:
                capture.release()
            if recognizer is not None:
                recognizer.close()
            with self._lock:
                self._latest = None
            self.runningChanged.emit()
