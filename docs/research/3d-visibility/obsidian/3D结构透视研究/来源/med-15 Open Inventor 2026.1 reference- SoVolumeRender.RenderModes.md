---
type: research-source
created: '2026-10-15'
updated: '2026-10-15'
status: 文献研究，未本地复现
id: med-15
year: null
source_type: official-doc
evidence: official-doc
methods:
- sum projection
- average projection
- MIP
- MinIP
- MIDA
- gradient difference accumulation
domains:
- scientific volume rendering
- medical and industrial visualization
source_url: https://developer.openinventor.com/refmans/2026.1/RefManJava/com/openinventor/volumeviz/nodes/SoVolumeRender.RenderModes.html
accessed: '2026-10-15'
method_families:
- 09
---

# Open Inventor 2026.1 reference: SoVolumeRender.RenderModes

返回 [[3D结构透视研究/00 3D结构透视研究 Dashboard|研究 Dashboard]] · [[3D结构透视研究/03 来源索引|来源索引]]

[原始来源](https://developer.openinventor.com/refmans/2026.1/RefManJava/com/openinventor/volumeviz/nodes/SoVolumeRender.RenderModes.html)

作者/机构：Open Inventor / Thermo Fisher Scientific。年份：未核实，见来源核对说明。证据层级：官方文档。

## 机制

2026.1 API明确列出alpha合成、最大/最小、总和/平均，以及强度/梯度差调制。总和按统一名义采样数归一化；平均按每射线实际样本数归一化。

## 能够显露的信息

总和/平均显示整条射线的总体标量贡献；差调制让内部强度跃迁或梯度跃迁更突出，形成不同信息摘要。

## 几何与坐标

保留数据位置，改变射线合成规则。图像值是汇总量，不是某一个实体表面的真实位置。

## 代价

压缩成总和/均值会混合前后对象；平均还可能被大量低值体素稀释。统计贡献存在不代表独立层可被辨认。

## 评价证据

已打开2026.1官方API及2023.1用户指南；仅验证当前版本文档存在这些模式，不宣称已测试性能。

## 交互

应用通过renderMode选择方法；窗口、颜色表及采样参数仍影响结果。

## 实现与数据要求

可直接使用VolumeViz渲染模式；用户指南指出非普通体渲染合成仅支持raycasting且不保留深度信息。

## 来源核对

2026.1是所读API版本而非可核实发布日期，因此year=null；新版文档证明这些组合仍是实际产品能力。

## 限制

总和投影不是完整物理X射线传播模型；不能把所有体素参与数值合成等同于所有对象视觉可辨。

## 方法与关联

[[3D结构透视研究/方法/09 联动多视窗、切片图册与小图|联动多视窗、切片图册与小图]]

- [[3D结构透视研究/来源/med-13 3D Slicer documentation- Volume rendering|med-13 · 3D Slicer documentation: Volume rendering (未核实年份)]]
- [[3D结构透视研究/来源/med-20 Instant Volume Visualization using Maximum Intensity Difference Accu|med-20 · Instant Volume Visualization using Maximum Intensity Difference Accumulation (2009)]]
