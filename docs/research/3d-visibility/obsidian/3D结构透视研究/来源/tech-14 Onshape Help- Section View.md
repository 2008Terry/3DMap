---
type: research-source
created: '2026-10-15'
updated: '2026-10-15'
status: 文献研究，未本地复现
id: tech-14
year: 2026
source_type: official-doc
evidence: official-doc
methods:
- interactive planar section
- multiple section planes
- include/exclude components
- section interference coloring
domains:
- CAD
- Part Studio
- assembly
source_url: https://cad.onshape.com/help/Content/View/section_view.htm
accessed: '2026-10-15'
method_families:
- '03'
---

# Onshape Help: Section View

返回 [[3D结构透视研究/00 3D结构透视研究 Dashboard|研究 Dashboard]] · [[3D结构透视研究/03 来源索引|来源索引]]

[原始来源](https://cad.onshape.com/help/Content/View/section_view.htm)

作者/机构：Onshape / PTC。年份：2026。证据层级：官方文档。

## 机制

选择平面、面或Mate connector建立一个或多个剖切面，拖动或数值设置深度和角度；可以明确包含/排除被剖切部件，使目标完整保留、外壳被切开。

## 能够显露的信息

揭示孔、空腔、内装零件和截面；相交部件默认红色可提示干涉，还可对截面可见的面、边、点测量。

## 几何与坐标

剖切显示而非移动零件，原始装配位置保留；可开关恢复。

## 代价

只展示保留半空间与切面，其他区域在当前视图消失；弯曲结构可能无法用单个平面全部揭示。

## 评价证据

官方逐步操作文档和截图证明控件存在，不是对其理解收益的用户研究；本次未操作实际账户模型。

## 交互

平移/角度操纵器、数值输入、翻转、切换默认面、保存Named View、重新编辑。

## 实现与数据要求

这些是现成CAD模式，组合多个平面和排除列表即可形成局部上下文剖切。

## 来源核对

已打开完整官方文档；页面明确Last Updated: October 09, 2026，year据此记录。

## 限制

文档证明功能而非任意场景全可见；include/exclude操作不等于自动求最优切口。

## 方法与关联

[[3D结构透视研究/方法/03 平面、目标驱动与非平面剖切|平面、目标驱动与非平面剖切]]

- [[3D结构透视研究/来源/tech-01 Interactive Cutaway Illustrations of Complex 3D Models|tech-01 · Interactive Cutaway Illustrations of Complex 3D Models (2007)]]
- [[3D结构透视研究/来源/tech-09 Design Principles for Cutaway Visualization of Geological Models|tech-09 · Design Principles for Cutaway Visualization of Geological Models (2012)]]
- [[3D结构透视研究/来源/tech-15 Onshape Help- Isolate|tech-15 · Onshape Help: Isolate (2026)]]
- [[3D结构透视研究/来源/tech-17 Autodesk Fusion Help- Create a 3D section view|tech-17 · Autodesk Fusion Help: Create a 3D section view (未核实年份)]]
