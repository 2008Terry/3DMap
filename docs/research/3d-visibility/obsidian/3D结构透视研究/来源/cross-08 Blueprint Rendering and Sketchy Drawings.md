---
type: research-source
created: '2026-10-15'
updated: '2026-10-15'
status: 文献研究，未本地复现
id: cross-08
year: 2005
source_type: official-doc
evidence: official-doc
methods:
- blueprint
- hidden lines
- depth peeling
domains:
- technical illustration
- architecture
source_url: https://developer.nvidia.com/gpugems/gpugems2/part-ii-shading-lighting-and-shadows/chapter-15-blueprint-rendering-and-sketchy
accessed: '2026-10-15'
method_families:
- '02'
---

# Blueprint Rendering and Sketchy Drawings

返回 [[3D结构透视研究/00 3D结构透视研究 Dashboard|研究 Dashboard]] · [[3D结构透视研究/03 来源索引|来源索引]]

[原始来源](https://developer.nvidia.com/gpugems/gpugems2/part-ii-shading-lighting-and-shadows/chapter-15-blueprint-rendering-and-sketchy)

作者/机构：Marc Nienhaus; Jürgen Döllner。年份：2005。证据层级：官方文档。

## 机制

深度剥离提取多层表面，检测深度与法线间断，把可见和隐藏的特征线合成蓝图。

## 能够显露的信息

内外结构边界可同时出现在原位。

## 几何与坐标

保留坐标，删减面填充、强调边。

## 代价

大量隐藏线仍会拥挤、交叉和失去层序；多层提取增加成本。

## 评价证据

官方技术章节与示例，不是建筑理解用户实验。

## 交互

交互能力以原始资料为准；本条机制与适用条件见下。

## 实现与数据要求

多层深度/法线、轮廓提取、线条分级。

## 来源核对

已读NVIDIA原始章节。

## 限制

大量隐藏线仍会拥挤、交叉和失去层序；多层提取增加成本。

## 方法与关联

[[3D结构透视研究/方法/02 隐藏线、轮廓与语义着色|隐藏线、轮廓与语义着色]]

- [[3D结构透视研究/来源/cross-09 Exploring and Expanding the Continuum of OIT Algorithms|cross-09 · Exploring and Expanding the Continuum of OIT Algorithms (2016)]]
