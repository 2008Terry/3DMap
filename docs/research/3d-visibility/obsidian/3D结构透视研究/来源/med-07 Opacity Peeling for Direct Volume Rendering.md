---
type: research-source
created: '2026-10-15'
updated: '2026-10-15'
status: 文献研究，未本地复现
id: med-07
year: 2006
source_type: paper
evidence: full-primary
methods:
- opacity peeling
- layered volume rendering
- threshold hysteresis
- multisampling
domains:
- MRI
- preoperative and intraoperative medical data
source_url: https://www.cg.informatik.uni-siegen.de/sites/www.cg.informatik.uni-siegen.de/files/data/Publications/2006/OpacityPeeling_EG06-fin-electronic.pdf
accessed: '2026-10-15'
method_families:
- '10'
---

# Opacity Peeling for Direct Volume Rendering

返回 [[3D结构透视研究/00 3D结构透视研究 Dashboard|研究 Dashboard]] · [[3D结构透视研究/03 来源索引|来源索引]]

[原始来源](https://www.cg.informatik.uni-siegen.de/sites/www.cg.informatik.uni-siegen.de/files/data/Publications/2006/OpacityPeeling_EG06-fin-electronic.pdf)

作者/机构：Christof Rezk-Salama; Andreas Kolb。年份：2006。证据层级：全文级原始资料。

## 机制

前向累积达到高阈值后不终止射线，而等待当前样本不透明度降到低阈值再开始新层；双阈值避免厚组织被反复切成碎层。

## 能够显露的信息

可逐层显现被皮肤、脂肪、脑膜遮住的脑表面与更深结构，即使组织强度相同、常规传递函数无法区分。

## 几何与坐标

保留体素位置，输出多张分层图；某层显示时抑制其前方内容，未把原体几何移开。

## 代价

层是沿视线的光学层，并非稳定语义器官分割；低阈值不当会出洞，噪声使相邻射线换层位置跳变。

## 评价证据

已打开10页原文，包含临床MRI、噪声数据、性能与多重采样示例；不将示例改善当成受控诊断研究。

## 交互

选层、调两项剥离阈值及亮度/不透明度窗口，旋转后重新生成视点相关层。

## 实现与数据要求

可改造现有ray caster，单pass写多个render targets；多重采样降低噪声引发的层不连续。

## 来源核对

原文强调最适合洋葱式组织分层，且明确承认图像仍有伪影。

## 限制

依赖低透明度或梯度边界分隔组织；剥开外层后内部自身仍会遮挡。

## 方法与关联

[[3D结构透视研究/方法/10 时间扫描、路径游览与运动视差|时间扫描、路径游览与运动视差]]

- [[3D结构透视研究/来源/med-02 Multidimensional Transfer Functions for Interactive Volume Rendering|med-02 · Multidimensional Transfer Functions for Interactive Volume Rendering (2002)]]
- [[3D结构透视研究/来源/med-03 Importance-Driven Volume Rendering|med-03 · Importance-Driven Volume Rendering (2004)]]
- [[3D结构透视研究/来源/med-13 3D Slicer documentation- Volume rendering|med-13 · 3D Slicer documentation: Volume rendering (未核实年份)]]
