from __future__ import annotations

import argparse
import hashlib
import html
import json
import os
import re
import shutil
import tempfile
import time
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

import fitz


FONT_CANDIDATES = [
    "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
    "/System/Library/Fonts/STHeiti Medium.ttc",
    "/System/Library/Fonts/Hiragino Sans GB.ttc",
    "/Library/Fonts/Arial Unicode.ttf",
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
]

ARCHIVE_ROOT = Path(
    os.environ.get(
        "CODEX_LITERATURE_ARCHIVE_ROOT",
        Path.home() / "CodexLiteratureArchive" / "Skill生成结果_含原始文献PDF归档",
    )
).expanduser()
DEFAULT_OUTPUT_DIR = ARCHIVE_ROOT / "01_翻译全文_skill"


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Translate a full PDF while preserving page visuals.")
    parser.add_argument("input_pdf", type=Path)
    parser.add_argument("--output", type=Path, default=None)
    parser.add_argument("--workdir", type=Path, default=None)
    parser.add_argument("--source", default="en")
    parser.add_argument("--target", default="zh-CN")
    parser.add_argument("--font", type=Path, default=None)
    parser.add_argument("--cache", type=Path, default=None)
    parser.add_argument("--table-overlays", type=Path, default=None)
    parser.add_argument("--preview-pages", default="1,2,5,last")
    parser.add_argument("--translate-authors", action="store_true")
    parser.add_argument("--backend", choices=("model", "google"), default="model",
                        help="model: offline manifest/render; google: explicitly send text to Google")
    parser.add_argument("--extract-only", action="store_true",
                        help="Export a translation manifest without network access or PDF rendering")
    parser.add_argument("--overwrite", action="store_true", help="Explicitly replace an existing output PDF after successful rendering")
    parser.add_argument("--manifest", type=Path, default=None,
                        help="Extraction destination (default: WORKDIR/translation_manifest.json)")
    parser.add_argument("--translations", type=Path, default=None,
                        help="Complete merged manifest with model-written translations")
    return parser.parse_args(argv)


def find_font(explicit: Path | None) -> Path:
    if explicit:
        if not explicit.exists():
            raise FileNotFoundError(explicit)
        return explicit
    for candidate in FONT_CANDIDATES:
        path = Path(candidate)
        if path.exists():
            return path
    raise FileNotFoundError("No CJK-capable font found. Pass --font /path/to/font.ttf")


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def document_key(input_pdf: Path) -> str:
    safe_stem = re.sub(r"[^A-Za-z0-9_.-]+", "_", input_pdf.stem).strip("_") or "pdf"
    return f"{safe_stem}_{file_sha256(input_pdf)[:12]}"


def default_output_path(input_pdf: Path) -> Path:
    output_dir = DEFAULT_OUTPUT_DIR / document_key(input_pdf) / "生成结果PDF"
    return output_dir / f"{input_pdf.stem}_中文翻译版.pdf"


def default_workdir(input_pdf: Path) -> Path:
    return Path(tempfile.gettempdir()) / "translate_full_pdf_work" / document_key(input_pdf)


def archive_source_pdf(input_pdf: Path, output_pdf: Path) -> None:
    if output_pdf.parent.name != "生成结果PDF":
        return
    paper_dir = output_pdf.parent.parent
    source_dir = paper_dir / "原始文献PDF"
    source_dir.mkdir(parents=True, exist_ok=True)
    target = source_dir / input_pdf.name
    if input_pdf.resolve() != target.resolve():
        if target.exists():
            if file_sha256(target) != file_sha256(input_pdf):
                raise FileExistsError(f"Refusing to replace a different archived source: {target}")
            return
        shutil.copy2(input_pdf, target)


