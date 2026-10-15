---
type: research-source
created: '2026-10-15'
updated: '2026-10-15'
status: 文献研究，未本地复现
id: tech-13
year: 2003
source_type: paper
evidence: abstract-primary
methods:
- illustration-derived cutaway rules
- interactive cutaway rendering
- style-independent disclosure
domains:
- technical illustration
- solid opaque models
source_url: https://onlinelibrary.wiley.com/doi/10.1111/1467-8659.t01-3-00700
accessed: '2026-10-15'
method_families:
- '03'
---

# Interactive Cutaway Illustrations

返回 [[3D结构透视研究/00 3D结构透视研究 Dashboard|研究 Dashboard]] · [[3D结构透视研究/03 来源索引|来源索引]]

[原始来源](https://onlinelibrary.wiley.com/doi/10.1111/1467-8659.t01-3-00700)

作者/机构：Joachim Diepstraten, Daniel Weiskopf, Thomas Ertl。年份：2003。证据层级：原始摘要或受限索引。

## 机制

分析传统切开插图，从中提炼一组用于计算机生成的规则，并用当时图形硬件功能实现交互。其核心是有选择地去除外部遮挡、仍用插图风格交代外形与内部，而非复制物理材质。

## 能够显露的信息

让原本实心不透明对象里的结构可被查看，并允许与多种艺术或技术绘制风格搭配。

## 几何与坐标

改变哪些对象片段被渲染，内部目标仍可维持原位；不意味着必须把实体数据永久修改。

## 代价

被省略部分无法在同一视图检查；切口需要解释清楚，否则容易把展示用省略误读为真实缺口。

## 评价证据

出版商摘要确认多种风格结合及交互帧率；未读取受控理解实验或场景规模数字，不据此断言知觉效果已普遍验证。

## 交互

交互帧率下切口观察；摘要未详列具体控件，因此不杜撰产品式操作。

## 实现与数据要求

为后来的自适应切口提供插图原则和硬件渲染起点；今天实现需要替换旧式图形API。

## 来源核对

已打开Wiley原始页面，卷22第3期、523–532页，2003；只读摘要及书目信息。

## 限制

作为基础源的价值是设计传统和方法类别；本次证据不足以复原其全部规则或复现性能。

## 方法与关联

[[3D结构透视研究/方法/03 平面、目标驱动与非平面剖切|平面、目标驱动与非平面剖切]]

- [[3D结构透视研究/来源/tech-01 Interactive Cutaway Illustrations of Complex 3D Models|tech-01 · Interactive Cutaway Illustrations of Complex 3D Models (2007)]]
- [[3D结构透视研究/来源/tech-06 Adaptive Cutaways for Comprehensible Rendering of Polygonal Scenes|tech-06 · Adaptive Cutaways for Comprehensible Rendering of Polygonal Scenes (2008)]]
- [[3D结构透视研究/来源/tech-07 Transparency in Interactive Technical Illustrations|tech-07 · Transparency in Interactive Technical Illustrations (2002)]]
