---
type: research-source
created: '2026-10-15'
updated: '2026-10-15'
status: 文献研究，未本地复现
id: tech-09
year: 2012
source_type: paper
evidence: abstract-primary
methods:
- oblique cutaway
- simple box-shaped cuts
- context alignment
- shadow and contour depth cues
- decoupled camera/cut
domains:
- geology
- layered polygonal models
source_url: https://vis.test.uib.no/publications/Lidal12Design/
accessed: '2026-10-15'
method_families:
- '03'
---

# Design Principles for Cutaway Visualization of Geological Models

返回 [[3D结构透视研究/00 3D结构透视研究 Dashboard|研究 Dashboard]] · [[3D结构透视研究/03 来源索引|来源索引]]

[原始来源](https://vis.test.uib.no/publications/Lidal12Design/)

作者/机构：Endre M. Lidal, Helwig Hauser, Ivan Viola。年份：2012。证据层级：原始摘要或受限索引。

## 机制

提出五项设计原则：切口轴与视向留角度、使用简单盒形切口、与熟悉的上下文结构对齐、以阴影和轮廓强调内部层次、放松视点依赖以保留运动视差。

## 能够显露的信息

让内部通道所属地层、与切壁的距离、形状和空间顺序更可读，避免切口正对相机时整个内部像贴在表面。

## 几何与坐标

目标坐标保留，遮挡物局部省略；保留固定切壁作为深度参照。

## 代价

相机与切口不再完全绑定后，旋转到某些角度目标会再次被遮挡；简单切口还可能移除更多无关材料。

## 评价证据

依据地质插图、原型开发、与专业插画师和领域专家讨论形成原则；已打开摘要没有受试者对照实验指标。

## 交互

旋转查看时允许相机独立于切口，小角度运动产生可比较视差。

## 实现与数据要求

原则可迁移到分层对象，但地质常是层饼结构而非解剖学的同心壳层，不能直接套用所有既有切口。

## 来源核对

已打开Bergen作者研究组页面，完整摘要列出五原则；正式年份2012。

## 限制

作者PDF打开失败；建议的知觉依据不等于本论文已证明所有结构理解任务收益。

## 方法与关联

[[3D结构透视研究/方法/03 平面、目标驱动与非平面剖切|平面、目标驱动与非平面剖切]]

- [[3D结构透视研究/来源/tech-01 Interactive Cutaway Illustrations of Complex 3D Models|tech-01 · Interactive Cutaway Illustrations of Complex 3D Models (2007)]]
- [[3D结构透视研究/来源/tech-06 Adaptive Cutaways for Comprehensible Rendering of Polygonal Scenes|tech-06 · Adaptive Cutaways for Comprehensible Rendering of Polygonal Scenes (2008)]]
- [[3D结构透视研究/来源/tech-14 Onshape Help- Section View|tech-14 · Onshape Help: Section View (2026)]]
- [[3D结构透视研究/来源/tech-18 Rhino 8 Help- ClippingPlane and related section commands|tech-18 · Rhino 8 Help: ClippingPlane and related section commands (未核实年份)]]
