const INTEGRATED_CAMERA_LABEL = /\bintegrated\b|\bbuilt[ -]?in\b|\bwebcam\b|内置|集成摄像头/i;

export function chooseInitialCamera(devices, selectedCameraId) {
  if (selectedCameraId) return selectedCameraId;
  return devices.find((device) => INTEGRATED_CAMERA_LABEL.test(device.label))?.deviceId ?? '';
}
