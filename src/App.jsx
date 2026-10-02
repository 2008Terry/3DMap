import React, { useState } from 'react';
import CampusScene from './CampusScene.jsx';
import { BUILDINGS, CAMPUS_CONTEXT, MAP_CENTER } from './campusData.js';

export default function App() {
  const [selectedBuildingId, setSelectedBuildingId] = useState(null);
  const [resetCameraKey, setResetCameraKey] = useState(0);
  const selectedBuilding = BUILDINGS.find((building) => building.id === selectedBuildingId);
  const clearSelection = () => setSelectedBuildingId(null);

  return (
    <main className="app-shell" id="top">
      <header className="topbar">
        <a className="brand" href="#top" aria-label="空间档案首页">
          <span className="brand-mark" aria-hidden="true"><i /><i /><i /></span>
          <span>空间档案<span className="brand-en"> / CAMPUS SPACES</span></span>
        </a>
        <div className="topbar-meta"><span className="live-dot" />校园导览原型 <span className="meta-divider">/</span> 08 栋</div>
      </header>

      <section className="intro" aria-labelledby="page-title">
        <div>
          <p className="eyebrow"><span>美国 · 密歇根大学</span><span className="eyebrow-line" /><span>CENTRAL CAMPUS</span></p>
          <h1 id="page-title">对角广场与中央校区<span>The Diag · University of Michigan</span></h1>
        </div>
        <p className="intro-note">沿着 Diag 探索周边建筑。<br />拖动地图，点选建筑查看概况。</p>
      </section>

      <p className="map-caveat" role="note"><span className="caveat-mark" aria-hidden="true">!</span><span><strong>示意地图 · 仅供方位参考</strong> 建筑中心坐标取自 OpenStreetMap 衍生数据；建筑轮廓、高度、楼层数及周边道路和步道形状均为示意估算，不是取自 OSM 的建筑多边形。请勿用于测绘或正式导航。</span></p>

      <section className="workspace" aria-label="Diag 校园建筑探索器">
        <aside className="building-panel panel" aria-label="建筑列表">
          <div className="panel-heading"><span>建筑索引</span><span className="panel-index">BUILDINGS / {String(BUILDINGS.length).padStart(2, '0')}</span></div>
          <p className="panel-subtitle">选择一栋建筑查看示意位置与资料</p>
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
          <div className="panel-footer"><span className="status-mark" />{BUILDINGS.length} 个建筑中心点 <span>·</span> 示意模型</div>
        </aside>

        <section className="model-panel" aria-label="可交互中央校区示意地图">
          <div className="model-toolbar">
            <div className="view-label"><span className="view-dot" />Diag 鸟瞰 <span className="view-coordinate">{MAP_CENTER.lat.toFixed(4)}° N&nbsp; {Math.abs(MAP_CENTER.lon).toFixed(4)}° W</span></div>
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
            />
            <div className="scene-caption"><span className="caption-rule" />拖动旋转 <span>·</span> 滚轮缩放 <span>·</span> 点击建筑查看</div>
          </div>
          <div className="model-legend"><span><i className="legend-dot legend-active" />已选建筑</span><span><i className="legend-dot legend-rest" />其他建筑</span><span className="model-scale">约 800 米核心区域 · 非比例测绘</span></div>
        </section>

        <aside className="detail-panel panel" aria-label="建筑详情">
          <div className="panel-heading"><span>建筑详情</span><span className="panel-index">BUILDING / INFO</span></div>
          {selectedBuilding ? (
            <div className="detail-populated" aria-live="polite">
              <span className="detail-kicker">SELECTED BUILDING</span>
              <h2>{selectedBuilding.name}</h2>
              <p className="detail-use">{selectedBuilding.description}</p>
              <dl className="detail-facts">
                <div><dt>类别 / 用途</dt><dd>{selectedBuilding.category} <small>名称及用途概述</small></dd></div>
                <div><dt>建筑中心</dt><dd>{selectedBuilding.center.lat.toFixed(5)}° N<br />{Math.abs(selectedBuilding.center.lon).toFixed(5)}° W <small>OSM 衍生坐标</small></dd></div>
                <div><dt>楼层数</dt><dd>{selectedBuilding.levels} 层 <small>{selectedBuilding.heightIsEstimate ? '示意估算' : '来源记录'}</small></dd></div>
                <div><dt>高度</dt><dd>约 {selectedBuilding.heightMeters} 米 <small>{selectedBuilding.heightIsEstimate ? '示意估算' : '来源记录'}</small></dd></div>
                <div><dt>建筑轮廓</dt><dd>{selectedBuilding.footprintIsEstimate ? '示意估算' : '来源记录'}</dd></div>
              </dl>
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
        <span>© OpenStreetMap contributors · <a href="https://www.openstreetmap.org/copyright" target="_blank" rel="noreferrer">ODbL</a> <span className="footer-separator">/</span> <a href="https://github.com/BereZone/umichfreepark" target="_blank" rel="noreferrer">UMichFreePark (MIT)</a> 建筑中心数据</span>
      </footer>
    </main>
  );
}
