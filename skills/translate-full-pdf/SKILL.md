---
name: translate-full-pdf
description: "Translate complete PDFs into Chinese while preserving the original visual layout, images, figures, and page structure, then export a translated PDF. Use when the user asks to translate a full PDF/article/paper/book/report, says phrases such as 翻译全文, 翻译整篇文章, 整篇PDF翻译, 导出翻译后的PDF, 保留图片/格式/版式, or wants the same workflow of using the original PDF as a page background, covering source text, writing Chinese text, and manually fixing broken tables when needed."
---

# Translate Full PDF

## Purpose

Produce a readable Chinese PDF translation of a full source PDF while keeping the original page design and images intact. Prefer a visual-preservation workflow over plain text extraction: use each original page as the background, cover source text blocks, insert translated Chinese text, keep figure/image regions untouched, and inspect rendered previews before finishing.

## Output Location

Always save the final translated PDF in the user's PDF-only archive. Resolve the archive root from `CODEX_LITERATURE_ARCHIVE_ROOT` when set; otherwise use `~/CodexLiteratureArchive/Skill生成结果_含原始文献PDF归档`.

`${CODEX_LITERATURE_ARCHIVE_ROOT:-~/CodexLiteratureArchive/Skill生成结果_含原始文献PDF归档}/01_翻译全文_skill/{source-stem}/生成结果PDF/`

Also copy the original source PDF into:

`${CODEX_LITERATURE_ARCHIVE_ROOT:-~/CodexLiteratureArchive/Skill生成结果_含原始文献PDF归档}/01_翻译全文_skill/{source-stem}/原始文献PDF/`

Use a clear final filename such as `<source-stem>_中文翻译版.pdf`. The archive folders must contain PDFs only: final translated PDFs and original literature PDFs. Keep preview PNGs, caches, table-overlay JSON, extracted text, Markdown drafts, and other intermediate files outside the archive, preferably under `/tmp` or a task working directory; delete or ignore them after QA.

## Workflow

1. Inspect the PDF first.
   - Confirm page count, text layer quality, page size, and rough image/figure locations.
   - Use the bundled `pdf` skill as needed for PDF basics.
   - If the PDF is scanned with no text layer, OCR first, then continue.

2. Run the bundled translator script.
   - Use the Codex bundled Python when available because it usually has PDF libraries:

```bash
python3 "$CODEX_HOME/skills/translate-full-pdf/scripts/translate_full_pdf.py" "/path/to/source.pdf"
```

   - If `fitz` / PyMuPDF is missing, install it into the active Python environment:

```bash
python3 -m pip install pymupdf
```

3. Review rendered previews.
   - Render preview PNGs to `/tmp` or another scratch folder, not inside the final archive.
   - Always inspect at least: first page, one figure-heavy page, one dense text page, one table page, and the last page.
   - Check for question marks/garbled Chinese, missing images, text overflows, and tables whose original text was split into unusable fragments.

4. Fix layout issues, then rerun.
   - If Chinese renders as `????`, switch to a real CJK font with `--font`.
   - If a table is broken, create a table overlay JSON and rerun with `--table-overlays`.
   - Keep images and figure internals untranslated unless the user explicitly asks to translate figure text.

5. Deliver the final PDF.
   - Place the final PDF in the `生成结果PDF` subfolder and the source PDF in the paired `原始文献PDF` subfolder.
   - Mention both final archive paths and whether previews were checked.
   - Do not leave non-PDF files in the archive.

## Final Archive Rules

- Final archive root: `CODEX_LITERATURE_ARCHIVE_ROOT` if set, otherwise `~/CodexLiteratureArchive/Skill生成结果_含原始文献PDF归档`.
- This skill's category folder is `01_翻译全文_skill`.
- Each translated paper gets its own `{source-stem}` folder with exactly two PDF-focused subfolders: `生成结果PDF` and `原始文献PDF`.
- The archive is PDF-only. Do not save `.md`, `.txt`, `.json`, `.png`, `.jpg`, caches, logs, extracted pages, or skill zip files there.
- If the user later asks to delete old copies, first verify the archived PDFs exist and match, then move old copies to Trash rather than permanently deleting them.

## Table Overlays

Use table overlays only for tables that look bad after automatic block replacement. The overlay JSON covers the old table area and draws a clean translated table.

Example:

```json
[
  {
    "page": 5,
    "area": [50.5, 455.0, 293.5, 583.5],
    "title": "表 1. DRT 峰值及其在 ASSB 中可能的归属总结",
    "columns": ["峰", "时间常数 (s)", "动力学过程"],
    "rows": [
      ["D1", "10−7–10−6", "固态电解质晶界"],
      ["D2", "10−5–10−4", "正极颗粒之间，以及集流体与正极之间的接触"]
    ]
  }
]
```

Run:

```bash
python3 "$CODEX_HOME/skills/translate-full-pdf/scripts/translate_full_pdf.py" \
  "/path/to/source.pdf" \
  --output "$HOME/CodexLiteratureArchive/Skill生成结果_含原始文献PDF归档/01_翻译全文_skill/source/生成结果PDF/source_中文翻译版.pdf" \
  --table-overlays "/path/to/table_overlays.json"
```

## Notes

- The default translation backend is the public Google Translate endpoint. If it is blocked or quality is insufficient, translate blocks with another available translator or the model, then adapt the cache JSON.
- Keep terminology consistent for battery papers: cathode = 正极, anode = 负极, solid electrolyte = 固态电解质, interphase = 界面相, all-solid-state battery = 全固态电池, energy barrier = 能垒.
- Do not call the job done until the generated PDF has been rendered and spot-checked.
