"""Search, selection, and camera commands shared by QML and gestures."""

from __future__ import annotations

import time
from math import exp, hypot, log
from typing import Any

from PySide6.QtCore import QEvent, QObject, Property, QTimer, Qt, Signal, Slot

if __package__:
    from .campus_data import Building, CampusExtent, pick_building
    from .gesture_input import HandInterpreter, HOLD_SECONDS, LABELS
else:
    from campus_data import Building, CampusExtent, pick_building
    from gesture_input import HandInterpreter, HOLD_SECONDS, LABELS


class MapController(QObject):
    resetCameraRequested = Signal()
    panRequested = Signal(float, float)
    zoomRequested = Signal(float)
    selectionChanged = Signal(str)
    gestureStatusChanged = Signal(str)
    detailsChanged = Signal()
    focusRequested = Signal(float, float, float)
    pointingChanged = Signal(float, float, bool)
    lookRequested = Signal(float, float)
    walkRequested = Signal(float)
    orbitRequested = Signal(float, float)
    selectRequested = Signal(float, float)
    gestureControlsChanged = Signal()
    gestureFeedbackChanged = Signal()

    def __init__(self, buildings: list[Building], extent: CampusExtent, inspector=None, environment=None):
        super().__init__()
        self._buildings = buildings
        self._by_id = {building.id: building for building in buildings}
        self._extent = extent
        self._selected_id = ""
        self._gesture_status = "Gesture camera inactive"
        self._inspector = inspector
        self._bus_stops = (environment or {}).get("busStops", [])
        self._hand = HandInterpreter()
        self._frame = None
        self._last_frame_at = self._last_tick = time.monotonic()
        self._motion_position = None
        self._motion_spread = None
        self._motion_key = ""
        self._action_latch = ""
        self._last_floor_at = 0.0
        self._last_point = None
        self._neutral_since = None
        self._enabled = self._window_active = True
        self._manual_until = 0.0
        self._manual_keys = set()
        self._manual_mouse = self._manual_touch = self._manual_native = False
        self._blocked_last = False
        self._sensitivity = 1.0
        self._comfort = 0.8
        self._point_center = (0.5, 0.5)
        self._last_cursor = None
        self._dwell_enabled = True
        self._navigation_span = max(extent.width, extent.depth)
        self._feedback = {"label": "等待手势", "progress": 0.0, "points": []}
        self._context = None
        self._timer = QTimer(self)
        self._timer.setInterval(16)
        self._timer.timeout.connect(self._gesture_tick)
        self._timer.start()

    @Property(bool, notify=gestureControlsChanged)
    def gestures_enabled(self):
        return self._enabled

    @Property(float, notify=gestureControlsChanged)
    def gesture_sensitivity(self):
        return self._sensitivity

    @Property(float, notify=gestureControlsChanged)
    def comfort_range(self):
        return self._comfort

    @Property(bool, notify=gestureControlsChanged)
    def dwell_enabled(self):
        return self._dwell_enabled

    @Property("QVariantMap", notify=gestureFeedbackChanged)
    def gesture_feedback(self):
        return self._feedback

    def _stop_motion(self):
        self._frame = None
        self._motion_position = None
        self._motion_spread = None
        self._motion_key = ""
        self.pointingChanged.emit(0, 0, False)

    def _release_hand(self):
        self._stop_motion()
        self._hand.reset()
        self._action_latch = ""
        self._last_point = None
        self._neutral_since = None

    @Slot()
    def stop_gesture_input(self):
        self._release_hand()
        self._feedback = {"label": "手势已停止", "progress": 0.0, "points": []}
        self.gestureFeedbackChanged.emit()

    def _interrupt_observation(self):
        self._stop_motion()
        self._hand.reset()
        self._neutral_since = self._last_point = self._last_cursor = None
        self._feedback = {"label": "观测中断 · 已停止", "progress": 0.0, "points": []}
        self.set_gesture_status("观测中断 · 等待新手部观测")
        self.gestureFeedbackChanged.emit()

    @Slot(bool)
    def set_gestures_enabled(self, enabled):
        self._enabled = bool(enabled)
        self._release_hand()
        self.gestureControlsChanged.emit()
        self._feedback = {"label": "等待重新稳定" if enabled else "手势已暂停", "progress": 0.0, "points": []}
        self.gestureFeedbackChanged.emit()
        self.set_gesture_status("等待重新稳定手势" if enabled else "手势已暂停 · 控制开关手势、空格或按钮恢复")

    @Slot(bool)
    def set_window_active(self, active):
        self._window_active = bool(active)
        if not active:
            self._manual_keys.clear()
            self._manual_mouse = self._manual_touch = self._manual_native = False
        self._release_hand()

    @Slot(float)
    def set_gesture_sensitivity(self, value):
        self._sensitivity = max(0.5, min(1.75, value))
        self.gestureControlsChanged.emit()

    @Slot(float)
    def set_comfort_range(self, value):
        self._comfort = max(0.55, min(1.0, value))
        self._release_hand()
        self.gestureControlsChanged.emit()

    @Slot()
    def calibrate_pointer(self):
        if not self._last_cursor or time.monotonic() - self._last_cursor[2] > 3.0:
            self.set_gesture_status("先舒适地举起食指，再点击设为中心")
            return
        self._point_center = tuple(max(0.15, min(0.85, v)) for v in self._last_cursor[:2])
        self._release_hand()
        self.set_gesture_status("已设指向中心 · 放松后重新指向")

    @Slot()
    def reset_pointer_center(self):
        self._point_center = (0.5, 0.5)
        self._release_hand()

    @Slot(bool)
    def set_dwell_enabled(self, enabled):
        self._dwell_enabled = bool(enabled)
        self.gestureControlsChanged.emit()

    @Slot(float)
    def set_navigation_span(self, span):
        self._navigation_span = max(8.0, min(16000.0, span))

    @Slot()
    def manual_input(self):
        self._manual_until = time.monotonic() + 0.6
        self._release_hand()

    def _manual_blocked(self, now):
        return bool(self._manual_keys or self._manual_mouse or self._manual_touch or
                    self._manual_native or now < self._manual_until)

    def eventFilter(self, watched, event):
        kind = event.type()
        if kind in (QEvent.Type.MouseButtonPress, QEvent.Type.MouseButtonDblClick,
                    QEvent.Type.MouseButtonRelease, QEvent.Type.MouseMove):
            self._manual_mouse = event.buttons() != Qt.MouseButton.NoButton
            if self._manual_mouse or kind != QEvent.Type.MouseMove:
                self.manual_input()
        elif kind in (QEvent.Type.KeyPress, QEvent.Type.KeyRelease):
            key = event.nativeScanCode() or event.key()
            if kind == QEvent.Type.KeyPress:
                self._manual_keys.add(key)
            elif not event.isAutoRepeat():
                self._manual_keys.discard(key)
            self.manual_input()
        elif kind in (QEvent.Type.TouchBegin, QEvent.Type.TouchUpdate,
                      QEvent.Type.TouchEnd, QEvent.Type.TouchCancel):
            self._manual_touch = kind in (QEvent.Type.TouchBegin, QEvent.Type.TouchUpdate)
            self.manual_input()
        elif kind == QEvent.Type.NativeGesture:
            if event.gestureType() == Qt.NativeGestureType.BeginNativeGesture:
                self._manual_native = True
            elif event.gestureType() == Qt.NativeGestureType.EndNativeGesture:
                self._manual_native = False
            self.manual_input()
        elif kind in (QEvent.Type.Wheel, QEvent.Type.InputMethod):
            self.manual_input()
        return False

    @Slot()
    def go_back(self):
        self._stop_motion()
        inspector = self._inspector
        if inspector and inspector.active:
            if inspector.mode == "inside":
                inspector.set_mode("dollhouse")
            else:
                inspector.close()

    @Slot()
    def cycle_structure_mode(self):
        inspector = self._inspector
        if inspector and inspector.active:
            modes = ("dollhouse", "section", "xray", "explode", "floor")
            index = modes.index(inspector.mode) if inspector.mode in modes else -1
            inspector.set_mode(modes[(index + 1) % len(modes)])

    @Slot()
    def enter_structure(self):
        inspector = self._inspector
        if not inspector or not self._selected_id:
            self.set_gesture_status("先指向选择建筑，再握拳进入")
        elif not inspector.active:
            inspector.open()
        elif inspector.mode != "inside":
            inspector.set_mode("inside")
        else:
            inspector.set_mode("dollhouse")

    def _gesture_tick(self):
        now = time.monotonic()
        dt, self._last_tick = min(0.05, max(0.0, now - self._last_tick)), now
        if self._frame is None:
            return
        if now - self._last_frame_at > 0.25:
            self._interrupt_observation()
            return
        if not self._enabled or not self._window_active or self._manual_blocked(now):
            self._stop_motion()
            return
        frame = self._frame
        if not frame.ready or frame.key not in ("Thumb_Up", "Thumb_Down"):
            return
        inspector = self._inspector
        direction = 1 if frame.key == "Thumb_Up" else -1
        if inspector and inspector.active:
            if inspector.mode == "inside":
                self.walkRequested.emit(direction * dt * 2.0 * self._sensitivity)
            elif frame.held >= 0.4 and now - self._last_floor_at >= 0.8:
                self._last_floor_at = now
                previous_floor = inspector.selected_floor
                inspector.change_floor(direction)
                if inspector.selected_floor != previous_floor and inspector.mode != "floor":
                    inspector.set_mode("floor")
        else:
            self.zoom_by(exp(-direction * dt * 0.65 * self._sensitivity))

    @Property("QVariantMap", notify=detailsChanged)
    def selected_details(self):
        building = self._by_id.get(self._selected_id)
        if not building:
            return {}
        record = building.to_qml()
        points = [p for part in building.parts for p in part["footprint"]]
        cx = (min(p[0] for p in points) + max(p[0] for p in points)) / 2
        cz = (min(p[1] for p in points) + max(p[1] for p in points)) / 2
        stops = sorted(self._bus_stops, key=lambda s: hypot(s["position"][0] - cx, s["position"][1] - cz))
        record["nearbyStops"] = [
            {**stop, "distance": round(hypot(stop["position"][0] - cx, stop["position"][1] - cz))}
            for stop in stops[:3] if hypot(stop["position"][0] - cx, stop["position"][1] - cz) < 250
        ]
        return record

    @Property(str, notify=gestureStatusChanged)
    def gesture_status(self) -> str:
        return self._gesture_status

    def set_gesture_status(self, status: str) -> None:
        if status != self._gesture_status:
            self._gesture_status = status
            self.gestureStatusChanged.emit(status)

    @Slot(str, result="QVariantList")
    def search(self, query: str) -> list[dict[str, str]]:
        needle = query.strip().casefold()
        if not needle:
            return []
        results = []
        for building in self._buildings:
            fields = (building.name, building.facility_id, building.id, building.campus)
            if any(needle in value.casefold() for value in fields if value):
                results.append({
                    "id": building.id,
                    "facility_id": building.facility_id,
                    "name": building.name,
                    "campus": building.campus,
                })
        return results[:60]

    @Slot(str, result="QVariant")
    def select_building(self, building_id: str) -> dict[str, Any]:
        building = self._by_id.get(building_id)
        if building is None:
            return {}
        self._selected_id = building.id
        if self._inspector:
            self._inspector.select(building.id)
        self.selectionChanged.emit(building.id)
        self.detailsChanged.emit()
        return building.to_qml()

    @Slot(str)
    def focus_building(self, building_id):
        if self._inspector and self._inspector.active:
            self._inspector.close()
        if not self.select_building(building_id):
            return
        building = self._by_id[building_id]
        points = [point for part in building.parts for point in part["footprint"]]
        xs, zs = [p[0] for p in points], [p[1] for p in points]
        self.focusRequested.emit((min(xs) + max(xs)) / 2, (min(zs) + max(zs)) / 2,
                                 max(100, max(xs) - min(xs), max(zs) - min(zs)) * 2.1)

    @Slot(str)
    def focus_campus(self, campus):
        if self._inspector and self._inspector.active:
            self._inspector.close()
        subset = [b for b in self._buildings if campus in b.campus]
        if not subset:
            self.reset_camera()
            return
        points = [p for b in subset for part in b.parts for p in part["footprint"]]
        xs, zs = [p[0] for p in points], [p[1] for p in points]
        self.focusRequested.emit((min(xs) + max(xs)) / 2, (min(zs) + max(zs)) / 2,
                                 max(max(xs) - min(xs), max(zs) - min(zs)) * 0.9)

    @Slot(float, float, float, result=str)
    def select_at(self, x: float, y: float, z: float) -> str:
        building = pick_building((x, y, z))
        if building is None:
            return ""
        self.select_building(building.id)
        return building.id

    @Slot()
    def reset_camera(self) -> None:
        self.resetCameraRequested.emit()

    @Slot(float, float)
    def pan_by(self, delta_x: float, delta_y: float) -> None:
        self.panRequested.emit(delta_x, delta_y)

    @Slot(float)
    def zoom_by(self, factor: float) -> None:
        self.zoomRequested.emit(factor)

    @Slot(str, float, "QVariant")
    def handle_gesture(self, key: str, confidence: float, landmarks: Any,
                       world_landmarks=None, image_aspect=0.75, observed_at=None) -> None:
        now = time.monotonic()
        observed_at = now if observed_at is None else observed_at
        if observed_at <= self._last_frame_at:
            return
        if now - observed_at > 0.25:
            self._interrupt_observation()
            return
        self._last_frame_at = observed_at
        inspector = self._inspector
        inspecting = bool(inspector and inspector.active)
        inside = inspecting and inspector.mode == "inside"
        context = (self._selected_id, inspecting, inspector.mode if inspecting else "campus",
                   inspector.inspection_key if inspecting else "",
                   inspector.selected_floor if inspecting else -1)
        if context != self._context:
            self._context = context
            self._motion_position = None
            self._motion_spread = None
            self._motion_key = ""
            self._last_point = None
            self._last_floor_at = now
        blocked = not self._enabled or not self._window_active or self._manual_blocked(now)
        if self._blocked_last and not blocked:
            self._hand.reset()
        self._blocked_last = blocked
        frame = self._hand.update(key, confidence, landmarks, observed_at, world_landmarks, image_aspect)
        points = [{"x": 1.0 - float(p[0]), "y": float(p[1])} for p in landmarks] if len(landmarks) == 21 else []
        self._feedback = {"label": LABELS.get(frame.key, "未识别姿态") if frame else "放松手部 / 等待识别",
                          "progress": frame.progress if frame else 0.0,
                          "source": "关键点几何" if frame and frame.geometric else "本地模型",
                          "points": points, "imageAspect": image_aspect}
        if self._last_point and now - self._last_point[2] > 0.8:
            self._last_point = None
        if frame is None and not landmarks:
            if self._neutral_since is None:
                self._neutral_since = observed_at
            if observed_at - self._neutral_since >= 0.22:
                self._action_latch = ""
        else:
            self._neutral_since = None
            if frame and frame.ready and self._action_latch and frame.key != self._action_latch:
                self._action_latch = ""
        if frame and frame.key == "ILoveYou" and self._window_active and not self._manual_blocked(now):
            self._stop_motion()
            if frame.held >= HOLD_SECONDS[frame.key] and self._action_latch != frame.key:
                self.set_gestures_enabled(not self._enabled)
                self._action_latch = frame.key
            else:
                self.set_gesture_status("松开后重新操作" if self._action_latch == frame.key else
                                        "拇指 + 食指 + 小指 · 保持以暂停/恢复")
                self.gestureFeedbackChanged.emit()
            return
        if blocked:
            self._stop_motion()
            label = ("控制已暂停" if not self._enabled else "窗口未激活" if not self._window_active else "键鼠优先")
            self._feedback["label"] += " · " + label
            self._feedback["progress"] = 0.0
            self.gestureFeedbackChanged.emit()
            return
        self.gestureFeedbackChanged.emit()
        self._frame = frame
        if frame is None:
            self._stop_motion()
            self.set_gesture_status("放松即停止 · 指向、捏合或张开手掌开始")
            return
        if not frame.ready:
            self._stop_motion()
            self.set_gesture_status("正在稳定 · " + LABELS[frame.key])
            return
        if frame.key != "Pointing_Up":
            self.pointingChanged.emit(0, 0, False)
        if frame.key == "Pointing_Up":
            self._last_cursor = (*frame.cursor, observed_at)
            def project(v, center):
                reach = min(self._comfort / 2, center - 0.02 if v < center else 0.98 - center)
                return max(0.0, min(1.0, 0.5 + (v - center) / (2 * reach)))
            x, y = (project(v, center) for v, center in zip(frame.cursor, self._point_center))
            self._last_point = (x, y, observed_at)
            self._motion_position = None
            self._motion_key = frame.key
            self.pointingChanged.emit(x, y, True)
            self.set_gesture_status("指向后捏合确认" + (" · 或停留选择" if self._dwell_enabled else ""))
        elif frame.key in ("Open_Palm", "Pinch", "Victory"):
            if self._motion_key != frame.key:
                if (frame.key == "Pinch" and self._action_latch != "Pinch" and
                        self._last_point and now - self._last_point[2] < 0.8):
                    self.selectRequested.emit(self._last_point[0], self._last_point[1])
                    self._action_latch = "Pinch"
                self._motion_position = None
                self._motion_spread = None
                self._motion_key = frame.key
            dx = dy = 0.0
            if self._motion_position is not None:
                dx = max(-0.04, min(0.04, frame.position[0] - self._motion_position[0]))
                dy = max(-0.04, min(0.04, frame.position[1] - self._motion_position[1]))
                dx = 0.0 if abs(dx) < 0.0007 else dx * self._sensitivity
                dy = 0.0 if abs(dy) < 0.0007 else dy * self._sensitivity
                if inside:
                    self.lookRequested.emit(dx * 160, dy * 110)
                elif frame.key == "Victory":
                    self.orbitRequested.emit(-dx * 220, -dy * 140)
                elif frame.key == "Pinch" and inspecting and inspector.mode == "section":
                    delta = dx if inspector.cut_axis == "x" else -dy if inspector.cut_axis == "y" else dy
                    inspector.set_cut(inspector.cut + delta * 1.8)
                elif frame.key == "Pinch" and inspecting and inspector.mode == "explode":
                    inspector.set_spread(inspector.spread - dy * 60)
                elif frame.key == "Pinch" and inspecting and inspector.mode == "xray":
                    inspector.set_shell_opacity(inspector.shell_opacity + dy * 0.8)
                else:
                    self.pan_by(-dx * self._navigation_span, -dy * self._navigation_span)
            if frame.key == "Victory" and not inside:
                if self._motion_spread is not None and min(frame.spread, self._motion_spread) > 0.1:
                    change = log(frame.spread / self._motion_spread)
                    if abs(change) >= 0.05:
                        self.zoom_by(max(0.94, min(1.06, exp(-change * 0.7 * self._sensitivity))))
                        self._motion_spread = frame.spread
                else:
                    self._motion_spread = frame.spread
            if self._motion_position is None or dx or dy:
                self._motion_position = frame.position
            if inside:
                status = "环顾 · 松手停止"
            elif frame.key == "Victory":
                status = "双指移动旋转 · 张合双指缩放"
            elif frame.key == "Pinch" and inspecting and inspector.mode == "section":
                status = f"捏合拖动 · {inspector.cut_axis.upper()} 切面 {inspector.cut:.0%}"
            elif frame.key == "Pinch" and inspecting and inspector.mode == "explode":
                status = f"捏合上下 · 楼层展开 {inspector.spread:.1f} m"
            elif frame.key == "Pinch" and inspecting and inspector.mode == "xray":
                status = f"捏合上下 · 外壳透视 {1 - inspector.shell_opacity:.0%}"
            else:
                status = "捏合拖动地图" if frame.key == "Pinch" else "手掌拖动地图"
            self.set_gesture_status(status)
        elif frame.key in HOLD_SECONDS:
            self._motion_position = None
            self._motion_key = frame.key
            if frame.key in ("Closed_Fist", "Thumb_Right") and not self._selected_id:
                self.set_gesture_status("先指向选择建筑，再握拳或拇指向右进入")
                return
            if frame.key == "Three_Fingers" and not inspecting:
                self.set_gesture_status("打开建筑后，三指切换结构视图")
                return
            if frame.key == "Thumb_Left" and not inspecting:
                self.set_gesture_status("已经在校园 · R 或按钮复位视角")
                return
            if frame.held >= HOLD_SECONDS[frame.key] and self._action_latch != frame.key:
                self._action_latch = frame.key
                if frame.key in ("Closed_Fist", "Thumb_Right"):
                    self.enter_structure()
                elif frame.key == "Three_Fingers":
                    self.cycle_structure_mode()
                else:
                    self.go_back()
            self.set_gesture_status("松开后重新操作" if self._action_latch == frame.key else
                                    LABELS[frame.key] + " · 保持以确认")
        else:
            self._motion_position = None
            self._motion_key = frame.key
            self.set_gesture_status("拇指持续前进/后退 · 松手停止" if inside else
                                    "拇指切换楼层" if inspecting else "拇指持续缩放 · 松手停止")

    @Slot(str, str, float, object)
    def handle_recognition(self, key, label, confidence, landmarks):
        """Receive the worker's actual Qt signature on the controller's GUI thread."""
        if label == "已停止":
            self.stop_gesture_input()
        elif label == "没有新手部观测":
            self._interrupt_observation()
        else:
            if isinstance(landmarks, dict):
                self.handle_gesture(key, confidence, landmarks["landmarks"],
                                    landmarks["worldLandmarks"], landmarks["imageAspect"], landmarks["observedAt"])
            else:
                self.handle_gesture(key, confidence, landmarks)
