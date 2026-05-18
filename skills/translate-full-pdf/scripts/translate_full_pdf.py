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


def parse_args() -> argparse.Namespace:
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
    return parser.parse_args()


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


def default_output_path(input_pdf: Path) -> Path:
    output_dir = DEFAULT_OUTPUT_DIR / input_pdf.stem / "生成结果PDF"
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir / f"{input_pdf.stem}_中文翻译版.pdf"


def default_workdir(input_pdf: Path) -> Path:
    safe_stem = re.sub(r"[^A-Za-z0-9_.-]+", "_", input_pdf.stem).strip("_") or "pdf"
    return Path(tempfile.gettempdir()) / "translate_full_pdf_work" / safe_stem


def archive_source_pdf(input_pdf: Path, output_pdf: Path) -> None:
    if output_pdf.parent.name != "生成结果PDF":
        return
    paper_dir = output_pdf.parent.parent
    source_dir = paper_dir / "原始文献PDF"
    source_dir.mkdir(parents=True, exist_ok=True)
    target = source_dir / input_pdf.name
    if input_pdf.resolve() != target.resolve():
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
    replacements = {
        "固体电解质": "固态电解质",
        "电解质间相": "电解质界面相",
        "阴极": "正极",
        "阳极": "负极",
        "无花果。": "图",
        "图。": "图",
        "表格": "表",
        "参考": "参考文献",
    }
    for source, target in replacements.items():
        text = text.replace(source, target)
    text = re.sub(r"\s+", " ", text)
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
    markers = [
        "ACS Nano www.acsnano.org Article",
        "https://doi.org/",
        "Downloaded via",
        "sharingguidelines",
        "© ",
        "Copyright",
    ]
    if any(marker in clean for marker in markers):
        return True
    if rect.y0 > page.rect.height - 42:
        return True
    if rect.y1 < 53 and ("Article" in clean or "www." in clean or "Journal" in clean):
        return True
    return False


def cover_without_text(text: str) -> bool:
    clean = normalized_text(text)
    return "Downloaded via" in clean or "sharingguidelines" in clean


def mostly_nonlanguage(text: str) -> bool:
    clean = normalized_text(text)
    if len(clean) < 2:
        return True
    letters = len(re.findall(r"[A-Za-z]", clean))
    symbols = len(re.findall(r"[^A-Za-z\u4e00-\u9fff]", clean))
    return letters < 3 and symbols > letters


def should_leave_untranslated(text: str, translate_authors: bool) -> bool:
    clean = normalized_text(text)
    if mostly_nonlanguage(clean):
        return True
    if not translate_authors and re.search(r"\b[A-Z][a-z]+ [A-Z][a-z]+", clean) and " and " in clean and len(clean) < 350:
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
        if spare >= -0.1:
            page.insert_textbox(
                rect,
                text,
                fontname=font_name,
                fontsize=size,
                color=(0.05, 0.05, 0.05),
                align=align,
            )
            return size
    page.insert_textbox(rect, text, fontname=font_name, fontsize=3.4, color=(0.05, 0.05, 0.05), align=align)
    return 3.4


def load_table_overlays(path: Path | None) -> list[dict[str, Any]]:
    if not path:
        return []
    return json.loads(path.read_text(encoding="utf-8"))


def rects_overlap(a: fitz.Rect, b: fitz.Rect) -> bool:
    return not (a.x1 <= b.x0 or a.x0 >= b.x1 or a.y1 <= b.y0 or a.y0 >= b.y1)


