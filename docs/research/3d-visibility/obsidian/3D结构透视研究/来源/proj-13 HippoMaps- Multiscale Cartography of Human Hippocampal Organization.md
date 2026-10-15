---
type: research-source
created: '2026-10-15'
updated: '2026-10-15'
status: 文献研究，未本地复现
id: proj-13
year: 2025
source_type: paper
evidence: full-primary
methods:
- topology-informed unfolding
- intrinsic coordinates
- multimodal surface atlas
domains:
- 神经影像
- 褶皱薄层
- 多尺度数据图册
source_url: https://www.nature.com/articles/s41592-025-02783-3
accessed: '2026-10-15'
method_families:
- 08
- '11'
---

# HippoMaps: Multiscale Cartography of Human Hippocampal Organization

返回 [[3D结构透视研究/00 3D结构透视研究 Dashboard|研究 Dashboard]] · [[3D结构透视研究/03 来源索引|来源索引]]

[原始来源](https://www.nature.com/articles/s41592-025-02783-3)

作者/机构：Jordan DeKraker; Donna Gift Cabalo; Jessica Royer; Alexander Ngo; Ali R. Khan; Boris C. Bernhardt; and collaborators。年份：2025。证据层级：全文级原始资料。

## 机制

依赖统一海马分割、已知拓扑及形状内在配准，建立统一展开坐标，将不同受试者和模态的表面属性映射到可比较图册。

## 能够显露的信息

把紧密卷曲、普通稀疏切片难以理解的海马层结构与组织学、MRI、功能和电生理属性并列展示；显露的是具有已知薄层拓扑的亚区组织。

## 几何与坐标

提供折叠和展开两种空间；新坐标保存有意义的内在邻接与轴向顺序，但不保原空间距离。

## 代价

图册需要强领域先验，展开位置不等于原解剖位置；跨人群配准与属性聚合会隐藏个体差异及深度细节。

## 评价证据

Nature Methods 22,2211–2222，2025-10-01；提供30幅整理后的组平均图，含离体组织学、9.4T MRI、3T/7T MRI与颅内记录，开放代码数据。

## 交互

工具箱和在线数据仓库支持统一空间查阅与比较；建筑类比应采用点击房间/墙面回到三维的联动。

## 实现与数据要求

需稳定分割、拓扑先验、原空间到内在坐标的映射、标准化网格和数据属性投影。

## 来源核对

已打开Nature完整官方正文，明确发表于2025-10-01；同一页面推荐的2026论文不是本论文日期。本文依赖HippUnfold等先前分割技术。

## 限制

作为建筑平面化灵感有价值，但海马的片状拓扑与房间/楼层网络不同；不证明任意建筑可用同样方法铺平。

## 方法与关联

[[3D结构透视研究/方法/08 曲面重采样、解缠与表面展开|曲面重采样、解缠与表面展开]] · [[3D结构透视研究/方法/11 拓扑、语义与几何的混合表达|拓扑、语义与几何的混合表达]]

- [[3D结构透视研究/来源/proj-10 Nondistorting Flattening Maps and the 3-D Visualization of Colon CT|proj-10 · Nondistorting Flattening Maps and the 3-D Visualization of Colon CT Images (2000)]]
- [[3D结构透视研究/来源/proj-12 Unlocking History through Automated Virtual Unfolding of Sealed Docu|proj-12 · Unlocking History through Automated Virtual Unfolding of Sealed Documents Imaged by X-ray Microtomography (2021)]]
- [[3D结构透视研究/来源/proj-17 OGC IndoorGML 2.0 Part 1- Conceptual Model|proj-17 · OGC IndoorGML 2.0 Part 1: Conceptual Model (2025)]]
- [[3D结构透视研究/来源/proj-09 Occlusion-Free Conformal Lensing for Spatiotemporal Visualization in|proj-09 · Occlusion-Free Conformal Lensing for Spatiotemporal Visualization in 3D Urban Analytics (2026)]]
