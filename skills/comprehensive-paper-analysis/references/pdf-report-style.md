# PDF learning report

Read only when a PDF report is requested. User templates, length, accessibility needs, and output location take priority.

## Default layout

Use a compact academic report: A4 portrait, readable CJK font, restrained headings, and page numbers. Start with the paper title, a short finding, and any source limitations; a decorative cover is unnecessary. Blue headings and light table headers are optional style choices.

Follow the paper's argument with as many sections as it needs. Place readable source figures near their explanations, retaining panel labels, axes, legends, scale bars, and source locators. Split dense figures across pages if necessary. Use tables for comparisons and extraction fields only when they improve readability.

Keep numerical values and conditions traceable. Do not convert a proposed mechanism into a caption that says it is proved. Missing SI and unreadable source details must remain visible as limitations in the delivered report.

## Files and archive compatibility

- Respect the user's output location or established session location first, then a configured `CODEX_LITERATURE_ARCHIVE_ROOT`. If neither applies, use a suitable project output folder and report its path.
- When the literature archive workflow is requested or already established, use `{archive-root}/02_全文解析_skill/{paper-short-name}/生成结果PDF/`. With no user/session/configured archive root, the portable fallback is `~/CodexLiteratureArchive/Skill生成结果_含原始文献PDF归档`.
- In that archive workflow, copy available source PDFs into the paired `原始文献PDF/` directory and verify the copies; never move or overwrite originals. Keep scratch renders/extractions outside those final PDF directories. Archive conventions do not authorize deleting existing files or changing a requested output format.

## Render and inspect

Render the final PDF and inspect the first and last pages, figure pages, and dense tables; expand inspection if a repeated layout problem appears. Check CJK glyphs, clipping, page flow, table width, figure legibility, source captions, and page numbers. Fix detected problems and recheck affected pages. If rendering cannot be performed, state that visual layout remains unverified instead of claiming it passed.
