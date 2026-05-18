# Aspect-Focused PDF Report Style

Use this reference whenever `multi-paper-aspect-review` exports a Chinese PDF report. It adapts the user's accepted single-paper report style to focused multi-paper extraction around one narrow research aspect.

## Layout

- Page size: A4 portrait.
- Margins: about 18 mm left/right and 16-18 mm top/bottom.
- Use a CJK-capable Song/Hei font combination. Avoid missing glyph boxes.
- Use restrained academic blue for numbered headings, light blue table headers, black body text, thin grey table grid lines.
- Footer: small grey report title on the left and page number centered or right-aligned.
- Do not create a decorative cover. The first page starts the report directly.
- Keep compact spacing and dense evidence. Avoid large blank regions, decorative blocks, or generic overview pages.

## First Page

Start directly with:

1. Centered report title: `{target aspect} 多论文深度提取报告`.
2. Centered subtitle: `中文主题证据链与创新点报告`.
3. Small centered logic line: `按主题逻辑：...` summarizing the sub-question chain.
4. Small centered output-location line when a file is saved.
5. Three compact paragraphs:
   - `一句话结论：...`
   - `范围边界：...` defining what is inside/outside the selected aspect and what data are missing.
   - `适合用途：...` such as proposal, manuscript mechanism section, PPT, or experiment planning.
6. Section `1. 研究问题与范围界定` with a two-column table.
7. Continue into Section 2 on the first page if space allows.

## Section Order

Use numbered sections. Preferred order:

1. `研究问题与范围界定`
2. `一句话总览结论`
3. `概念拆解与分析框架`
4. `逐篇主题证据卡`
5. `主题证据对比表`
6. `关键数值与实验条件表`
7. `一致结论、矛盾点与可能原因`
8. `证据强度与可比性评级`
9. `机制整合模型`
10. `研究空白与可创新点`
11. `下一步查补清单`
12. `可直接用于综述/PPT的中文表述`
13. `最终判断`

Adapt section count to the aspect, but keep the first-page structure, numbered blue headings, dense tables, and final judgment.

## Figure And Evidence Pages

Use aspect-centered evidence figures, not a full figure-by-figure summary.

- Choose figures that directly prove the selected aspect: operando/in situ traces, lattice-parameter plots, diffusion paths, activation barriers, spectroscopy, microscopy, phase evolution, failure evidence, or synthesis-condition evidence.
- Heading format: `{n}. Evidence Figure：{paper short name / figure number / aspect role}`.
- Place a readable crop or full-page image immediately below the heading.
- Caption format: `原图裁剪：{paper short name} Figure {i}，用于证明 {aspect claim}.`
- Subsections:
  - `{n}.1 这张图对该主题证明了什么`
  - `{n}.2 关键分图/数据点`
  - `{n}.3 证据强度与局限`
  - `{n}.4 与其他论文的对应或冲突`
- Mention axes, units, state of charge, temperature, voltage window, scan/current rate, sample names, and physical level.

## Tables

Use dense tables with light blue header rows and thin grey grid lines. Include at least:

- Scope boundary table.
- Aspect taxonomy table.
- One evidence card per paper or compact evidence-card table.
- Theme evidence comparison table.
- Key values and experimental conditions table.
- Agreement/contradiction/non-comparability table.
- Evidence-strength rating table.
- Gap-to-experiment innovation table.

Use `未报道/未明确/需查补充信息` for missing details. Never invent values.

## Writing Style

- Chinese, theme-focused, technically precise.
- Stay on the selected aspect. Do not drift into whole-paper summaries unless needed for context.
- Distinguish `原文报道`, `作者解释`, and `Codex推断`.
- Separate physical levels carefully, for example unit-cell volume, lattice plane spacing, particle dimension, electrode thickness, and full-cell swelling.
- Preserve exact reported values and units before normalizing.
- Innovation ideas must include a concrete validation experiment, expected data, and a falsification criterion when possible.

## Export And QA

- Save final generated PDFs under `${CODEX_LITERATURE_ARCHIVE_ROOT:-~/CodexLiteratureArchive/Skill生成结果_含原始文献PDF归档}/03_多论文联合与同一方面深度分析_skill/{topic-short-name}/生成结果PDF/` unless the user explicitly requests another location.
- Copy all original literature PDFs used by the report into the paired `{topic-short-name}/原始文献PDF/` folder, deduplicating repeated downloads of the same paper.
- The final archive must contain PDFs only: final report PDFs and original literature PDFs. Keep Markdown drafts, extracted text, tables, JSON, figure crops, rendered QA PNGs, logs, and caches outside the archive.
- Render at least the first page, one figure/evidence page, one table-heavy page, and the last page to PNG in `/tmp` or a separate working folder before final delivery.
- Check that Chinese glyphs render, headings are numbered and blue, tables fit page width, figures are readable, no decorative cover or huge blank first page appears, footer/page numbers are present, and the archive topic folder contains only PDFs under `生成结果PDF/` and `原始文献PDF/`.
