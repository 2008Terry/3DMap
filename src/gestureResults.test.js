import assert from 'node:assert/strict';
import test from 'node:test';
import { chooseInitialCamera } from './cameraDevices.js';

const { toGestureViewModel } = await import('./gestureResults.js').catch(() => ({}));

test('maps a recognized MediaPipe gesture to the localized display model', () => {
  assert.deepEqual(toGestureViewModel({
    gestures: [[{ categoryName: 'Open_Palm', score: 0.94 }]],
    landmarks: [[{ x: 0.2, y: 0.3, z: 0 }]],
    handedness: [[{ categoryName: 'Right' }]],
  }), {
    state: 'recognized',
    key: 'Open_Palm',
    label: '张开手掌',
    confidence: 0.94,
    landmarks: [{ x: 0.2, y: 0.3, z: 0 }],
  });
});

test('distinguishes an unrecognized hand from no detected hand', () => {
  assert.equal(toGestureViewModel({
    gestures: [[{ categoryName: 'None', score: 0.62 }]],
    landmarks: [[{ x: 0.5, y: 0.5, z: 0 }]],
  }).state, 'unrecognized');

  assert.equal(toGestureViewModel({ gestures: [], landmarks: [] }).state, 'no-hand');
});

test('marks unsupported model categories as unrecognized', () => {
  assert.equal(toGestureViewModel({
    gestures: [[{ categoryName: 'Custom_Sign', score: 0.8 }]],
    landmarks: [[{ x: 0.5, y: 0.5, z: 0 }]],
  }).state, 'unrecognized');
});

test('prefers an integrated webcam over a virtual camera when no camera was chosen', () => {
  assert.equal(chooseInitialCamera([
    { deviceId: 'virtual', label: 'TranScreen Camera' },
    { deviceId: 'integrated', label: 'Integrated Camera (04f2:b7b4)' },
  ], ''), 'integrated');
});

test('preserves an explicit camera selection', () => {
  assert.equal(chooseInitialCamera([
    { deviceId: 'integrated', label: 'Integrated Camera' },
  ], 'external'), 'external');
});

test('leaves browser default selected when no integrated webcam is identifiable', () => {
  assert.equal(chooseInitialCamera([
    { deviceId: 'virtual', label: 'TranScreen Camera' },
    { deviceId: 'usb', label: 'Logitech BRIO' },
  ], ''), '');
});
