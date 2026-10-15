---
type: research-source
created: '2026-10-15'
updated: '2026-10-15'
status: 文献研究，未本地复现
id: proj-03
year: 2004
source_type: paper
evidence: full-primary
methods:
- cross-slits camera
- serial blending
- interactive picture surface
domains:
- 街景
- 城市街区
- 长场景总览
source_url: https://graphics.stanford.edu/papers/multi-cross-slits/interactive-multi-X-slits.pdf
accessed: '2026-10-15'
method_families:
- '07'
---

# Interactive Design of Multi-Perspective Images for Visualizing Urban Landscapes

返回 [[3D结构透视研究/00 3D结构透视研究 Dashboard|研究 Dashboard]] · [[3D结构透视研究/03 来源索引|来源索引]]

[原始来源](https://graphics.stanford.edu/papers/multi-cross-slits/interactive-multi-X-slits.pdf)

作者/机构：Augusto Román; Gaurav Garg; Marc Levoy。年份：2004。证据层级：全文级原始资料。

## 机制

从侧向移动视频建立多个双狭缝相机；用户指定第二狭缝及画面曲面，系统插入相机使相邻边界射线一致，从而无缝连接局部透视。

## 能够显露的信息

同图汇总弯曲街道、路口、巷道和深广场，保留沿街连续感；可以避免普通推扫全景把巷道扩张得难以辨认。

## 几何与坐标

原三维空间或拍摄对象不移动，输出图像的横纵透视关系和尺度经过设计。

## 代价

消除接缝不等于消除透视失真；需要人工设计，主要针对大致平面、沿线展开的场景，有限输入视线看不到的室内不能凭此恢复。

## 评价证据

以真实城市街区图像示例验证交互构图和失真控制，未报告通用室内用户研究。

## 交互

调整狭缝位置、区间和画面曲面，直观改变不同区域的透视。

## 实现与数据要求

需有位姿的侧向图像序列、双狭缝采样与插值、画面参数化；若改用于几何模型可按所定义射线渲染。

## 来源核对

已打开Stanford作者项目页及8页PDF；页面给出IEEE Visualization 2004，并明确展示推扫和人工设计结果的巷道与树木失真差别。

## 限制

城市外部条带图像方法，不是建筑体积展开；不能从外观视频生成未观测内部。

## 方法与关联

[[3D结构透视研究/方法/07 广义相机、多透视与投影变化|广义相机、多透视与投影变化]]

- [[3D结构透视研究/来源/proj-04 Automatic Multiperspective Images|proj-04 · Automatic Multiperspective Images (2006)]]
- [[3D结构透视研究/来源/proj-01 General Linear Cameras|proj-01 · General Linear Cameras (2004)]]
- [[3D结构透视研究/来源/proj-20 Multiperspective Modeling, Rendering, and Imaging|proj-20 · Multiperspective Modeling, Rendering, and Imaging (2008)]]
