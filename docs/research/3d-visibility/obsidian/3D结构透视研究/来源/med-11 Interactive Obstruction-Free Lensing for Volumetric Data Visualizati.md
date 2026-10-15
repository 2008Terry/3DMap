---
type: research-source
created: '2026-10-15'
updated: '2026-10-15'
status: 文献研究，未本地复现
id: med-11
year: 2019
source_type: paper
evidence: abstract-primary
methods:
- obstruction-free lens
- deformed ray casting
- fish-eye
- local viewpoint
domains:
- baggage inspection
- 3D fluid flow
- chest radiology
- air traffic
- DTI fibers
source_url: https://pubmed.ncbi.nlm.nih.gov/30235132/
accessed: '2026-10-15'
method_families:
- '04'
- '06'
---

# Interactive Obstruction-Free Lensing for Volumetric Data Visualization

返回 [[3D结构透视研究/00 3D结构透视研究 Dashboard|研究 Dashboard]] · [[3D结构透视研究/03 来源索引|来源索引]]

[原始来源](https://pubmed.ncbi.nlm.nih.gov/30235132/)

作者/机构：Michael Traoré; Christophe Hurter; Alexandru Telea。年份：2019。证据层级：原始摘要或受限索引。

## 机制

用户指定部分可见的目标区域，透镜在边界把遮挡物视觉上推开，再用鱼眼扩展视野，并允许只在镜内改变观察点。

## 能够显露的信息

可查看与遮挡物密度近似、难以用传递函数分开的隐藏目标及邻域；论文举五类跨领域场景。

## 几何与坐标

原始体数据不必改变；通过弯曲采样射线/局部视点产生显示变形，不能说完全保留原来的投影几何。

## 代价

推开遮挡与鱼眼会改变局部空间外观；原位尺度、角度和距离不再能从镜内图像直接读取。

## 评价证据

已打开PubMed原始摘要；作者/大学PDF打开失败。摘要只支持五场景演示与实时实现，不支持受控用户实验结论。

## 交互

放置透镜、调整范围及镜内局部视点，适合从已露出的线索追踪隐蔽物。

## 实现与数据要求

需GPU ray caster支持射线变形、局部光照与局部相机，复杂度高于裁切或alpha调节。

## 来源核对

在线先发表为2018-09-18；最终TVCG卷25期1为2019。该记录year采用最终卷年，非网页抓取日期。

## 限制

方法从部分可见的目标出发；不能假定自动发现完全隐藏且未知的对象，也不保全度量几何。

## 方法与关联

[[3D结构透视研究/方法/04 局部X-ray与体数据透镜|局部X-ray与体数据透镜]] · [[3D结构透视研究/方法/06 剥皮、铰链、翻页与非刚性变形|剥皮、铰链、翻页与非刚性变形]]

- [[3D结构透视研究/来源/med-05 ClearView- An Interactive Context Preserving Hotspot Visualization T|med-05 · ClearView: An Interactive Context Preserving Hotspot Visualization Technique (2006)]]
- [[3D结构透视研究/来源/med-09 Advanced Curved Planar Reformation- Flattening of Vascular Structure|med-09 · Advanced Curved Planar Reformation: Flattening of Vascular Structures (2003)]]
- [[3D结构透视研究/来源/med-12 Interactive Importance-Driven Visualization Techniques for Medical V|med-12 · Interactive Importance-Driven Visualization Techniques for Medical Volume Data (2005)]]
