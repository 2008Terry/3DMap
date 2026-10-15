---
type: research-source
created: '2026-10-15'
updated: '2026-10-15'
status: 文献研究，未本地复现
id: cross-22
year: 2018
source_type: paper
evidence: abstract-primary
methods:
- semantic shading
- multiscale abstraction
domains:
- molecular visualization
- biology
source_url: https://www.cg.tuwien.ac.at/research/publications/2018/koch_bernhard_2018-1/
accessed: '2026-10-15'
method_families:
- '02'
- '11'
---

# Semantic Screen-Space Occlusion for Multiscale Molecular Visualization

返回 [[3D结构透视研究/00 3D结构透视研究 Dashboard|研究 Dashboard]] · [[3D结构透视研究/03 来源索引|来源索引]]

[原始来源](https://www.cg.tuwien.ac.at/research/publications/2018/koch_bernhard_2018-1/)

作者/机构：Thomas Bernhard Koch et al.。年份：2018。证据层级：原始摘要或受限索引。

## 机制

仅让选定语义层级产生遮蔽阴影，其余保持平坦，控制多尺度场景的着色杂乱。

## 能够显露的信息

突出组织层级与重要结构边界。

## 几何与坐标

几何原位，改变语义层级的光照表达。

## 代价

阴影是深度提示，不负责穿透外壳；着色过多本身会制造拥挤。

## 评价证据

作者摘要及生物场景示例；无本次核实的理解效果量。

## 交互

交互能力以原始资料为准；本条机制与适用条件见下。

## 实现与数据要求

层级语义数据、选择性屏幕空间着色。

## 来源核对

TU Wien原始页面，2018-09。

## 限制

阴影是深度提示，不负责穿透外壳；着色过多本身会制造拥挤。

## 方法与关联

[[3D结构透视研究/方法/02 隐藏线、轮廓与语义着色|隐藏线、轮廓与语义着色]] · [[3D结构透视研究/方法/11 拓扑、语义与几何的混合表达|拓扑、语义与几何的混合表达]]

- [[3D结构透视研究/来源/cross-21 Visibility Equalizer- Cutaway Visualization of Mesoscopic Biological|cross-21 · Visibility Equalizer: Cutaway Visualization of Mesoscopic Biological Models (2016)]]
- [[3D结构透视研究/来源/cross-06 Evaluation of depth perception in crowded volumes|cross-06 · Evaluation of depth perception in crowded volumes (2024)]]
