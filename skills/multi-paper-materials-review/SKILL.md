---
name: multi-paper-materials-review
description: Multi-paper linked analysis for materials science, battery, electrochemistry, and functional-materials literature. Use when the user provides or plans to provide multiple papers/PDFs/articles about one material system, such as Nb14W3O44, and wants core summaries, material/synthesis/test-system extraction, electrochemical parameter and performance comparison, paper-to-paper inheritance, supporting or contradictory results, field development mainline, research gaps, innovation ideas, or Chinese review/PPT-ready wording.
---

# Multi-Paper Materials Review

## Overview

Use this skill to turn several related materials papers into a linked Chinese analysis report rather than isolated paper summaries. The default output should help the user write a literature review, design experiments, or build PPT slides.

## Workflow

1. **Confirm scope from files and prompt.** Identify the target material/system, application, and paper set. If the user has not specified an output format, default to a structured Chinese report with comparison tables. Ask only for blockers; otherwise proceed and mark missing details as `未报道/未明确`.

2. **Ingest each paper.** For PDFs, use the PDF-reading workflow first. Extract the title, year, authors/team, journal, target material, research question, experimental route, and all main figures/tables relevant to synthesis, structure, cell configuration, and performance.

3. **Create one paper card per article.** Each card must include:
   - Core contribution in 3-6 Chinese sentences.
   - Material system: composition, phase, dopants, morphology, particle size, coating/composite design, crystal-structure claims.
   - Synthesis route: precursors, molar/mass ratios if reported, solvents, atmosphere, temperature/time, calcination/annealing, post-treatment, scale and reproducibility notes.
   - Electrode/cell/test system: active material/conductive agent/binder ratio, mass loading, current collector, electrolyte, separator, counter/reference electrode, coin/pouch/three-electrode format, voltage window, temperature, rate settings, cycling protocol, CV/EIS/GITT/PITT settings, activation steps.
   - Key data: first-cycle capacity/ICE, rate capability, long-cycle retention, Coulombic efficiency, diffusion coefficient, impedance values, structural-change evidence, and final headline performance.
   - Limitations: what is missing, what is weakly controlled, and what affects comparison fairness.

4. **Normalize before comparing.** Convert units only when unambiguous. Keep both original and normalized forms when useful. Always state the basis of comparison: active material mass, electrode composite mass, cathode/anode mass, full cell, areal capacity, or volumetric basis. Flag unfair comparisons such as different voltage windows, mass loading, electrolyte amount, current definitions, half-cell versus full-cell, and small-cycle versus long-cycle data.

5. **Build the cross-paper analysis.** Compare papers along time, material design, synthesis, mechanism, and performance:
   - Inheritance: which paper established the material, which improved morphology/synthesis, which added coating/doping/composite, which moved toward practical cells.
   - Mutual support: repeated mechanisms, consistent structure-performance links, repeated electrochemical trends.
   - Contradictions: opposite claims, inconsistent capacities/rate performance, different explanations for the same behavior, incompatible test settings.
   - Development mainline: summarize the field's trajectory from discovery to optimization to mechanism to application.

6. **Generate research gaps and innovation points.** Combine evidence across papers; do not list generic ideas. Prefer gaps tied to specific contradictions, untested regimes, missing controls, or practical bottlenecks. For each innovation idea, state the rationale, feasible experiment, expected data, and risk.

7. **Produce writing-ready Chinese.** Include polished paragraphs suitable for a review article and concise bullets suitable for PPT. Keep claims traceable to papers and avoid overstating beyond the evidence. If the user asks for an exported PDF report, read `references/pdf-report-style.md`, follow the user's standard dense Chinese report style, save the final PDF in the user's PDF-only archive, copy the original literature PDFs into the paired source-PDF folder, and render-check representative pages before final delivery.

## Output Structure

Default to this order unless the user requests another format:

1. `总览结论`: one-page executive summary.
2. `逐篇论文核心摘要`: one subsection per paper.
3. `材料-合成-测试-性能对比表`: dense comparison table.
4. `关键数据表`: rate/cycling/ICE/retention/impedance/diffusion values.
5. `论文之间的继承关系`: timeline or Mermaid flowchart when helpful.
6. `互相支持与互相矛盾`: evidence matrix.
7. `领域发展主线`: 3-6 paragraph narrative.
8. `研究空白与可创新点`: prioritized, experiment-ready ideas.
9. `可直接用于综述/PPT的中文表述`: review paragraphs plus slide bullets.
10. `可比性与证据强度提示`: what cannot be directly compared and why.

For detailed table schemas and Chinese phrasing templates, read `references/report-template.md` when drafting a full report.

For exported PDF reports, also read `references/pdf-report-style.md`. Use the user's standard report format: direct title-first page, concise `一句话总览` and `重要边界`, numbered blue headings, dense comparison tables, readable figure/evidence pages, footer page numbers, and visual QA after rendering.

## Output Location And Archive Workflow

Use the PDF-only archive root. Resolve it from `CODEX_LITERATURE_ARCHIVE_ROOT` when set; otherwise use:

`~/CodexLiteratureArchive/Skill生成结果_含原始文献PDF归档`

This skill shares the multi-paper category with `multi-paper-aspect-review` because their source papers often overlap:

`03_多论文联合与同一方面深度分析_skill/{topic-short-name}/`

Inside each topic folder, create exactly two PDF-focused subfolders:

- `生成结果PDF/` for the final multi-paper review PDF.
- `原始文献PDF/` for all original literature PDFs used by the report.

The archive must contain PDFs only. Do not save Markdown drafts, extracted text, tables, JSON, figure crops, rendered PNG QA pages, caches, logs, or skill zip files in the archive. Put intermediate files in `/tmp` or a separate working folder and keep only the final report PDF plus original source PDFs in the archive. Deduplicate original PDFs when there are repeated downloads of the same paper.

## Quality Rules

- Do not invent missing synthesis ratios, cell recipes, or test parameters. Use `未报道`, `未明确`, or `需查补充信息`.
- Distinguish direct extraction from inference: write `原文报道` for values and `推断/可能原因` for interpretation.
- Cite paper names and figure/table/page identifiers whenever available.
- Preserve exact reported values before normalizing; include units.
- Treat electrochemical data carefully: rate performance is not comparable unless voltage window, current definition, loading, electrode composition, and cell type are known.
- When conclusions conflict, do not force agreement. Explain whether the conflict may come from material differences, synthesis history, electrode recipe, test window, mass loading, or reporting basis.
- When exporting a PDF, embed readable representative figures or evidence crops when available, keep tables within page width, avoid decorative cover pages, and verify at least the first page, one figure/evidence page, one table-heavy page, and the last page.
- After exporting, verify that the archive topic folder contains only PDFs and that the original literature PDFs have been copied into `原始文献PDF/`.
- If the user later asks to delete old copies, first verify the archived PDFs exist and match, then move old copies to Trash rather than permanently deleting them.
