---
type: research-method
created: '2026-10-15'
updated: '2026-10-15'
status: 文献研究，未本地复现
method_id: '01'
---

# 透明、转移函数与OIT

返回 [[3D结构透视研究/00 3D结构透视研究 Dashboard|研究 Dashboard]] · [[3D结构透视研究/02 方法对照矩阵|方法对照矩阵]]

## 如何显露

把表面片元或体采样值映射为颜色和不透明度。转移函数还可用梯度、类别、重要度等维度分开组织；OIT解决提交顺序与混合的实现问题。选择性透明只淡化挡住目标的部分，比全部统一alpha更有任务针对性。

## 能读什么

原位的外壳与内部可以同时留下视觉贡献，适合定位一个目标、比较少数层或检查材料类别。

## 牺牲什么

多层颜色会混合，深度顺序和轮廓会竞争。假设每层不透明度为0.2，10层后累计不透明度为1−0.8^10≈0.893，尚未计入光照与背景。混合正确也可能近乎不透明；继续降低alpha又会让每个构件更难辨认。

## 保留什么

保留原始几何和投影；牺牲表面分离度与部分深度线索。

## 需要什么

需能单独识别目标和遮挡物，或有体标量/分类。精确排序、深度剥离、随机方法和加权方法分别付出显存、通道、噪声或近似代价。

## 证据边界

没有一项这里的证据保证任意深度复杂度的所有内部同时可读。检查目标检出、层序判断和颜色误解，不能只检验alpha是否小于1。

## 原始资料

- [[3D结构透视研究/来源/cross-02 Employing Dynamic Transparency for 3D Occlusion Management- Design I|cross-02 · Employing Dynamic Transparency for 3D Occlusion Management: Design Issues and Evaluation (2007)]]
- [[3D结构透视研究/来源/cross-05 Seeing Through the Overlap- The Impact of Color and Opacity on Depth|cross-05 · Seeing Through the Overlap: The Impact of Color and Opacity on Depth Order Perception in Visualization (2025)]]
- [[3D结构透视研究/来源/cross-09 Exploring and Expanding the Continuum of OIT Algorithms|cross-09 · Exploring and Expanding the Continuum of OIT Algorithms (2016)]]
- [[3D结构透视研究/来源/cross-10 Stochastic Transparency|cross-10 · Stochastic Transparency (2010)]]
- [[3D结构透视研究/来源/cross-11 Vulkan Order-Independent Transparency Sample|cross-11 · Vulkan Order-Independent Transparency Sample (未核实年份)]]
- [[3D结构透视研究/来源/tech-07 Transparency in Interactive Technical Illustrations|tech-07 · Transparency in Interactive Technical Illustrations (2002)]]
- [[3D结构透视研究/来源/tech-15 Onshape Help- Isolate|tech-15 · Onshape Help: Isolate (2026)]]
- [[3D结构透视研究/来源/med-01 Display of Surfaces from Volume Data|med-01 · Display of Surfaces from Volume Data (1988)]]
- [[3D结构透视研究/来源/med-02 Multidimensional Transfer Functions for Interactive Volume Rendering|med-02 · Multidimensional Transfer Functions for Interactive Volume Rendering (2002)]]
- [[3D结构透视研究/来源/med-13 3D Slicer documentation- Volume rendering|med-13 · 3D Slicer documentation: Volume rendering (未核实年份)]]
- [[3D结构透视研究/来源/med-17 Nested Semi-Transparent Isosurface Simulated Volume-Rendering (NESTI|med-17 · Nested Semi-Transparent Isosurface Simulated Volume-Rendering (NESTIS-VR) - An efficient on-device rendering approach for Augmented Reality headsets increasing surgeon confidence of kidney donor arterial anatomy (2024)]]
- [[3D结构透视研究/来源/med-20 Instant Volume Visualization using Maximum Intensity Difference Accu|med-20 · Instant Volume Visualization using Maximum Intensity Difference Accumulation (2009)]]
