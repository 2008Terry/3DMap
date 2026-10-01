import React, { useState } from 'react';
import BuildingScene from './BuildingScene.jsx';
import { FLOORS, ROOMS } from './buildingData.js';

export default function App() {
  const [selectedRoomId, setSelectedRoomId] = useState(null);
  const [selectedFloor, setSelectedFloor] = useState(null);
  const [exploded, setExploded] = useState(false);
  const [resetCameraKey, setResetCameraKey] = useState(0);
  const selectedRoom = ROOMS.find((room) => room.id === selectedRoomId);

  return (
    <main className="app-shell">
      <header className="topbar">
        <a className="brand" href="#top" aria-label="空间档案首页">
          <span className="brand-mark" aria-hidden="true"><i /><i /><i /></span>
          <span>空间档案<span className="brand-en"> / CAMPUS SPACES</span></span>
        </a>
        <div className="topbar-meta"><span className="live-dot" />交互原型 <span className="meta-divider">/</span> 01 栋</div>
      </header>

      <section className="intro" id="top">
        <div>
          <p className="eyebrow"><span>建筑 A—01</span><span className="eyebrow-line" /><span>VIRTUAL BUILDING</span></p>
          <h1>北岸学习中心<span>North Quay · Learning Commons</span></h1>
        </div>
        <p className="intro-note">转动建筑，拆开展示楼层。<br />选择房间，看看这里能做什么。</p>
      </section>

      <section className="workspace" aria-label="建筑空间探索器">
        <aside className="floor-panel panel">
          <div className="panel-heading"><span>楼层导航</span><span className="panel-index">LEVELS / 04</span></div>
          <button className="overview-button" type="button" aria-pressed={selectedFloor === null} onClick={() => setSelectedFloor(null)}>
            <span className="overview-icon" aria-hidden="true">⌂</span><span>整栋建筑</span><span className="overview-arrow">↗</span>
          </button>
          <div className="floor-list" role="group" aria-label="选择楼层">
            {FLOORS.map((floor) => (
              <button className={`floor-option${selectedFloor === floor.id ? ' is-current' : ''}`} type="button" key={floor.id} aria-pressed={selectedFloor === floor.id} onClick={() => setSelectedFloor(floor.id)}>
                <span className="floor-number">{floor.label}</span>
                <span className="floor-label">{floor.name.split(' · ')[1]}<small>FLOOR {floor.label}</small></span>
                <span className="floor-indicator" aria-hidden="true" />
              </button>
            ))}
          </div>
          <div className="panel-footer"><span className="status-mark" />4 个楼层 <span>·</span> 16 个空间</div>
        </aside>

        <section className="model-panel" aria-label="可交互建筑模型">
          <div className="model-toolbar">
            <div className="view-label"><span className="view-dot" />空间总览 <span className="view-coordinate">31° 14′ N&nbsp;&nbsp; 121° 28′ E</span></div>
            <div className="model-actions">
              <button className="tool-button" type="button" aria-pressed={exploded} onClick={() => setExploded((value) => !value)}><span aria-hidden="true">▤</span>{exploded ? '合起楼层' : '拆开楼层'}</button>
              <button className="icon-button" type="button" aria-label="重置视角" onClick={() => setResetCameraKey((key) => key + 1)}><span aria-hidden="true">⟳</span></button>
            </div>
          </div>
          <div className="scene-placeholder">
            <BuildingScene
              rooms={ROOMS}
              selectedFloor={selectedFloor}
              selectedRoomId={selectedRoomId}
              exploded={exploded}
              resetCameraKey={resetCameraKey}
              onRoomSelect={setSelectedRoomId}
              onClearSelection={() => setSelectedRoomId(null)}
            />
            <div className="scene-caption"><span className="caption-rule" />拖动旋转 <span>·</span> 滚轮缩放 <span>·</span> 点击房间查看</div>
          </div>
          <div className="model-legend"><span><i className="legend-dot legend-active" />当前楼层</span><span><i className="legend-dot legend-rest" />其他楼层</span><span className="model-scale">模型比例&nbsp; 1:250</span></div>
        </section>

        <aside className="detail-panel panel">
          <div className="panel-heading"><span>空间详情</span><span className="panel-index">ROOM / INFO</span></div>
          {selectedRoom ? (
            <div className="detail-populated" aria-live="polite">
              <div className="detail-room-id">{selectedRoom.number}<span>ROOM / {String(selectedRoom.floor).padStart(2, '0')}</span></div>
              <h2>{selectedRoom.name}</h2>
              <p className="detail-use">{selectedRoom.use}</p>
              <div className="detail-floor-tag"><span className="status-mark" />{FLOORS.find((floor) => floor.id === selectedRoom.floor)?.name}</div>
              <button className="clear-room-button" type="button" onClick={() => setSelectedRoomId(null)}>清除选择 <span aria-hidden="true">×</span></button>
            </div>
          ) : (
            <>
              <div className="detail-empty">
                <div className="room-glyph" aria-hidden="true"><span /><span /><span /><span /></div>
                <p>选择一个房间</p>
                <span>空间编号与用途<br />会显示在这里</span>
              </div>
              <div className="detail-hint"><span className="hint-arrow">↖</span><span>试着点选楼体中的<br />任意一个空间</span></div>
            </>
          )}
          <div className="detail-footer"><span>SPACE ID</span><span>{selectedRoom?.number ?? '— — —'}</span></div>
        </aside>
      </section>

      <footer className="page-footer"><span>SPATIAL INTERFACE STUDY <b>·</b> 2026</span><span>用空间理解校园 <i>✳</i></span></footer>
    </main>
  );
}
