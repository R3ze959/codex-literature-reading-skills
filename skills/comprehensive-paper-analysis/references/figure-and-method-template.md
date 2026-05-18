# Figure and Methods Template

Use this reference for full single-paper explanation reports.

## Whole-Paper Analysis Block

Before figure-by-figure explanation, include these dimensions:

1. **研究问题拆解**
   - The practical or scientific problem.
   - Why prior work is insufficient.
   - What variable, material design, mechanism, or method the paper focuses on.

2. **作者假设与设计逻辑**
   - What the authors believe will solve the problem.
   - Why the selected material/method should work.
   - Which assumptions are explicit and which are implicit.

3. **论证链**
   - Claim 1 → supporting experiment/figure/table → key evidence → residual uncertainty.
   - Claim 2 → supporting experiment/figure/table → key evidence → residual uncertainty.
   - Final conclusion → combined evidence → overclaim risk.

4. **创新性分析**
   - New material/composition/structure.
   - New synthesis or processing route.
   - New mechanism insight.
   - New test condition or practical validation.
   - New comparison standard or application scenario.

5. **可靠性与局限**
   - Controls and baselines.
   - Sample size/reproducibility.
   - Whether test conditions are practical or only idealized.
   - Whether performance metrics are fairly compared.
   - Missing characterization or missing long-term validation.

## Figure Explanation Block

For each figure, use this structure:

1. **这张图想回答什么问题**
2. **实验/计算对象是什么**
3. **横轴、纵轴、单位、颜色、符号分别代表什么**
4. **每个 panel 的读图步骤**
5. **关键数值**
6. **作者用它支持什么结论**
7. **初学者容易误解的地方**
8. **这张图和前后图的关系**

## Methods Extraction Checklist

| Category | Details to extract |
|---|---|
| Material synthesis | Precursors, ratios, solvent, pH, atmosphere, temperature, time, heating rate, washing/drying/calcination |
| Electrode preparation | Active material, conductive agent, binder, mass ratio, solvent, slurry process, current collector, loading, electrode thickness |
| Cell assembly | Cell format, counter/reference electrode, electrolyte, separator, pressure, atmosphere |
| Electrochemical testing | Voltage window, rate/current density, C-rate definition, temperature, activation, cycle count, rest time |
| Characterization | XRD, Rietveld, SEM/TEM, XPS, Raman, BET, TGA, CV, EIS, GITT, in/ex situ methods |
| Data processing | Capacity basis, retention formula, CE/ICE, diffusion coefficient equation, fitting model |

## Evidence Chain Table

| Author claim | Evidence used | Strong points | Weak points | Best follow-up experiment |
|---|---|---|---|---|

## Novelty and Contribution Table

| Claimed novelty | Evidence in paper | How strong is it? | What literature comparison is needed? |
|---|---|---|---|

## Critical Reading Questions

- If the headline performance is high, is it measured at a practical mass loading?
- Is the comparison baseline synthesized/tested under the same conditions?
- Are voltage window, rate definition, and capacity basis consistent?
- Does the mechanism rely on direct in/ex situ evidence, or only post-mortem characterization?
- Are morphology, carbon content, electrolyte amount, or electrode thickness responsible for part of the improvement?
- Does the paper show long-cycle stability after activation, or only short-term performance?
- Does the full-cell result support the half-cell claim?
- What single missing control would most change confidence in the paper?

## Beginner Parameter Explanation Pattern

Use this order:

`参数名称 → 它衡量什么 → 单位是什么意思 → 图中如何读取 → 数值高/低通常意味着什么 → 本文中作者如何解释`

Example:

`库仑效率 η 衡量充进去的电荷有多少能在放电时回来，通常写成 discharge capacity / charge capacity × 100%。如果 η 接近 100%，说明副反应少、可逆性好；如果首圈 η 很低，往往说明形成 SEI 或不可逆嵌锂/转化反应消耗了锂。`

## Review and PPT Wording

- `该工作围绕{问题}提出了{策略}，通过{关键表征/测试}证明{核心结论}。`
- `从 Figure {n} 可以看出，{关键数据}直接支持{结论}，但该结果仍受{测试条件/对照不足}限制。`
- `该论文的价值不只在于性能提升，还在于将{结构/界面/动力学}与{电化学行为}建立了对应关系。`
- `从论证链来看，作者首先通过{结构/形貌证据}证明{材料设计成立}，随后利用{电化学数据}证明{性能改善}，最后借助{机理表征}解释{改善来源}。`
- `需要注意的是，本文的结论主要建立在{测试条件}下；若要证明其实用价值，还需要在{高负载/全电池/长循环/温度窗口/规模化合成}条件下进一步验证。`
