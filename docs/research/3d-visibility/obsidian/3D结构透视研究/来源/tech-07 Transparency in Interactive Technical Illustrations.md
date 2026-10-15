---
type: research-source
created: '2026-10-15'
updated: '2026-10-15'
status: 文献研究，未本地复现
id: tech-07
year: 2002
source_type: paper
evidence: abstract-primary
methods:
- view-dependent illustrative transparency
- image-space depth sorting
- non-photorealistic rendering
domains:
- technical illustration
- layered CAD
source_url: https://onlinelibrary.wiley.com/doi/abs/10.1111/1467-8659.t01-1-00591
accessed: '2026-10-15'
method_families:
- '01'
- '02'
---

# Transparency in Interactive Technical Illustrations

返回 [[3D结构透视研究/00 3D结构透视研究 Dashboard|研究 Dashboard]] · [[3D结构透视研究/03 来源索引|来源索引]]

[原始来源](https://onlinelibrary.wiley.com/doi/abs/10.1111/1467-8659.t01-1-00591)

作者/机构：Joachim Diepstraten, Daniel Weiskopf, Thomas Ertl。年份：2002。证据层级：原始摘要或受限索引。

## 机制

从传统手绘透明技术提炼规则，建立随视点变化的透明模型，并用硬件加速的图像空间深度排序将不透明和半透明对象组合。核心是有意设计透明的显示语法，而非每个对象给同一个alpha。

## 能够显露的信息

内部对象可与外部轮廓共同出现，外层仍提供位置及结构参照，并能结合其他非写实风格强调形状。

## 几何与坐标

不改变对象位置和模型几何，改变表面显示与合成。

## 代价

半透明仍会混合颜色、叠加轮廓并产生层次歧义；正确排序只是合成正确，不代表视觉理解必然正确。

## 评价证据

出版商摘要报告实时渲染和与其他NPR技术结合；未读取到受控用户实验、量化理解准确率或通用最佳透明度。

## 交互

面向交互视点下持续更新的技术插图；摘要未给出具体编辑控件清单。

## 实现与数据要求

需知道场景表面及深度顺序，不能从一张没有内部信息的图像恢复隐藏几何。

## 来源核对

已打开Wiley原始出版页。年份按2002期刊卷期，页面同时列2003上线时间，不能以抓取时间代替年份。

## 限制

仅核对摘要，不为特定边界透明规则或适用层数作超出来源的断言。

## 方法与关联

[[3D结构透视研究/方法/01 透明、转移函数与OIT|透明、转移函数与OIT]] · [[3D结构透视研究/方法/02 隐藏线、轮廓与语义着色|隐藏线、轮廓与语义着色]]

- [[3D结构透视研究/来源/tech-08 Real-time External Labeling of Ghosted Views|tech-08 · Real-time External Labeling of Ghosted Views (2019)]]
- [[3D结构透视研究/来源/tech-13 Interactive Cutaway Illustrations|tech-13 · Interactive Cutaway Illustrations (2003)]]
- [[3D结构透视研究/来源/tech-15 Onshape Help- Isolate|tech-15 · Onshape Help: Isolate (2026)]]
