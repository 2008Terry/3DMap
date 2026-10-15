---
type: research-source
created: '2026-10-15'
updated: '2026-10-15'
status: 文献研究，未本地复现
id: tech-06
year: 2008
source_type: paper
evidence: abstract-primary
methods:
- view-dependent adaptive cutaway
- image-space cutaway surface
- NPR context cues
domains:
- architecture
- path planning
- games
- polygonal scenes
source_url: https://collaborate.princeton.edu/en/publications/adaptive-cutaways-for-comprehensible-rendering-of-polygonal-scene/
accessed: '2026-10-15'
method_families:
- '03'
- '12'
---

# Adaptive Cutaways for Comprehensible Rendering of Polygonal Scenes

返回 [[3D结构透视研究/00 3D结构透视研究 Dashboard|研究 Dashboard]] · [[3D结构透视研究/03 来源索引|来源索引]]

[原始来源](https://collaborate.princeton.edu/en/publications/adaptive-cutaways-for-comprehensible-rendering-of-polygonal-scene/)

作者/机构：Michael Burns, Adam Finkelstein。年份：2008。证据层级：原始摘要或受限索引。

## 机制

根据目标在当前相机中的深度投影生成切口，视点和目标移动时持续更新。作者PDF索引说明采用jump flooding生成深度图表示的切口面，再修改多边形渲染管线去除遮挡并表现新切面。

## 能够显露的信息

建筑内部家具、角色或船体内部等目标保持原位可见，余下墙面和风格化线索交代它们位于何处。

## 几何与坐标

在渲染阶段省略遮挡片段，目标不移动；不是必须永久修改场景网格。

## 代价

动态切口可能削弱固定空间参照；可见目标并不自动产生准确深度感，切掉的上下文仍有信息损失。

## 评价证据

主来源摘要确认交互帧率和建筑、路径及游戏应用；未从已打开摘要取得受试人数或控制实验结果。

## 交互

旋转、缩放、目标变化触发切口自适应，适合相机与内容均动态的场景。

## 实现与数据要求

需要目标/次要对象区分和深度缓冲；多边形切面表现是不同于体绘制的关键工程问题。

## 来源核对

已打开Princeton机构论文页；算法细节核对其作者PDF返回的引言全文段落，直接PDF打开失败。

## 限制

不把摘要中的'comprehensible'当成已量化的人类理解收益；详细硬件性能与模型假设尚需全文复核。

## 方法与关联

[[3D结构透视研究/方法/03 平面、目标驱动与非平面剖切|平面、目标驱动与非平面剖切]] · [[3D结构透视研究/方法/12 可见性度量与自动显露优化|可见性度量与自动显露优化]]

- [[3D结构透视研究/来源/tech-01 Interactive Cutaway Illustrations of Complex 3D Models|tech-01 · Interactive Cutaway Illustrations of Complex 3D Models (2007)]]
- [[3D结构透视研究/来源/tech-09 Design Principles for Cutaway Visualization of Geological Models|tech-09 · Design Principles for Cutaway Visualization of Geological Models (2012)]]
