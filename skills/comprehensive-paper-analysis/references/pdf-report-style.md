# PDF Report Style

Use this reference whenever `comprehensive-paper-analysis` exports a Chinese PDF learning report. Match a dense academic report style: title-first first page, compact Chinese explanation, numbered blue headings, dense tables, figure crops followed by explanation, and footer page numbers.

## Layout

- Page size: A4 portrait.
- Margins: about 18 mm left/right and 16-18 mm top/bottom.
- Main font: readable Chinese Song/Heiti combination. Use a CJK-capable font; avoid missing glyph boxes.
- Color: restrained academic blue for headings, light blue table headers, black body text.
- Footer: small grey report title on the left and page number centered or right-aligned. Do not make a decorative cover.
- The first page starts the report directly: large centered paper title, subtitle `中文全面解析报告`, one short logic-line, output location, then summary paragraphs and a basic information table.
- Use compact spacing and dense text. Avoid large blank regions, card-like callouts, oversized typography, or decorative blocks.

## First Page Structure

1. Centered paper title, wrapped into 2-3 lines if long.
2. Centered subtitle: `中文全面解析报告`.
3. Small centered line: `按原文逻辑：...` summarizing the argument flow.
4. Small centered output-location line.
5. Three compact paragraphs:
   - `一句话读懂：...`
   - `重要边界：...` describing unavailable SI, missing methods, or extraction limits.
   - `适合读者：...`
6. Section `1. 论文基本信息` with a two-column table.
7. Continue into Section 2 on the first page if space allows.

## Section Order

Use numbered sections instead of the unnumbered chat-output template. Preferred order:

1. `论文基本信息`
2. `先补基础：这篇文章到底在解决什么问题`
3. `按原文逻辑拆解`
4. `实验体系与方法细节`
5. `Figure 1：{figure-specific title}`
6. `Figure 2：{figure-specific title}`
7. Continue one section per main figure.
8. `关键数据总表`
9. `证据链：每个结论由哪些数据支撑`
10. `论文价值与创新点`
11. `局限、疑问与可改进处`
12. `后续研究空白与创新点建议`
13. `可直接用于综述/PPT的中文表述`
14. `术语表`
15. `最终判断`

For a paper with fewer or more main figures, adapt the figure section count but keep the surrounding structure.

## Figure Sections

Each main figure gets its own numbered section:

- Heading format: `{n}. Figure {i}：{one-line figure role}`.
- Place a readable crop or full page image of the figure immediately below the heading. Use enough width for panel labels and axes to be legible.
- Caption format: `Figure {i} 原图裁剪：{what the figure proves}.`
- Subsections:
  - `{n}.1 这张图想回答什么`
  - `{n}.2 分图细讲`
  - `{n}.3 关键补充数据` when useful.
  - `{n}.4 这张图的结论` when useful.
- Explain panels with bullets starting `• a：`, `• b：`, etc. Keep panel explanations compact but technically precise.
- Mention axes, units, colors/legends, key values, and what cannot be concluded.

## Tables

- Use dense tables with light blue header rows and thin grey grid lines.
- Keep table cells concise; wrap long content naturally.
- Include at least:
  - Basic information table.
  - Beginner parameter table if the paper has many electrochemical/characterization parameters.
  - Method/system table.
  - Key data table.
  - Evidence-chain table.
- Use `未报道/未明确` for missing details, never invent values.

## Writing Style

- Chinese, learning-oriented, technically precise.
- Explain from intuition to mechanism.
- Keep exact reported values and units.
- Separate direct evidence from interpretation and caveats.
- Include `重要边界` early when Supporting Information is missing or when values are not in the provided file.
- For battery papers, always clarify capacity basis, voltage window, current/rate definition, loading, full-cell normalization, and whether comparisons are fair.

## Export And QA

- Save final generated PDFs under `${CODEX_LITERATURE_ARCHIVE_ROOT:-~/CodexLiteratureArchive/Skill生成结果_含原始文献PDF归档}/02_全文解析_skill/{paper-short-name}/生成结果PDF/` unless the user explicitly requests another location.
- Copy the original source literature PDF into the paired `{paper-short-name}/原始文献PDF/` folder.
- The final archive must contain PDFs only: final report PDFs and original literature PDFs. Keep figure crops, rendered QA PNGs, extracted text, Markdown drafts, JSON, logs, and caches outside the archive.
- Render at least the first page, one figure page, one table-heavy page, and the last page to PNG in `/tmp` or a separate working folder before final delivery.
- Check for:
  - Chinese glyphs render correctly.
  - Headings are numbered and blue.
  - Tables fit the page width.
  - Figure labels and axes are readable.
  - No huge blank first page or malformed title.
  - Footer/page numbers present.
  - The archive paper folder contains only PDFs and has both `生成结果PDF/` and `原始文献PDF/`.
