---
type: research-source
created: '2026-10-15'
updated: '2026-10-15'
status: 文献研究，未本地复现
id: med-16
year: 2025
source_type: paper
evidence: full-primary
methods:
- clippable Gaussian splatting
- cinematic rendering
- learnable truncation
- adaptive Gaussian deformation
domains:
- CT
- anatomical slice data
- interactive medical visualization
source_url: https://papers.miccai.org/miccai-2025/paper/0380_paper.pdf
accessed: '2026-10-15'
method_families:
- '03'
- '16'
---

# ClipGS: Clippable Gaussian Splatting for Interactive Cinematic Visualization of Volumetric Medical Data

返回 [[3D结构透视研究/00 3D结构透视研究 Dashboard|研究 Dashboard]] · [[3D结构透视研究/03 来源索引|来源索引]]

[原始来源](https://papers.miccai.org/miccai-2025/paper/0380_paper.pdf)

作者/机构：Chengkun Li; Yuqi Tong; Kai Chen; Zhenya Yang; Ruiyang Li; Shi Qiu; Jason Ying-Kuen Chan; Pheng-Ann Heng; Qi Dou。年份：2025。证据层级：全文级原始资料。

## 机制

把高质量体渲染表示为Gaussian splatting，引入随裁切平面调整primitive可见性的可学习截断，以及动态Gaussian变形调节模型。

## 能够显露的信息

交互裁切平面可显露内部截面，同时保留较高质量的照明和解剖表现，缓解传统电影级渲染速度不足。

## 几何与坐标

原数据转成学习的Gaussian表示，显示可截断/变形；裁切部分从当前图像移除。

## 代价

高画质不等于完整可见，内部依旧靠切平面暴露；学习表示的图像相似度不能保证小病灶、测量或所有未见切面准确。

## 评价证据

已打开MICCAI官方11页开放论文。五组医学体数据上报告平均PSNR 36.635、156 FPS、16.1 MB；其实验用RTX 4090，非任意设备承诺。

## 交互

改变视点和裁切平面，实时更新内部截面外观。

## 实现与数据要求

需离线训练/构建、动态截断和GPU splat渲染；不是向已有普通表面网格直接加透明度即可。

## 来源核对

2025-07-09 arXiv首发、MICCAI2025官方论文；性能为原文实验数字，未在当前项目复现。

## 限制

PSNR/FPS是渲染质量/速度指标，不是诊断准确度；不从未采集的体积信息创造可靠解剖。

## 方法与关联

[[3D结构透视研究/方法/03 平面、目标驱动与非平面剖切|平面、目标驱动与非平面剖切]] · [[3D结构透视研究/方法/16 单图去遮挡与生成式补全|单图去遮挡与生成式补全]]

- [[3D结构透视研究/来源/med-07 Opacity Peeling for Direct Volume Rendering|med-07 · Opacity Peeling for Direct Volume Rendering (2006)]]
- [[3D结构透视研究/来源/med-13 3D Slicer documentation- Volume rendering|med-13 · 3D Slicer documentation: Volume rendering (未核实年份)]]
- [[3D结构透视研究/来源/med-18 MedVA- An End-to-End Neuro-Symbolic Agentic System for Medical Volum|med-18 · MedVA: An End-to-End Neuro-Symbolic Agentic System for Medical Volume Visualization (2026)]]
