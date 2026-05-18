# Multi-Paper Materials Report Template

Use this reference when producing a full linked-analysis report.

## Paper Card Fields

| Field | Required content |
|---|---|
| Bibliography | Title, year, journal, first/corresponding group if identifiable |
| Core claim | What the paper proves in one sentence |
| Material system | Formula, phase, dopant/coating/composite, morphology, particle size |
| Synthesis | Precursors, ratios, solvent, method, atmosphere, temperature, time, post-treatment |
| Structure evidence | XRD/Rietveld, SEM/TEM, XPS, Raman, in/ex situ evidence |
| Electrode recipe | Active/conductive/binder ratio, binder type, solvent, current collector, loading |
| Cell setup | Half/full cell, counter/reference electrode, electrolyte, separator, cell format |
| Test protocol | Voltage window, current rates, C-rate definition, temperature, cycle count, CV/EIS/GITT settings |
| Key performance | Capacity, ICE, rate data, long-cycle retention, CE, impedance, diffusion coefficient |
| Mechanism | Reported storage mechanism, phase transition, structural stability, Li diffusion pathway |
| Limits | Missing parameters, weak controls, comparability caveats |

## Comparison Tables

### Materials-Synthesis-Test-Performance Table

| Paper | Material design | Synthesis method | Electrode/cell setup | Test window/rates | Best rate data | Long-cycle data | Main mechanism | Caveats |
|---|---|---|---|---|---|---|---|---|

### Key Electrochemical Data Table

| Paper | Material | Cell type | Loading | Voltage | Current/rate | Capacity | Cycle number | Retention | CE/ICE | Notes |
|---|---|---|---|---|---|---|---|---|---|---|

### Support/Contradiction Matrix

| Topic | Papers supporting | Papers conflicting | Likely reason | What experiment resolves it |
|---|---|---|---|---|

## Inheritance Map Pattern

Use a timeline or Mermaid flowchart:

```mermaid
flowchart LR
  A["Discovery / baseline material"] --> B["Morphology or synthesis optimization"]
  B --> C["Composite/coating/doping strategy"]
  C --> D["Mechanism verification"]
  D --> E["Practical-cell or high-loading validation"]
```

## Chinese Review Wording Templates

Use polished, evidence-aware language:

- `围绕{材料}的研究首先集中于{结构/储锂机制/本征优势}，随后逐步转向{形貌调控/界面工程/复合导电网络/实际电极条件}。`
- `{Paper A}奠定了{基准性能/结构认识}，而{Paper B}通过{策略}解决了{问题}，使{倍率/循环/稳定性}得到提升。`
- `多篇研究共同表明，{性能提升}并非单一因素导致，而是{离子扩散路径、电子导电性、颗粒尺度、界面稳定性}协同作用的结果。`
- `现有工作仍主要停留在{半电池/低负载/短循环/经验优化}层面，对{高负载全电池、失效机理、规模化合成、界面副反应}的系统研究不足。`

## PPT Slide Patterns

### Slide: Field Mainline

- Title: `{材料}研究从结构认知走向实用化电极设计`
- Bullets:
  - `早期：确认晶体结构与储锂机制，建立基准容量和倍率性能。`
  - `中期：通过纳米化、导电复合、包覆或掺杂改善动力学。`
  - `近期：关注高负载、长循环、全电池和机理诊断。`

### Slide: Innovation Opportunities

- `机会1：围绕{矛盾/空白}设计控制实验，厘清{机制}。`
- `机会2：把已验证的{材料策略}推进到{高负载/全电池/低温/快充}场景。`
- `机会3：建立统一测试基准，解决现有文献中{不可比参数}导致的性能判断偏差。`
