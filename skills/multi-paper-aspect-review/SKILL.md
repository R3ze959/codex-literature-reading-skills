---
name: multi-paper-aspect-review
description: Focused multi-paper literature analysis for one specified aspect/theme across related materials, battery, electrochemistry, or functional-materials papers. Use when the user provides multiple papers/PDFs/articles and asks to extract, compare, and deeply analyze one narrow topic such as structure, zero strain/near-zero volume change, negative thermal expansion, crystallographic shear planes, lithium diffusion mechanism, coating/interface, dopants, synthesis parameter, failure mode, operando evidence, or safety; especially when they want contradictions, evidence strength, research gaps, innovation ideas, Chinese review/PPT-ready wording, or a task-specific PDF/Markdown report.
---

# Multi-Paper Aspect Review

## Overview

Use this skill to turn multiple related papers into a focused, evidence-traceable analysis of one selected aspect, not a general summary of every paper.

Default behavior: produce a detailed Chinese report with aspect-specific evidence cards, comparison tables, contradiction analysis, mechanism explanation, research gaps, and innovation directions, and export a clean PDF report by default. Save the final PDF in the user's PDF-only archive and copy the original literature PDFs into the paired source-PDF folder. Create Markdown only when it helps drafting or the user asks for it, and do not place Markdown or other intermediates in the final archive.

## When To Use

Use this skill when the user asks for multi-paper analysis around one narrow theme, for example:

- "用这个 skill 提取这些 NWO 文献里结构、零应变、负热膨胀相关信息"
- "多篇论文只比较界面包覆对倍率性能的作用"
- "从这些文献里专门分析 Li 扩散路径和势垒矛盾"
- "只看 cracking/failure 机制，做表格和创新点"
- "围绕某一种表征证据做跨文献对比"

If the request is a broad whole-paper review, prefer a general multi-paper review skill. If the request names one aspect, this skill is the tighter fit.

## Workflow

1. Define the scope.
   Identify the paper set, target material/system, and target aspect. If the aspect is vague, infer a bounded aspect from the prompt and state the boundary. Ask only if a missing choice blocks the work.

2. Ingest the papers.
   Use the PDF workflow first for local PDFs. Extract aspect-relevant text, figure captions, tables, methods, and bibliographic context. Do not spend equal effort on unrelated sections.

3. Build an aspect taxonomy.
   Break the aspect into sub-questions before comparing papers. For "NWO structure, zero strain, and negative thermal expansion", useful sub-questions include crystal framework, Wadsley-Roth block type, lattice parameters, anisotropic a/b/c evolution, unit-cell volume change, thermal expansion coefficient, stress/strain mechanism, defect or prestress origin, operando evidence, and link to electrochemical cycling.

4. Create aspect cards.
   Make one card per paper. Each card should include bibliography, why the paper matters for the aspect, direct evidence, quantitative values, measurement conditions, author interpretation, cautious cross-paper inference, and limitations.

5. Normalize evidence.
   Preserve original units and add normalized values when useful. Record state basis such as temperature range, state of charge, voltage window, C-rate, electrode loading, particle size, cell type, and whether the result is thermal, crystallographic, particle-level, electrode-level, or full-cell-level.

6. Compare across papers.
   Separate agreement, partial agreement, contradiction, and non-comparable claims. Do not force a single story if the evidence does not support it.

7. Explain the mechanism deeply.
   Teach the concepts behind the chosen aspect using the papers as evidence. Distinguish reported facts from inference. For strain topics, separate thermal negative expansion, electrochemical lattice volume change, particle swelling, electrode thickness change, and device-level swelling.

8. Rate evidence strength.
   Grade important claims by evidence quality. Prefer direct operando/in situ quantitative evidence, then direct ex situ or computational evidence, then indirect correlations, then speculative claims.

9. Derive gaps and innovation points.
   Tie each gap to a specific missing control, contradiction, weak evidence chain, or untested mechanism. For each innovation point, propose concrete experiments, expected data, and risks.

