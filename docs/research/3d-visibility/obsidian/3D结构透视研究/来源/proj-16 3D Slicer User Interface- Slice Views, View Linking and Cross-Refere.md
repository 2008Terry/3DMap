---
type: research-source
created: '2026-10-15'
updated: '2026-10-15'
status: 文献研究，未本地复现
id: proj-16
year: null
source_type: official-doc
evidence: official-doc
methods:
- linked 2D/3D views
- orthogonal/oblique slicing
- crosshair cross-reference
- lightbox
domains:
- 医学体数据
- 内部定位
- 多视图
source_url: https://slicer.readthedocs.io/en/latest/user_guide/user_interface.html
accessed: '2026-10-15'
method_families:
- 09
---

# 3D Slicer User Interface: Slice Views, View Linking and Cross-Reference

返回 [[3D结构透视研究/00 3D结构透视研究 Dashboard|研究 Dashboard]] · [[3D结构透视研究/03 来源索引|来源索引]]

[原始来源](https://slicer.readthedocs.io/en/latest/user_guide/user_interface.html)

作者/机构：3D Slicer。年份：未核实，见来源核对说明。证据层级：官方文档。

## 机制

把轴向、冠状、矢状或斜切面与三维视图组成布局；联动体数据选择、缩放等属性，并将同一RAS坐标通过十字线同步到各视图。

## 能够显露的信息

内部体素可直接在切面读出，同时借三维视窗定位；跨视图指向同一点能减少小图与原空间的对应负担。

## 几何与坐标

原空间坐标保持，切面只是取样；独立二维窗口不需要改变模型几何。

## 代价

切片仍需浏览或充分采样；lightbox并非所有操作都支持，文档明确可能将来移除，不能以旧版截图假定稳定功能。

## 评价证据

官方文档提供功能与交互说明，没有本次设备性能或用户实验；用于说明成熟实现范式。

## 交互

Shift移动十字线联动其他切片到同坐标，视图可同步、放大和切换方向，切面可显示在三维中。

## 实现与数据要求

需要统一世界坐标、对象/体素ID、切面求交、交叉引用事件和视图分组；建筑可将RAS换成建筑世界坐标。

## 来源核对

已打开最新官方User Interface全文，核对Cross-Reference、view link、切片方向；文档没有明确出版年份，year=null。

## 限制

医学网格切片与建筑网格语义不同；若只显示墙面交线，房间家具等需要额外标签与筛选。

## 方法与关联

[[3D结构透视研究/方法/09 联动多视窗、切片图册与小图|联动多视窗、切片图册与小图]]

- [[3D结构透视研究/来源/proj-14 ParaView Documentation 6.2.0- Displaying Data|proj-14 · ParaView Documentation 6.2.0: Displaying Data (未核实年份)]]
- [[3D结构透视研究/来源/proj-15 ParaView Documentation 6.2.0- Comparative Visualization|proj-15 · ParaView Documentation 6.2.0: Comparative Visualization (未核实年份)]]
- [[3D结构透视研究/来源/proj-06 An Evaluation of 3-D Scene Exploration Using a Multiperspective Imag|proj-06 · An Evaluation of 3-D Scene Exploration Using a Multiperspective Image Framework (2011)]]
