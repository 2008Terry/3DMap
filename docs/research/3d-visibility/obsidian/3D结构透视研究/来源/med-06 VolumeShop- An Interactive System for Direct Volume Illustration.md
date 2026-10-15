---
type: research-source
created: '2026-10-15'
updated: '2026-10-15'
status: 文献研究，未本地复现
id: med-06
year: 2005
source_type: paper
evidence: full-primary
methods:
- volumetric painting
- selection and ghost
- selective deformation
- cutaway
- multi-object compositing
domains:
- medical and biological illustration
- technical illustration
source_url: https://www.cg.tuwien.ac.at/research/publications/2005/TR-186-2-05-04/TR-186-2-05-04-Technical%20Report.pdf
accessed: '2026-10-15'
method_families:
- '06'
---

# VolumeShop: An Interactive System for Direct Volume Illustration

返回 [[3D结构透视研究/00 3D结构透视研究 Dashboard|研究 Dashboard]] · [[3D结构透视研究/03 来源索引|来源索引]]

[原始来源](https://www.cg.tuwien.ac.at/research/publications/2005/TR-186-2-05-04/TR-186-2-05-04-Technical%20Report.pdf)

作者/机构：Stefan Bruckner; M. Eduard Gröller。年份：2005。证据层级：全文级原始资料。

## 机制

把场景分为选中体、原位置ghost和背景。用户涂画选区后可移动、旋转或放大选中结构，结合裁切、透明和二维交叉传递函数表现相交区域。

## 能够显露的信息

内部器官可被单独放大或移出遮挡，原位置ghost帮助追踪来源，交叉区域可显示接触或碰撞关系。

## 几何与坐标

既可只调外观，也可显式变换选中体；数据原位置通过ghost保留，而显示几何会重排或放大。

## 代价

移动/缩放后不再保持原来的空间距离和尺度；需要明确连接、ghost与原图，避免把插图布局误当真实解剖。

## 评价证据

已打开作者15页技术报告，核实三对象模型与GPU实现；该系统以交互插图制作为目标，不能据此宣称临床测量准确。

## 交互

三维体涂画、变换选区、调每类及交叉传递函数、自动放置标注。

## 实现与数据要求

选区体、标量体、变换矩阵与多对象GPU合成；原报告使用C++/Cg/OpenGL。

## 来源核对

已核实2005年4月技术报告；同名IEEE Visualization 2005论文为同一研究，不计作第二个来源。

## 限制

大量对象交叉的组合会迅速增长；可表达关系的插图不应直接承担真实位置测量。

## 方法与关联

[[3D结构透视研究/方法/06 剥皮、铰链、翻页与非刚性变形|剥皮、铰链、翻页与非刚性变形]]

- [[3D结构透视研究/来源/med-04 Illustrative Context-Preserving Volume Rendering|med-04 · Illustrative Context-Preserving Volume Rendering (2005)]]
- [[3D结构透视研究/来源/med-09 Advanced Curved Planar Reformation- Flattening of Vascular Structure|med-09 · Advanced Curved Planar Reformation: Flattening of Vascular Structures (2003)]]
- [[3D结构透视研究/来源/med-12 Interactive Importance-Driven Visualization Techniques for Medical V|med-12 · Interactive Importance-Driven Visualization Techniques for Medical Volume Data (2005)]]
