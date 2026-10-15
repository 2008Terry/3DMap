---
type: research-source
created: '2026-10-15'
updated: '2026-10-15'
status: 文献研究，未本地复现
id: med-01
year: 1988
source_type: paper
evidence: abstract-primary
methods:
- direct volume rendering
- scalar opacity classification
- gradient shading
- alpha compositing
domains:
- medical imaging
- molecular graphics
source_url: https://graphics.stanford.edu/papers/volume-cga88/
accessed: '2026-10-15'
method_families:
- '01'
---

# Display of Surfaces from Volume Data

返回 [[3D结构透视研究/00 3D结构透视研究 Dashboard|研究 Dashboard]] · [[3D结构透视研究/03 来源索引|来源索引]]

[原始来源](https://graphics.stanford.edu/papers/volume-cga88/)

作者/机构：Marc Levoy; Stanford-hosted author archive / IEEE CG&A。年份：1988。证据层级：原始摘要或受限索引。

## 机制

直接对体素分类、着色并沿视线合成，不必先拟合三角网格。标量与边界检测决定部分不透明度，局部梯度作为表面法向。

## 能够显露的信息

可保留弱边界和部分体积特征，把多种组织及电子密度等标量场映射成同一幅二维图。

## 几何与坐标

原体数据坐标不重排；只改变体素的光学映射与图像合成。

## 代价

后方贡献仍被前方累积不透明度衰减；降低全部不透明度会混色，不能保证每个内部目标可辨认。

## 评价证据

原作者页面给出医学和分子图形示例、平滑轮廓与抗锯齿描述；此轮未读完整原文，未核实任务实验。

## 交互

基础机制允许更换视点、分类范围与透明度；具体现代交互界面并非此文证据。

## 实现与数据要求

体数据采样、梯度计算、前后顺序合成是核心。作者特别更正：插值时颜色应预乘透明度，避免边界渗色。

## 来源核对

已打开作者原始摘要及纠错页；它建立DVR机制，而不是证明全体积同时无歧义可见。

## 限制

需要已采集的三维标量数据；显示透明度不能发现扫描中没有的结构，也不能从外壳模型恢复内部。

## 方法与关联

[[3D结构透视研究/方法/01 透明、转移函数与OIT|透明、转移函数与OIT]]

- [[3D结构透视研究/来源/med-02 Multidimensional Transfer Functions for Interactive Volume Rendering|med-02 · Multidimensional Transfer Functions for Interactive Volume Rendering (2002)]]
- [[3D结构透视研究/来源/med-04 Illustrative Context-Preserving Volume Rendering|med-04 · Illustrative Context-Preserving Volume Rendering (2005)]]
- [[3D结构透视研究/来源/med-13 3D Slicer documentation- Volume rendering|med-13 · 3D Slicer documentation: Volume rendering (未核实年份)]]
