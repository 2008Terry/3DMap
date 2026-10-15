---
type: research-source
created: '2026-10-15'
updated: '2026-10-15'
status: 文献研究，未本地复现
id: proj-18
year: 2024
source_type: paper
evidence: full-primary
methods:
- simplex facet projection
- barycentric ratios
- multiple corresponding projections
domains:
- 组成数据
- 高维统计可视化
- 四维类比
source_url: https://arxiv.org/pdf/2403.11141
accessed: '2026-10-15'
method_families:
- '07'
---

# The Simplex Projection: Lossless Visualization of 4D Compositional Data on a 2D Canvas

返回 [[3D结构透视研究/00 3D结构透视研究 Dashboard|研究 Dashboard]] · [[3D结构透视研究/03 来源索引|来源索引]]

[原始来源](https://arxiv.org/pdf/2403.11141)

作者/机构：Marvin Schmitt; Yuga Hikida; Stefan T. Radev; Filip Sadlo; Paul-Christian Bürkner。年份：2024。证据层级：全文级原始资料。

## 机制

四个正分量和为一的数据位于三维单纯形；把点分别从多个顶点投到对面的三角面，并以一组相互对应的投影编码原点。每次投影保留其余分量比例。

## 能够显露的信息

可在二维画布检查四部分组成关系、点云与密度示例；其启发是增加多个有对应关系的表示，而不是一条普通投影射线保存全部空间深度。

## 几何与坐标

不保原欧氏三维形状；保留的是特定组成数据表示中的比例/可恢复关系，和空间几何不是同一任务。

## 代价

单个原点对应多个二维点，不是将任意四维物体一一映为单个二维坐标；点身份与投影间关联不可省。密度近似与数学信息保留应分开讨论。

## 评价证据

2024-03-17预印本，含数学证明和Dirichlet解析边缘分布对照；没有针对建筑内部可见性或人类识别能力的研究。

## 交互

论文以静态绘图为主；大量点需颜色、索引或交互联动帮助区分对应投影。

## 实现与数据要求

适用输入必须满足组成约束；实现多面重心投影并保存对应元组。不可把任意房间坐标归一化后就宣称空间可见性无损。

## 来源核对

已打开14页arXiv PDF及摘要页，核对多面投影、正分量和为一及理论/数值示例；其lossless结论按论文限定数据和编码解释。

## 限制

本次未独立复核所有数学证明，尤其不把有限边缘密度图普遍恢复任意联合密度当作已验证普适定理；这不是4D绕过3D遮挡的证据。

## 方法与关联

[[3D结构透视研究/方法/07 广义相机、多透视与投影变化|广义相机、多透视与投影变化]]

- [[3D结构透视研究/来源/proj-01 General Linear Cameras|proj-01 · General Linear Cameras (2004)]]
- [[3D结构透视研究/来源/proj-15 ParaView Documentation 6.2.0- Comparative Visualization|proj-15 · ParaView Documentation 6.2.0: Comparative Visualization (未核实年份)]]
- [[3D结构透视研究/来源/proj-17 OGC IndoorGML 2.0 Part 1- Conceptual Model|proj-17 · OGC IndoorGML 2.0 Part 1: Conceptual Model (2025)]]
