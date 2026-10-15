---
type: research-source
created: '2026-10-15'
updated: '2026-10-15'
status: 文献研究，未本地复现
id: proj-19
year: 2024
source_type: survey
evidence: full-primary
methods:
- why/what/how taxonomy
- occlusion handling survey
- physical/thematic view integration
domains:
- 城市可视分析
- 建筑
- 工程
source_url: https://arxiv.org/html/2404.15976v1
accessed: '2026-10-15'
method_families:
- 09
---

# The State of the Art in Visual Analytics for 3D Urban Data

返回 [[3D结构透视研究/00 3D结构透视研究 Dashboard|研究 Dashboard]] · [[3D结构透视研究/03 来源索引|来源索引]]

[原始来源](https://arxiv.org/html/2404.15976v1)

作者/机构：Fabio Miranda; Thomas Ortner; Gustavo Moreira; Maryam Hosseini; Milena Vuckovic; Filip Biljecki; Claudio T. Silva; Marcos Lage; Nivan Ferreira。年份：2024。证据层级：全文级原始资料。

## 机制

按分析目的、数据和表达方式整理3D城市研究，分离物理几何与专题属性，讨论多视图、嵌入图、去遮挡和导航策略，帮助避免把不同任务的成功混为一谈。

## 能够显露的信息

提供选择方法的知识框架：要看室内连通、几何形状、空间属性和时间趋势时，需要不同表示组合；综述本身不渲染隐藏内容。

## 几何与坐标

取决于所综述方法，可保几何、重排多视图或变形；不能对全部类别给统一保真承诺。

## 代价

物理真实性与抽象属性可读性存在冲突；第三维带来遮挡与上下文整合成本，二维指标也可能遗漏真实三维影响。

## 评价证据

2024年CGF43(3)综述，arXiv首版2024-04-24；回顾20余个期刊/会议、2008至2023研究，指出经验验证不足。

## 交互

包括导航、筛选、嵌入及联动等模式；没有单一现成交互实现。

## 实现与数据要求

可用于先建立任务与覆盖矩阵，再为物理层、专题层及去遮挡策略选择独立模块，工程流程属于综合推断。

## 来源核对

已打开完整arXiv HTML，核对作者、2024年卷期、检索范围和Why/What/How框架；正式综述也是寻找近期主要文献的入口。

## 限制

主要检索范围截至2023，不等于覆盖2024–2026最新进展；不提供统一全内部可见算法。

## 方法与关联

[[3D结构透视研究/方法/09 联动多视窗、切片图册与小图|联动多视窗、切片图册与小图]]

- [[3D结构透视研究/来源/proj-07 Interactive Urban Context-Aware Visualization via Multiple Disocclus|proj-07 · Interactive Urban Context-Aware Visualization via Multiple Disocclusion Operators (2016)]]
- [[3D结构透视研究/来源/proj-08 Multi-perspective occlusion-free urban navigation visualization|proj-08 · Multi-perspective occlusion-free urban navigation visualization (2026)]]
- [[3D结构透视研究/来源/proj-09 Occlusion-Free Conformal Lensing for Spatiotemporal Visualization in|proj-09 · Occlusion-Free Conformal Lensing for Spatiotemporal Visualization in 3D Urban Analytics (2026)]]
- [[3D结构透视研究/来源/proj-17 OGC IndoorGML 2.0 Part 1- Conceptual Model|proj-17 · OGC IndoorGML 2.0 Part 1: Conceptual Model (2025)]]
