export const GESTURE_LABELS = {
  Closed_Fist: '握拳',
  Open_Palm: '张开手掌',
  Pointing_Up: '向上指',
  Thumb_Down: '拇指向下',
  Thumb_Up: '拇指向上',
  Victory: '胜利手势',
  ILoveYou: 'I Love You',
};

export function toGestureViewModel(result) {
  const landmarks = result?.landmarks?.[0] ?? null;
  if (!landmarks) {
    return { state: 'no-hand', key: null, label: '未检测到手', confidence: 0, landmarks: null };
  }

  const category = result.gestures?.[0]?.[0];
  const key = category?.categoryName;
  const label = GESTURE_LABELS[key];
  if (!label) {
    return {
      state: 'unrecognized',
      key: key ?? null,
      label: '未识别手势',
      confidence: category?.score ?? 0,
      landmarks,
    };
  }

  return {
    state: 'recognized',
    key,
    label,
    confidence: category.score,
    landmarks,
  };
}
