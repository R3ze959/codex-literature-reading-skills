# Offline translation and layout

Use this helper for a PDF with a usable text layer. It needs Python and PyMuPDF (`pymupdf`; tested with 1.27.2.3); use an existing compatible runtime, or install dependencies in an isolated environment. It does not perform OCR or call an LLM API. The active agent supplies the translations.

Paths below are examples. Resolve the script relative to this skill's actual installation directory; do not assume `CODEX_HOME` is set. Run `--help` for the current options.

## Extract

```bash
python3 /path/to/translate-full-pdf/scripts/translate_full_pdf.py source.pdf \
  --extract-only --manifest /path/to/work/blocks.json
```

The manifest contains a schema version, source PDF SHA-256, language pair, page count, author-translation setting, and identified text blocks. Each block records `id`, `page`, `bbox`, `source`, `action`, and `translation`. Translate the blocks marked `translate` by replacing their null `translation` fields with complete translations. Keep source text, IDs, coordinates, actions, and document metadata unchanged. Review `preserve` decisions against the source image; intentional preservation must not hide untranslated prose.

For parallel translation, distribute disjoint block IDs/page ranges in separate files. Merge results into one copy of the original manifest by ID, then check that each required block has exactly one nonempty translation. Resolve disagreements against the PDF and glossary. Do not let workers write the same manifest or cache.

## Render

```bash
python3 /path/to/translate-full-pdf/scripts/translate_full_pdf.py source.pdf \
  --translations /path/to/work/completed.json \
  --output /path/to/results/source_中文翻译版.pdf \
  --workdir /path/to/work
```

The default model backend validates the completed manifest and renders locally. Missing or mismatched translations must not trigger network fallback. Source hashes protect against accidentally applying one paper's translation to another. Pass matching `--source`, `--target`, and `--translate-authors` settings in extraction and rendering when changing their defaults.

Existing results are protected by default. Prefer a new output filename when revising a translation; use `--overwrite` only when replacing that exact result is intended. The helper's default archive subdirectory includes a sanitized source stem and a source-hash suffix so different papers with the same filename stay separate.

The helper is a layout aid, not a scientific or visual acceptance test. Review `layout_stats.json`, rendered previews, and the actual translated PDF. Inspect and repair any blocks listed in `small_font_blocks_review_required`; fitting text into a box does not establish readability. An overflow failure needs a layout repair or a clearly identified reflowed alternative. Changing only the cache cannot repair an unreadable source/OCR error. Formula-heavy, scanned, rotated, and complex table pages may need a separate PDF workflow. Extraction also refuses to overwrite an existing manifest; choose a new path so completed translations remain intact.

## Layout repairs

Use `--font /path/to/cjk-font.ttf` if automatic font discovery fails. For a broken table, supply `--table-overlays /path/to/table-overlays.json` with its one-based page number and PDF-point rectangle, for example:

```json
[
  {
    "page": 2,
    "area": [50, 300, 540, 440],
    "title": "表 1. 测试条件",
    "columns": ["样品", "温度 (°C)"],
    "rows": [["A", "25"], ["B", "40"]]
  }
]
```

Check all original rows, footnotes, symbols, and values before using an overlay; do not replace raw data with guessed values. Review the full region for figures or text that the overlay could cover. Supply the same overlay file at extraction and rendering so its content hash matches the manifest.

## Optional external backend

`--backend google` explicitly selects the legacy public Google Translate endpoint and sends source text there. Use it only within the user's authorization for that external service; a normal model-based translation needs no such step. Availability and translation quality are not guaranteed. `--cache` is for this optional backend; it is not a substitute for the identified model-translation manifest.
