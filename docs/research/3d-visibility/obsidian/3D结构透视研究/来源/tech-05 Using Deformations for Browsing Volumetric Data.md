---
type: research-source
created: '2026-10-15'
updated: '2026-10-15'
status: 文献研究，未本地复现
id: tech-05
year: 2003
source_type: paper
evidence: full-primary
methods:
- hinging
- spreading
- sphere expansion
- leafing
- fanning
- flipping
- peeling
- radial peeling
domains:
- volume exploration
- anatomy
- layered data
source_url: https://www.dgp.toronto.edu/~mjmcguff/research/volumetricBrowsing/volumetricBrowsing.pdf
accessed: '2026-10-15'
method_families:
- '06'
---

# Using Deformations for Browsing Volumetric Data

返回 [[3D结构透视研究/00 3D结构透视研究 Dashboard|研究 Dashboard]] · [[3D结构透视研究/03 来源索引|来源索引]]

[原始来源](https://www.dgp.toronto.edu/~mjmcguff/research/volumetricBrowsing/volumetricBrowsing.pdf)

作者/机构：Michael J. McGuffin, Liviu Tancau, Ravin Balakrishnan。年份：2003。证据层级：全文级原始资料。

## 机制

把语义层当作可翻页、张开或剥皮的材料；铰链展开、球形扩张、翻页和径向剥皮将外层移开，既露出内部又让被移开的内容留在周围。不同层可受不同程度变形。

## 能够显露的信息

内部层表面、层间接口及被移开内容的形状；动画让用户追踪结构从何处来。

## 几何与坐标

同时含刚体和非刚体变形，不是物理可信手术模拟；变形与相机旋转解耦。

## 代价

距离、角度、局部形状乃至连接连续性会失真；移开的层仍会遮挡其他区域，复杂控件也可造成杂乱。

## 评价证据

全文报告实验室非正式试用及一名专业解剖学者约一小时的演示/探索；动画可理解性反馈良好，但没有受控比较实验。

## 交互

就地3D控件、弹出菜单、逐层调节、连续动画及任意视角旋转。

## 实现与数据要求

假定能得到有意义的层；作者承认真实组织分割、噪声和非层状器官不总满足该前提。

## 来源核对

已打开作者8页论文并核对工具、语义层假设、反馈性质与限制。

## 限制

它是最接近'物理上做不到的窥视'的路线之一，但用形变换取信息可见性，无法同时保持全部原始度量。

## 方法与关联

[[3D结构透视研究/方法/06 剥皮、铰链、翻页与非刚性变形|剥皮、铰链、翻页与非刚性变形]]

- [[3D结构透视研究/来源/tech-02 Automated Generation of Interactive 3D Exploded View Diagrams|tech-02 · Automated Generation of Interactive 3D Exploded View Diagrams (2008)]]
- [[3D结构透视研究/来源/tech-11 Clipping spline- interactive, dynamic 4D volume clipping and analysi|tech-11 · Clipping spline: interactive, dynamic 4D volume clipping and analysis based on thin plate spline (2025)]]
