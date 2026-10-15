---
type: research-source
created: '2026-10-15'
updated: '2026-10-15'
status: 文献研究，未本地复现
id: med-09
year: 2003
source_type: paper
evidence: full-primary
methods:
- helical CPR
- untangled CPR
- branch-point rotation
- vascular flattening
domains:
- vascular tree visualization
- CTA
source_url: https://www.cg.tuwien.ac.at/research/vis/adapt/Vis2003_03/AKanitsar_Adv.pdf
accessed: '2026-10-15'
method_families:
- 08
---

# Advanced Curved Planar Reformation: Flattening of Vascular Structures

返回 [[3D结构透视研究/00 3D结构透视研究 Dashboard|研究 Dashboard]] · [[3D结构透视研究/03 来源索引|来源索引]]

[原始来源](https://www.cg.tuwien.ac.at/research/vis/adapt/Vis2003_03/AKanitsar_Adv.pdf)

作者/机构：Armin Kanitsar; Rainer Wegenkittl; Dominik Fleischmann; M. Eduard Gröller。年份：2003。证据层级：全文级原始资料。

## 机制

螺旋CPR用围绕中心线的采样螺旋覆盖管腔更多位置；解缠CPR在分叉点微调子树角度并分配图像区域，消除投影血管重叠。

## 能够显露的信息

显示直线切面漏掉的偏心狭窄通道，并让整棵血管树的分支与连通关系可追踪。

## 几何与坐标

体数据不变，但螺旋重采样与图像空间分支旋转改变显示；保拓扑比保原始角度/位置优先。

## 代价

以放松空间一致性换特征完整；螺旋模式可能重复显示同一病灶，角采样会放大中心且增加畸变。

## 评价证据

已打开8页原文，包含病变phantom及真实CTA实例；未把全部血管可见的算法目标扩展为临床检测性能保证。

## 交互

选择重采样方向、常角/常弧长采样及固定/自适应树布局，可连续查看解缠结果。

## 实现与数据要求

需中心线树、子树包围hull、非交叉旋转与图像分区；算法不会仅靠透明材质实现。

## 来源核对

论文直接说明两方法都牺牲一定空间一致性，以提高管腔病变与完整分支的可感知性。

## 限制

解缠图不能直接代表患者体内真实分支夹角；螺旋映射需要解释图例与原位视图对照。

## 方法与关联

[[3D结构透视研究/方法/08 曲面重采样、解缠与表面展开|曲面重采样、解缠与表面展开]]

- [[3D结构透视研究/来源/med-06 VolumeShop- An Interactive System for Direct Volume Illustration|med-06 · VolumeShop: An Interactive System for Direct Volume Illustration (2005)]]
- [[3D结构透视研究/来源/med-08 CPR - Curved Planar Reformation|med-08 · CPR - Curved Planar Reformation (2002)]]
- [[3D结构透视研究/来源/med-11 Interactive Obstruction-Free Lensing for Volumetric Data Visualizati|med-11 · Interactive Obstruction-Free Lensing for Volumetric Data Visualization (2019)]]
