# Linked-review PDF delivery

Read only when a PDF deliverable is requested or already agreed. The user's layout, length, format, and destination take precedence over the defaults here. PDF delivery does not by itself require a full-length report or an archive.

## Layout and evidence

For a Chinese report with no specified style, use A4, margins around 16–18 mm, readable embedded CJK fonts, restrained blue headings/table headers, and page numbers. Start with the report title, main conclusion, and scope/coverage limits; avoid a decorative cover. Choose sections and table density to fit the question instead of enforcing a fixed report outline.

Use representative evidence that connects the papers and makes synthesis, testing, performance, or mechanism comparisons auditable. Include original paper ID and figure/panel/page in captions and explain what is observed, what is inferred, and the main limit. Prefer readable crops to unreadably reduced full figures; do not crop away relevant axes, legends, or conditions. Do not invent replacement data figures for missing source images.

Keep units, normalization bases, and source locations visible in tables. Split wide tables rather than shrinking text excessively. Use the field and evidence rules in the skill; PDF styling must not change scientific conclusions.

## Destination and optional archive

Save to the user's explicit destination or an already agreed session location. Otherwise use the task's output folder. Avoid exposing local filesystem paths inside a report intended for sharing.

When archival delivery is requested or already agreed, resolve the archive root in this order:

1. The user's explicit or existing session archive location.
2. The environment variable `CODEX_LITERATURE_ARCHIVE_ROOT`, if set.
3. `~/CodexLiteratureArchive/Skill生成结果_含原始文献PDF归档`.

The optional PDF archive convention is `03_多论文联合与同一方面深度分析_skill/{topic-short-name}/`, with `生成结果PDF/` for final PDFs and `原始文献PDF/` for available original PDFs actually used. Expand home/environment paths with the runtime's path utilities. Copy sources without altering originals; deduplicate identical bytes and retain distinct versions. State unavailable source PDFs rather than inventing or fetching replacements silently. Keep working notes, extracted tables/text, and rendered QA images in a separate working directory. This PDF-only convention applies only to this archive and does not restrict user-requested Markdown, spreadsheets, or other deliverables elsewhere. Do not clean up or delete existing files unless asked.

## Export checks

Render the PDF before delivery and inspect the first and last pages plus representative figure/table pages; for a short report inspect every page. Fix missing glyphs, clipped or overflowing content, unreadable figures/tables, and pagination issues. Check source captions, reported units, and material numerical claims in the rendered output. If an archive was requested, verify the final report and available source copies at the resolved destination and keep newly generated intermediates outside it. Deliver a working file link with any unresolved coverage or rendering limit.
