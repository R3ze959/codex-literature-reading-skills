---
name: comprehensive-paper-analysis
description: Deep single-paper reading, explanation, and critical analysis for academic articles, PDFs, research papers, and review articles. Use when the user asks to comprehensively analyze, fully explain, teach from beginning to end, summarize in depth, extract methods/results/data, explain every figure/table, define parameters, assess novelty/evidence/limitations, connect the paper to the field, identify follow-up experiments or innovation points, or produce Chinese study notes/report/PDF/PPT-ready wording for one paper/article, especially scientific and battery/materials papers.
---

# Comprehensive Paper Analysis

## Overview

Use this skill to produce a complete Chinese learning-oriented and critique-oriented analysis of one paper. The default style should be beginner-friendly but technically precise: follow the original paper's logic, explain terms and parameters, analyze each main figure/table separately, and also evaluate the paper's scientific question, novelty, evidence chain, methodological reliability, limitations, and value to the field.

## Workflow

1. **Inspect the paper first.** Identify title, authors, journal, year, DOI, page count, sections, main figures/tables, supplementary-material references, and whether the PDF has a usable text layer. Use the `pdf` skill for PDF extraction/rendering.

2. **Build the paper map.** Reconstruct the author's logic in order:
   - Research background and unresolved problem.
   - Hypothesis or design idea.
   - Materials, methods, and experimental system.
   - Results in the same order as the figures.
   - Mechanism discussion.
   - Conclusions, significance, and limitations.

3. **Analyze the paper itself, not only the figures.** Extract and critique:
   - The central scientific question and why it matters.
   - The authors' implicit assumptions and design logic.
   - The novelty relative to prior work as stated by the authors and as inferable from the paper.
   - The evidence chain: which experiments support which claims.
   - The methods' reliability, controls, reproducibility, and possible confounders.
   - The strength and weakness of the conclusions.
   - The paper's position in the broader field and what it changes.

4. **Explain from shallow to deep.** Start each major section with plain-language intuition, then add technical details. Define equations, abbreviations, units, electrochemical parameters, characterization terms, and domain-specific assumptions when first used.

5. **Analyze every main figure/table.** For each figure:
   - State the question the figure answers.
   - Explain each panel, axis, unit, symbol, color/legend, and experimental condition.
   - Extract the key numbers.
   - Explain the direct conclusion and what cannot be concluded.
   - Link the figure back to the paper's argument.

6. **Extract experimental reproducibility details.** Capture synthesis recipes, electrode preparation, cell assembly, electrolyte/separator/current collector, active material ratio, mass loading, voltage window, rate definition, cycle protocol, CV/EIS/GITT settings, and data-processing formulas. Use `未报道/未明确` for missing information.

7. **Assess evidence strength.** Separate reported facts from interpretation. Flag weak controls, missing comparisons, possible artifacts, unfair baselines, overclaiming, and limits of generalization. Identify what additional experiment would most directly strengthen or falsify the authors' claim.

8. **Produce reusable Chinese writing.** Include polished paragraphs for literature review, concise PPT bullets, and optionally a glossary or study checklist. If the user asks to export a PDF/docx/pptx, use the corresponding document skill and render-check the result. When exporting a PDF learning report, read `references/pdf-report-style.md` and follow that standard report format.

9. **Save exported PDFs to the final PDF archive.** When exporting a PDF report from this skill, resolve the archive root from `CODEX_LITERATURE_ARCHIVE_ROOT` when set; otherwise use `~/CodexLiteratureArchive/Skill生成结果_含原始文献PDF归档`. Save the final report under `02_全文解析_skill/{paper-short-name}/生成结果PDF/`, and copy the original literature PDF into the paired `原始文献PDF/` folder. Use a filename based on the paper title, with `讲解`, `全面解析`, or another clear Chinese suffix.

## Default Output Structure

1. `一句话读懂`
2. `论文基本信息`
3. `背景：作者为什么做这项研究`
4. `核心科学问题、假设和作者的论证路线`
5. `创新点分析：真正新在哪里`
6. `实验体系与方法细节`
7. `按原文逻辑逐节讲解`
8. `逐图/逐表详细讲解`
9. `关键数据汇总表`
10. `证据链分析：每个结论由哪些数据支撑`
11. `方法可靠性、对照实验和可重复性评价`
12. `与领域背景的关系：它推进了什么`
13. `论文贡献、局限、潜在争议和可延伸问题`
14. `后续实验建议和可创新点`
15. `可直接用于综述/PPT的中文表述`
16. `术语表`

Read `references/figure-and-method-template.md` when drafting a full report; it includes figure, method, evidence-chain, critique, and writing templates.

For exported PDF reports, also read `references/pdf-report-style.md`. The PDF must follow the user's standard report style: title-first page with one-sentence summary and boundary note, numbered blue section headings, dense tables, figure image followed by explanation subsections, footer page numbers, and visual QA after rendering.

## Output Location

For generated PDF reports, use the PDF-only archive root. Resolve it from `CODEX_LITERATURE_ARCHIVE_ROOT` when set; otherwise use:

`~/CodexLiteratureArchive/Skill生成结果_含原始文献PDF归档`

This skill's category folder is `02_全文解析_skill`. For each paper, create:

- `{paper-short-name}/生成结果PDF/` for the final analysis PDF.
- `{paper-short-name}/原始文献PDF/` for the original source PDF.

The archive must contain PDFs only: final report PDFs and original literature PDFs. Put rendered QA pages, figure crops, extracted text, Markdown drafts, JSON files, and other intermediate artifacts in `/tmp` or a separate working folder, not in the archive. Mention the final absolute archive path in the response.

## Quality Rules

- Do not skip figures. If a figure is supplementary-only and not in the provided file, state that it is referenced but unavailable.
- Do not invent missing methods, ratios, or parameters.
- Keep exact reported values and units.
- Make comparison basis explicit: active material mass, electrode mass, full cell, areal loading, volumetric basis, or unspecified.
- For beginner users, explain what a parameter measures before interpreting whether the value is good or bad.
- Do not let figure explanation replace paper analysis. Always include the broader argument, methods, novelty, evidence strength, and field significance.
- When judging novelty, distinguish `作者声称的新颖性`, `从本文证据可确认的新颖性`, and `仍需文献对比确认的新颖性`.
- When judging mechanisms, separate direct evidence from plausible interpretation.
- Include at least one section on "what experiment would make this paper stronger" for research users unless the user asks for a short answer.
- If exporting a learning PDF, embed readable figures, save the final PDF in the `02_全文解析_skill/{paper-short-name}/生成结果PDF/` archive folder, copy the source PDF to `原始文献PDF/`, follow `references/pdf-report-style.md`, and verify rendered pages before final delivery.
- Do not leave non-PDF files in the final archive. The archive should contain only final generated PDFs and original literature PDFs.
- If the user later asks to delete old copies, first verify the archived PDFs exist and match, then move old copies to Trash rather than permanently deleting them.
