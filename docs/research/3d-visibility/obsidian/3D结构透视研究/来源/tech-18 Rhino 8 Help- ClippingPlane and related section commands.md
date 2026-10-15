---
type: research-source
created: '2026-10-15'
updated: '2026-10-15'
status: 文献研究，未本地复现
id: tech-18
year: null
source_type: official-doc
evidence: official-doc
methods:
- viewport-specific clipping
- finite-thickness slabs
- per-object exclusion
- section styles
- linked 2D section drawings
domains:
- CAD
- architecture
- NURBS and mesh modeling
source_url: https://docs.mcneel.com/rhino/8/help/en-us/commands/clippingplane.htm
accessed: '2026-10-15'
method_families:
- '03'
---

# Rhino 8 Help: ClippingPlane and related section commands

返回 [[3D结构透视研究/00 3D结构透视研究 Dashboard|研究 Dashboard]] · [[3D结构透视研究/03 来源索引|来源索引]]

[原始来源](https://docs.mcneel.com/rhino/8/help/en-us/commands/clippingplane.htm)

作者/机构：Robert McNeel & Associates。年份：未核实，见来源核对说明。证据层级：官方文档。

## 机制

创建指定视口使用的裁剪平面；可设置有限Custom Depth形成一定厚度的可见切片，按对象/图层控制被裁剪内容，设置截面样式并保存关联命名视图。

## 能够显露的信息

观察建筑或实体内部、厚切片和二维截面；相关命令可提取截面曲线、填充、隐藏线与背景轮廓用于图纸。

## 几何与坐标

ClippingPlane只影响可见性；ExtractClippingSlices则生成实际输出几何，只有闭合交线对象能输出切片。

## 代价

裁剪去掉上下文；二维输出投影牺牲深度。切面显示和真正提取实体切片是两种操作，不能混淆。

## 评价证据

官方长文档给出控件、截图及更新规则，证明可用功能；没有用户对照结果或全模型最佳可视性保证。

## 交互

移动平面和深度点、翻转、视口开关、命名视图、提取/导出图纸，厚度以模型单位设置。

## 实现与数据要求

关联图纸随平面移动更新，但输入几何编辑或新增对象后需UpdateClippingDrawings；不是所有更改都自动刷新。

## 来源核对

已打开完整Rhino8官方页，核对有限厚度、显示/几何提取区别及手动更新限制；页面日期不明，year为null。

## 限制

不把Rhino8产品名推定为网页年份或新技术年份；现成裁剪是用户指定操作，不能称为自动语义切口优化。

## 方法与关联

[[3D结构透视研究/方法/03 平面、目标驱动与非平面剖切|平面、目标驱动与非平面剖切]]

- [[3D结构透视研究/来源/tech-09 Design Principles for Cutaway Visualization of Geological Models|tech-09 · Design Principles for Cutaway Visualization of Geological Models (2012)]]
- [[3D结构透视研究/来源/tech-14 Onshape Help- Section View|tech-14 · Onshape Help: Section View (2026)]]
- [[3D结构透视研究/来源/tech-17 Autodesk Fusion Help- Create a 3D section view|tech-17 · Autodesk Fusion Help: Create a 3D section view (未核实年份)]]
