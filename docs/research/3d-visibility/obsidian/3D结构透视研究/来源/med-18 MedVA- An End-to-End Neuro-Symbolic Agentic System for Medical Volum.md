---
type: research-source
created: '2026-10-15'
updated: '2026-10-15'
status: 文献研究，未本地复现
id: med-18
year: 2026
source_type: paper
evidence: abstract-primary
methods:
- intent-grounded ROI selection
- multi-model segmentation
- volume-based visibility objective
- automated visualization optimization
domains:
- medical volume visualization
- natural-language interaction
source_url: https://arxiv.org/abs/2609.14874
accessed: '2026-10-15'
method_families:
- '12'
---

# MedVA: An End-to-End Neuro-Symbolic Agentic System for Medical Volume Visualization

返回 [[3D结构透视研究/00 3D结构透视研究 Dashboard|研究 Dashboard]] · [[3D结构透视研究/03 来源索引|来源索引]]

[原始来源](https://arxiv.org/abs/2609.14874)

作者/机构：Haill An; Suhyeon Kim; Minjun Kang; Eunwoo Lee; Bin Sheng; Lei Bi; Younhyun Jung。年份：2026。证据层级：原始摘要或受限索引。

## 机制

三个环节分别把自然语言意图转为有临床知识约束的ROI要求、在原体数据调用分割模型找ROI、用体积可见性目标优化其强调与遮挡。

## 能够显露的信息

目标不是额外发明一种透视材质，而是根据任务选择哪些内部区域需要露出，并显式检查它们在原数据中的遮挡。

## 几何与坐标

摘要说在原体数据识别和评估ROI；具体通过哪些渲染参数改变几何/可见性尚未从全文确认。

## 代价

ROI和目标函数决定什么被优先展示；分割、意图解释错误会把错误对象突出，优化分数也不等于人能理解所有关系。

## 评价证据

原始arXiv摘要声明多数据/交互场景的agent和系统评估及形成性用户研究；本轮全文不可开，未核实样本数、收益幅度或公式。

## 交互

自然语言请求到自动ROI识别和视觉优化，可作为半自动探索工作流。

## 实现与数据要求

需要临床知识推理、医学分割模型和体积可见性度量；本轮未验证官方代码。

## 来源核对

arXiv原始摘要检索可读，首发2026-09-14；直接abs/HTML/PDF打开均失败，因此严格限于摘要，不把聚合网站评语作证据。

## 限制

新预印本，尚无本轮可验证独立复现；不会从只有外表面的模型恢复可信内部解剖。

## 方法与关联

[[3D结构透视研究/方法/12 可见性度量与自动显露优化|可见性度量与自动显露优化]]

- [[3D结构透视研究/来源/med-03 Importance-Driven Volume Rendering|med-03 · Importance-Driven Volume Rendering (2004)]]
- [[3D结构透视研究/来源/med-16 ClipGS- Clippable Gaussian Splatting for Interactive Cinematic Visua|med-16 · ClipGS: Clippable Gaussian Splatting for Interactive Cinematic Visualization of Volumetric Medical Data (2025)]]
- [[3D结构透视研究/来源/med-19 Hidden Tumour Visualization in Augmented Monocular Liver Laparoscopy|med-19 · Hidden Tumour Visualization in Augmented Monocular Liver Laparoscopy (2026)]]
