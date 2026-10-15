---
type: research-source
created: '2026-10-15'
updated: '2026-10-15'
status: 文献研究，未本地复现
id: cross-10
year: 2010
source_type: paper
evidence: full-primary
methods:
- stochastic transparency
- multisampling
domains:
- rendering
source_url: https://www.nvidia.com/docs/IO/88888/StochasticTransparency_I3D2010.pdf
accessed: '2026-10-15'
method_families:
- '01'
---

# Stochastic Transparency

返回 [[3D结构透视研究/00 3D结构透视研究 Dashboard|研究 Dashboard]] · [[3D结构透视研究/03 来源索引|来源索引]]

[原始来源](https://www.nvidia.com/docs/IO/88888/StochasticTransparency_I3D2010.pdf)

作者/机构：Eric Enderton et al.。年份：2010。证据层级：全文级原始资料。

## 机制

以随机样本覆盖表示透明，借助多重采样在无排序条件下估计合成。

## 能够显露的信息

减少排序依赖，适合大量透明细节。

## 几何与坐标

几何原位。

## 代价

有限样本带来噪声，收敛与时域稳定性有代价；仍会重叠混合。

## 评价证据

论文算法示例与性能分析，不等于可读性实证。

## 交互

交互能力以原始资料为准；本条机制与适用条件见下。

## 实现与数据要求

MSAA、随机覆盖与抗噪处理。

## 来源核对

核对NVIDIA作者全文。

## 限制

有限样本带来噪声，收敛与时域稳定性有代价；仍会重叠混合。

## 方法与关联

[[3D结构透视研究/方法/01 透明、转移函数与OIT|透明、转移函数与OIT]]

- [[3D结构透视研究/来源/cross-09 Exploring and Expanding the Continuum of OIT Algorithms|cross-09 · Exploring and Expanding the Continuum of OIT Algorithms (2016)]]
