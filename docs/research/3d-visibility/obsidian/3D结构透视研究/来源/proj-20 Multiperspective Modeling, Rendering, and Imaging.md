---
type: research-source
created: '2026-10-15'
updated: '2026-10-15'
status: 文献研究，未本地复现
id: proj-20
year: 2008
source_type: survey
evidence: abstract-primary
methods:
- multiperspective ray geometry survey
- camera classification
- distortion analysis
domains:
- 计算机图形学
- 计算机视觉
- 艺术投影
source_url: https://diglib.eg.org/items/3a46658f-7a6c-4d2d-9606-7d03601dc099
accessed: '2026-10-15'
method_families:
- '07'
---

# Multiperspective Modeling, Rendering, and Imaging

返回 [[3D结构透视研究/00 3D结构透视研究 Dashboard|研究 Dashboard]] · [[3D结构透视研究/03 来源索引|来源索引]]

[原始来源](https://diglib.eg.org/items/3a46658f-7a6c-4d2d-9606-7d03601dc099)

作者/机构：Jingyi Yu; Leonard McMillan; Peter Sturm。年份：2008。证据层级：原始摘要或受限索引。

## 机制

综述如何把不同视点采样汇为一个图像，联系艺术多透视、通用射线相机、图像生成与重建，强调设计相机映射而不必固守针孔模型。

## 能够显露的信息

有助于寻找广角、沿路径展开、反射/折射与多透视构图方案；这类相机能合并不共视的局部特征，但需要实际可获得的射线。

## 几何与坐标

一般不改变源几何，而改变射线组织与图像参数化；具体方法也可能组合空间变形。

## 代价

不同相机的投影、校准、采样和变形性质不同；无缝、保角、保尺度、完整覆盖不能默认同时满足。

## 评价证据

Eurographics2008 State-of-the-Art Report，属于文献综合。作者2010课程页也明确列出2008报告及后续期刊版本，避免将教程年份套到报告。

## 交互

艺术/设计者可控制图像构成，自动构图与可理解交互并非所有方法都有。

## 实现与数据要求

需按选定模型实现射线生成、采样或前向投影，并确保选择/测量能回到原三维。综述不提供一个通吃的渲染器。

## 来源核对

已打开Eurographics官方条目并核对标题、三位作者及下载入口；报告年份由作者官方CVPR2010课程的相关出版列表交叉确认。本文未读完报告PDF。

## 限制

保守记录为官方摘要/条目证据，不将综述中的单个方法效果作为已经全文核实的结论；更具体结论由本清单原论文支撑。

## 方法与关联

[[3D结构透视研究/方法/07 广义相机、多透视与投影变化|广义相机、多透视与投影变化]]

- [[3D结构透视研究/来源/proj-01 General Linear Cameras|proj-01 · General Linear Cameras (2004)]]
- [[3D结构透视研究/来源/proj-03 Interactive Design of Multi-Perspective Images for Visualizing Urban|proj-03 · Interactive Design of Multi-Perspective Images for Visualizing Urban Landscapes (2004)]]
- [[3D结构透视研究/来源/proj-05 Single Camera Flexible Projection|proj-05 · Single Camera Flexible Projection (2007)]]
- [[3D结构透视研究/来源/proj-06 An Evaluation of 3-D Scene Exploration Using a Multiperspective Imag|proj-06 · An Evaluation of 3-D Scene Exploration Using a Multiperspective Image Framework (2011)]]
