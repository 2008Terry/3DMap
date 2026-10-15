---
type: research-source
created: '2026-10-15'
updated: '2026-10-15'
status: 文献研究，未本地复现
id: proj-12
year: 2021
source_type: paper
evidence: full-primary
methods:
- X-ray microtomography
- surface reconstruction
- virtual unfolding
- texture transfer
domains:
- 文化遗产
- 折叠薄片
- 密封信件
source_url: https://www.nature.com/articles/s41467-021-21326-w.pdf
accessed: '2026-10-15'
method_families:
- 08
---

# Unlocking History through Automated Virtual Unfolding of Sealed Documents Imaged by X-ray Microtomography

返回 [[3D结构透视研究/00 3D结构透视研究 Dashboard|研究 Dashboard]] · [[3D结构透视研究/03 来源索引|来源索引]]

[原始来源](https://www.nature.com/articles/s41467-021-21326-w.pdf)

作者/机构：Jana Dambrogio; Amanda Ghassaei; Daniel Starza Smith; Holly Jackson; Martin L. Demaine; Graham Davis; David Mills; Rebekah Ahrendt; Nadine Akkerman; David van der Linden; Erik D. Demaine。年份：2021。证据层级：全文级原始资料。

## 机制

从体扫描重建复杂折叠、插入和切缝的纸张层，再计算展开并转移扫描中的文字信息，产生平面可读文本及折痕图。

## 能够显露的信息

外部完全看不到的内层文字和折叠结构可在平面被检查；这是先有内部成像数据、再改变表示的强例子，不能凭外部RGB照片推断隐藏内容。

## 几何与坐标

将三维折叠薄片重参数化成二维纸面，位置明显改变，但对应关系可保存以回溯折叠证据。

## 代价

纸张必须可靠分层，接触、破损、扫描对比不足会影响重建；平面图牺牲原折叠空间位置，需要保留映射和折痕证据。

## 评价证据

Nature Communications 12,1184，2021-03-02；在四封文艺复兴时期信包上演示，首次读取其中一封未拆信。数据、代码及补充方法公开。

## 交互

主要是自动离线流程与可浏览重建结果；不是实时交互相机技术。

## 实现与数据要求

需高分辨率体扫描、层面提取、网格重建、展开和纹理采样；建筑应用的类比是给每面内墙建立平面图册并链接原位置。

## 来源核对

已打开Nature官方10页PDF，出版商摘要核对日期与四信包案例；网页和PMC曾受访问限制，但官方PDF成功。

## 限制

方法基于薄片性质，不能直接无损铺平任意有体积物体；可读结果受数据采集和分割质量限制。

## 方法与关联

[[3D结构透视研究/方法/08 曲面重采样、解缠与表面展开|曲面重采样、解缠与表面展开]]

- [[3D结构透视研究/来源/proj-10 Nondistorting Flattening Maps and the 3-D Visualization of Colon CT|proj-10 · Nondistorting Flattening Maps and the 3-D Visualization of Colon CT Images (2000)]]
- [[3D结构透视研究/来源/proj-11 Volumetric Colon Wall Unfolding Using Harmonic Differentials|proj-11 · Volumetric Colon Wall Unfolding Using Harmonic Differentials (2011)]]
- [[3D结构透视研究/来源/proj-13 HippoMaps- Multiscale Cartography of Human Hippocampal Organization|proj-13 · HippoMaps: Multiscale Cartography of Human Hippocampal Organization (2025)]]