def normalized_text(text: str) -> str:
    text = text.replace("\u00ad", "")
    text = re.sub(r"(?<=\w)-\s+(?=\w)", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def cache_key(text: str, source: str, target: str) -> str:
    payload = f"{source}>{target}\n{text}"
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def split_for_translate(text: str, limit: int = 2600) -> list[str]:
    if len(text) <= limit:
        return [text]
    parts: list[str] = []
    current = ""
    sentences = re.split(r"(?<=[.!?;。；])\s+", text)
    for sentence in sentences:
        if not sentence:
            continue
        if len(current) + len(sentence) + 1 > limit and current:
            parts.append(current.strip())
            current = sentence
        else:
            current = f"{current} {sentence}".strip()
        while len(current) > limit:
            parts.append(current[:limit].strip())
            current = current[limit:].strip()
    if current:
        parts.append(current.strip())
    return parts


def translate_piece(text: str, source: str, target: str, retries: int = 4) -> str:
    url = (
        "https://translate.googleapis.com/translate_a/single?"
        + urllib.parse.urlencode(
            {
                "client": "gtx",
                "sl": source,
                "tl": target,
                "dt": "t",
                "q": text,
            }
        )
    )
    last_error: Exception | None = None
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(url, timeout=30) as response:
                payload = json.loads(response.read().decode("utf-8"))
            return html.unescape("".join(chunk[0] for chunk in payload[0] if chunk and chunk[0]))
        except Exception as exc:
            last_error = exc
            time.sleep(1.2 * (attempt + 1))
    raise RuntimeError(f"Translation failed: {last_error}")


def postprocess_translation(text: str) -> str:
    # Terminology depends on context: never replace cathode/anode or other terms globally.
    return text.strip()


def translate(text: str, cache: dict[str, str], cache_path: Path, source: str, target: str) -> str:
    clean = normalized_text(text)
    if not clean:
        return ""
    key = cache_key(clean, source, target)
    if key in cache:
        return cache[key]
    translated = "".join(translate_piece(piece, source, target) for piece in split_for_translate(clean))
    translated = postprocess_translation(translated)
    cache[key] = translated
    cache_path.write_text(json.dumps(cache, ensure_ascii=False, indent=2), encoding="utf-8")
    time.sleep(0.12)
    return translated


def is_boilerplate(text: str, rect: fitz.Rect, page: fitz.Page) -> bool:
    clean = normalized_text(text)
    # A DOI or "Copyright" embedded in substantive prose must not skip the whole block.
    if len(clean) > 220:
        return False
    if re.fullmatch(r"https?://doi\.org/\S+", clean):
        return True
    if re.match(r"^(Downloaded via\b|©|Copyright\b)", clean) and (rect.y0 > page.rect.height - 100 or rect.y1 < 100):
        return True
    if rect.y0 > page.rect.height - 42 and (clean.isdigit() or "doi.org/" in clean or "www." in clean):
        return True
    if rect.y1 < 53 and ("www." in clean or "Journal" in clean):
        return True
    return clean == "ACS Nano www.acsnano.org Article"


def mostly_nonlanguage(text: str) -> bool:
    clean = normalized_text(text)
    if len(clean) < 2:
        return True
    letters = sum(char.isalpha() for char in clean)
    symbols = sum(not char.isalpha() for char in clean)
    return letters < 3 and symbols > letters


def should_leave_untranslated(text: str, translate_authors: bool) -> bool:
    clean = normalized_text(text)
    if mostly_nonlanguage(clean):
        return True
    if not translate_authors and len(clean) < 350:
        # Require an entire list of names, not a capitalized name somewhere in prose.
        names = re.split(r",\s*|\s+and\s+", clean)
        name_pattern = r"[A-Z][a-z]+(?:[-'][A-Z]?[a-z]+)?(?: [A-Z](?:\.|[a-z]+)){1,3}"
        if len(names) > 1 and all(re.fullmatch(name_pattern, name) for name in names):
            return True
    return False


def font_size_for_block(text: str, rect: fitz.Rect, page_no: int) -> float:
    clean = normalized_text(text)
    if page_no == 1 and rect.y0 < 220:
        return 11.8
    if clean.isupper() and len(clean) < 50:
        return 8.0
    if clean.startswith("Figure") or clean.startswith("Table"):
        return 5.7
    if rect.height < 28:
        return 5.2
    if len(clean) > 3200:
        return 5.0
    if len(clean) > 1800:
        return 5.6
    return 6.2


def insert_fitting_text(
    page: fitz.Page,
    rect: fitz.Rect,
    text: str,
    source_text: str,
    page_no: int,
    font_name: str,
    font_file: Path,
) -> float:
    align = fitz.TEXT_ALIGN_CENTER if page_no == 1 and rect.y0 < 230 else fitz.TEXT_ALIGN_LEFT
    start = font_size_for_block(source_text, rect, page_no)
    sizes = [start, start - 0.35, start - 0.7, start - 1.05, start - 1.4, 4.7, 4.3, 3.9, 3.5]
    for size in [s for s in sizes if s > 0]:
        trial_doc = fitz.open()
        trial_page = trial_doc.new_page(width=page.rect.width, height=page.rect.height)
        trial_page.insert_font(fontname=font_name, fontfile=str(font_file))
        spare = trial_page.insert_textbox(rect, text, fontname=font_name, fontsize=size, align=align)
        trial_doc.close()
        if spare >= 0:
            actual_spare = page.insert_textbox(
                rect,
                text,
                fontname=font_name,
                fontsize=size,
                color=(0.05, 0.05, 0.05),
                align=align,
            )
            if actual_spare < 0:
                raise LayoutOverflow(f"Page {page_no}: text insertion failed at {list(rect)}")
            return size
    raise LayoutOverflow(f"Page {page_no}: text does not fit at {list(rect)}; revise layout or use a concise translation without omitting content")


def load_table_overlays(path: Path | None) -> list[dict[str, Any]]:
    if not path:
        return []
    overlays = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(overlays, list):
        raise ValueError("Table overlays must be a list")
    for item in overlays:
        if not isinstance(item, dict) or not isinstance(item.get("page"), int) or item["page"] < 1:
            raise ValueError("Every table overlay needs a positive integer page")
        columns, rows = item.get("columns"), item.get("rows")
        if not isinstance(columns, list) or not columns or not isinstance(rows, list):
            raise ValueError("Every table overlay needs columns and rows")
        if any(not isinstance(row, list) or len(row) != len(columns) for row in rows):
            raise ValueError("Every table row must match the number of columns")
        widths = item.get("widths", [1] * len(columns))
        if len(widths) != len(columns) or any(not isinstance(w, (int, float)) or w <= 0 for w in widths):
            raise ValueError("Table widths must be positive and match the columns")
        area = item.get("area")
        if not isinstance(area, list) or len(area) != 4 or fitz.Rect(area).is_empty or fitz.Rect(area).is_infinite:
            raise ValueError("Every table overlay needs a valid area rectangle")
    return overlays


def rects_overlap(a: fitz.Rect, b: fitz.Rect) -> bool:
    return not (a.x1 <= b.x0 or a.x0 >= b.x1 or a.y1 <= b.y0 or a.y0 >= b.y1)


class LayoutOverflow(ValueError):
    """A required translation could not be rendered; no final PDF may be saved."""


def checked_textbox(page: fitz.Page, rect: fitz.Rect, text: str, **kwargs: Any) -> None:
    if page.insert_textbox(rect, text, **kwargs) < 0:
        raise LayoutOverflow(f"Page {page.number + 1}: table text does not fit at {list(rect)}")


def draw_table_overlay(page: fitz.Page, overlay: dict[str, Any], font_name: str) -> None:
    area = fitz.Rect(*overlay["area"])
    page.draw_rect(area, color=(1, 1, 1), fill=(1, 1, 1), overlay=True)
    page.draw_line((area.x0, area.y0 + 1), (area.x1, area.y0 + 1), color=(0.86, 0.36, 0.05), width=0.7)
    title_h = 20.0 if overlay.get("title") else 4.0
    if overlay.get("title"):
        checked_textbox(
            page, fitz.Rect(area.x0 + 1.5, area.y0 + 5, area.x1 - 1.5, area.y0 + title_h),
            overlay["title"],
            fontname=font_name,
            fontsize=5.8,
            color=(0.05, 0.05, 0.05),
        )
    columns = overlay["columns"]
    rows = overlay["rows"]
    table_top = area.y0 + title_h + 8
    table_bottom = area.y1 - 8
    row_h = (table_bottom - table_top) / (len(rows) + 1)
    if row_h <= 3:
        raise LayoutOverflow(f"Page {page.number + 1}: table rows exceed the overlay area")
    widths = overlay.get("widths") or [1] * len(columns)
    total = sum(widths)
    xs = [area.x0]
    for width in widths:
        xs.append(xs[-1] + area.width * (width / total))
    page.draw_rect(fitz.Rect(area.x0, table_top, area.x1, table_top + row_h), color=None, fill=(0.9, 0.9, 0.9))
    for row_index, row in enumerate([columns] + rows):
        top = table_top + row_index * row_h
        if row_index > 0 and row_index % 2 == 0:
            page.draw_rect(fitz.Rect(area.x0, top, area.x1, top + row_h), color=None, fill=(0.98, 0.98, 0.98))
        for i, cell in enumerate(row):
            checked_textbox(
                page, fitz.Rect(xs[i] + 1.5, top + 2, xs[i + 1] - 1.5, top + row_h - 1),
                str(cell),
                fontname=font_name,
                fontsize=float(overlay.get("fontsize", 4.5)),
                color=(0.05, 0.05, 0.05),
            )
    for x in xs:
        page.draw_line((x, table_top), (x, table_top + row_h * (len(rows) + 1)), color=(0.78, 0.78, 0.78), width=0.35)
    for i in range(len(rows) + 2):
        y = table_top + i * row_h
        page.draw_line((area.x0, y), (area.x1, y), color=(0.78, 0.78, 0.78), width=0.35)
    page.draw_line((area.x0, area.y1 - 2), (area.x1, area.y1 - 2), color=(0.86, 0.36, 0.05), width=0.7)


def parse_preview_pages(value: str, page_count: int) -> list[int]:
    result: list[int] = []
    for item in value.split(","):
        item = item.strip().lower()
        if not item:
            continue
        page_no = page_count if item == "last" else int(item)
        if 1 <= page_no <= page_count and page_no not in result:
            result.append(page_no)
    return result


def render_previews(pdf_path: Path, out_dir: Path, preview_pages: list[int]) -> None:
    preview_dir = out_dir / "preview"
    preview_dir.mkdir(parents=True, exist_ok=True)
    doc = fitz.open(pdf_path)
    try:
        for page_no in preview_pages:
            pix = doc[page_no - 1].get_pixmap(matrix=fitz.Matrix(1.5, 1.5), alpha=False)
            pix.save(preview_dir / f"page_{page_no:02d}.png")
    finally:
        doc.close()



def build_manifest(
    input_pdf: Path, source: str, target: str, translate_authors: bool,
    overlays_path: Path | None = None,
) -> dict[str, Any]:
    """Extract native text only. OCR and figure/formula decisions require human/model review."""
    overlays = load_table_overlays(overlays_path)
    blocks: list[dict[str, Any]] = []
    page_stats: list[dict[str, Any]] = []
    with fitz.open(input_pdf) as doc:
        if any(item["page"] > len(doc) for item in overlays):
            raise ValueError("Table overlay page is outside the source PDF")
        for page_index, page in enumerate(doc):
            page_no = page_index + 1
            image_rects = [fitz.Rect(item["bbox"]) for item in page.get_image_info()]
            overlay_rects = [fitz.Rect(item["area"]) for item in overlays if int(item["page"]) == page_no]
            if any(not page.rect.contains(area) for area in overlay_rects):
                raise ValueError(f"Page {page_no}: table overlay extends outside the page")
            native_count = 0
            for block_index, block in enumerate(page.get_text("blocks")):
                if len(block) > 6 and block[6] != 0:  # image blocks are never text
                    continue
                clean = normalized_text(block[4])
                if not clean:
                    continue
                native_count += 1
                rect = fitz.Rect(block[:4])
                bbox = [round(v, 4) for v in rect]
                reason = None
                intersecting_overlays = [area for area in overlay_rects if rects_overlap(rect, area)]
                if intersecting_overlays:
                    if not any(area.contains(rect) for area in intersecting_overlays):
                        raise ValueError(f"Page {page_no}: table overlay only partly covers a text block; revise the area")
                    reason = "table-overlay"
                elif any(rects_overlap(rect, area) for area in image_rects):
                    reason = "image-overlap-review"
                elif is_boilerplate(clean, rect, page):
                    reason = "boilerplate-heuristic-review"
                elif should_leave_untranslated(clean, translate_authors):
                    reason = "nonlanguage-or-author-heuristic-review"
                identity = json.dumps([page_no, block_index, bbox, clean], ensure_ascii=False)
                block_id = f"p{page_no:04d}-b{block_index:04d}-{hashlib.sha256(identity.encode()).hexdigest()[:12]}"
                blocks.append({
                    "id": block_id, "page": page_no, "bbox": bbox, "source": clean,
                    "action": "preserve" if reason else "translate", "reason": reason,
                    "translation": None,
                })
            page_stats.append({"page": page_no, "text_blocks": native_count, "image_count": len(image_rects)})
        page_count = len(doc)
    return {
        "schema_version": 1, "source_sha256": file_sha256(input_pdf),
        "source_language": source, "target_language": target, "page_count": page_count,
        "translate_authors": translate_authors,
        "table_overlays_sha256": file_sha256(overlays_path) if overlays_path else None,
        "pages": page_stats,
        "limitations": [
            "Native-text extraction only; scanned text requires OCR and a new reviewed source PDF.",
            "Preservation rules are heuristics. Review authors, equations, figure labels, reading order, and tables.",
            "Original images and vectors are retained except in explicit table-overlay areas; text layout is not pixel-identical.",
        ],
        "blocks": blocks,
    }


def validate_translations(expected: dict[str, Any], supplied: Any) -> dict[str, str]:
    if not isinstance(supplied, dict):
        raise ValueError("Translations must be one merged manifest object")
    for key in ("schema_version", "source_sha256", "source_language", "target_language",
                "page_count", "translate_authors", "table_overlays_sha256"):
        if supplied.get(key) != expected[key]:
            raise ValueError(f"Translation manifest mismatch: {key}")
    supplied_blocks = supplied.get("blocks")
    if not isinstance(supplied_blocks, list):
        raise ValueError("Translation manifest must contain a blocks list")
    expected_blocks = {item["id"]: item for item in expected["blocks"]}
    seen: set[str] = set()
    translations: dict[str, str] = {}
    for item in supplied_blocks:
        if not isinstance(item, dict) or not isinstance(item.get("id"), str):
            raise ValueError("Every translation block needs a string id")
        block_id = item["id"]
        if block_id in seen:
            raise ValueError(f"Duplicate translation block: {block_id}")
        seen.add(block_id)
        if block_id not in expected_blocks:
            raise ValueError(f"Unknown translation block: {block_id}")
        original = expected_blocks[block_id]
        for key in ("page", "bbox", "source", "action"):
            if item.get(key) != original[key]:
                raise ValueError(f"Translation block {block_id} mismatch: {key}")
        if original["action"] == "translate":
            translated = item.get("translation")
            if not isinstance(translated, str) or not translated.strip():
                raise ValueError(f"Empty translation: {block_id}")
            translations[block_id] = translated.strip()
    missing = set(expected_blocks) - seen
    if missing:
        raise ValueError(f"Missing translation blocks: {', '.join(sorted(missing))}")
    return translations


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)
    input_pdf = args.input_pdf.expanduser().resolve()
    if not input_pdf.is_file():
        raise FileNotFoundError(input_pdf)
    output = (args.output or default_output_path(input_pdf)).expanduser().resolve()
    if output == input_pdf or (output.exists() and os.path.samefile(input_pdf, output)):
        raise ValueError("Input and output PDF must be different files")
    if output.exists() and not args.overwrite and not args.extract_only:
        raise FileExistsError(f"Output already exists; choose a new path or explicitly pass --overwrite: {output}")
    if args.translations and args.backend != "model":
        raise ValueError("--translations is an offline model input; do not combine with --backend google")
    if not args.extract_only and args.backend == "model" and not args.translations:
        raise ValueError("Offline mode requires --translations. First run --extract-only, fill the manifest, then render.")
    workdir = (args.workdir or default_workdir(input_pdf)).expanduser().resolve()
    workdir.mkdir(parents=True, exist_ok=True)
    manifest = build_manifest(input_pdf, args.source, args.target, args.translate_authors, args.table_overlays)
    if args.extract_only:
        manifest_path = (args.manifest or workdir / "translation_manifest.json").expanduser().resolve()
        if manifest_path.exists():
            raise FileExistsError(f"Manifest already exists; choose a new path to preserve completed work: {manifest_path}")
        write_json(manifest_path, manifest)
        print(manifest_path)
        return
    if not any(block["action"] == "translate" for block in manifest["blocks"]):
        raise ValueError("No translatable native-text blocks found; review extraction or prepare an OCR source first")
    if args.backend == "model":
        supplied = json.loads(args.translations.expanduser().read_text(encoding="utf-8"))
        translations = validate_translations(manifest, supplied)
    else:
        cache_path = (args.cache or workdir / "translation_cache.json").expanduser().resolve()
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        cache = json.loads(cache_path.read_text(encoding="utf-8")) if cache_path.exists() else {}
        translations = {
            block["id"]: translate(block["source"], cache, cache_path, args.source, args.target)
            for block in manifest["blocks"] if block["action"] == "translate"
        }
        if any(not value.strip() for value in translations.values()):
            raise ValueError("Google returned an empty translation")
    font = find_font(args.font)
    overlays = load_table_overlays(args.table_overlays)
    # Verify/protect the source archive before producing a final PDF.
    archive_source_pdf(input_pdf, output)
    output.parent.mkdir(parents=True, exist_ok=True)
    stats: list[dict[str, Any]] = []
    font_name = "cjk"
    temp_output: Path | None = None
    try:
        with fitz.open(input_pdf) as source_doc, fitz.open() as out_doc:
            out_doc.insert_pdf(source_doc)
            for page_index, page in enumerate(out_doc):
                page_no = page_index + 1
                page_blocks = [block for block in manifest["blocks"] if block["page"] == page_no and block["action"] == "translate"]
                # Remove selected native text only. No white rectangles over images/line art.
                removed_blocks = page_blocks + [block for block in manifest["blocks"] if block["page"] == page_no and block["reason"] == "table-overlay"]
                for block in removed_blocks:
                    page.add_redact_annot(fitz.Rect(block["bbox"]), fill=False, cross_out=False)
                if removed_blocks:
                    page.apply_redactions(images=0, graphics=0, text=0)
                # Redaction cleans unused fonts, so register the translation font afterwards.
                page.insert_font(fontname=font_name, fontfile=str(font))
                for block in page_blocks:
                    rect = fitz.Rect(block["bbox"])
                    inset = fitz.Rect(rect.x0 + 1.1, rect.y0 + 0.8, rect.x1 - 1.1, rect.y1 - 0.6)
                    size = insert_fitting_text(page, inset, translations[block["id"]], block["source"], page_no, font_name, font)
                    stats.append({"id": block["id"], "page": page_no, "bbox": block["bbox"], "font_size": round(size, 2)})
                for overlay in overlays:
                    if int(overlay["page"]) == page_no:
                        draw_table_overlay(page, overlay, font_name)
                print(f"page {page_no}/{len(source_doc)} rendered", flush=True)
            with tempfile.NamedTemporaryFile(prefix=".translation-", suffix=".pdf", dir=output.parent, delete=False) as temp:
                temp_output = Path(temp.name)
            out_doc.save(temp_output, garbage=4, deflate=True)
        os.replace(temp_output, output)
    except Exception as exc:
        write_json(workdir / "layout_stats.json", {"status": "failed", "error": str(exc), "rendered_blocks": stats})
        raise
    finally:
        if temp_output and temp_output.exists():
            temp_output.unlink()
    write_json(workdir / "layout_stats.json", {
        "status": "rendered-review-required", "source_sha256": manifest["source_sha256"],
        "backend": args.backend, "translated_blocks": len(stats),
        "preserved_blocks": [b["id"] for b in manifest["blocks"] if b["action"] == "preserve"],
        "pages_without_native_text": [p["page"] for p in manifest["pages"] if not p["text_blocks"]],
        "small_font_blocks_review_required": [b["id"] for b in stats if b["font_size"] < 6],
        "limitations": manifest["limitations"], "blocks": stats,
    })
    render_previews(output, workdir, parse_preview_pages(args.preview_pages, manifest["page_count"]))
    print(output)
    print(workdir)


if __name__ == "__main__":
    main()
