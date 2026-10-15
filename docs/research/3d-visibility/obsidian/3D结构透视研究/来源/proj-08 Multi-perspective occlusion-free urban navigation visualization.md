---
type: research-source
created: '2026-10-15'
updated: '2026-10-15'
status: 文献研究，未本地复现
id: proj-08
year: 2026
source_type: paper
evidence: abstract-primary
methods:
- undulating curved projection surface
- route segmentation
- distance-weighted building displacement and scaling
domains:
- 城市导航
- focus+context
source_url: https://www.sciencedirect.com/science/article/pii/S1569843225007216
accessed: '2026-10-15'
method_families:
- '07'
- '12'
---

# Multi-perspective occlusion-free urban navigation visualization

返回 [[3D结构透视研究/00 3D结构透视研究 Dashboard|研究 Dashboard]] · [[3D结构透视研究/03 来源索引|来源索引]]

[原始来源](https://www.sciencedirect.com/science/article/pii/S1569843225007216)

作者/机构：Shen Ying; Haoran Yang; Junru Su。年份：2026。证据层级：原始摘要或受限索引。

## 机制

用起伏曲面承接多透视投影，再按路线分段调整相机倾角与视场角；通过基于用户距离的权重移动和缩放挡路建筑。

## 能够显露的信息

单屏同时容纳较大城市范围与局部路线细节，使导航路线免于相关建筑遮挡；不以室内墙体或全部体积结构为对象。

## 几何与坐标

同时改变投影与建筑位置/尺度，不保留严格原位置。

## 代价

路线可见是选择性目标；建筑地理位置和大小被调整，多透视产生尺度变化。所谓occlusion-free必须限定为文中的导航路线。

## 评价证据

出版商摘要报告巴塞罗那区域案例及信息细节度量，并与单调圆柱曲面和固定权重方法比较；无法核对全文实验参数和普适性。

## 交互

距离权重和焦点到上下文转换随观察关系调整；具体操作界面未在可访问摘要中说明。

## 实现与数据要求

摘要可证需要路线分段、曲面参数、相机倾角/FOV以及遮挡建筑优化；求解细节待取得全文。

## 来源核对

出版商原始索引返回完整摘要与卷146、105074、2026年2月；DOI为10.1016/j.jag.2025.105074。已尝试直接打开出版商页，返回403；因此仅记摘要证据。

## 限制

不把DOI中的2025误写为卷期日期；未取得全文，不能验证其所谓无挡路线保证的约束、失败案例或用户效应。

## 方法与关联

[[3D结构透视研究/方法/07 广义相机、多透视与投影变化|广义相机、多透视与投影变化]] · [[3D结构透视研究/方法/12 可见性度量与自动显露优化|可见性度量与自动显露优化]]

- [[3D结构透视研究/来源/proj-07 Interactive Urban Context-Aware Visualization via Multiple Disocclus|proj-07 · Interactive Urban Context-Aware Visualization via Multiple Disocclusion Operators (2016)]]
- [[3D结构透视研究/来源/proj-03 Interactive Design of Multi-Perspective Images for Visualizing Urban|proj-03 · Interactive Design of Multi-Perspective Images for Visualizing Urban Landscapes (2004)]]
- [[3D结构透视研究/来源/proj-09 Occlusion-Free Conformal Lensing for Spatiotemporal Visualization in|proj-09 · Occlusion-Free Conformal Lensing for Spatiotemporal Visualization in 3D Urban Analytics (2026)]]
