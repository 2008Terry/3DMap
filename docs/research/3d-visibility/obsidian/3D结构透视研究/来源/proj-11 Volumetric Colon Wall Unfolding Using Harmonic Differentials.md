---
type: research-source
created: '2026-10-15'
updated: '2026-10-15'
status: 文献研究，未本地复现
id: proj-11
year: 2011
source_type: paper
evidence: full-primary
methods:
- volumetric harmonic mapping
- tetrahedral mesh
- canonical cuboid
- direct volume rendering
domains:
- 厚壁体积展开
- 医学
- 管状结构
source_url: https://pmc.ncbi.nlm.nih.gov/articles/PMC3134375/
accessed: '2026-10-15'
method_families:
- 08
---

# Volumetric Colon Wall Unfolding Using Harmonic Differentials

返回 [[3D结构透视研究/00 3D结构透视研究 Dashboard|研究 Dashboard]] · [[3D结构透视研究/03 来源索引|来源索引]]

[原始来源](https://pmc.ncbi.nlm.nih.gov/articles/PMC3134375/)

作者/机构：Wei Zeng; Joseph Marino; Arie Kaufman; Xianfeng David Gu。年份：2011。证据层级：全文级原始资料。

## 机制

把CT内外壁之间的组织建成四面体体网格，沿经向面切开，求三组调和1-形式并积分，将有厚度管壁周期映射到规范长方体。

## 能够显露的信息

比只展内壁更进一步，保留从内壁至外壁的厚度方向采样，便于体绘制、纹理分析和虚拟活检；可同时查看沿管道的组织分布。

## 几何与坐标

显示坐标被体积映射改变；内外壁对应到长方体两平行面，原三维网格可通过映射保留对应。

## 代价

体积虽展开成规则块仍需要选择厚度采样、切片或体绘制；原空间度量发生变形，复杂拓扑要增加切面与处理。

## 评价证据

2011年Computers & Graphics论文，在真实医学数据上展示算法和体绘制；调和能量最小化及稀疏系统提供理论/计算基础，未证任意体积可无失真压成平面。

## 交互

算法自动化并允许人为干预；查看结果可使用平面图、厚度切片和联动原模型。

## 实现与数据要求

需内外壁分割、四面体剖分、经向面计算、调和形式线性系统、参数域体绘制和可逆位置映射。

## 来源核对

已打开PMC作者全文；正式出版为2011-06-01，PMC可访问日期2012不是出版年。全文明确原有中心线截面可能交叉、重复或遗漏。

## 限制

主要建立管状厚壁的规范参数域，不能不经适配直接用于分支、多房间建筑；长方体仍是三维表示而非一次性消除所有体积遮挡。

## 方法与关联

[[3D结构透视研究/方法/08 曲面重采样、解缠与表面展开|曲面重采样、解缠与表面展开]]

- [[3D结构透视研究/来源/proj-10 Nondistorting Flattening Maps and the 3-D Visualization of Colon CT|proj-10 · Nondistorting Flattening Maps and the 3-D Visualization of Colon CT Images (2000)]]
- [[3D结构透视研究/来源/proj-12 Unlocking History through Automated Virtual Unfolding of Sealed Docu|proj-12 · Unlocking History through Automated Virtual Unfolding of Sealed Documents Imaged by X-ray Microtomography (2021)]]
- [[3D结构透视研究/来源/proj-14 ParaView Documentation 6.2.0- Displaying Data|proj-14 · ParaView Documentation 6.2.0: Displaying Data (未核实年份)]]
