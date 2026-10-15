---
type: research-source
created: '2026-10-15'
updated: '2026-10-15'
status: 文献研究，未本地复现
id: med-12
year: 2005
source_type: paper
evidence: abstract-primary
methods:
- volumetric lens
- convex 3D focus region
- local rendering style
- non-photorealistic rendering
domains:
- medical volume exploration
source_url: https://viscom.uni-ulm.de/publications/interactive-importance-driven-visualization-techniques-for-medical-volume-data/
accessed: '2026-10-15'
method_families:
- '04'
- '12'
---

# Interactive Importance-Driven Visualization Techniques for Medical Volume Data

返回 [[3D结构透视研究/00 3D结构透视研究 Dashboard|研究 Dashboard]] · [[3D结构透视研究/03 来源索引|来源索引]]

[原始来源](https://viscom.uni-ulm.de/publications/interactive-importance-driven-visualization-techniques-for-medical-volume-data/)

作者/机构：Timo Ropinski; Frank Steinicke; Klaus Hinrichs。年份：2005。证据层级：原始摘要或受限索引。

## 机制

用凸三维形状定义焦点区域，区域与体数据相交的部分采用不同视觉外观，在同一数据上局部启用非真实感显示。

## 能够显露的信息

让局部目标从其余体数据中突出，背景仍给出定位；适合比较同一位置在不同渲染规则下的内部特征。

## 几何与坐标

摘要描述为局部外观变化，而非空间重排；几何默认原位保留，具体透镜种类需查原文。

## 代价

改变镜内风格只改善局部表达，镜外遮挡仍可能挡住镜内目标；必须决定背景是否透明、裁切或另画。

## 评价证据

已打开作者大学页面，摘要说明给出实现和性能结果；未取得全文，不能补写用户数量或诊断收益。

## 交互

交互定义/移动凸焦点体，并在探索过程中改变局部显示规则。

## 实现与数据要求

以三维区域相交判定驱动样本着色；需处理区域边界、焦点与上下文合成。

## 来源核对

已核实2005年、作者、凸3D焦点及局部非真实感渲染；没有把泛称透镜误当作所有透镜都能穿透遮挡。

## 限制

本轮证据仅作者摘要；具体控制方式和各类透镜是否需要分割尚未核实。

## 方法与关联

[[3D结构透视研究/方法/04 局部X-ray与体数据透镜|局部X-ray与体数据透镜]] · [[3D结构透视研究/方法/12 可见性度量与自动显露优化|可见性度量与自动显露优化]]

- [[3D结构透视研究/来源/med-05 ClearView- An Interactive Context Preserving Hotspot Visualization T|med-05 · ClearView: An Interactive Context Preserving Hotspot Visualization Technique (2006)]]
- [[3D结构透视研究/来源/med-06 VolumeShop- An Interactive System for Direct Volume Illustration|med-06 · VolumeShop: An Interactive System for Direct Volume Illustration (2005)]]
- [[3D结构透视研究/来源/med-11 Interactive Obstruction-Free Lensing for Volumetric Data Visualizati|med-11 · Interactive Obstruction-Free Lensing for Volumetric Data Visualization (2019)]]
