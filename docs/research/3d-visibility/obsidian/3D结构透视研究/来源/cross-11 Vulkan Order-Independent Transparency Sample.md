---
type: research-source
created: '2026-10-15'
updated: '2026-10-15'
status: 文献研究，未本地复现
id: cross-11
year: null
source_type: official-doc
evidence: official-doc
methods:
- OIT
- WBOIT
- A-buffer
domains:
- rendering
- implementation
source_url: https://github.com/nvpro-samples/vk_order_independent_transparency
accessed: '2026-10-15'
method_families:
- '01'
---

# Vulkan Order-Independent Transparency Sample

返回 [[3D结构透视研究/00 3D结构透视研究 Dashboard|研究 Dashboard]] · [[3D结构透视研究/03 来源索引|来源索引]]

[原始来源](https://github.com/nvpro-samples/vk_order_independent_transparency)

作者/机构：NVIDIA nvpro-samples。年份：未核实，见来源核对说明。证据层级：官方文档。

## 机制

官方示例对照七类OIT实现，包括链表、循环、互锁及加权混合。

## 能够显露的信息

提供透明渲染实现与对比入口。

## 几何与坐标

原位。

## 代价

有限片元容量会溢出或退化；加权混合为近似；部分路径需要特定硬件扩展。

## 评价证据

维护中的示例，未核对发行年；访问日期不是发表年。

## 交互

交互能力以原始资料为准；本条机制与适用条件见下。

## 实现与数据要求

Vulkan与对应GPU功能；可研究实现原则，不作为本项目选型限制。

## 来源核对

已读官方README与算法约束。

## 限制

有限片元容量会溢出或退化；加权混合为近似；部分路径需要特定硬件扩展。

## 方法与关联

[[3D结构透视研究/方法/01 透明、转移函数与OIT|透明、转移函数与OIT]]

- [[3D结构透视研究/来源/cross-09 Exploring and Expanding the Continuum of OIT Algorithms|cross-09 · Exploring and Expanding the Continuum of OIT Algorithms (2016)]]
