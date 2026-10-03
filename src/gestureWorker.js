import { FilesetResolver, GestureRecognizer } from '@mediapipe/tasks-vision';

const version = '1.0.1';
const wasmPath = `https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@${version}/wasm`;
const modelPath = 'https://storage.googleapis.com/mediapipe-models/gesture_recognizer/gesture_recognizer/float16/1/gesture_recognizer.task';

let recognizer;

self.onmessage = async ({ data }) => {
  if (data.type === 'init') {
    try {
      const vision = await FilesetResolver.forVisionTasks(wasmPath, true);
      const options = {
        runningMode: 'VIDEO',
        numHands: 1,
      };
      let delegate = 'GPU';
      try {
        recognizer = await GestureRecognizer.createFromOptions(vision, {
          ...options,
          baseOptions: { modelAssetPath: modelPath, delegate: 'GPU' },
        });
      } catch {
        delegate = 'CPU';
        recognizer = await GestureRecognizer.createFromOptions(vision, {
          ...options,
          baseOptions: { modelAssetPath: modelPath, delegate: 'CPU' },
        });
      }
      self.postMessage({ type: 'ready', delegate });
    } catch (error) {
      self.postMessage({ type: 'error', message: error instanceof Error ? error.message : String(error) });
    }
    return;
  }

  if (data.type !== 'frame') return;

  const { bitmap, timestamp } = data;
  try {
    if (!recognizer) throw new Error('识别模型尚未准备好。');
    const startedAt = performance.now();
    const result = recognizer.recognizeForVideo(bitmap, timestamp);
    self.postMessage({
      type: 'result',
      result: {
        gestures: result.gestures,
        landmarks: result.landmarks,
      },
      inferenceMs: performance.now() - startedAt,
    });
  } catch (error) {
    self.postMessage({ type: 'error', message: error instanceof Error ? error.message : String(error) });
  } finally {
    bitmap.close();
  }
};
