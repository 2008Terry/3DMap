---
type: research-source
created: '2026-10-15'
updated: '2026-10-15'
status: 文献研究，未本地复现
id: proj-07
year: 2016
source_type: paper
evidence: full-primary
methods:
- constrained optimization
- view elevation
- road shifting
- building scaling
- building displacement
domains:
- 城市可视化
- 导航路线
- 重要地理要素
source_url: https://geogother.bnu.edu.cn/teacherweb/zhangliqiang/papers/Interactive%20Urban%20Context-Aware%20Visualization-proof.pdf
accessed: '2026-10-15'
method_families:
- '03'
- '10'
- '12'
---

# Interactive Urban Context-Aware Visualization via Multiple Disocclusion Operators

返回 [[3D结构透视研究/00 3D结构透视研究 Dashboard|研究 Dashboard]] · [[3D结构透视研究/03 来源索引|来源索引]]

[原始来源](https://geogother.bnu.edu.cn/teacherweb/zhangliqiang/papers/Interactive%20Urban%20Context-Aware%20Visualization-proof.pdf)

作者/机构：Hao Deng; Liqiang Zhang; Xiancheng Mao; Huamin Qu。年份：2016。证据层级：全文级原始资料。

## 机制

联合视点抬高、道路位移、建筑缩放与建筑位移四种操作，以约束优化和后处理在目标可见与城市失真之间寻找折中。

## 能够显露的信息

让被成簇建筑挡住的兴趣要素、路线和信息覆盖得到清晰总览；目标必须先定义，算法不是枚举所有建筑内部。

## 几何与坐标

除相机变化外明确修改对象位置和缩放，不能作为精确建筑测量视图。

## 代价

保持城市外观近似需要让多个操作分担变形，但建筑精确位置、体积和道路尺度仍发生变化；同时显示大量目标会增加约束冲突。

## 评价证据

原论文与作者稿展示真实城市数据的交互结果及导航、寻路、信息覆盖场景；未在此摘录未经进一步核对的参与人数或效应量。

## 交互

随用户关注目标提供上下文感知去遮挡；恢复原布局或动画对应是应用设计的必要配套。

## 实现与数据要求

需建筑分组、道路与兴趣要素语义、可见性约束、优化器及后处理；迁移到室内应先界定允许移动的墙、家具或楼层。

## 来源核对

已打开北京师范大学作者13页校样PDF，书目信息以正式TVCG 22(7),1862–1874及2016年7月为准；DOI含2015不等于卷期年份。

## 限制

研究关注城市外部要素；将其变形优化用于室内是可行性推断，尚非该文已验证结论。

## 方法与关联

[[3D结构透视研究/方法/03 平面、目标驱动与非平面剖切|平面、目标驱动与非平面剖切]] · [[3D结构透视研究/方法/10 时间扫描、路径游览与运动视差|时间扫描、路径游览与运动视差]] · [[3D结构透视研究/方法/12 可见性度量与自动显露优化|可见性度量与自动显露优化]]

- [[3D结构透视研究/来源/proj-08 Multi-perspective occlusion-free urban navigation visualization|proj-08 · Multi-perspective occlusion-free urban navigation visualization (2026)]]
- [[3D结构透视研究/来源/proj-09 Occlusion-Free Conformal Lensing for Spatiotemporal Visualization in|proj-09 · Occlusion-Free Conformal Lensing for Spatiotemporal Visualization in 3D Urban Analytics (2026)]]
- [[3D结构透视研究/来源/proj-19 The State of the Art in Visual Analytics for 3D Urban Data|proj-19 · The State of the Art in Visual Analytics for 3D Urban Data (2024)]]
