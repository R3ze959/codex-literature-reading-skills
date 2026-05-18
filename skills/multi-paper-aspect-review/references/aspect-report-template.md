# Focused Aspect Report Template

Use this template when producing a full focused-aspect review from multiple papers.

## Aspect Card Schema

| Field | Content |
| --- | --- |
| Bibliography | Title, year, journal, and first/corresponding author if useful |
| Aspect relevance | Why this paper matters for the selected aspect |
| Direct evidence | Reported statements, data, figures, tables, or page references |
| Quantitative values | Values, units, original state, and normalized value if appropriate |
| Measurement conditions | Technique, temperature, SOC, voltage window, C-rate, loading, cell type, atmosphere, synthesis state |
| Author interpretation | Mechanism or conclusion proposed by the paper |
| Codex inference | Cross-paper interpretation, clearly marked as inference |
| Limitations | Missing controls, ambiguity, unfair comparison, or weak evidence |

## Comparison Tables

### Evidence Matrix

| Sub-topic | Paper | Evidence | Value | Condition | Supports | Caveat |
| --- | --- | --- | --- | --- | --- | --- |

### Contradiction Matrix

| Question | Paper A says | Paper B says | Conflict type | Likely cause | Resolving experiment |
| --- | --- | --- | --- | --- | --- |

### Evidence Strength Rating

Use this scale:

| Rating | Meaning |
| --- | --- |
| A | Direct operando/in situ quantitative evidence under relevant conditions |
| B | Direct ex situ evidence or strong quantitative computation supporting the mechanism |
| C | Indirect characterization, correlation, or partial evidence |
| D | Speculative claim, missing controls, or insufficient reporting |

## Concept Separation Checklist

- Thermal NTE: temperature-driven lattice shrinkage. Compare coefficient of thermal expansion and temperature range.
- Electrochemical zero strain: Li insertion/extraction-driven change in unit cell, lattice plane, particle, or electrode dimension.
- Particle/electrode strain: morphology and composite-level swelling/cracking, not identical to unit-cell strain.
- Full-cell deformation/safety: pouch swelling, gas, thermal abuse, nail test, or mechanical deformation. These are not direct lattice-strain measurements.
- Structural framework: crystallographic shear planes, tunnel/block dimensions, cation disorder, and defect chemistry should be tied to transport or strain only when evidence exists.

## Chinese Wording Templates

### Scope

本报告不做逐篇全文综述，而是围绕`[主题]`进行跨文献证据提取和机制整合。分析重点包括`[子问题1]`、`[子问题2]`和`[子问题3]`，并区分原文直接报道、作者解释与跨文献推断。

### Contradiction

两篇文献表面上均使用`[术语]`，但物理层级不同：`[文献A]`讨论的是`[层级A]`，而`[文献B]`讨论的是`[层级B]`。因此二者不一定构成直接矛盾，更可能反映了测试尺度和状态变量不同。

### Gap

现有研究的关键空白不是缺少性能数据，而是缺少能够同时连接`[结构变量]`、`[中间机制]`和`[目标性质]`的原位/定量证据链。后续可通过`[实验]`在`[条件]`下验证，如果观察到`[预期信号]`，则可支持`[机制]`；若出现`[反例信号]`，则需要修正该机制。

### Innovation

可创新点应从"再做一种材料"转向"验证并调控一个可量化机制"。例如，以`[结构参数]`为调控变量，结合`[表征/计算]`追踪`[目标性质]`，有望把经验性的性能提升转化为可预测的结构设计规则。
