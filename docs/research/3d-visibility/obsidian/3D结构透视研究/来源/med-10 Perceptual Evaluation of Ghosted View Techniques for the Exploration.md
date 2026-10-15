---
type: research-source
created: '2026-10-15'
updated: '2026-10-15'
status: 文献研究，未本地复现
id: med-10
year: 2011
source_type: paper
evidence: full-primary
methods:
- ghosted vessel surface
- flow visibility
- depth enhancement
- controlled perception experiments
domains:
- cerebral aneurysm
- vascular flow simulation
source_url: https://www.vismd.de/wp-content/uploads/legacy/baer_2011_eurovis.pdf
accessed: '2026-10-15'
method_families:
- '02'
- '13'
---

# Perceptual Evaluation of Ghosted View Techniques for the Exploration of Vascular Structures and Embedded Flow

返回 [[3D结构透视研究/00 3D结构透视研究 Dashboard|研究 Dashboard]] · [[3D结构透视研究/03 来源索引|来源索引]]

[原始来源](https://www.vismd.de/wp-content/uploads/legacy/baer_2011_eurovis.pdf)

作者/机构：Alexandra Baer; Rocco Gasteiger; Douglas Cunningham; Bernhard Preim。年份：2011。证据层级：全文级原始资料。

## 机制

用选择性ghosting表现包围血管壁与内部流线，并比较额外深度增强；重点不是把整个表面用同一alpha淡化，而是保留帮助识别形状的线索。

## 能够显露的信息

同时观察血管外形与腔内流动编码，评估表面形状、前后关系与内部颜色是否可正确辨认。

## 几何与坐标

保持血管和流线几何位置，选择性改变外壁可见性与深度编码。

## 代价

壁和流同时显示会互相影响；深度增强可能改变颜色或增加负担，偏好更高不代表每项任务都更准确。

## 评价证据

已打开10页原始论文；摘要确认三项受控感知研究，以五个临床数据集的动脉瘤模型为刺激，测准确率、反应时间与偏好。报告对两种ghosting的强偏好。

## 交互

研究条件涉及模型浏览/旋转，不能把有限刺激实验外推为任意镜头与任意密度场景。

## 实现与数据要求

需表面与嵌入流对象分别着色，控制外壁ghost表示并加入可选深度提示。

## 来源核对

存在直接比较普通半透明与两类ghosting的任务实验；仅据本轮核实内容不报告未确认的人数或统一胜出结论。

## 限制

刺激来自少量动脉瘤数据，不能推论所有内部3D结构；旋转、颜色任务与空间任务应分别评估。

## 方法与关联

[[3D结构透视研究/方法/02 隐藏线、轮廓与语义着色|隐藏线、轮廓与语义着色]] · [[3D结构透视研究/方法/13 感知、评价与失败模式|感知、评价与失败模式]]

- [[3D结构透视研究/来源/med-04 Illustrative Context-Preserving Volume Rendering|med-04 · Illustrative Context-Preserving Volume Rendering (2005)]]
- [[3D结构透视研究/来源/med-05 ClearView- An Interactive Context Preserving Hotspot Visualization T|med-05 · ClearView: An Interactive Context Preserving Hotspot Visualization Technique (2006)]]
- [[3D结构透视研究/来源/med-19 Hidden Tumour Visualization in Augmented Monocular Liver Laparoscopy|med-19 · Hidden Tumour Visualization in Augmented Monocular Liver Laparoscopy (2026)]]
