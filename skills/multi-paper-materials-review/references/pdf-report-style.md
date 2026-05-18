# Multi-Paper PDF Report Style

Use this reference whenever `multi-paper-materials-review` exports a Chinese PDF report. It adapts the user's accepted single-paper report style to multi-paper linked literature analysis.

## Layout

- Page size: A4 portrait.
- Margins: about 18 mm left/right and 16-18 mm top/bottom.
- Use a CJK-capable Song/Hei font combination. Avoid missing glyph boxes.
- Use restrained academic blue for numbered headings, light blue table headers, black body text, thin grey table grid lines.
- Footer: small grey report title on the left and page number centered or right-aligned.
- Do not create a decorative cover. The first page starts the report directly.
- Keep compact spacing and dense information. Avoid large blank regions, card-like callouts, oversized typography, or decorative blocks.

## First Page

Start directly with:

1. Centered report title: `{material/system} 多论文联合分析报告`.
2. Centered subtitle: `中文综合综述与研究思路报告`.
3. Small centered logic line: `按文献链条：...` summarizing how the papers connect.
4. Small centered output-location line when a file is saved.
5. Three compact paragraphs:
   - `一句话总览：...`
   - `重要边界：...` describing missing SI, incomplete data, non-comparable test systems, or extraction limits.
   - `适合用途：...` such as literature review, PPT, experiment design, proposal, or manuscript story.
6. Section `1. 文献集合与分析范围` with a two-column table.
7. Continue into Section 2 on the first page if space allows.

## Section Order

Use numbered sections. Preferred order:

1. `文献集合与分析范围`
2. `一句话总览结论`
3. `领域发展主线：这些论文如何接起来`
4. `逐篇论文核心卡`
5. `材料-合成-测试体系对比表`
6. `关键性能与参数总表`
7. `论文之间的继承关系`
8. `互相支持、互相矛盾与不可比点`
9. `机制整合与证据链`
10. `可比性与证据强度提示`
11. `研究空白与可创新点`
12. `可直接用于综述/PPT的中文表述`
13. `最终判断`

Adapt section count to the paper set, but keep the first-page structure, numbered blue headings, dense tables, and final judgment.

## Figure And Evidence Pages

Use figures selectively. Do not force every main figure from every paper into the report.

- Prefer representative figures, phase diagrams, synthesis schematics, operando evidence, performance comparisons, and mechanism figures that support the cross-paper story.
- Heading format: `{n}. Evidence Figure：{paper short name / figure number / role}`.
- Place a readable crop or full-page image immediately below the heading.
- Caption format: `原图裁剪：{paper short name} Figure {i}，用于证明 {claim}.`
- Subsections:
  - `{n}.1 这张图在文献链条中的作用`
  - `{n}.2 关键分图/数据点`
  - `{n}.3 与其他论文的对应或冲突`
  - `{n}.4 可用于综述的结论`
- Explain axes, units, legends, sample names, test conditions, and what cannot be concluded.

## Tables

Use dense tables with light blue header rows and thin grey grid lines. Include at least:

- Paper set and scope table.
- One paper-card table or compact card subsections.
- Material-composition/synthesis/test-system comparison table.
- Electrochemical or functional performance data table.
- Evidence-chain table mapping claims to papers/figures.
- Contradiction/non-comparability table.
- Research-gap and experiment-ready innovation table.

Use `未报道/未明确/需查补充信息` for missing details. Never invent values.

## Writing Style

- Chinese, review-oriented, technically precise.
- Start from the field mainline, then compare evidence.
- Preserve exact reported values and units before normalizing.
- Separate `原文报道`, `作者解释`, and `Codex推断`.
- For battery papers, always clarify capacity basis, voltage window, current/rate definition, loading, cell type, full-cell normalization, and comparison fairness.
- Innovation ideas must be tied to specific evidence gaps, contradictions, missing controls, or practical bottlenecks.

## Export And QA

- Save final generated PDFs under `${CODEX_LITERATURE_ARCHIVE_ROOT:-~/CodexLiteratureArchive/Skill生成结果_含原始文献PDF归档}/03_多论文联合与同一方面深度分析_skill/{topic-short-name}/生成结果PDF/` unless the user explicitly requests another location.
- Copy all original literature PDFs used by the report into the paired `{topic-short-name}/原始文献PDF/` folder, deduplicating repeated downloads of the same paper.
- The final archive must contain PDFs only: final report PDFs and original literature PDFs. Keep Markdown drafts, extracted text, tables, JSON, figure crops, rendered QA PNGs, logs, and caches outside the archive.
- Render at least the first page, one figure/evidence page, one table-heavy page, and the last page to PNG in `/tmp` or a separate working folder before final delivery.
- Check that Chinese glyphs render, headings are numbered and blue, tables fit page width, figures are readable, no decorative cover or huge blank first page appears, footer/page numbers are present, and the archive topic folder contains only PDFs under `生成结果PDF/` and `原始文献PDF/`.
