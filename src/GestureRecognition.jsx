import React, { useCallback, useEffect, useRef, useState } from 'react';
import { GESTURE_LABELS, toGestureViewModel } from './gestureResults.js';

const CONNECTIONS = [
  [0, 1], [1, 2], [2, 3], [3, 4],
  [0, 5], [5, 6], [6, 7], [7, 8],
  [5, 9], [9, 10], [10, 11], [11, 12],
  [9, 13], [13, 14], [14, 15], [15, 16],
  [13, 17], [17, 18], [18, 19], [19, 20], [0, 17],
];

const CAMERA_ERRORS = {
  NotAllowedError: '浏览器未获得摄像头权限。请在地址栏权限设置中允许访问后重试。',
  NotFoundError: '没有找到可用摄像头。请连接摄像头后重试。',
  NotReadableError: '摄像头当前无法读取，可能正被其他应用占用。',
  OverconstrainedError: '摄像头不支持请求的视频尺寸，请更换摄像头后重试。',
};

export default function GestureRecognition() {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const streamRef = useRef(null);
  const workerRef = useRef(null);
  const frameRef = useRef(0);
  const busyRef = useRef(false);
  const lastFrameAtRef = useRef(0);
  const cameraRunRef = useRef(0);
  const frameTimesRef = useRef([]);
  const [cameraState, setCameraState] = useState('idle');
  const [cameraError, setCameraError] = useState('');
  const [gesture, setGesture] = useState(toGestureViewModel(null));
  const [fps, setFps] = useState(0);
  const [inferenceMs, setInferenceMs] = useState(null);
  const [inferenceBackend, setInferenceBackend] = useState('');
  const [cameraDevices, setCameraDevices] = useState([]);
  const [selectedCameraId, setSelectedCameraId] = useState('');

  const refreshCameras = useCallback(async () => {
    const devices = await navigator.mediaDevices?.enumerateDevices().catch(() => []);
    setCameraDevices((devices ?? []).filter((device) => device.kind === 'videoinput'));
  }, []);

  const stopCamera = useCallback(() => {
    cameraRunRef.current += 1;
    cancelAnimationFrame(frameRef.current);
    streamRef.current?.getTracks().forEach((track) => track.stop());
    streamRef.current = null;
    if (videoRef.current) videoRef.current.srcObject = null;
    workerRef.current?.terminate();
    workerRef.current = null;
    busyRef.current = false;
    frameTimesRef.current = [];
    setCameraState('idle');
    setCameraError('');
    setGesture(toGestureViewModel(null));
    setFps(0);
    setInferenceMs(null);
    setInferenceBackend('');
  }, []);

  useEffect(() => () => {
    cancelAnimationFrame(frameRef.current);
    streamRef.current?.getTracks().forEach((track) => track.stop());
    workerRef.current?.terminate();
  }, []);

  useEffect(() => {
    refreshCameras();
    navigator.mediaDevices?.addEventListener('devicechange', refreshCameras);
    return () => navigator.mediaDevices?.removeEventListener('devicechange', refreshCameras);
  }, [refreshCameras]);

  const startCamera = async () => {
    const cameraRun = cameraRunRef.current + 1;
    cameraRunRef.current = cameraRun;
    setCameraError('');
    setCameraState('starting');
    if (!navigator.mediaDevices?.getUserMedia) {
      setCameraError('此页面无法访问摄像头。请使用 HTTPS 或 localhost 打开。');
      setCameraState('error');
      return;
    }

    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        audio: false,
        video: {
          width: { ideal: 640 },
          height: { ideal: 480 },
          ...(selectedCameraId ? { deviceId: { exact: selectedCameraId } } : {}),
        },
      });
      if (cameraRunRef.current !== cameraRun) {
        stream.getTracks().forEach((track) => track.stop());
        return;
      }
      streamRef.current = stream;
      refreshCameras();
      videoRef.current.srcObject = stream;
      await videoRef.current.play();
      if (cameraRunRef.current !== cameraRun) {
        stream.getTracks().forEach((track) => track.stop());
        videoRef.current.srcObject = null;
        return;
      }

      const worker = new Worker(new URL('./gestureWorker.js', import.meta.url), { type: 'module' });
      workerRef.current = worker;
      const captureFrame = async (now) => {
        frameRef.current = requestAnimationFrame(captureFrame);
        if (busyRef.current || now - lastFrameAtRef.current < 66) return;
        const video = videoRef.current;
        if (!video || video.readyState < HTMLMediaElement.HAVE_CURRENT_DATA || !workerRef.current) return;

        busyRef.current = true;
        lastFrameAtRef.current = now;
        try {
          const bitmap = await createImageBitmap(video);
          if (!workerRef.current) {
            bitmap.close();
            busyRef.current = false;
            return;
          }
          workerRef.current.postMessage({ type: 'frame', bitmap, timestamp: now }, [bitmap]);
        } catch {
          busyRef.current = false;
        }
      };
      worker.onmessage = ({ data }) => {
        if (data.type === 'ready') {
          setInferenceBackend(data.delegate);
          setCameraState('running');
          lastFrameAtRef.current = 0;
          frameRef.current = requestAnimationFrame(captureFrame);
          return;
        }
        if (data.type === 'result') {
          busyRef.current = false;
          const now = performance.now();
          frameTimesRef.current = [...frameTimesRef.current.filter((time) => now - time < 1000), now];
          setFps(frameTimesRef.current.length);
          setInferenceMs(data.inferenceMs);
          setGesture(toGestureViewModel(data.result));
          return;
        }
        if (data.type === 'error') {
          busyRef.current = false;
          cancelAnimationFrame(frameRef.current);
          streamRef.current?.getTracks().forEach((track) => track.stop());
          streamRef.current = null;
          if (videoRef.current) videoRef.current.srcObject = null;
          workerRef.current?.terminate();
          workerRef.current = null;
          setCameraError(`手势模型无法启动或识别失败：${data.message}`);
          setCameraState('error');
        }
      };
      worker.onerror = () => {
        busyRef.current = false;
        cancelAnimationFrame(frameRef.current);
        streamRef.current?.getTracks().forEach((track) => track.stop());
        streamRef.current = null;
        if (videoRef.current) videoRef.current.srcObject = null;
        workerRef.current?.terminate();
        workerRef.current = null;
        setCameraError('识别 Worker 无法运行。请刷新页面后重试。');
        setCameraState('error');
      };
      worker.postMessage({ type: 'init' });
    } catch (error) {
      if (cameraRunRef.current !== cameraRun) return;
      streamRef.current?.getTracks().forEach((track) => track.stop());
      streamRef.current = null;
      if (videoRef.current) videoRef.current.srcObject = null;
      setCameraError(CAMERA_ERRORS[error?.name] ?? `无法启动摄像头：${error?.message ?? '未知错误'}`);
      setCameraState('error');
    }
  };

  useEffect(() => {
    const canvas = canvasRef.current;
    const video = videoRef.current;
    if (!canvas || !video) return;
    const draw = () => {
      const { width, height } = canvas.getBoundingClientRect();
      const ratio = window.devicePixelRatio || 1;
      canvas.width = Math.max(1, Math.round(width * ratio));
      canvas.height = Math.max(1, Math.round(height * ratio));
      const context = canvas.getContext('2d');
      context.setTransform(ratio, 0, 0, ratio, 0, 0);
      context.clearRect(0, 0, width, height);

      const points = gesture.landmarks;
      if (!points || !video.videoWidth || !video.videoHeight) return;
      const scale = Math.min(width / video.videoWidth, height / video.videoHeight);
      const renderedWidth = video.videoWidth * scale;
      const renderedHeight = video.videoHeight * scale;
      const offsetX = (width - renderedWidth) / 2;
      const offsetY = (height - renderedHeight) / 2;
      const position = (point) => ({
        x: offsetX + (1 - point.x) * renderedWidth,
        y: offsetY + point.y * renderedHeight,
      });

      context.lineWidth = 2;
      context.strokeStyle = 'rgba(102, 239, 198, .9)';
      for (const [start, end] of CONNECTIONS) {
        const a = position(points[start]);
        const b = position(points[end]);
        context.beginPath();
        context.moveTo(a.x, a.y);
        context.lineTo(b.x, b.y);
        context.stroke();
      }
      points.forEach((point, index) => {
        const { x, y } = position(point);
        context.beginPath();
        context.arc(x, y, index === 0 || [4, 8, 12, 16, 20].includes(index) ? 4 : 2.7, 0, Math.PI * 2);
        context.fillStyle = index === 0 ? '#fff3bf' : '#66efc6';
        context.fill();
      });
    };
    draw();
    const observer = new ResizeObserver(draw);
    observer.observe(canvas.parentElement);
    return () => observer.disconnect();
  }, [gesture]);

  const isActive = cameraState === 'starting' || cameraState === 'running';
  const statusText = cameraState === 'running'
    ? `摄像头已启动 · 本机 ${inferenceBackend} 推理`
    : cameraState === 'starting'
      ? '正在启动摄像头和识别模型…'
      : cameraState === 'error'
        ? '无法启动识别'
        : '摄像头未启动';

  return (
    <main className="gesture-shell">
      <header className="gesture-topbar">
        <a className="gesture-brand" href="#top" aria-label="手势识别演示首页">
          <span className="gesture-brand-mark" aria-hidden="true"><i /><i /><i /></span>
          <span>手势实验室<span className="gesture-brand-en"> / GESTURE LAB</span></span>
        </a>
        <span className="local-badge"><i />ON-DEVICE INFERENCE</span>
      </header>

      <section className="gesture-intro" id="top">
        <div>
          <p className="gesture-eyebrow">CAMERA INPUT <span /> SINGLE-HAND TRACKING</p>
          <h1>看见手势<span>实时追踪，逐帧分类</span></h1>
        </div>
        <p className="gesture-intro-note">用一只手试试张掌、握拳、指向和手势符号。<br />摄像头画面留在此设备，识别类别实时显示。</p>
      </section>

      <section className="gesture-workspace" aria-label="手势识别工作区">
        <section className="camera-panel" aria-label="摄像头预览">
          <div className="camera-panel-top">
            <div><span className={`camera-status-dot${cameraState === 'running' ? ' is-live' : ''}`} /><span>{statusText}</span></div>
            <span className="camera-technical">RGB CAMERA / MAX 1 HAND</span>
          </div>
          <div className={`camera-stage${isActive ? ' is-active' : ''}`}>
            <video ref={videoRef} className="camera-video" muted playsInline aria-label="镜像摄像头预览" />
            <canvas ref={canvasRef} className="landmark-canvas" aria-hidden="true" />
            {!isActive && (
              <div className="camera-placeholder">
                <div className="hand-orbit" aria-hidden="true"><span /><i /><i /><i /><i /><i /></div>
                <strong>{cameraState === 'error' ? '摄像头没有启动' : '准备好看见手势了吗？'}</strong>
                <span>{cameraError || '启动后，将一只手举到画面中央。'}</span>
              </div>
            )}
            {isActive && <span className="camera-corner camera-corner-tl" />}
            {isActive && <span className="camera-corner camera-corner-tr" />}
            {isActive && <span className="camera-corner camera-corner-bl" />}
            {isActive && <span className="camera-corner camera-corner-br" />}
            {cameraState === 'starting' && <div className="camera-loading">正在加载手势模型</div>}
          </div>
          <div className="camera-panel-bottom">
            <label className="camera-select">
              <span>摄像头</span>
              <select value={selectedCameraId} onChange={(event) => setSelectedCameraId(event.target.value)} disabled={isActive}>
                <option value="">系统默认</option>
                {cameraDevices.map((device, index) => (
                  <option value={device.deviceId} key={device.deviceId}>{device.label || `摄像头 ${index + 1}`}</option>
                ))}
              </select>
            </label>
            <div className="camera-metrics">
              <span><small>识别帧率</small><strong>{isActive ? <>{fps} <small>FPS</small></> : '—'}</strong></span>
              <span><small>单帧推理</small><strong>{inferenceMs === null ? '—' : `${inferenceMs.toFixed(0)} ms`}</strong></span>
            </div>
            {isActive ? (
              <button className="camera-button stop-button" type="button" onClick={stopCamera}><i />停止摄像头</button>
            ) : (
              <button className="camera-button start-button" type="button" onClick={startCamera} disabled={cameraState === 'starting'}>
                <span aria-hidden="true">◉</span>{cameraState === 'starting' ? '正在连接…' : '启动摄像头'}
              </button>
            )}
          </div>
        </section>

        <aside className="classification-panel" aria-label="手势分类结果">
          <div className="classification-head">
            <div><p className="panel-kicker">LIVE CLASSIFICATION</p><h2>当前识别</h2></div>
            <span className={`recognition-state state-${gesture.state}`}>{gesture.state === 'recognized' ? '已识别' : gesture.state === 'unrecognized' ? '未识别手势' : '等待手部'}</span>
          </div>
          <div className={`active-gesture${gesture.state === 'recognized' ? ' has-result' : ''}`}>
            <span className="gesture-bracket" aria-hidden="true">{gesture.state === 'recognized' ? '✳' : '—'}</span>
            <strong>{gesture.label}</strong>
            {gesture.state === 'recognized' && <span className="gesture-code">{gesture.key}</span>}
            {gesture.state === 'no-hand' && <small>把手放在摄像头画面内</small>}
            {gesture.state === 'unrecognized' && <small>检测到手，但不属于当前七类手势</small>}
          </div>
          <div className="confidence-row"><span>置信度</span><strong>{gesture.state === 'recognized' ? `${Math.round(gesture.confidence * 100)}%` : '—'}</strong></div>
          <div className="confidence-track"><span style={{ width: gesture.state === 'recognized' ? `${Math.round(gesture.confidence * 100)}%` : '0%' }} /></div>
          <div className="catalog-head"><span>内置分类</span><span>7 CLASSES</span></div>
          <div className="gesture-catalog">
            {Object.entries(GESTURE_LABELS).map(([key, label]) => (
              <div className={`gesture-chip${gesture.key === key ? ' is-current' : ''}`} key={key}>
                <span className="gesture-chip-mark" />
                <span>{label}</span>
                <small>{key.replaceAll('_', ' ')}</small>
              </div>
            ))}
          </div>
          <p className="recognition-note">识别器只跟踪一只手。未检测到手与不属于已知类别的手势会分别显示。</p>
        </aside>
      </section>

      <footer className="gesture-footer">
        <span>MEDIAPIPE GESTURE RECOGNIZER</span>
        <span>摄像头画面在浏览器本地处理 · 第一次启动需要下载识别模型</span>
      </footer>
    </main>
  );
}
