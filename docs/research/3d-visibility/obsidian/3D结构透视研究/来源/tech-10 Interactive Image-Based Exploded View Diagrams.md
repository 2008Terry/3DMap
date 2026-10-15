---
type: research-source
created: '2026-10-15'
updated: '2026-10-15'
status: 文献研究，未本地复现
id: tech-10
year: 2004
source_type: paper
evidence: abstract-primary
methods:
- 2.5D image-layer explosion
- expand/collapse
- part search
domains:
- legacy technical illustrations
- mechanical manuals
source_url: https://grail.cs.washington.edu/projects/exview/
accessed: '2026-10-15'
method_families:
- '05'
---

# Interactive Image-Based Exploded View Diagrams

返回 [[3D结构透视研究/00 3D结构透视研究 Dashboard|研究 Dashboard]] · [[3D结构透视研究/03 来源索引|来源索引]]

[原始来源](https://grail.cs.washington.edu/projects/exview/)

作者/机构：Wilmot Li, Maneesh Agrawala, David Salesin。年份：2004。证据层级：原始摘要或受限索引。

## 机制

把现有二维爆炸插图半自动拆成可控的层，作者指定部件的展开、合拢和相互遮挡关系；用户拖动或搜索即可动态筛选细节，不必先建立完整三维CAD模型。

## 能够显露的信息

已有图片中绘制的完整零件和装配层次可被逐步展开，保留原图任意手绘或技术风格。

## 几何与坐标

移动的是二维/2.5D图层，模型不是可测量的真实三维实体；原位距离在展开时改变。

## 代价

它不能显示原图根本没画出的背面和内部，也不支持任意三维相机；2.5D层次不自动证明实际装配可行。

## 评价证据

作者项目页以主缸等示例说明少量创作工作可产生交互图；页面未提供对照用户研究或准确率数据。

## 交互

直接展开/收拢，动态信息过滤和单独零件搜索。

## 实现与数据要求

适合历史手册、插图再利用；需要分层与作者标注遮挡关系，但避免完整三维建模成本。

## 来源核对

已打开UW作者项目页，确认以二维图像为输入、半自动作者工具、2.5D表示和查看界面。

## 限制

奖项和示例不替代用户实证；应与自动三维爆炸图分开，不能将两者能力混写。

## 方法与关联

[[3D结构透视研究/方法/05 层级、紧凑与多透视爆炸图|层级、紧凑与多透视爆炸图]]

- [[3D结构透视研究/来源/tech-02 Automated Generation of Interactive 3D Exploded View Diagrams|tech-02 · Automated Generation of Interactive 3D Exploded View Diagrams (2008)]]
- [[3D结构透视研究/来源/tech-04 Multi-perspective Compact Explosion Diagrams|tech-04 · Multi-perspective Compact Explosion Diagrams (2011)]]
