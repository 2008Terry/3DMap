---
type: research-source
created: '2026-10-15'
updated: '2026-10-15'
status: 文献研究，未本地复现
id: med-05
year: 2006
source_type: paper
evidence: full-primary
methods:
- distortion-free hotspot
- layered ray casting
- curvature-preserving ghosting
- focus and context
domains:
- medical visualization
- technical volumes
source_url: https://www.cs.cit.tum.de/cg/research/publications/2006/clearview-an-interactive-context-preserving-hotspot-visualization-technique/
accessed: '2026-10-15'
method_families:
- '04'
---

# ClearView: An Interactive Context Preserving Hotspot Visualization Technique

返回 [[3D结构透视研究/00 3D结构透视研究 Dashboard|研究 Dashboard]] · [[3D结构透视研究/03 来源索引|来源索引]]

[原始来源](https://www.cs.cit.tum.de/cg/research/publications/2006/clearview-an-interactive-context-preserving-hotspot-visualization-technique/)

作者/机构：Jens Krüger; Jens Schneider; Rüdiger Westermann。年份：2006。证据层级：全文级原始资料。

## 机制

先把焦点与上下文层渲染到位置、法向及曲率纹理，再合成。球形热点内让上下文衰减，同时保留曲率高的边缘；可按结构间距控制透明。

## 能够显露的信息

局部内层及其外层轮廓、相邻结构距离可同时显现，热点外保持整体概观；不需要预先生成额外特征体。

## 几何与坐标

热点为无畸变显示，保留体数据坐标；改变可见性与着色，不是把组织挤开。

## 代价

层的阈值和先后关系仍需指定。原文要求用户保证层顺序；不同层相交时，正确混合没有保证。

## 评价证据

已打开8页原文和作者页，核实方法、示例与性能讨论；作者页报告相关工具获2006可视化竞赛奖，不能等同受控医学效果证据。

## 交互

点选热点、调球半径与透明度、选择着色器；可随鼠标和视角交互探索。

## 实现与数据要求

GPU多通道ray casting、geometry image、屏幕空间曲率和延迟着色；可用曲率或距离重要度。

## 来源核对

ClearView不是一般透明材质，而是热点、层提取、特征重要度与合成的组合。

## 限制

主要解决局部焦点与背景协调；不能保证复杂相交层或所有分支都无遮挡。

## 方法与关联

[[3D结构透视研究/方法/04 局部X-ray与体数据透镜|局部X-ray与体数据透镜]]

- [[3D结构透视研究/来源/med-03 Importance-Driven Volume Rendering|med-03 · Importance-Driven Volume Rendering (2004)]]
- [[3D结构透视研究/来源/med-04 Illustrative Context-Preserving Volume Rendering|med-04 · Illustrative Context-Preserving Volume Rendering (2005)]]
- [[3D结构透视研究/来源/med-11 Interactive Obstruction-Free Lensing for Volumetric Data Visualizati|med-11 · Interactive Obstruction-Free Lensing for Volumetric Data Visualization (2019)]]
- [[3D结构透视研究/来源/med-12 Interactive Importance-Driven Visualization Techniques for Medical V|med-12 · Interactive Importance-Driven Visualization Techniques for Medical Volume Data (2005)]]
