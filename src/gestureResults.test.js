import assert from 'node:assert/strict';
import test from 'node:test';

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
