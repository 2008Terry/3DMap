---
type: research-source
created: '2026-10-15'
updated: '2026-10-15'
status: 文献研究，未本地复现
id: proj-10
year: 2000
source_type: paper
evidence: full-primary
methods:
- conformal flattening
- Laplace–Beltrami finite elements
- cine distortion correction
domains:
- 管状器官内表面
- 虚拟结肠镜
- 医学
source_url: https://repository.gatech.edu/server/api/core/bitstreams/787dbaab-cb92-48fa-bae2-2bed515c7500/content
accessed: '2026-10-15'
method_families:
- 08
---

# Nondistorting Flattening Maps and the 3-D Visualization of Colon CT Images

返回 [[3D结构透视研究/00 3D结构透视研究 Dashboard|研究 Dashboard]] · [[3D结构透视研究/03 来源索引|来源索引]]

[原始来源](https://repository.gatech.edu/server/api/core/bitstreams/787dbaab-cb92-48fa-bae2-2bed515c7500/content)

作者/机构：Steven Haker; Sigurd Angenent; Allen Tannenbaum; Ron Kikinis。年份：2000。证据层级：全文级原始资料。

## 机制

从三角网格内壁离散Laplace–Beltrami算子，利用有限元和边界条件将管状表面共形铺平；通过动态显示的局部尺度修正检查表面。

## 能够显露的信息

把弯折器官的隐藏内壁作为平面图册浏览，使褶皱深处不再按原相机方向相互遮挡；对象是二维曲面，非任意三维实体内部。

## 几何与坐标

建立新的二维参数域并改变表面显示坐标；原网格可以保存，平面位置不是解剖位置。

## 代价

共形保角不等于整体保长度、面积和原位置；标题中的nondistorting包含动态局部校正，不能简化为一张平图全局无失真。

## 评价证据

2000年7月IEEE TMI 19(7),665–670；论文提供CT表面映射及动态校正实例，属于算法验证，不是临床诊断效能定论。

## 交互

以cine连续检查不同局部，使校正尺度跟随查看区域；联动原三维位置可补回空间定位。

## 实现与数据要求

需要可靠分割、三角化内壁、拓扑处理、边界选择、稀疏线性求解与纹理/属性重采样。

## 来源核对

已打开Georgia Tech学术库6页原论文，封面明确2000年7月；摘要明确使用保角映射和实时cine公式纠正失真。

## 限制

只解决可参数化表面显示；把建筑所有房间墙面拼成图册需另定义切缝、门户关系及重复边界。

## 方法与关联

[[3D结构透视研究/方法/08 曲面重采样、解缠与表面展开|曲面重采样、解缠与表面展开]]

- [[3D结构透视研究/来源/proj-11 Volumetric Colon Wall Unfolding Using Harmonic Differentials|proj-11 · Volumetric Colon Wall Unfolding Using Harmonic Differentials (2011)]]
- [[3D结构透视研究/来源/proj-12 Unlocking History through Automated Virtual Unfolding of Sealed Docu|proj-12 · Unlocking History through Automated Virtual Unfolding of Sealed Documents Imaged by X-ray Microtomography (2021)]]
- [[3D结构透视研究/来源/proj-13 HippoMaps- Multiscale Cartography of Human Hippocampal Organization|proj-13 · HippoMaps: Multiscale Cartography of Human Hippocampal Organization (2025)]]
