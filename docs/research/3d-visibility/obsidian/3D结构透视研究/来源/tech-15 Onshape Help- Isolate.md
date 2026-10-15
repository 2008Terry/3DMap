---
type: research-source
created: '2026-10-15'
updated: '2026-10-15'
status: 文献研究，未本地复现
id: tech-15
year: 2026
source_type: official-doc
evidence: official-doc
methods:
- focus opacity
- context ghosting
- connectivity expansion
- proximity expansion
- transparent selection
domains:
- CAD
- assembly inspection
source_url: https://cad.onshape.com/help/Content/View/isolate.htm
accessed: '2026-10-15'
method_families:
- '01'
---

# Onshape Help: Isolate

返回 [[3D结构透视研究/00 3D结构透视研究 Dashboard|研究 Dashboard]] · [[3D结构透视研究/03 来源索引|来源索引]]

[原始来源](https://cad.onshape.com/help/Content/View/isolate.htm)

作者/机构：Onshape / PTC。年份：2026。证据层级：官方文档。

## 机制

让被选实体保持不透明，其他实体透明；滑条分别控制透明对象外缘与内部几何的呈现。还可按物理距离或配合连接逐步把更多上下文恢复为不透明。

## 能够显露的信息

能看见、选择、测量和编辑被外壳挡住的边、面、点、Mate connector；轮廓可以保留为定位参照。

## 几何与坐标

无几何位移，只有显示与交互可选性的变化。

## 代价

透明叠层仍有颜色与深度歧义；完全淡出上下文时会失去包围关系，透明对象是否可选也需明确设置。

## 评价证据

官方文档详细列出功能、示例和限制；没有证明其比切口或爆炸图更有效的控制实验。

## 交互

Shift+i累积隔离、Shift+t反向使选中者透明、透明几何选择开关、距离与连接扩张。

## 实现与数据要求

按连接扩张只在Assembly可用；文档注明iOS只支持距离扩张。退出可恢复可见状态。

## 来源核对

已打开完整官方页面，核对滑条非简单统一alpha、透明选择和平台差异；更新日期2026-10-09。

## 限制

Expand在这里是焦点集合扩张，不是空间爆炸；不能误写成自动把零件推开。

## 方法与关联

[[3D结构透视研究/方法/01 透明、转移函数与OIT|透明、转移函数与OIT]]

- [[3D结构透视研究/来源/tech-07 Transparency in Interactive Technical Illustrations|tech-07 · Transparency in Interactive Technical Illustrations (2002)]]
- [[3D结构透视研究/来源/tech-08 Real-time External Labeling of Ghosted Views|tech-08 · Real-time External Labeling of Ghosted Views (2019)]]
- [[3D结构透视研究/来源/tech-14 Onshape Help- Section View|tech-14 · Onshape Help: Section View (2026)]]
- [[3D结构透视研究/来源/tech-16 Onshape Help- Exploded Views|tech-16 · Onshape Help: Exploded Views (2026)]]
