---
type: research-source
created: '2026-10-15'
updated: '2026-10-15'
status: 文献研究，未本地复现
id: med-19
year: 2026
source_type: paper
evidence: abstract-primary
methods:
- mesh-over-tumour
- ROI mesh
- virtual window
- metric depth indicator
- instrument occlusion handling
domains:
- monocular laparoscopy
- surgical AR
- subsurface target visualization
source_url: https://pmc.ncbi.nlm.nih.gov/articles/PMC12889570/
accessed: '2026-10-15'
method_families:
- '02'
- '13'
---

# Hidden Tumour Visualization in Augmented Monocular Liver Laparoscopy

返回 [[3D结构透视研究/00 3D结构透视研究 Dashboard|研究 Dashboard]] · [[3D结构透视研究/03 来源索引|来源索引]]

[原始来源](https://pmc.ncbi.nlm.nih.gov/articles/PMC12889570/)

作者/机构：Kirana Hanifati; Mohammad Alkhatib; Erol Ozgur; Emmanuel Buc; Bertrand Le Roy; Hestiasari Rante; Youcef Mezouar; Adrien Bartoli。年份：2026。证据层级：原始摘要或受限索引。

## 机制

用术中超声做刚性肿瘤配准，把表面或ROI网格覆盖在肿瘤图像之上，通过部分遮挡使其看起来位于肝内；RoT-D再加深度指示条。

## 能够显露的信息

单目二维手术画面内同时呈现隐藏肿瘤位置与表面关系，避免普通透明叠加让目标看似漂浮在外面。

## 几何与坐标

原CT肿瘤经刚性配准；显示加入估计表面网格、窗口及深度符号，没有把人体真实切开。

## 代价

需要可靠配准和工具遮挡处理；文中由学习深度生成的表面网格可对齐图像但未必几何准确，不能把网格当精确测量表面。

## 评价证据

PMC索引可读方法与结果：39人含10名外科医生，以10次手术图像投票，偏好RoT-D；这是偏好证据，不能当作毫米级深度误差实测。

## 交互

面向持续手术指导、超声定位及处理器械前后关系；本轮未实际操作系统。

## 实现与数据要求

需要CT分割模型、LUS到相机配准、深度读取、虚拟窗口、网格及工具分割。

## 来源核对

正式发表2026-02-10，DOI10.1049/htl2.70043；PMC搜索索引返回较完整方法/结果，但直接打开被验证码阻挡，保守按摘要级记录。

## 限制

论文只实验单肿瘤；多肿瘤与血管为作者提出的扩展。深度传达改善与深度值真实准确是两个问题。

## 方法与关联

[[3D结构透视研究/方法/02 隐藏线、轮廓与语义着色|隐藏线、轮廓与语义着色]] · [[3D结构透视研究/方法/13 感知、评价与失败模式|感知、评价与失败模式]]

- [[3D结构透视研究/来源/med-05 ClearView- An Interactive Context Preserving Hotspot Visualization T|med-05 · ClearView: An Interactive Context Preserving Hotspot Visualization Technique (2006)]]
- [[3D结构透视研究/来源/med-10 Perceptual Evaluation of Ghosted View Techniques for the Exploration|med-10 · Perceptual Evaluation of Ghosted View Techniques for the Exploration of Vascular Structures and Embedded Flow (2011)]]
- [[3D结构透视研究/来源/med-18 MedVA- An End-to-End Neuro-Symbolic Agentic System for Medical Volum|med-18 · MedVA: An End-to-End Neuro-Symbolic Agentic System for Medical Volume Visualization (2026)]]
