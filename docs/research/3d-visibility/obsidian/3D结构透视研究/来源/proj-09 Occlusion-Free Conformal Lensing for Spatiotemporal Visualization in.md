---
type: research-source
created: '2026-10-15'
updated: '2026-10-15'
status: 文献研究，未本地复现
id: proj-09
year: 2026
source_type: paper
evidence: full-primary
methods:
- conformal footprint partition
- nested temporal ribbons
- view-dependent cutaway
- embedded lens
domains:
- 城市时间数据
- 建筑立面
- 沉浸式分析
source_url: https://arxiv.org/html/2602.03743v1
accessed: '2026-10-15'
method_families:
- '03'
- '04'
- '13'
---

# Occlusion-Free Conformal Lensing for Spatiotemporal Visualization in 3D Urban Analytics

返回 [[3D结构透视研究/00 3D结构透视研究 Dashboard|研究 Dashboard]] · [[3D结构透视研究/03 来源索引|来源索引]]

[原始来源](https://arxiv.org/html/2602.03743v1)

作者/机构：Roberta Mota; Julio D. Silva; Fabio Miranda; Usman Alim; Ehud Sharlin; Nivan Ferreira。年份：2026。证据层级：全文级原始资料。

## 机制

先将不规则建筑底面按骨架与图分区，分别作Schwarz–Christoffel映射并拼接；以嵌套条带编码时间，用依赖视角的双面剖切持续暴露时间显示。

## 能够显露的信息

同一层高可同时比较建筑各立面多个时间状态；它揭示的是嵌入的时间属性，不是楼内墙、房间或设备的全部真实几何。

## 几何与坐标

总体建筑布局保留；删除当前遮挡表面，显示底面内重编码条带；不是保持所有几何完整可见。

## 代价

剖去自遮挡外壳会削弱深度线索；高度不规则、细长、锐角/深凹底面存在数值拥挤和间距失真，细条带损害读值。

## 评价证据

2026-02-03预印本；28人、168次任务，均值误差8.17%对16.66%及23.3%。时间40.87s对51.5s的两种x-ray条件无明确差异，均快于102.7s基线。

## 交互

支持角向空间筛选、径向时间筛选和循环重排、桌面缩略透镜；实验刻意未测这些缩略图交互。

## 实现与数据要求

Unity、Quest2、RTX3060约45FPS；映射为Matlab离线预计算，交互时不重算SC布局。需底面、立面属性和剖切渲染。

## 来源核对

已打开完整arXiv HTML，核对方法、实验和限制；没有把摘要的总体时间提升误写成相对x-ray基线的显著提速。

## 限制

预印本证据，不宣称已确认最终期刊发表；单一时间属性、少量任务与时空实例，外推到密集内部结构尚无验证。

## 方法与关联

[[3D结构透视研究/方法/03 平面、目标驱动与非平面剖切|平面、目标驱动与非平面剖切]] · [[3D结构透视研究/方法/04 局部X-ray与体数据透镜|局部X-ray与体数据透镜]] · [[3D结构透视研究/方法/13 感知、评价与失败模式|感知、评价与失败模式]]

- [[3D结构透视研究/来源/proj-07 Interactive Urban Context-Aware Visualization via Multiple Disocclus|proj-07 · Interactive Urban Context-Aware Visualization via Multiple Disocclusion Operators (2016)]]
- [[3D结构透视研究/来源/proj-08 Multi-perspective occlusion-free urban navigation visualization|proj-08 · Multi-perspective occlusion-free urban navigation visualization (2026)]]
- [[3D结构透视研究/来源/proj-13 HippoMaps- Multiscale Cartography of Human Hippocampal Organization|proj-13 · HippoMaps: Multiscale Cartography of Human Hippocampal Organization (2025)]]
- [[3D结构透视研究/来源/proj-19 The State of the Art in Visual Analytics for 3D Urban Data|proj-19 · The State of the Art in Visual Analytics for 3D Urban Data (2024)]]