10. Produce the deliverable.
    Default to Chinese, with tables and writing-ready paragraphs, then export a clean PDF report. Resolve the archive root from `CODEX_LITERATURE_ARCHIVE_ROOT` when set; otherwise use `~/CodexLiteratureArchive/Skill生成结果_含原始文献PDF归档`. Save the final PDF under `03_多论文联合与同一方面深度分析_skill/{topic-short-name}/生成结果PDF/`, and copy all original literature PDFs into the paired `原始文献PDF/` folder. When preparing a full report, load `references/aspect-report-template.md` and `references/pdf-report-style.md`, follow the user's standard dense Chinese report style, and render-check representative pages before final delivery.

## Default Report Structure

Use this structure unless the user requests a different format:

1. 研究问题与范围界定
2. 一句话总览结论
3. 概念拆解与分析框架
4. 逐篇主题证据卡
5. 主题证据对比表
6. 关键数值与实验条件表
7. 一致结论、矛盾点与可能原因
8. 机制整合模型
9. 证据强度与可比性评级
10. 研究空白与可创新点
11. 可直接用于综述/PPT的中文表述
12. 下一步查补清单

## Quality Rules

- Stay on the selected aspect. Mention unrelated synthesis, morphology, or electrochemical data only when it affects the aspect.
- Use labels such as `原文报道`, `作者解释`, and `Codex推断` so evidence and interpretation do not blur.
- Cite paper title or short name plus figure/table/page when available.
- Never invent missing values or test parameters. Use `未报道`, `未明确`, or `需查补充信息`.
- Treat terms carefully. "Zero strain" and "near-zero volume change" may refer to unit-cell volume, lattice plane spacing, particle dimension, electrode thickness, or full-cell swelling. Identify the physical level.
- For electrochemical comparisons, avoid direct ranking unless voltage window, C-rate, temperature, electrode loading, mass basis, and cell format are comparable.
- When contradictions appear, check for differences in synthesis route, defect state, crystallographic model, morphology, lithiation state, measurement method, temperature range, ex situ versus operando evidence, and data normalization.
- For innovation ideas, include what experiment would verify the idea and what result would falsify it.

## Output Style

Write in clear academic Chinese by default. Prefer dense, evidence-rich explanation over broad overview. Tables should be compact but specific enough to show what each paper actually proves.

Use English terminology in parentheses when it prevents ambiguity, for example `负热膨胀 (negative thermal expansion, NTE)` or `近零体积变化 (near-zero volume change)`.

For task-specific PDF reports, use `references/pdf-report-style.md`: direct title-first page, concise scope and boundary notes, numbered blue headings, dense evidence tables, aspect-centered figure/evidence pages, footer page numbers, and visual QA after rendering.

## Output Location And Archive Workflow

Use the PDF-only archive root. Resolve it from `CODEX_LITERATURE_ARCHIVE_ROOT` when set; otherwise use:

`~/CodexLiteratureArchive/Skill生成结果_含原始文献PDF归档`

This skill shares the multi-paper category with `multi-paper-materials-review` because their source papers often overlap:

`03_多论文联合与同一方面深度分析_skill/{topic-short-name}/`

Inside each topic folder, create exactly two PDF-focused subfolders:

- `生成结果PDF/` for the final aspect-focused PDF report.
- `原始文献PDF/` for all original literature PDFs used by the report.

The archive must contain PDFs only. Do not save Markdown drafts, extracted text, tables, JSON, figure crops, rendered PNG QA pages, caches, logs, or skill zip files in the archive. Put intermediate files in `/tmp` or a separate working folder and keep only the final report PDF plus original source PDFs in the archive. Deduplicate original PDFs when there are repeated downloads of the same paper.

After exporting, verify that the archive topic folder contains only PDFs and that the original literature PDFs have been copied into `原始文献PDF/`. If the user later asks to delete old copies, first verify the archived PDFs exist and match, then move old copies to Trash rather than permanently deleting them.
