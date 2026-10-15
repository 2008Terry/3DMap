---
type: research-source
created: '2026-10-15'
updated: '2026-10-15'
status: 文献研究，未本地复现
id: med-08
year: 2002
source_type: paper
evidence: full-primary
methods:
- curved planar reformation
- projected CPR
- stretched CPR
- straightened CPR
- thick and rotating CPR
domains:
- CT angiography
- tubular structures
source_url: https://cg.tuwien.ac.at/research/vis/adapt/Vis2002/AKanitsar_CPR.pdf
accessed: '2026-10-15'
method_families:
- 08
---

# CPR - Curved Planar Reformation

返回 [[3D结构透视研究/00 3D结构透视研究 Dashboard|研究 Dashboard]] · [[3D结构透视研究/03 来源索引|来源索引]]

[原始来源](https://cg.tuwien.ac.at/research/vis/adapt/Vis2002/AKanitsar_CPR.pdf)

作者/机构：Armin Kanitsar; Dominik Fleischmann; Rainer Wegenkittl; Petr Felkel; M. Eduard Gröller。年份：2002。证据层级：全文级原始资料。

## 机制

沿管道中心线构造弯曲采样面并映射到二维。比较投影、伸展和拉直三种方式，并扩展厚层、绕中心线旋转及多分支CPR。

## 能够显露的信息

一张图连续展示血管全长的管腔、管壁、钙化与附近组织，避免外表面渲染看不到内部通道。

## 几何与坐标

原体保留；显示采样面被展开或拉直。等距性指所述映射属性，不等于所有三维距离均被保留。

## 代价

投影CPR空间感较强但可能重叠且不等距；伸展保等距且消重叠；拉直也保等距但空间形状感最弱。

## 评价证据

已打开8页原文；对专门CT管道phantom进行短评估。原文将旋转CPR增加诊断信心写为推测，不当作已验证结论。

## 交互

提取/指定中心线、旋转采样方向、选择厚度和MIP/MinIP/平均重采样。

## 实现与数据要求

需要可信中心线、采样方向及体数据插值；多分支另需树状布局。

## 来源核对

原文表1明确列出三类CPR的空间感、等距性与遮挡权衡，是保持形状与完整显示不可兼得的直接证据。

## 限制

单采样面会漏掉未被切到的偏心病变；不能仅依赖一张CPR宣布整个管腔无异常。

## 方法与关联

[[3D结构透视研究/方法/08 曲面重采样、解缠与表面展开|曲面重采样、解缠与表面展开]]

- [[3D结构透视研究/来源/med-09 Advanced Curved Planar Reformation- Flattening of Vascular Structure|med-09 · Advanced Curved Planar Reformation: Flattening of Vascular Structures (2003)]]
- [[3D结构透视研究/来源/med-14 3D Slicer documentation- Reformat|med-14 · 3D Slicer documentation: Reformat (未核实年份)]]
