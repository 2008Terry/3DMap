import React, { useCallback, useRef, useState } from 'react';
import CampusScene from './CampusScene.jsx';
import GestureRecognition from './GestureRecognition.jsx';
import { BUILDINGS, CAMPUS_CONTEXT, MAP_CENTER } from './campusData.js';

export default function CampusExplorer({ gestureControl = false }) {
  const [selectedBuildingId, setSelectedBuildingId] = useState(null);
  const [resetCameraKey, setResetCameraKey] = useState(0);
  const gestureControlsRef = useRef(null);
  const previousPalmRef = useRef(null);
  const lastGestureRef = useRef(null);
  const lastDiscreteActionAtRef = useRef(0);
  const [gestureAction, setGestureAction] = useState('等待手势');
  const selectedBuilding = BUILDINGS.find((building) => building.id === selectedBuildingId);
  const clearSelection = () => setSelectedBuildingId(null);

  const handleGestureChange = useCallback((gesture) => {
    const controller = gestureControlsRef.current;
    if (!gestureControl || !controller) return;
    if (gesture.state !== 'recognized' || gesture.confidence < 0.68) {
      previousPalmRef.current = null;
      lastGestureRef.current = null;
      setGestureAction('等待手势');
      return;
    }

    if (gesture.key === 'Open_Palm') {
      setGestureAction((current) => current === '张开手掌 · 移动地图' ? current : '张开手掌 · 移动地图');
      const palm = gesture.landmarks?.[9];
      if (!palm) return;
      const position = { x: 1 - palm.x, y: palm.y };
      const previous = previousPalmRef.current;
      if (previous) {
        const deltaX = position.x - previous.x;
        const deltaY = position.y - previous.y;
        const filteredX = Math.abs(deltaX) < 0.003 ? 0 : Math.max(-0.06, Math.min(0.06, deltaX));
        const filteredY = Math.abs(deltaY) < 0.003 ? 0 : Math.max(-0.06, Math.min(0.06, deltaY));
        gestureControlsRef.current?.panBy(filteredX, filteredY);
      }
      previousPalmRef.current = position;
      lastGestureRef.current = 'Open_Palm';
      return;
    }

    previousPalmRef.current = null;
    if (lastGestureRef.current === gesture.key) return;
    lastGestureRef.current = gesture.key;
    if (gesture.key === 'Thumb_Up') {
      if (Date.now() - lastDiscreteActionAtRef.current < 700) return;
      lastDiscreteActionAtRef.current = Date.now();
      setGestureAction('拇指向上 · 放大地图');
      gestureControlsRef.current?.zoomBy(0.82);
    } else if (gesture.key === 'Thumb_Down') {
      if (Date.now() - lastDiscreteActionAtRef.current < 700) return;
      lastDiscreteActionAtRef.current = Date.now();
      setGestureAction('拇指向下 · 缩小地图');
      gestureControlsRef.current?.zoomBy(1.22);
    } else if (gesture.key === 'Victory') {
      setGestureAction('胜利手势 · 重置视角');
      gestureControlsRef.current?.reset();
    } else {
      setGestureAction(gesture.label);
    }
  }, [gestureControl]);

  return (
    <main className="app-shell" id="top">
      <header className="topbar">
        <a className="brand" href="#top" aria-label="空间档案首页">
          <span className="brand-mark" aria-hidden="true"><i /><i /><i /></span>
          <span>空间档案<span className="brand-en"> / CAMPUS SPACES</span></span>
        </a>
        <div className="topbar-meta"><span className="live-dot" />建筑轮廓来源：安娜堡市 <span className="meta-divider">/</span> 08 栋{!gestureControl && <a className="gesture-map-link" href="/gesture-map.html">手势地图 ↗</a>}</div>
      </header>

      <section className="intro" aria-labelledby="page-title">
        <div>
          <p className="eyebrow"><span>美国 · 密歇根大学</span><span className="eyebrow-line" /><span>CENTRAL CAMPUS</span></p>
          <h1 id="page-title">对角广场与中央校区<span>The Diag · University of Michigan</span></h1>
        </div>
        <p className="intro-note">从 Diag 鸟瞰 Central Campus。<br />拖动或张开手掌平移，滚轮或拇指缩放；胜利手势重置。</p>
      </section>

      <p className="map-caveat" role="note"><span className="caveat-mark" aria-hidden="true">!</span><span><strong>建筑轮廓来自安娜堡市数据</strong> 楼层数和建筑特征按已链接的校方资料展示；来源存在差异时会明确标出。Angell Hall 与 Hill Auditorium 的柱廊、窗面和腰线为校方资料支持的立面示意，细部尺寸不是测量值。Diag 草坪、道路和步道仍为简化示意，不用于测绘或正式导航；没有可靠平面图的楼不绘制内部结构。</span></p>

      <section className="workspace" aria-label="Diag 校园建筑探索器">
        <aside className="building-panel panel" aria-label="建筑列表">
          <div className="panel-heading"><span>建筑索引</span><span className="panel-index">BUILDINGS / {String(BUILDINGS.length).padStart(2, '0')}</span></div>
          <p className="panel-subtitle">选择建筑查看真实轮廓、已核实的楼层与外观资料</p>
          <div className="building-list" role="group" aria-label="选择建筑">
            {BUILDINGS.map((building, index) => (
              <button
                className={`building-option${selectedBuildingId === building.id ? ' is-current' : ''}`}
                type="button"
                key={building.id}
                aria-pressed={selectedBuildingId === building.id}
                onClick={() => setSelectedBuildingId(building.id)}
              >
                <span className="building-number">{String(index + 1).padStart(2, '0')}</span>
                <span className="building-option-copy"><strong>{building.name}</strong><small>{building.category}</small></span>
                <span className="building-indicator" aria-hidden="true" />
              </button>
            ))}
          </div>
          <div className="panel-footer"><span className="status-mark" />{BUILDINGS.length} 栋 <span>·</span> 市建筑轮廓</div>
        </aside>

        <section className="model-panel" aria-label="可交互密歇根大学中央校区全域地图">
          <div className="model-toolbar">
            <div className="view-label"><span className="view-dot" />Central Campus 鸟瞰 <span className="view-coordinate">{MAP_CENTER.lat.toFixed(4)}° N&nbsp; {Math.abs(MAP_CENTER.lon).toFixed(4)}° W</span></div>
            <button className="reset-button" type="button" onClick={() => setResetCameraKey((key) => key + 1)}><span aria-hidden="true">⟳</span> 重置视角</button>
          </div>
          <div className="scene-placeholder">
            <CampusScene
              buildings={BUILDINGS}
              context={CAMPUS_CONTEXT}
              selectedBuildingId={selectedBuildingId}
              resetCameraKey={resetCameraKey}
              onBuildingSelect={setSelectedBuildingId}
              onClearSelection={clearSelection}
              onGestureControlsReady={(controls) => { gestureControlsRef.current = controls; }}
            />
            <div className="scene-caption"><span className="caption-rule" />拖动旋转 <span>·</span> 滚轮缩放 <span>·</span> 点击建筑查看</div>
            {gestureControl && <div className="gesture-map-overlay">
              <GestureRecognition compact onGestureChange={handleGestureChange} />
              <div className="gesture-map-instructions" aria-label="手势操作说明">
                <span><b>张开手掌</b> 移动地图</span>
                <span><b>拇指 ↑ / ↓</b> 缩放地图</span>
                <span><b>胜利手势</b> 重置视角</span>
              </div>
              <div className="gesture-map-action" aria-live="polite">{gestureAction}</div>
            </div>}
          </div>
          <div className="model-legend"><span><i className="legend-dot legend-active" />已选建筑</span><span><i className="legend-dot legend-rest" />其他建筑</span><span className="model-scale">Central Campus 全域视野 · {BUILDINGS.length} 栋重点建筑轮廓</span></div>
        </section>

        <aside className="detail-panel panel" aria-label="建筑详情">
          <div className="panel-heading"><span>建筑详情</span><span className="panel-index">BUILDING / INFO</span></div>
          {selectedBuilding ? (
            <div className="detail-populated" aria-live="polite">
              <span className="detail-kicker">SELECTED BUILDING</span>
              <h2>{selectedBuilding.name}</h2>
              <p className="detail-use">{selectedBuilding.description}</p>
              <dl className="detail-facts">
                <div><dt>资料中的楼层</dt><dd>{selectedBuilding.floors}</dd></div>
                <div><dt>模型挤出高度</dt><dd>{selectedBuilding.heightLabel}<small>用于显示体量；市数据字段为平均结构高度</small></dd></div>
                <div><dt>轮廓组成</dt><dd>{selectedBuilding.parts.length} 个市图层建筑部件<small>按 City of Ann Arbor Facility ID 匹配</small></dd></div>
              </dl>
              {selectedBuilding.facts.length > 0 && <div className="detail-architecture">
                <h3>已核实的建筑特征</h3>
                <ul>{selectedBuilding.facts.map((fact) => <li key={fact}>{fact}</li>)}</ul>
                {selectedBuilding.floorPlanUrl && <a className="floor-plan-link" href={selectedBuilding.floorPlanUrl} target="_blank" rel="noreferrer">查看校方楼层平面图 ↗</a>}
              </div>}
              {selectedBuilding.floorPlanUrl && selectedBuilding.facts.length === 0 && <a className="floor-plan-link" href={selectedBuilding.floorPlanUrl} target="_blank" rel="noreferrer">查看校方楼层平面图 ↗</a>}
              <div className="building-sources">
                <h3>资料来源</h3>
                {selectedBuilding.sources.map((source) => <a key={source.url} href={source.url} target="_blank" rel="noreferrer">{source.label} ↗</a>)}
              </div>
              <button className="clear-selection-button" type="button" onClick={clearSelection}>清除选择 <span aria-hidden="true">×</span></button>
            </div>
          ) : (
            <div className="detail-empty" aria-live="polite">
              <div className="building-glyph" aria-hidden="true"><span /><span /><span /></div>
              <p>选择一栋建筑</p>
              <span>从列表或地图点选；<br />点击地图空地可清除选择。</span>
            </div>
          )}
          <div className="detail-footer"><span>BUILDING ID</span><span>{selectedBuilding?.id ?? '— — —'}</span></div>
        </aside>
      </section>

      <footer className="page-footer">
        <span>空间导览原型 · 非官方导航服务</span>
        <span>建筑轮廓：<a href="https://data.a2gov.org/@city-of-ann-arbor/building-footprints" target="_blank" rel="noreferrer">City of Ann Arbor Building Footprints</a> · Woolpert / City of Ann Arbor Community Services</span>
      </footer>
    </main>
  );
}