def draw_table_overlay(page: fitz.Page, overlay: dict[str, Any], font_name: str) -> None:
    area = fitz.Rect(*overlay["area"])
    page.draw_rect(area, color=(1, 1, 1), fill=(1, 1, 1), overlay=True)
    page.draw_line((area.x0, area.y0 + 1), (area.x1, area.y0 + 1), color=(0.86, 0.36, 0.05), width=0.7)
    title_h = 20.0 if overlay.get("title") else 4.0
    if overlay.get("title"):
        page.insert_textbox(
            fitz.Rect(area.x0 + 1.5, area.y0 + 5, area.x1 - 1.5, area.y0 + title_h),
            overlay["title"],
            fontname=font_name,
            fontsize=5.8,
            color=(0.05, 0.05, 0.05),
        )
    columns = overlay["columns"]
    rows = overlay["rows"]
    table_top = area.y0 + title_h + 8
    table_bottom = area.y1 - 8
    row_h = max(9.0, (table_bottom - table_top) / (len(rows) + 1))
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
            page.insert_textbox(
                fitz.Rect(xs[i] + 1.5, top + 2, xs[i + 1] - 1.5, top + row_h - 1),
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


def main() -> None:
    args = parse_args()
    input_pdf = args.input_pdf.expanduser().resolve()
    if not input_pdf.exists():
        raise FileNotFoundError(input_pdf)
    output = (args.output or default_output_path(input_pdf)).expanduser().resolve()
    workdir = (args.workdir or default_workdir(input_pdf)).expanduser().resolve()
    workdir.mkdir(parents=True, exist_ok=True)
    font = find_font(args.font)
    cache_path = (args.cache or workdir / "translation_cache.json").expanduser().resolve()
    cache: dict[str, str] = json.loads(cache_path.read_text(encoding="utf-8")) if cache_path.exists() else {}
    overlays = load_table_overlays(args.table_overlays)

    source_doc = fitz.open(input_pdf)
    out_doc = fitz.open()
    stats: list[dict[str, Any]] = []
    font_name = "cjk"

    for page_index, source_page in enumerate(source_doc):
        page_no = page_index + 1
        page = out_doc.new_page(width=source_page.rect.width, height=source_page.rect.height)
        page.show_pdf_page(page.rect, source_doc, page_index)
        page.insert_font(fontname=font_name, fontfile=str(font))
        page_overlays = [item for item in overlays if int(item["page"]) == page_no]
        overlay_rects = [fitz.Rect(*item["area"]) for item in page_overlays]

        for block in source_page.get_text("blocks"):
            x0, y0, x1, y1, text = block[:5]
            rect = fitz.Rect(x0, y0, x1, y1)
            clean = normalized_text(text)
            if not clean:
                continue
            if any(rects_overlap(rect, overlay_rect) for overlay_rect in overlay_rects):
                continue
            if cover_without_text(clean):
                page.draw_rect(rect + (-1, -1, 1, 1), color=(1, 1, 1), fill=(1, 1, 1), overlay=True)
                continue
            if is_boilerplate(clean, rect, source_page) or should_leave_untranslated(clean, args.translate_authors):
                continue

            translated = translate(clean, cache, cache_path, args.source, args.target)
            page.draw_rect(rect + (-1.4, -1.1, 1.4, 1.1), color=(1, 1, 1), fill=(1, 1, 1), overlay=True)
            inset = fitz.Rect(rect.x0 + 1.1, rect.y0 + 0.8, rect.x1 - 1.1, rect.y1 - 0.6)
            size = insert_fitting_text(page, inset, translated, clean, page_no, font_name, font)
            stats.append(
                {
                    "page": page_no,
                    "bbox": [round(v, 2) for v in (x0, y0, x1, y1)],
                    "font_size": round(size, 2),
                    "source": clean[:160],
                    "translation": translated[:160],
                }
            )

        for overlay in page_overlays:
            draw_table_overlay(page, overlay, font_name)
        print(f"page {page_no}/{len(source_doc)} done", flush=True)

    out_doc.save(output, garbage=4, deflate=True)
    out_doc.close()
    source_doc.close()
    (workdir / "layout_stats.json").write_text(json.dumps(stats, ensure_ascii=False, indent=2), encoding="utf-8")
    rendered_doc = fitz.open(output)
    try:
        output_page_count = len(rendered_doc)
    finally:
        rendered_doc.close()
    render_previews(output, workdir, parse_preview_pages(args.preview_pages, output_page_count))
    archive_source_pdf(input_pdf, output)
    print(output)
    print(workdir)


if __name__ == "__main__":
    main()
