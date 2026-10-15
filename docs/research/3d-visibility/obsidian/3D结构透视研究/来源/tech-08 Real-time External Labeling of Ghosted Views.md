---
type: research-source
created: '2026-10-15'
updated: '2026-10-15'
status: 文献研究，未本地复现
id: tech-08
year: 2019
source_type: paper
evidence: full-primary
methods:
- opacity-aware label anchoring
- external label layout
- fuzzy multi-criteria optimization
domains:
- ghosted CAD
- technical illustration
- anatomy
source_url: https://dcgi.fel.cvut.cz/wp-content/wpallimport-dist/publications/pdf/publications-2019-cmolik-tvcg-rtgv-paper.pdf
accessed: '2026-10-15'
method_families:
- '02'
- '11'
- '13'
---

# Real-time External Labeling of Ghosted Views

返回 [[3D结构透视研究/00 3D结构透视研究 Dashboard|研究 Dashboard]] · [[3D结构透视研究/03 来源索引|来源索引]]

[原始来源](https://dcgi.fel.cvut.cz/wp-content/wpallimport-dist/publications/pdf/publications-2019-cmolik-tvcg-rtgv-paper.pdf)

作者/机构：Ladislav Čmolík, Jiří Bittner。年份：2019。证据层级：全文级原始资料。

## 机制

在幽灵透明视图上联合选择标签位置和锚点，把对象的不透明度、覆盖和布局质量纳入模糊多准则决策，减少引线落在多个重叠物体上时的指代歧义。

## 能够显露的信息

不仅看到被遮物体，还知道每个名称到底指向哪一层、哪一个部件；旋转时标签实时更新。

## 几何与坐标

不移动模型；改变二维注释和锚点布局，透明视图本身由其他算法生成。

## 代价

标签及引线占用边缘屏幕空间；它解决识别与指代，不会增加可见像素或自动恢复精确深度。

## 评价证据

全文报告60名日常电脑用户，比较5种布局方法、4种模型；作者总体结论是可改善理解且布局可与人工相当，具体模型结果并非完全一致。

## 交互

多视点实时观察；标签随视图和透明遮挡更新。

## 实现与数据要求

需要对象ID、投影和透明信息；可搭配多种幽灵视图渲染算法，而不是完整的去遮挡算法。

## 来源核对

已打开作者12页版本，核对研究设计、样本数和与人工布局比较。期刊年份2019，DOI与版权注明2018。

## 限制

研究针对中等复杂度模型，不能外推到任意数量标签、所有专业任务或透明本身的深度判断提升。

## 方法与关联

[[3D结构透视研究/方法/02 隐藏线、轮廓与语义着色|隐藏线、轮廓与语义着色]] · [[3D结构透视研究/方法/11 拓扑、语义与几何的混合表达|拓扑、语义与几何的混合表达]] · [[3D结构透视研究/方法/13 感知、评价与失败模式|感知、评价与失败模式]]

- [[3D结构透视研究/来源/tech-04 Multi-perspective Compact Explosion Diagrams|tech-04 · Multi-perspective Compact Explosion Diagrams (2011)]]
- [[3D结构透视研究/来源/tech-07 Transparency in Interactive Technical Illustrations|tech-07 · Transparency in Interactive Technical Illustrations (2002)]]
- [[3D结构透视研究/来源/tech-15 Onshape Help- Isolate|tech-15 · Onshape Help: Isolate (2026)]]
