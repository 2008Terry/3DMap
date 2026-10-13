"""Small, local landmark interpreter with temporal gates and adaptive smoothing."""

from __future__ import annotations

from dataclasses import dataclass
from math import acos, degrees, dist, exp, isfinite, pi


LABELS = {
    "Pointing_Up": "食指指向", "Open_Palm": "张开手掌", "Pinch": "捏合",
    "Victory": "双指旋转", "Thumb_Up": "拇指向上", "Thumb_Down": "拇指向下",
    "Closed_Fist": "握拳", "Three_Fingers": "三指", "Thumb_Left": "拇指向左",
    "Thumb_Right": "拇指向右", "ILoveYou": "控制开关",
}
HOLD_SECONDS = {"Closed_Fist": 0.55, "Three_Fingers": 0.65, "Thumb_Left": 0.6,
                "Thumb_Right": 0.6, "ILoveYou": 0.85}


class OneEuro:
    """Casiez et al.: low cutoff at rest, higher cutoff during fast movement."""

    def __init__(self, min_cutoff=1.5, beta=4.0):
        self.min_cutoff, self.beta = min_cutoff, beta
        self.value = self.raw = self.timestamp = None
        self.derivative = 0.0

    def update(self, value, timestamp):
        if self.timestamp is None or timestamp - self.timestamp > 0.25:
            self.value = self.raw = value
            self.derivative = 0.0
        else:
            dt = max(0.001, timestamp - self.timestamp)
            alpha_d = 1.0 - exp(-2 * pi * dt)
            self.derivative += alpha_d * ((value - self.raw) / dt - self.derivative)
            cutoff = self.min_cutoff + self.beta * abs(self.derivative)
            alpha = 1.0 - exp(-2 * pi * cutoff * dt)
            self.value += alpha * (value - self.value)
            self.raw = value
        self.timestamp = timestamp
        return self.value


@dataclass
class HandFrame:
    key: str
    held: float
    ready: bool
    position: tuple[float, float]
    cursor: tuple[float, float]
    geometric: bool
    spread: float

    @property
    def progress(self):
        return min(1.0, self.held / HOLD_SECONDS.get(self.key, 0.12))


class HandInterpreter:
    def __init__(self):
        self.reset()

    def reset(self):
        self._candidate = ""
        self._since = self._last_at = 0.0
        self._pinching = False
        self._filters = [OneEuro() for _ in range(4)]
        self._spread_filter = OneEuro(min_cutoff=2.0, beta=1.0)
        self._last_position = None
        self._world_geometry = None

    @staticmethod
    def _joint_angle(points, mcp, pip, tip):
        a = tuple(points[mcp][i] - points[pip][i] for i in range(3))
        b = tuple(points[tip][i] - points[pip][i] for i in range(3))
        denominator = dist(a, (0, 0, 0)) * dist(b, (0, 0, 0))
        if denominator < 1e-8:
            return 0.0
        return degrees(acos(max(-1.0, min(1.0, sum(x*y for x, y in zip(a, b)) / denominator))))

    @classmethod
    def _extended(cls, points, mcp, pip, tip):
        return cls._joint_angle(points, mcp, pip, tip) > 155 and dist(points[tip], points[0]) > dist(points[pip], points[0]) * 1.08

    def update(self, key, confidence, landmarks, now, world_landmarks=None, image_aspect=0.75):
        if len(landmarks) != 21 or any(len(p) < 2 or not all(isfinite(float(v)) for v in p) for p in landmarks):
            self.reset()
            return None
        if now - self._last_at > 0.25:
            self.reset()
        self._last_at = now
        # MediaPipe image z uses the x scale; y uses the actual image height.
        image_points = [(float(p[0]), float(p[1]) * image_aspect, float(p[2]) if len(p) > 2 else 0.0)
                        for p in landmarks]
        image_palm_width = dist(image_points[5], image_points[17])
        if image_palm_width < 0.035 or image_palm_width > 0.65:
            self.reset()
            return None
        points, palm_width = image_points, image_palm_width
        using_world = False
        if (world_landmarks and len(world_landmarks) == 21 and
                all(len(p) == 3 and all(isfinite(float(v)) for v in p) for p in world_landmarks)):
            world_width = dist(world_landmarks[5], world_landmarks[17])
            if world_width > 1e-4:
                # The model already supplies these estimates; no extra inference pass.
                points = [tuple(float(v) for v in p) for p in world_landmarks]
                palm_width = world_width
                using_world = True
        if self._world_geometry is not None and self._world_geometry != using_world:
            self.reset()
            self._last_at = now
        self._world_geometry = using_world
        extended = [self._extended(points, *joints) for joints in
                    ((5, 6, 8), (9, 10, 12), (13, 14, 16), (17, 18, 20))]
        pinch_ratio = dist(points[4], points[8]) / palm_width
        # Separate close/open thresholds; a folded fist must not become a pinch.
        pinch_shape = (self._joint_angle(points, 5, 6, 8) > (90 if self._pinching else 100) and
                       dist(points[8], points[5]) > palm_width * (0.55 if self._pinching else 0.6) and
                       dist(points[4], points[2]) > palm_width * (0.3 if self._pinching else 0.35))
        self._pinching = pinch_shape and pinch_ratio < (0.42 if self._pinching else 0.27)
        geometric = False
        if self._pinching:
            key, geometric = "Pinch", True
        elif extended == [True, True, True, False]:
            key, geometric = "Three_Fingers", True
        elif extended == [True, True, False, False] and (key == "None" or confidence < 0.6):
            key, geometric = "Victory", True
        elif not any(extended):
            # Direction is in mirrored screen coordinates, regardless of handedness.
            dx = image_points[2][0] - image_points[4][0]
            dy = image_points[4][1] - image_points[2][1]
            outside_palm = (image_points[4][0] < min(image_points[5][0], image_points[17][0]) - image_palm_width * 0.12 or
                            image_points[4][0] > max(image_points[5][0], image_points[17][0]) + image_palm_width * 0.12)
            if (outside_palm and self._joint_angle(points, 2, 3, 4) > 145 and
                    abs(dx) > image_palm_width * 0.4 and abs(dx) > abs(dy) * 1.3):
                key, geometric = "Thumb_Left" if dx < 0 else "Thumb_Right", True
        threshold = 0.45 if key == self._candidate and now - self._since >= 0.12 else 0.6
        if not geometric and (confidence < threshold or key not in LABELS):
            self._candidate = ""
            return None

        position = (1.0 - float(landmarks[9][0]), float(landmarks[9][1]))
        cursor = (1.0 - float(landmarks[8][0]), float(landmarks[8][1]))
        if self._last_position is not None and dist(position, self._last_position) > 0.22:
            # A replacement hand / tracking jump requires a fresh clutch.
            self._candidate = ""
            self._filters = [OneEuro() for _ in range(4)]
            self._spread_filter = OneEuro(min_cutoff=2.0, beta=1.0)
        self._last_position = position
        filtered = [f.update(value, now) for f, value in zip(self._filters, (*position, *cursor))]
        if key != self._candidate:
            self._candidate, self._since = key, now
        held = now - self._since
        spread = self._spread_filter.update(dist(points[8], points[12]) / palm_width, now)
        return HandFrame(key, held, held >= 0.12, tuple(filtered[:2]), tuple(filtered[2:]), geometric, spread)
