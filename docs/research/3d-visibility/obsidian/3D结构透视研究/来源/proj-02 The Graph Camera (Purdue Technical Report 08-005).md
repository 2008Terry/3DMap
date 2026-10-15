---
type: research-source
created: '2026-10-15'
updated: '2026-10-15'
status: 文献研究，未本地复现
id: proj-02
year: 2008
source_type: paper
evidence: full-primary
methods:
- graph camera
- piecewise multiperspective
- frustum bending splitting merging
domains:
- 室内迷宫
- 场景总览
- 监控
source_url: https://www.cs.purdue.edu/cgvlab/www/resources/papers/Rosen-CS_Technical_reports-2008-The_graph_camera.pdf
accessed: '2026-10-15'
method_families:
- '07'
---

# The Graph Camera (Purdue Technical Report 08-005)

返回 [[3D结构透视研究/00 3D结构透视研究 Dashboard|研究 Dashboard]] · [[3D结构透视研究/03 来源索引|来源索引]]

[原始来源](https://www.cs.purdue.edu/cgvlab/www/resources/papers/Rosen-CS_Technical_reports-2008-The_graph_camera.pdf)

作者/机构：Paul Rosen; Voicu Popescu; Nicoletta Adamo-Villani。年份：2008。证据层级：全文级原始资料。

## 机制

把许多平面针孔相机组成图，通过弯折、分裂和合并视锥让视线绕过墙角，并将多个兴趣区域映入单层图像。迷宫版本利用几何与遍历路径递归构造相机。

## 能够显露的信息

可在一幅连续图中看到直视线后方的支路、转角与目标，适合显示走廊网络；与单纯把墙设透明相比，它把隐藏区域分配到不同屏幕区域。

## 几何与坐标

模型世界位置保留，但相机把普通投影重叠区域重新安置到不同屏幕位置，全球距离与方向不再直接可读。

## 代价

有环图若覆盖全部回边可能产生重复或图像不连续；远端分支会变小，屏幕分辨率限制实际可辨认的覆盖。

## 评价证据

技术报告展示虚拟场景、真实视频整合及交互渲染；后续2011年论文单独提供用户任务实验。

## 交互

支持动态场景和交互导航，构造参数可手工或按场景结构自动生成。

## 实现与数据要求

需房间/走廊门户或目标区域信息、相机图与分段投影；作者提出前向投影支持交互渲染。封闭物体内部没有可绕行射线时仍需另配裁切。

## 来源核对

已打开Purdue完整10页技术报告；其自动算法明确限定直角转弯迷宫，并把足够屏幕分辨率列为显示全部走廊的条件。另有2009年TOG正式版本，不能把该PDF封面年份写成2009。

## 限制

连续、无重复和完整覆盖不是对任意有环建筑同时成立的无条件性质；不等于显示每个房间内的所有表面。

## 方法与关联

[[3D结构透视研究/方法/07 广义相机、多透视与投影变化|广义相机、多透视与投影变化]]

- [[3D结构透视研究/来源/proj-01 General Linear Cameras|proj-01 · General Linear Cameras (2004)]]
- [[3D结构透视研究/来源/proj-06 An Evaluation of 3-D Scene Exploration Using a Multiperspective Imag|proj-06 · An Evaluation of 3-D Scene Exploration Using a Multiperspective Image Framework (2011)]]
- [[3D结构透视研究/来源/proj-17 OGC IndoorGML 2.0 Part 1- Conceptual Model|proj-17 · OGC IndoorGML 2.0 Part 1: Conceptual Model (2025)]]
