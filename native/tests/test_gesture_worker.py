import importlib.util
import sys
import threading
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
MODULE_PATH = ROOT / "native" / "gesture_worker.py"
MODEL_PATH = ROOT / "native" / "assets" / "gesture_recognizer.task"


def load_worker():
    assert MODULE_PATH.is_file(), "native gesture worker has not been implemented"
    sys.path.insert(0, str(ROOT / "native"))
    spec = importlib.util.spec_from_file_location("gesture_worker", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_unavailable_camera_reports_fallback_and_releases_capture(monkeypatch):
    module = load_worker()

    class ClosedCamera:
        released = False

        def isOpened(self):
            return False

        def set(self, *_):
            return True

        def release(self):
            self.released = True

    camera = ClosedCamera()
    monkeypatch.setattr(module.cv2, "VideoCapture", lambda *_: camera)
    worker = module.GestureWorker(MODEL_PATH)
    statuses = []
    worker.status_changed.connect(statuses.append)

    worker.run()

    assert camera.released is True
    assert any("camera unavailable" in status.lower() for status in statuses)
    assert any("mouse" in status.lower() for status in statuses)


def test_camera_read_failure_still_releases_camera(monkeypatch):
    module = load_worker()

    class FailingCamera:
        released = False
        settings = []

        def isOpened(self):
            return True

        def set(self, key, value):
            self.settings.append((key, value))
            return True

        def read(self):
            return False, None

        def release(self):
            self.released = True

    camera = FailingCamera()
    monkeypatch.setattr(module.cv2, "VideoCapture", lambda *_: camera)
    worker = module.GestureWorker(MODEL_PATH)
    statuses = []
    worker.status_changed.connect(statuses.append)

    worker.run()

    assert camera.released is True
    assert (module.cv2.CAP_PROP_FRAME_WIDTH, 640) in camera.settings
    assert (module.cv2.CAP_PROP_FRAME_HEIGHT, 480) in camera.settings
    assert any("frame" in status.lower() for status in statuses)


def test_stop_during_recognition_joins_worker_and_releases_camera(monkeypatch):
    module = load_worker()

    class RepeatingCamera:
        released = False

        def __init__(self):
            self.first_frame = threading.Event()

        def isOpened(self):
            return True

        def set(self, *_):
            return True

        def read(self):
            self.first_frame.set()
            return True, np.zeros((480, 640, 3), dtype=np.uint8)

        def release(self):
            self.released = True

    camera = RepeatingCamera()
    monkeypatch.setattr(module.cv2, "VideoCapture", lambda *_: camera)
    worker = module.GestureWorker(MODEL_PATH)

    worker.start()
    assert camera.first_frame.wait(5)
    worker.stop()

    assert not worker.isRunning()
    assert camera.released is True
