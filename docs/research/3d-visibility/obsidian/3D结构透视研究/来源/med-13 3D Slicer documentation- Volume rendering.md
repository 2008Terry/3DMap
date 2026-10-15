---
type: research-source
created: '2026-10-15'
updated: '2026-10-15'
status: 文献研究，未本地复现
id: med-13
year: null
source_type: official-doc
evidence: official-doc
methods:
- DVR presets
- MIP
- MinIP
- ROI crop
- segmentation mask
domains:
- CT
- MRI
- open-source medical software
source_url: https://slicer.readthedocs.io/en/latest/user_guide/modules/volumerendering.html
accessed: '2026-10-15'
method_families:
- '01'
---

# 3D Slicer documentation: Volume rendering

返回 [[3D结构透视研究/00 3D结构透视研究 Dashboard|研究 Dashboard]] · [[3D结构透视研究/03 来源索引|来源索引]]

[原始来源](https://slicer.readthedocs.io/en/latest/user_guide/modules/volumerendering.html)

作者/机构：3D Slicer contributors; Kitware; Isomics; PerkLab; SPL/BWH。年份：未核实，见来源核对说明。证据层级：官方文档。

## 机制

官方实现提供强度/梯度传递函数、阴影合成、逐射线最大值MIP、最小值MinIP，以及六平面ROI裁切和分割mask移除区域。

## 能够显露的信息

MIP选高强度血管等目标；MinIP选低强度通道；裁切或mask可让被肋骨等外层挡住的区域进入视线。

## 几何与坐标

DVR/投影保原坐标；裁切抑制显示范围；Mask volume可用空值重写被选区域。

## 代价

MIP/MinIP每射线只保留一个极值，深度顺序及非极值结构会丢失。mask修改的是另一个待显示体数据，应保留原体。

## 评价证据

已打开完整官方使用文档；这是功能和限制证据，未在本机执行，也不是效果比较研究。

## 交互

鼠标窗口/level调整、预设/offset、控制点编辑、裁切框、Paint/Scissors选区。

## 实现与数据要求

VTK CPU/GPU ray casting与实验性Multi-Volume；后者文档列明裁切及MIP/MinIP等限制。

## 来源核对

当前latest页面确实区分DVR、MIP、MinIP和显式遮挡移除；页面未给出版日期，year为null。

## 限制

预设需按数据调节；GPU分辨率/内存限制影响交互。X-ray-like显示不等于进行了真实X射线测量。

## 方法与关联

[[3D结构透视研究/方法/01 透明、转移函数与OIT|透明、转移函数与OIT]]

- [[3D结构透视研究/来源/med-01 Display of Surfaces from Volume Data|med-01 · Display of Surfaces from Volume Data (1988)]]
- [[3D结构透视研究/来源/med-07 Opacity Peeling for Direct Volume Rendering|med-07 · Opacity Peeling for Direct Volume Rendering (2006)]]
- [[3D结构透视研究/来源/med-14 3D Slicer documentation- Reformat|med-14 · 3D Slicer documentation: Reformat (未核实年份)]]
- [[3D结构透视研究/来源/med-15 Open Inventor 2026.1 reference- SoVolumeRender.RenderModes|med-15 · Open Inventor 2026.1 reference: SoVolumeRender.RenderModes (未核实年份)]]
