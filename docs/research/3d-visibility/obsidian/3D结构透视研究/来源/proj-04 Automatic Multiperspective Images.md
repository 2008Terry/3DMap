---
type: research-source
created: '2026-10-15'
updated: '2026-10-15'
status: 文献研究，未本地复现
id: proj-04
year: 2006
source_type: paper
evidence: abstract-primary
methods:
- automatic multiperspective optimization
- distortion metric
- importance/depth map
domains:
- 长街景
- 非平面街区
source_url: https://graphics.stanford.edu/papers/autoperspective/
accessed: '2026-10-15'
method_families:
- '07'
---

# Automatic Multiperspective Images

返回 [[3D结构透视研究/00 3D结构透视研究 Dashboard|研究 Dashboard]] · [[3D结构透视研究/03 来源索引|来源索引]]

[原始来源](https://graphics.stanford.edu/papers/autoperspective/)

作者/机构：Augusto Román; Hendrik P. A. Lensch。年份：2006。证据层级：原始摘要或受限索引。

## 机制

把偏离普通透视的变形量作为误差度量，优化每段视点和画面曲面；利用粗略深度图或二维重要性图，为高深度变化区域分配更合适的透视。

## 能够显露的信息

在单幅长全景中汇总许多位置的沿街细节，特别改善路口与巷道；作者页面示例沿旧金山18th Avenue约2公里。

## 几何与坐标

不移动原对象；改变输出画面参数化和局部透视，几何测量需返回原空间。

## 代价

长图仍需压缩、横向浏览或大量像素，不能同时保证全部细节可读；优化依赖输入图像、粗几何和重要性定义。

## 评价证据

作者页面展示推扫对照与长街景结果；本次PDF请求超时，因此不补写未核对的运行时间或定量实验细节。

## 交互

可自动生成，重要性图仍允许引入用户关注区域；结果可作为可浏览全景。

## 实现与数据要求

需要相机序列、粗深度或重要性图、分段投影优化和图像重采样。

## 来源核对

已打开Stanford作者页，核对EGSR 2006、摘要、示例说明及2公里案例；PDF链接已尝试但超时，未按全文证据记载。

## 限制

只保留输入照片中已有信息；扩展视野与减少失真不能保证暴露任意封闭内部。

## 方法与关联

[[3D结构透视研究/方法/07 广义相机、多透视与投影变化|广义相机、多透视与投影变化]]

- [[3D结构透视研究/来源/proj-03 Interactive Design of Multi-Perspective Images for Visualizing Urban|proj-03 · Interactive Design of Multi-Perspective Images for Visualizing Urban Landscapes (2004)]]
- [[3D结构透视研究/来源/proj-06 An Evaluation of 3-D Scene Exploration Using a Multiperspective Imag|proj-06 · An Evaluation of 3-D Scene Exploration Using a Multiperspective Image Framework (2011)]]
