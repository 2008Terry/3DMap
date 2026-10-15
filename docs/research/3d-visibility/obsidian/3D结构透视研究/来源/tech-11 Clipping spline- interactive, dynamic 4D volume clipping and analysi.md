---
type: research-source
created: '2026-10-15'
updated: '2026-10-15'
status: 文献研究，未本地复现
id: tech-11
year: 2025
source_type: paper
evidence: full-primary
methods:
- non-planar clipping
- thin plate spline
- binary volume mask
- time-varying clipping
- keyframe interpolation
domains:
- biomedical volume imaging
- OCT
- general volumetric data
source_url: https://pmc.ncbi.nlm.nih.gov/articles/PMC11828437/
accessed: '2026-10-15'
method_families:
- '03'
---

# Clipping spline: interactive, dynamic 4D volume clipping and analysis based on thin plate spline

返回 [[3D结构透视研究/00 3D结构透视研究 Dashboard|研究 Dashboard]] · [[3D结构透视研究/03 来源索引|来源索引]]

[原始来源](https://pmc.ncbi.nlm.nih.gov/articles/PMC11828437/)

作者/机构：Andre C. Faubert, Shang Wang。年份：2025。证据层级：全文级原始资料。

## 机制

用至少3个控制点定义曲率尽可能小的薄板样条曲面，再按曲面生成二值体掩膜决定保留哪些体素。可移动、增删点，并连接不同时间的控制点组产生平滑动态切口。

## 能够显露的信息

一幅图中可揭示传统平面难以完整露出的弯曲心管、输卵管等结构；还能观察心跳与发育两个时间尺度。

## 几何与坐标

原始体素位置保持，修改的是显示掩膜；4D在此明确指3D加时间，不能解释成第四个空间维。

## 代价

仍然删除一侧体素；单个坐标轴上的高度函数不能代表任意折叠或回绕切面，控制点外的外推也需检查。

## 评价证据

论文给出计算管线性能与胚胎小鼠OCT示例，非用户理解对照试验；掩膜创建和CPU/GPU传输是主要成本，粗网格上采样是性能折中。

## 交互

实时控制点编辑、局部精细化、可复现参数和自动时间过渡/flythrough。

## 实现与数据要求

作者开源实现位于OpenChronoMorphViewer；适用于已有体数据，不会从普通照片生成内部。

## 来源核对

直接打开PMC遇验证码，但已读取该原始全文的索引返回摘要、方法2.1、讨论4.1和结论；作者GitHub另已打开核对。

## 限制

源数据不是公开下载，需联系作者；本文能力展示不能等同所有成像模态均有验证。

## 方法与关联

[[3D结构透视研究/方法/03 平面、目标驱动与非平面剖切|平面、目标驱动与非平面剖切]]

- [[3D结构透视研究/来源/tech-05 Using Deformations for Browsing Volumetric Data|tech-05 · Using Deformations for Browsing Volumetric Data (2003)]]
- [[3D结构透视研究/来源/tech-14 Onshape Help- Section View|tech-14 · Onshape Help: Section View (2026)]]
- [[3D结构透视研究/来源/tech-17 Autodesk Fusion Help- Create a 3D section view|tech-17 · Autodesk Fusion Help: Create a 3D section view (未核实年份)]]
