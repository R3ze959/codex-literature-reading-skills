"""Offline integration checks using synthetic PDFs; no papers or network access required."""
from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import fitz

SCRIPT = Path(__file__).resolve().parents[1] / "skills/translate-full-pdf/scripts/translate_full_pdf.py"
spec = importlib.util.spec_from_file_location("translate_full_pdf", SCRIPT)
translator = importlib.util.module_from_spec(spec)
assert spec.loader
spec.loader.exec_module(translator)


class TranslationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.source = self.root / "source.pdf"
        # A bundled MuPDF font keeps tests independent of OS font installation.
        self.font = self.root / "test-font.ttf"
        self.font.write_bytes(fitz.Font("cjk").buffer)
        with fitz.open() as doc:
            page = doc.new_page(width=550, height=700)
            page.insert_text((40, 100), "First research paragraph with technical evidence.", fontsize=12)
            page.insert_text((40, 300), "Second paragraph discusses measurement limits.", fontsize=12)
            pix = fitz.Pixmap(fitz.csRGB, fitz.IRect(0, 0, 20, 20), False)
            pix.clear_with(125)
            page.insert_image(fitz.Rect(320, 380, 500, 560), pixmap=pix)
            page.insert_text((330, 420), "Native figure label", fontsize=10)
            page.draw_line((320, 580), (490, 580), color=(1, 0, 0), width=2)
            doc.save(self.source)
        self.manifest = translator.build_manifest(self.source, "en", "zh-CN", False)
        self.filled = copy.deepcopy(self.manifest)
        for block in self.filled["blocks"]:
            if block["action"] == "translate":
                block["translation"] = "Translated paragraph."
        self.filled["blocks"][0]["translation"] = "译文段落：测量证据。"
        self.manifest_path = self.root / "filled.json"
        self.manifest_path.write_text(json.dumps(self.filled), encoding="utf-8")
        self.output = self.root / "new-parent" / "output.pdf"
        self.work = self.root / "work"
        # Fail immediately if any test accidentally tries the real remote service.
        self.network = patch.object(translator.urllib.request, "urlopen", side_effect=AssertionError("Network forbidden"))
        self.network_mock = self.network.start()
        self.addCleanup(self.network.stop)

    def run_render(self, **kwargs):
        args = [str(self.source), "--translations", str(self.manifest_path),
                "--output", str(self.output), "--workdir", str(self.work), "--preview-pages", "", "--font", str(self.font)]
        for key, value in kwargs.items():
            if value is True:
                args.append("--" + key.replace("_", "-"))
                continue
            args.extend(["--" + key.replace("_", "-"), str(value)])
        translator.main(args)

    def test_extract_is_offline_stable_and_preserves_image_blocks(self):
        destination = self.root / "extract" / "blocks.json"
        translator.main([str(self.source), "--extract-only", "--manifest", str(destination), "--workdir", str(self.work)])
        extracted = json.loads(destination.read_text())
        self.assertEqual(extracted, self.manifest)
        self.assertEqual(extracted["source_sha256"], hashlib.sha256(self.source.read_bytes()).hexdigest())
        self.assertEqual(len(extracted["blocks"]), 3)
        figure_label = next(b for b in extracted["blocks"] if "figure label" in b["source"])
        self.assertEqual(figure_label["action"], "preserve")
        self.assertEqual(figure_label["reason"], "image-overlap-review")
        self.assertEqual(extracted["pages"][0]["image_count"], 1)
        self.network_mock.assert_not_called()
        with self.assertRaises(FileExistsError):
            translator.main([str(self.source), "--extract-only", "--manifest", str(destination), "--workdir", str(self.work)])

    def test_offline_render_keeps_images_vectors_and_marks_review_required(self):
        self.run_render()
        with fitz.open(self.source) as source, fitz.open(self.output) as result:
            self.assertEqual(len(result), len(source))
            self.assertEqual(len(result[0].get_images()), len(source[0].get_images()))
            self.assertEqual(len(result[0].get_drawings()), len(source[0].get_drawings()))
            region = fitz.Rect(320, 380, 500, 560)
            self.assertEqual(source[0].get_pixmap(clip=region).samples, result[0].get_pixmap(clip=region).samples)
            text = result[0].get_text()
            self.assertIn("Translated paragraph.", text)
            self.assertIn("译文段落：测量证据。", text)
            self.assertNotIn("First research paragraph", text)
            self.assertIn("Native figure label", text)
        report = json.loads((self.work / "layout_stats.json").read_text())
        self.assertEqual(report["status"], "rendered-review-required")
        self.assertEqual(report["translated_blocks"], 2)
        self.network_mock.assert_not_called()

    def test_manifest_rejects_missing_duplicate_unknown_empty_and_changed_source(self):
        mutations = {
            "missing": lambda doc: doc["blocks"].pop(),
            "duplicate": lambda doc: doc["blocks"].append(copy.deepcopy(doc["blocks"][0])),
            "unknown": lambda doc: doc["blocks"][0].update(id="unknown-id"),
            "empty": lambda doc: doc["blocks"][0].update(translation="  "),
            "hash": lambda doc: doc.update(source_sha256="wrong"),
            "source language": lambda doc: doc.update(source_language="fr"),
            "target language": lambda doc: doc.update(target_language="de"),
            "source text": lambda doc: doc["blocks"][0].update(source="altered source"),
            "bbox": lambda doc: doc["blocks"][0].update(bbox=[0, 0, 1, 1]),
            "action": lambda doc: doc["blocks"][0].update(action="preserve"),
        }
        for label, mutate in mutations.items():
            with self.subTest(label=label):
                bad = copy.deepcopy(self.filled)
                mutate(bad)
                self.manifest_path.write_text(json.dumps(bad))
                with self.assertRaises(ValueError):
                    self.run_render()
                self.assertFalse(self.output.exists())
        self.network_mock.assert_not_called()

    def test_default_backend_requires_model_input_without_network(self):
        with self.assertRaisesRegex(ValueError, "Offline mode requires"):
            translator.main([str(self.source), "--output", str(self.output)])
        self.assertFalse(self.output.exists())
        self.network_mock.assert_not_called()

    def test_source_and_archive_are_protected(self):
        source_bytes = self.source.read_bytes()
        with self.assertRaisesRegex(ValueError, "different files"):
            translator.main([str(self.source), "--output", str(self.source), "--translations", str(self.manifest_path)])
        self.assertEqual(self.source.read_bytes(), source_bytes)
        archive_output = self.root / "paper" / "生成结果PDF" / "result.pdf"
        translator.archive_source_pdf(self.source, archive_output)
        archive = archive_output.parent.parent / "原始文献PDF" / self.source.name
        self.assertEqual(archive.read_bytes(), source_bytes)
        archive.write_bytes(b"A different pre-existing source")
        with self.assertRaises(FileExistsError):
            translator.archive_source_pdf(self.source, archive_output)
        self.assertEqual(archive.read_bytes(), b"A different pre-existing source")

    def test_same_name_different_documents_use_different_default_paths(self):
        other = self.root / "other" / self.source.name
        other.parent.mkdir()
        with fitz.open(self.source) as doc:
            doc[0].insert_text((50, 600), "Another document")
            doc.save(other)
        self.assertNotEqual(translator.default_workdir(self.source), translator.default_workdir(other))
        self.assertNotEqual(translator.default_output_path(self.source), translator.default_output_path(other))

    def test_overflow_fails_without_replacing_output(self):
        self.filled["blocks"][0]["translation"] = "This cannot fit. " * 2000
        self.manifest_path.write_text(json.dumps(self.filled))
        self.output.parent.mkdir()
        self.output.write_bytes(b"Previous reviewed output")
        with self.assertRaises(translator.LayoutOverflow):
            self.run_render(overwrite=True)
        self.assertEqual(self.output.read_bytes(), b"Previous reviewed output")
        report = json.loads((self.work / "layout_stats.json").read_text())
        self.assertEqual(report["status"], "failed")
        self.network_mock.assert_not_called()

    def test_table_cell_overflow_is_not_silently_accepted(self):
        with fitz.open() as doc:
            page = doc.new_page()
            page.insert_font(fontname="test", fontfile=str(self.font))
            overlay = {"area": [20, 30, 60, 65], "columns": ["X"], "rows": [["Long cell " * 1000]]}
            with self.assertRaises(translator.LayoutOverflow):
                translator.draw_table_overlay(page, overlay, "test")

    def test_overlay_document_must_match_extract(self):
        overlays = self.root / "tables.json"
        overlays.write_text("[]")
        expected = translator.build_manifest(self.source, "en", "zh-CN", False, overlays)
        with self.assertRaisesRegex(ValueError, "table_overlays_sha256"):
            translator.validate_translations(expected, self.filled)

    def test_scanned_only_source_does_not_produce_a_complete_translation(self):
        scanned = self.root / "scan.pdf"
        with fitz.open() as doc:
            page = doc.new_page()
            image = fitz.Pixmap(fitz.csRGB, fitz.IRect(0, 0, 20, 20), False)
            image.clear_with(120)
            page.insert_image(page.rect, pixmap=image)
            doc.save(scanned)
        manifest = translator.build_manifest(scanned, "en", "zh-CN", False)
        self.assertEqual(manifest["blocks"], [])
        self.assertEqual(manifest["pages"][0]["text_blocks"], 0)
        self.manifest_path.write_text(json.dumps(manifest))
        with self.assertRaisesRegex(ValueError, "No translatable native-text"):
            translator.main([str(scanned), "--translations", str(self.manifest_path), "--output", str(self.output), "--workdir", str(self.work)])
        self.assertFalse(self.output.exists())

    def test_existing_output_requires_explicit_overwrite(self):
        self.output.parent.mkdir()
        self.output.write_bytes(b"An existing reviewed result")
        with self.assertRaises(FileExistsError):
            self.run_render()
        self.assertEqual(self.output.read_bytes(), b"An existing reviewed result")
        self.run_render(overwrite=True)
        with fitz.open(self.output) as doc:
            self.assertIn("Translated paragraph.", doc[0].get_text())

    def test_prose_containing_names_or_doi_is_still_translated(self):
        with fitz.open() as doc:
            page = doc.new_page()
            rect = fitz.Rect(30, 200, 500, 240)
            for text in (
                "See https://doi.org/10.1000/example for the measured results.",
                "https://doi.org/10.1000/example provides our baseline measurements.",
                "John Smith and Jane Doe found conductivity increases with temperature.",
            ):
                with self.subTest(text=text):
                    self.assertFalse(translator.is_boilerplate(text, rect, page))
                    self.assertFalse(translator.should_leave_untranslated(text, False))
            self.assertTrue(translator.is_boilerplate("https://doi.org/10.1000/example", rect, page))
            self.assertTrue(translator.should_leave_untranslated("John Smith and Jane Doe", False))
            self.assertFalse(translator.should_leave_untranslated("固态电池性能分析。", False))

    def test_overlay_cannot_partly_cover_a_text_block(self):
        overlays = self.root / "tables.json"
        block = self.manifest["blocks"][0]
        x0, y0, x1, y1 = block["bbox"]
        overlays.write_text(json.dumps([{
            "page": 1, "area": [x0, y0, (x0 + x1) / 2, y1],
            "columns": ["A"], "rows": [["25"]],
        }]))
        with self.assertRaisesRegex(ValueError, "partly covers"):
            translator.build_manifest(self.source, "en", "zh-CN", False, overlays)

    def test_overlay_rejects_dropped_columns(self):
        overlays = self.root / "tables.json"
        overlays.write_text(json.dumps([{
            "page": 1, "area": [10, 10, 200, 200],
            "columns": ["Sample", "Temperature"], "rows": [["A"]],
        }]))
        with self.assertRaisesRegex(ValueError, "number of columns"):
            translator.load_table_overlays(overlays)

    def test_semantic_terms_are_not_globally_rewritten(self):
        original = "阴极反应和阳极反应。参考表格。"
        self.assertEqual(translator.postprocess_translation(original), original)

    def test_google_is_only_reached_when_explicitly_selected(self):
        with patch.object(translator, "translate_piece", return_value="Explicit Google test.") as google:
            translator.main([str(self.source), "--backend", "google", "--output", str(self.output),
                             "--workdir", str(self.work), "--preview-pages", "", "--font", str(self.font)])
        self.assertEqual(google.call_count, 2)
        self.network_mock.assert_not_called()


if __name__ == "__main__":
    unittest.main()
