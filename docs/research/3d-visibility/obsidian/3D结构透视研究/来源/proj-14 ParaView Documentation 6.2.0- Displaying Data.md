---
type: research-source
created: '2026-10-15'
updated: '2026-10-15'
status: 文献研究，未本地复现
id: proj-14
year: null
source_type: official-doc
evidence: official-doc
methods:
- multiple coordinated views
- Slice View
- Quad View
- orthogonal slices
domains:
- 科学可视化
- 体数据
- 切片图册
source_url: https://docs.paraview.org/en/latest/UsersGuide/displayingData.html
accessed: '2026-10-15'
method_families:
- 09
---

# ParaView Documentation 6.2.0: Displaying Data

返回 [[3D结构透视研究/00 3D结构透视研究 Dashboard|研究 Dashboard]] · [[3D结构透视研究/03 来源索引|来源索引]]

[原始来源](https://docs.paraview.org/en/latest/UsersGuide/displayingData.html)

作者/机构：ParaView / Kitware。年份：未核实，见来源核对说明。证据层级：官方文档。

## 机制

将同一数据源分别放入多个渲染、图表和切片视图；Slice View按三个正交轴的偏移生成多张截面，用户增删和拖动截面位置。

## 能够显露的信息

各截面直接显示外壳后方的内部交线或体素，正交视图补足不同方向结构；若系统覆盖全部有效高度/部件，切片图册可系统检索内部。

## 几何与坐标

原始数据坐标保留；截面是对数据的选择性显示，独立视窗改变版面而非源几何。

## 代价

有限切片之间仍可能漏掉薄结构；同屏多视图分掉像素，需要标注坐标和截面相交线维持对应。不能把一个截面称为全部体积。

## 评价证据

这是可用软件功能的官方文档证据，不是比较用户表现的论文；本次没有启动软件或测速度。

## 交互

双击添加/删除切片、拖动位置、切换可见；视图可分割与重排。

## 实现与数据要求

网页迁移可用多个viewport、独立相机及裁剪/求交或体采样；共享对象ID与切片位置，将选中结构反向高亮到三维。

## 来源核对

已打开官方6.2.0文档全文，核对Multiple Views及Slice View章节与XSliceValues/Y/Z设置；页面未给明确发布日期，因此year=null。

## 限制

功能存在不等于对特定模型有完整覆盖；全覆盖需另外定义采样密度、边界和可读分辨率。

## 方法与关联

[[3D结构透视研究/方法/09 联动多视窗、切片图册与小图|联动多视窗、切片图册与小图]]

- [[3D结构透视研究/来源/proj-15 ParaView Documentation 6.2.0- Comparative Visualization|proj-15 · ParaView Documentation 6.2.0: Comparative Visualization (未核实年份)]]
- [[3D结构透视研究/来源/proj-16 3D Slicer User Interface- Slice Views, View Linking and Cross-Refere|proj-16 · 3D Slicer User Interface: Slice Views, View Linking and Cross-Reference (未核实年份)]]
- [[3D结构透视研究/来源/proj-11 Volumetric Colon Wall Unfolding Using Harmonic Differentials|proj-11 · Volumetric Colon Wall Unfolding Using Harmonic Differentials (2011)]]
