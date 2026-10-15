---
type: research-source
created: '2026-10-15'
updated: '2026-10-15'
status: 文献研究，未本地复现
id: med-14
year: null
source_type: official-doc
evidence: official-doc
methods:
- MPR
- oblique slice
- slice offset
- slice normal
domains:
- medical cross-sectional imaging
- volumetric inspection
source_url: https://slicer.readthedocs.io/en/latest/user_guide/modules/reformat.html
accessed: '2026-10-15'
method_families:
- 09
---

# 3D Slicer documentation: Reformat

返回 [[3D结构透视研究/00 3D结构透视研究 Dashboard|研究 Dashboard]] · [[3D结构透视研究/03 来源索引|来源索引]]

[原始来源](https://slicer.readthedocs.io/en/latest/user_guide/modules/reformat.html)

作者/机构：3D Slicer; Michael Jeulin-Lagarrigue / Kitware。年份：未核实，见来源核对说明。证据层级：官方文档。

## 机制

从原体数据重采样一个可定位、旋转的切片平面，提供轴向/矢状/冠状、任意法向、相机对齐及平面内旋转。

## 能够显露的信息

直接查看特定深度的内部横截面；外层不会像三维投影那样遮住切面内的数据。

## 几何与坐标

原体不变；显示一个采样面，不把所有三维内容压在同一投影里。

## 代价

一张薄切片只显示与平面相交的体素，其余结构暂时不可见；需要扫动、多个相交切片或原位3D视图来重建整体。

## 评价证据

已打开官方Reformat文档，验证控件和精确参数；未测试应用，亦无任务研究数据。

## 交互

改变offset、origin、normal或三个旋转角；可将切面法向对齐当前相机。

## 实现与数据要求

需要三维标量/图像数据、世界坐标转换与切面插值；对只有封闭表面的模型只能得到几何截线而非内部影像。

## 来源核对

MPR是对已有体数据的重采样，解决特定切面可见性；官方文档未署出版年，year为null。

## 限制

斜切插值会受体素各向异性和原始分辨率影响，此为机制推论；文档未量化精度。

## 方法与关联

[[3D结构透视研究/方法/09 联动多视窗、切片图册与小图|联动多视窗、切片图册与小图]]

- [[3D结构透视研究/来源/med-08 CPR - Curved Planar Reformation|med-08 · CPR - Curved Planar Reformation (2002)]]
- [[3D结构透视研究/来源/med-13 3D Slicer documentation- Volume rendering|med-13 · 3D Slicer documentation: Volume rendering (未核实年份)]]
