---
type: research-source
created: '2026-10-15'
updated: '2026-10-15'
status: 文献研究，未本地复现
id: med-04
year: 2005
source_type: paper
evidence: full-primary
methods:
- context-preserving volume rendering
- selective opacity modulation
- illustrative ghosting
domains:
- CT visualization
- medical illustration
source_url: https://www.cg.tuwien.ac.at/research/vis/adapt/2004_cpvr/
accessed: '2026-10-15'
method_families:
- '02'
---

# Illustrative Context-Preserving Volume Rendering

返回 [[3D结构透视研究/00 3D结构透视研究 Dashboard|研究 Dashboard]] · [[3D结构透视研究/03 来源索引|来源索引]]

[原始来源](https://www.cg.tuwien.ac.at/research/vis/adapt/2004_cpvr/)

作者/机构：Stefan Bruckner; Sören Grimm; Armin Kanitsar; M. Eduard Gröller。年份：2005。证据层级：全文级原始资料。

## 机制

用着色强度、梯度幅度、到眼睛距离与已累积不透明度共同调制后续样本，降低不重要区域的遮挡，由两个参数控制整体效果。

## 能够显露的信息

查看内部骨骼、组织与血管时仍保留部分外部形状和定位线索，缓解硬裁切丢失上下文的问题。

## 几何与坐标

不重排体素、不改变真实形状；对屏幕贡献进行特征驱动的透明度调制。

## 代价

保留的上下文只是被选择的视觉线索，非全部表面细节；透明多层仍可能混叠，特征判定也可能压低需要的信息。

## 评价证据

已打开作者页面及8页PDF。页面提供相同传递函数下DVR、梯度调制、裁切与本法比较，以及手、头、全身CT示例；不宣称临床诊断获益。

## 交互

两个连续参数配合旋转和传递函数；可调制参数使特定组织如骨保持不可穿透。

## 实现与数据要求

在DVR采样着色阶段加入局部调制函数；需梯度、深度与累计不透明度。

## 来源核对

作者明确指出过透明会产生重叠杂乱，裁切会移除潜在重要上下文；本法是二者之间的可调折中。

## 限制

没有在一幅图内无损展示所有深度；页面路径含2004，但论文出版年份为EuroVis 2005。

## 方法与关联

[[3D结构透视研究/方法/02 隐藏线、轮廓与语义着色|隐藏线、轮廓与语义着色]]

- [[3D结构透视研究/来源/med-01 Display of Surfaces from Volume Data|med-01 · Display of Surfaces from Volume Data (1988)]]
- [[3D结构透视研究/来源/med-03 Importance-Driven Volume Rendering|med-03 · Importance-Driven Volume Rendering (2004)]]
- [[3D结构透视研究/来源/med-05 ClearView- An Interactive Context Preserving Hotspot Visualization T|med-05 · ClearView: An Interactive Context Preserving Hotspot Visualization Technique (2006)]]
- [[3D结构透视研究/来源/med-10 Perceptual Evaluation of Ghosted View Techniques for the Exploration|med-10 · Perceptual Evaluation of Ghosted View Techniques for the Exploration of Vascular Structures and Embedded Flow (2011)]]
