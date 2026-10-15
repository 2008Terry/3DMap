---
type: research-source
created: '2026-10-15'
updated: '2026-10-15'
status: 文献研究，未本地复现
id: tech-01
year: 2007
source_type: paper
evidence: abstract-primary
methods:
- geometry-aware cutaway
- target-driven disclosure
- cut-surface shading
domains:
- CAD
- anatomy
- technical illustration
source_url: https://grail.cs.washington.edu/projects/cutaways/
accessed: '2026-10-15'
method_families:
- '03'
- '12'
---

# Interactive Cutaway Illustrations of Complex 3D Models

返回 [[3D结构透视研究/00 3D结构透视研究 Dashboard|研究 Dashboard]] · [[3D结构透视研究/03 来源索引|来源索引]]

[原始来源](https://grail.cs.washington.edu/projects/cutaways/)

作者/机构：Wilmot Li, Lincoln Ritter, Maneesh Agrawala, Brian Curless, David Salesin。年份：2007。证据层级：原始摘要或受限索引。

## 机制

作者先给每个部件添加几何类型和切口参数，即rigging；浏览者只选择内部目标，系统据此自动切开遮挡物，并保留周围结构。相比统一平面切割，切口顺应管、盒、壳等部件的形状。

## 能够显露的信息

暴露目标的形状、原位朝向及其与邻近部件的关系，外壳局部和切面继续提供包含、层次和厚度线索。

## 几何与坐标

目标保持原始坐标；上下文局部被显示性切除，不是把目标移到外面。

## 代价

被切去的遮挡部分在当前画面缺失；目标并不等于全部内部结构同时可见。作者必须了解模型、指定好视点及修正自动切口。

## 评价证据

论文全文的公开索引报告示例约90%的部件可自动完成切口映射，并明确没有正式用户研究；医学教育者、插画师等反馈属于非正式证据。

## 交互

选择目标结构、高层切口控制、旋转查看；创作者另有半自动和草图式rigging界面。

## 实现与数据要求

适合带独立部件及几何语义的模型；不是仅靠最终截图就能应用的通用滤镜。

## 来源核对

已打开UW作者项目页；其摘要确认几何感知rigging与目标选择。全文PDF超过工具大小限制，评价细节仅核对作者PDF索引返回段落。

## 限制

本次未完整打开11页PDF，因此不把示例成效当作普遍的理解提升或任意模型保证。

## 方法与关联

[[3D结构透视研究/方法/03 平面、目标驱动与非平面剖切|平面、目标驱动与非平面剖切]] · [[3D结构透视研究/方法/12 可见性度量与自动显露优化|可见性度量与自动显露优化]]

- [[3D结构透视研究/来源/tech-02 Automated Generation of Interactive 3D Exploded View Diagrams|tech-02 · Automated Generation of Interactive 3D Exploded View Diagrams (2008)]]
- [[3D结构透视研究/来源/tech-06 Adaptive Cutaways for Comprehensible Rendering of Polygonal Scenes|tech-06 · Adaptive Cutaways for Comprehensible Rendering of Polygonal Scenes (2008)]]
- [[3D结构透视研究/来源/tech-09 Design Principles for Cutaway Visualization of Geological Models|tech-09 · Design Principles for Cutaway Visualization of Geological Models (2012)]]
