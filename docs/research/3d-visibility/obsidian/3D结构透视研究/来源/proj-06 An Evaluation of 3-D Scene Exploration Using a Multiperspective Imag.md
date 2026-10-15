---
type: research-source
created: '2026-10-15'
updated: '2026-10-15'
status: 文献研究，未本地复现
id: proj-06
year: 2011
source_type: paper
evidence: full-primary
methods:
- graph camera
- multiperspective user study
domains:
- 迷宫搜索
- 计数
- 空间定向
source_url: https://www.cs.purdue.edu/xrlab/assets/pdf/popescuGC_CGI2011.pdf
accessed: '2026-10-15'
method_families:
- '07'
- '10'
- '13'
---

# An Evaluation of 3-D Scene Exploration Using a Multiperspective Image Framework

返回 [[3D结构透视研究/00 3D结构透视研究 Dashboard|研究 Dashboard]] · [[3D结构透视研究/03 来源索引|来源索引]]

[原始来源](https://www.cs.purdue.edu/xrlab/assets/pdf/popescuGC_CGI2011.pdf)

作者/机构：Paul Rosen; Voicu Popescu。年份：2011。证据层级：全文级原始资料。

## 机制

使用可调多透视框架，把遮挡目标映射到不同画面区域，并将去遮挡能力与图像复杂度作为可调权衡。

## 能够显露的信息

让侧走廊中的静态和动态目标同时出现，支持发现、搜索和计数，而非通过连续相机旅行记忆目标。

## 几何与坐标

三维几何不移动，屏幕空间关系被重组；原位置可通过另一个正常视图或点选映射保留参照。

## 代价

发现与计数更好不代表空间定向更好；多透视改变全局关系，画面足够大仍受用户并行处理能力限制。

## 评价证据

47人完成搜索、计数与空间定向任务；摘要报告搜索平均快28%，计数准确率91%对普通图像42%。问卷路径匹配略偏普通相机；实验是抽象迷宫而非真实建筑。

## 交互

支持交互导航与动态场景；论文区分短时观看和多次练习情形。

## 实现与数据要求

需要graph camera渲染基础、可控视锥图和用于实验的真实目标覆盖记录；应用时应另测房间辨认、上下楼和距离理解。

## 来源核对

已打开Purdue完整10页作者稿并核对实验、表格与结论；作者明确讨论封闭发动机等无直接可达射线情况需结合透明，以及全局空间理解可能不适用。

## 限制

受控任务的显著收益不能外推到所有BIM、任意室内模型或全部结构同时理解。

## 方法与关联

[[3D结构透视研究/方法/07 广义相机、多透视与投影变化|广义相机、多透视与投影变化]] · [[3D结构透视研究/方法/10 时间扫描、路径游览与运动视差|时间扫描、路径游览与运动视差]] · [[3D结构透视研究/方法/13 感知、评价与失败模式|感知、评价与失败模式]]

- [[3D结构透视研究/来源/proj-02 The Graph Camera (Purdue Technical Report 08-005)|proj-02 · The Graph Camera (Purdue Technical Report 08-005) (2008)]]
- [[3D结构透视研究/来源/proj-04 Automatic Multiperspective Images|proj-04 · Automatic Multiperspective Images (2006)]]
- [[3D结构透视研究/来源/proj-16 3D Slicer User Interface- Slice Views, View Linking and Cross-Refere|proj-16 · 3D Slicer User Interface: Slice Views, View Linking and Cross-Reference (未核实年份)]]
