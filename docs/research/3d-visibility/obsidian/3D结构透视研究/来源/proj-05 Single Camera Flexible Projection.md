---
type: research-source
created: '2026-10-15'
updated: '2026-10-15'
status: 文献研究，未本地复现
id: proj-05
year: 2007
source_type: paper
evidence: abstract-primary
methods:
- flexible viewing volume
- curved projectors
- nonlinear projection
domains:
- 艺术投影
- 计算机图形学
- 可定制相机
source_url: https://brosz.ca/research/projection/index.html
accessed: '2026-10-15'
method_families:
- '07'
---

# Single Camera Flexible Projection

返回 [[3D结构透视研究/00 3D结构透视研究 Dashboard|研究 Dashboard]] · [[3D结构透视研究/03 来源索引|来源索引]]

[原始来源](https://brosz.ca/research/projection/index.html)

作者/机构：John Brosz; Faramarz Samavati; Sheelagh Carpendale; Mario Costa Sousa。年份：2007。证据层级：原始摘要或受限索引。

## 机制

用参数化体积定义近远裁剪面和投射线，允许视锥及投射线弯曲，在单个相机框架内形成线性、非线性和手工艺术投影。

## 能够显露的信息

可针对场景让射线绕向侧面或汇集通常不兼容的局部视图；提供设计可见性分配的基础，不能自动判定每个内部部件应出现在哪里。

## 几何与坐标

原模型坐标可保留，变化发生在视体、射线和屏幕映射；并非把所有物体搬开。

## 代价

画面可能弯曲、非均匀放大，屏幕到世界点的逆映射更复杂；相机模型自由度高会增加设计与理解负担。

## 评价证据

作者页展示投影样例，论文摘要说明光线投射和受限GPU扫描转换两种渲染方式；本次完整PDF因大小限制未成功解析，不报告其具体速度或用户实验。

## 交互

以参数或控制点调整弯曲视体；对应界面需要另行设计。

## 实现与数据要求

需参数化视体、按曲线采样射线和相交运算，或实现其适用范围有限的GPU近似；标准透视相机插件不足以完整实现。

## 来源核对

已打开作者页，确认NPAR 2007与后续2009/2010扩展；大学论文索引的原文摘要可访问，完整11MB PDF尝试受大小限制。

## 限制

本文证明投影表达能力，不证明对任意场景存在不失真、无重复、无限分辨率的完全可见图。

## 方法与关联

[[3D结构透视研究/方法/07 广义相机、多透视与投影变化|广义相机、多透视与投影变化]]

- [[3D结构透视研究/来源/proj-01 General Linear Cameras|proj-01 · General Linear Cameras (2004)]]
- [[3D结构透视研究/来源/proj-02 The Graph Camera (Purdue Technical Report 08-005)|proj-02 · The Graph Camera (Purdue Technical Report 08-005) (2008)]]
- [[3D结构透视研究/来源/proj-20 Multiperspective Modeling, Rendering, and Imaging|proj-20 · Multiperspective Modeling, Rendering, and Imaging (2008)]]
