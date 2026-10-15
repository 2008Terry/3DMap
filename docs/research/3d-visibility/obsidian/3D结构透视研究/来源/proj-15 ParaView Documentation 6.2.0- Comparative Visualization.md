---
type: research-source
created: '2026-10-15'
updated: '2026-10-15'
status: 文献研究，未本地复现
id: proj-15
year: null
source_type: official-doc
evidence: official-doc
methods:
- small multiples
- parameter study
- linked interactions
domains:
- 参数比较
- 多切片
- 分层图册
source_url: https://docs.paraview.org/en/latest/ReferenceManual/comparativeViews.html
accessed: '2026-10-15'
method_families:
- 09
---

# ParaView Documentation 6.2.0: Comparative Visualization

返回 [[3D结构透视研究/00 3D结构透视研究 Dashboard|研究 Dashboard]] · [[3D结构透视研究/03 来源索引|来源索引]]

[原始来源](https://docs.paraview.org/en/latest/ReferenceManual/comparativeViews.html)

作者/机构：ParaView / Kitware。年份：未核实，见来源核对说明。证据层级：官方文档。

## 机制

建立可配置m×n内部渲染视图，让同一数据与显示属性同步，按视图改变过滤器参数或时间值；交互同步更新。

## 能够显露的信息

可把不同楼层高度、剖切深度、时间或阈值的结果同时排列，避免仅靠滑块前后记忆；采用切片参数时可做内部结构联系图。

## 几何与坐标

各视图保留源几何坐标；增加的是独立显示空间，不是移动实体。

## 代价

小图数量多会降低每图可辨信息；所有视图都显示同一原模型时仍有普通遮挡，必须配合切片或其他过滤器。

## 评价证据

官方文档给出工作流程和参数比较示例；未声称小倍图在所有空间任务上优于单图。

## 交互

共享颜色、表示和相机交互，统一改变参数范围；支持叠加全部比较结果，但叠加可能重新形成遮挡。

## 实现与数据要求

需共享数据状态、每视窗的参数与可见性、同步选择/相机；单页面WebGL scissor viewports或离屏纹理均是工程推断。

## 来源核对

已打开官方Comparative View全文；m×n、参数/时间变化、属性同步和交互联动均明确记载。无明确发布日期，year=null。

## 限制

软件示例用于参数研究；转换成楼层图册的设计属于应用推断，需单独实现覆盖与对应关系。

## 方法与关联

[[3D结构透视研究/方法/09 联动多视窗、切片图册与小图|联动多视窗、切片图册与小图]]

- [[3D结构透视研究/来源/proj-14 ParaView Documentation 6.2.0- Displaying Data|proj-14 · ParaView Documentation 6.2.0: Displaying Data (未核实年份)]]
- [[3D结构透视研究/来源/proj-16 3D Slicer User Interface- Slice Views, View Linking and Cross-Refere|proj-16 · 3D Slicer User Interface: Slice Views, View Linking and Cross-Reference (未核实年份)]]
- [[3D结构透视研究/来源/proj-17 OGC IndoorGML 2.0 Part 1- Conceptual Model|proj-17 · OGC IndoorGML 2.0 Part 1: Conceptual Model (2025)]]
