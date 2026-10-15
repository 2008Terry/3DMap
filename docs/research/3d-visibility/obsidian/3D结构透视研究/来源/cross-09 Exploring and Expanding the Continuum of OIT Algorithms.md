---
type: research-source
created: '2026-10-15'
updated: '2026-10-15'
status: 文献研究，未本地复现
id: cross-09
year: 2016
source_type: paper
evidence: full-primary
methods:
- OIT
- fragment storage
- transparency algorithms
domains:
- rendering
source_url: https://research.nvidia.com/sites/default/files/pubs/2016-06_Exploring-and-Expanding/hpg16_oitContinuum.pdf
accessed: '2026-10-15'
method_families:
- '01'
---

# Exploring and Expanding the Continuum of OIT Algorithms

返回 [[3D结构透视研究/00 3D结构透视研究 Dashboard|研究 Dashboard]] · [[3D结构透视研究/03 来源索引|来源索引]]

[原始来源](https://research.nvidia.com/sites/default/files/pubs/2016-06_Exploring-and-Expanding/hpg16_oitContinuum.pdf)

作者/机构：Chris Wyman。年份：2016。证据层级：全文级原始资料。

## 机制

把片元保存、排序、压缩和合成看作连续设计空间，比较精确与近似透明算法。

## 能够显露的信息

避免物体绘制顺序造成的透明错误。

## 几何与坐标

不改变几何。

## 代价

正确合成不等于每层可读；存储、带宽、通道数、近似误差仍需取舍。

## 评价证据

算法与性能比较，未评价复杂内部结构的理解。

## 交互

交互能力以原始资料为准；本条机制与适用条件见下。

## 实现与数据要求

按场景深度复杂度和显存选择方案；不是靠更低alpha解决排序。

## 来源核对

已读作者11页全文。

## 限制

正确合成不等于每层可读；存储、带宽、通道数、近似误差仍需取舍。

## 方法与关联

[[3D结构透视研究/方法/01 透明、转移函数与OIT|透明、转移函数与OIT]]

- [[3D结构透视研究/来源/cross-10 Stochastic Transparency|cross-10 · Stochastic Transparency (2010)]]
- [[3D结构透视研究/来源/cross-11 Vulkan Order-Independent Transparency Sample|cross-11 · Vulkan Order-Independent Transparency Sample (未核实年份)]]
