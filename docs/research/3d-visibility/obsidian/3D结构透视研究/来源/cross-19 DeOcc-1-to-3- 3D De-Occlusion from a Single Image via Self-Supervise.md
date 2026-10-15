---
type: research-source
created: '2026-10-15'
updated: '2026-10-15'
status: 文献研究，未本地复现
id: cross-19
year: 2026
source_type: paper
evidence: abstract-primary
methods:
- generative deocclusion
- multi-view diffusion
domains:
- computer vision
- data inference
source_url: https://ojs.aaai.org/index.php/AAAI/article/view/37820
accessed: '2026-10-15'
method_families:
- '16'
---

# DeOcc-1-to-3: 3D De-Occlusion from a Single Image via Self-Supervised Multi-View Diffusion

返回 [[3D结构透视研究/00 3D结构透视研究 Dashboard|研究 Dashboard]] · [[3D结构透视研究/03 来源索引|来源索引]]

[原始来源](https://ojs.aaai.org/index.php/AAAI/article/view/37820)

作者/机构：Yuze Wang; You Shen; Shengchuan Zhang; Liujuan Cao。年份：2026。证据层级：原始摘要或受限索引。

## 机制

从被遮挡的单图经扩散模型生成一致新视图，以伪真值学习补全。

## 能够显露的信息

产生合理的完整物体外观或形状假设。

## 几何与坐标

推断并生成缺失数据。

## 代价

生成内容不等于被测真实内部；物体表面补全不能证明实际室内墙体位置。

## 评价证据

出版社摘要报告基准实验；本次未读完整实验表。

## 交互

交互能力以原始资料为准；本条机制与适用条件见下。

## 实现与数据要求

训练数据、生成模型与置信/来源标记。

## 来源核对

AAAI2026出版社页面，2026-03-14；DOI10.1609/aaai.v40i11.37820。

## 限制

生成内容不等于被测真实内部；物体表面补全不能证明实际室内墙体位置。

## 方法与关联

[[3D结构透视研究/方法/16 单图去遮挡与生成式补全|单图去遮挡与生成式补全]]

- [[3D结构透视研究/来源/cross-14 Imaging hidden objects with consumer LiDAR via motion-induced sampli|cross-14 · Imaging hidden objects with consumer LiDAR via motion-induced sampling (2026)]]
