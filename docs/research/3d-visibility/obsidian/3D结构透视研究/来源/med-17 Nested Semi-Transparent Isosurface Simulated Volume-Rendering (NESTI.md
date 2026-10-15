---
type: research-source
created: '2026-10-15'
updated: '2026-10-15'
status: 文献研究，未本地复现
id: med-17
year: 2024
source_type: paper
evidence: abstract-primary
methods:
- nested semitransparent isosurfaces
- interactive rendering parameters
- 2D versus stereoscopic display
domains:
- kidney donor MRA
- vascular surgical planning
source_url: https://pubmed.ncbi.nlm.nih.gov/39405728/
accessed: '2026-10-15'
method_families:
- '01'
- '13'
- '14'
---

# Nested Semi-Transparent Isosurface Simulated Volume-Rendering (NESTIS-VR) - An efficient on-device rendering approach for Augmented Reality headsets increasing surgeon confidence of kidney donor arterial anatomy

返回 [[3D结构透视研究/00 3D结构透视研究 Dashboard|研究 Dashboard]] · [[3D结构透视研究/03 来源索引|来源索引]]

[原始来源](https://pubmed.ncbi.nlm.nih.gov/39405728/)

作者/机构：Fabian N. Necker; Marc L. Melcher; Stephan Busque; Christoph W. Leuze; Pejman Ghanouni; Chris Le Castillo; Elizabeth Nguyen; Bruce L. Daniel。年份：2024。证据层级：原始摘要或受限索引。

## 机制

用多个嵌套半透明等值面模拟体渲染，减少设备端实时ray casting开销；允许用户调整基本渲染参数。

## 能够显露的信息

帮助检查肾蒂动脉及分支；通过交互阈值/外观探索，让预计算固定参数图像未强调的结构出现。

## 几何与坐标

保留等值面原位，改变标量到嵌套表面的表示；未进行分支布局重排。

## 代价

离散等值面是体数据的近似，透明层仍可重叠；新颖显示设备与交互参数两个因素不能混为同一效果。

## 评价证据

已打开PubMed摘要：2位移植外科医生、20位潜在供体，测信心。2D交互NESTIS也优于预计算2D体渲染；双眼3D相对2D没有显著差异。

## 交互

设备端实时调渲染参数和观察方向；主要获益被作者归因于交互参数控制。

## 实现与数据要求

面向HoloLens计算限制的多层表面替代方案；本轮未取得全文算法和源代码。

## 来源核对

正式卷期为2024年12月，2024-10-12在线；证据支持信心提高，不能改写成诊断正确率或3D显示必然更好。

## 限制

仅2名专家且比较项包含交互与静态差异；属于AR研究，但其2D对照直接与普通屏幕有关。

## 方法与关联

[[3D结构透视研究/方法/01 透明、转移函数与OIT|透明、转移函数与OIT]] · [[3D结构透视研究/方法/13 感知、评价与失败模式|感知、评价与失败模式]] · [[3D结构透视研究/方法/14 双目、双眼差异与光场硬件|双目、双眼差异与光场硬件]]

- [[3D结构透视研究/来源/med-02 Multidimensional Transfer Functions for Interactive Volume Rendering|med-02 · Multidimensional Transfer Functions for Interactive Volume Rendering (2002)]]
- [[3D结构透视研究/来源/med-13 3D Slicer documentation- Volume rendering|med-13 · 3D Slicer documentation: Volume rendering (未核实年份)]]
- [[3D结构透视研究/来源/med-16 ClipGS- Clippable Gaussian Splatting for Interactive Cinematic Visua|med-16 · ClipGS: Clippable Gaussian Splatting for Interactive Cinematic Visualization of Volumetric Medical Data (2025)]]
