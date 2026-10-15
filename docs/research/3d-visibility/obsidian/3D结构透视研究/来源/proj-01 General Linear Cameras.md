---
type: research-source
created: '2026-10-15'
updated: '2026-10-15'
status: 文献研究，未本地复现
id: proj-01
year: 2004
source_type: paper
evidence: full-primary
methods:
- generalized camera
- two-plane ray parameterization
- multiperspective projection
domains:
- 计算机图形学
- 计算成像
source_url: https://groups.csail.mit.edu/graphics/pubs/eccv2004_linearcameras.pdf
accessed: '2026-10-15'
method_families:
- '07'
---

# General Linear Cameras

返回 [[3D结构透视研究/00 3D结构透视研究 Dashboard|研究 Dashboard]] · [[3D结构透视研究/03 来源索引|来源索引]]

[原始来源](https://groups.csail.mit.edu/graphics/pubs/eccv2004_linearcameras.pdf)

作者/机构：Jingyi Yu; Leonard McMillan。年份：2004。证据层级：全文级原始资料。

## 机制

用两平面交点给视线四维参数，并将三条生成射线的仿射组合定义为相机；统一针孔、正交、推扫、双狭缝等模型。这里的四维是射线空间，不能理解为额外空间维度让人直接绕过所有实体。

## 能够显露的信息

可把通常需要多个视点的特征组织在同一图像中；给长走廊、街区等设计不同方向或位置的采样视线提供基础。论文本身没有自动寻找建筑所有内表面的算法。

## 几何与坐标

原始三维顶点无需移动；改变的是像素与射线之间的映射，因此屏幕上的位置与普通透视不一致。

## 代价

局部透视关系、尺度和直线形状可能改变，某些相机类型具有退化或特殊成像性质；射线仍会命中首先遇到的遮挡物。

## 评价证据

论文给出相机分类、几何推导和合成图像示例，属于数学与图形验证；未给出完整建筑内部覆盖率或用户研究。

## 交互

相机生成射线和图像区域可由应用配置；并非现成的房间交互界面。

## 实现与数据要求

需实现按像素生成射线的光线追踪，或从已有光场取样；常规单个4×4投影矩阵不足以覆盖全部类型。

## 来源核对

已打开MIT作者PDF，14页；正文明确把GLC定义为四维射线参数空间中的二维仿射子空间，并列出八种标准相机类型。

## 限制

提供通用相机表达，不提供无条件内部可见保证；遮挡处理还需目标选择、路径构造、裁切或其他表示。

## 方法与关联

[[3D结构透视研究/方法/07 广义相机、多透视与投影变化|广义相机、多透视与投影变化]]

- [[3D结构透视研究/来源/proj-02 The Graph Camera (Purdue Technical Report 08-005)|proj-02 · The Graph Camera (Purdue Technical Report 08-005) (2008)]]
- [[3D结构透视研究/来源/proj-05 Single Camera Flexible Projection|proj-05 · Single Camera Flexible Projection (2007)]]
- [[3D结构透视研究/来源/proj-20 Multiperspective Modeling, Rendering, and Imaging|proj-20 · Multiperspective Modeling, Rendering, and Imaging (2008)]]
