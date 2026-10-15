---
type: research-source
created: '2026-10-15'
updated: '2026-10-15'
status: 文献研究，未本地复现
id: tech-04
year: 2011
source_type: paper
evidence: full-primary
methods:
- multiperspective explosion
- optimized inset views
- automatic viewpoint selection
- small-part labels
domains:
- CAD
- technical manuals
source_url: https://markustatzgern.com/papers/2011_cag_multiperspective_compact.pdf
accessed: '2026-10-15'
method_families:
- '05'
- '07'
---

# Multi-perspective Compact Explosion Diagrams

返回 [[3D结构透视研究/00 3D结构透视研究 Dashboard|研究 Dashboard]] · [[3D结构透视研究/03 来源索引|来源索引]]

[原始来源](https://markustatzgern.com/papers/2011_cag_multiperspective_compact.pdf)

作者/机构：Markus Tatzgern, Denis Kalkofen, Dieter Schmalstieg。年份：2011。证据层级：全文级原始资料。

## 机制

在紧凑爆炸布局之后检测难以看清的子装配，改用更好的次级视向生成嵌入图，并用标签连接主图；主图与嵌图保持可对应的布局，限制相机角度差。

## 能够显露的信息

同一页容纳原本互相遮挡或背面的装配细节；小部件可获得额外放大和标签。

## 几何与坐标

主图是展开后的位置，局部嵌图另用相机观察；几何形状一般保留，投影一致性让位于可见性。

## 代价

没有一个全局统一的透视，相同对象可能出现多次；读者需在主图和嵌图间建立对应，角度差过大时困难。

## 评价证据

15页全文展示CAD结果、优化及视角限制对比；结尾明确计划未来进行用户研究，不能声称已证明理解速度提升。

## 交互

布局参数和视点限制可调；特别适用于不能旋转的教材、印刷手册。

## 实现与数据要求

先完成代表组合优化，再检测糟糕的局部可见性，避免直接拿掉这些对象损害主图上下文。

## 来源核对

已打开作者15页论文，核对多视点、标签、角度约束和未来用户研究声明。

## 限制

这只是局部多视点拼接，不是一次投影中真实看见全部表面；重复结构推断仍可能遗漏实例差异。

## 方法与关联

[[3D结构透视研究/方法/05 层级、紧凑与多透视爆炸图|层级、紧凑与多透视爆炸图]] · [[3D结构透视研究/方法/07 广义相机、多透视与投影变化|广义相机、多透视与投影变化]]

- [[3D结构透视研究/来源/tech-03 Compact Explosion Diagrams|tech-03 · Compact Explosion Diagrams (2010)]]
- [[3D结构透视研究/来源/tech-08 Real-time External Labeling of Ghosted Views|tech-08 · Real-time External Labeling of Ghosted Views (2019)]]
