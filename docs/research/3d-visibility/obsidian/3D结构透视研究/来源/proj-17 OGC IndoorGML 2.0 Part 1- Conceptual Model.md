---
type: research-source
created: '2026-10-15'
updated: '2026-10-15'
status: 文献研究，未本地复现
id: proj-17
year: 2025
source_type: official-doc
evidence: official-doc
methods:
- indoor cellular space
- topological navigation model
- geometry/graph correspondence
domains:
- 室内空间
- 跨楼层导航
- 图与几何混合
source_url: https://www.ogc.org/announcement/ogc-publishes-indoorgml-2-0-part-1-conceptual-model-standard/
accessed: '2026-10-15'
method_families:
- '11'
---

# OGC IndoorGML 2.0 Part 1: Conceptual Model

返回 [[3D结构透视研究/00 3D结构透视研究 Dashboard|研究 Dashboard]] · [[3D结构透视研究/03 来源索引|来源索引]]

[原始来源](https://www.ogc.org/announcement/ogc-publishes-indoorgml-2-0-part-1-conceptual-model-standard/)

作者/机构：Open Geospatial Consortium。年份：2025。证据层级：官方文档。

## 机制

将室内可导航空间及其连接以标准概念模型表达，使房间、通道和连接能与几何关联。以此构建抽象连通图时，可显示全部房间节点而无需让所有三维墙面无遮挡。

## 能够显露的信息

适合完整检查有哪些空间、哪些门/楼梯/电梯连接它们，以及路线经过哪层；图不能单独揭示墙厚、局部形状和室内物品。

## 几何与坐标

源几何可以保留；图节点屏幕位置可以重新布局，保留的是明确编码的关系。标准本身并未规定无重叠可视布局。

## 代价

拓扑保连接不等于保距离、方向和几何布局；连通图中相交的边也不一定是实际空间交叉。

## 评价证据

2025-08-28官方发布IndoorGML2.0 Part1；这是互操作标准，不是证明某种平面布局易懂或全覆盖的实验。

## 交互

建议图节点与三维空间、楼层平面图双向联动；此为应用层推断，不当成标准提供的现成交互。

## 实现与数据要求

需要房间/门/楼梯等语义划分、可达性边、唯一ID和几何映射；具体XML/版本适配须阅读完整标准。

## 来源核对

已打开OGC官方标准页与2025年发布说明；完整22-045r5 HTML/PDF因24.8MB/16.3MB超出读取限制，故仅以官方概览核实范围，不宣称完成标准全文审阅。

## 限制

为导航而设计，不覆盖建筑的全部结构语义；仅可作为保持连通性的底层资料，不是自动拓扑保真的二维制图算法。

## 方法与关联

[[3D结构透视研究/方法/11 拓扑、语义与几何的混合表达|拓扑、语义与几何的混合表达]]

- [[3D结构透视研究/来源/proj-02 The Graph Camera (Purdue Technical Report 08-005)|proj-02 · The Graph Camera (Purdue Technical Report 08-005) (2008)]]
- [[3D结构透视研究/来源/proj-13 HippoMaps- Multiscale Cartography of Human Hippocampal Organization|proj-13 · HippoMaps: Multiscale Cartography of Human Hippocampal Organization (2025)]]
- [[3D结构透视研究/来源/proj-15 ParaView Documentation 6.2.0- Comparative Visualization|proj-15 · ParaView Documentation 6.2.0: Comparative Visualization (未核实年份)]]
