from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from s02_block_review import (
    build_approved_document,
    materialize_review_html,
    review_payload,
    save_approved,
    validate_approved,
)
from s02_semantic_pipeline import build, read_json, write_json


class S02BlockReviewTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.timeline = self.root / "S01" / "text-unit-timeline.json"
        self.decisions = self.root / "decisions.json"
        self.s02 = self.root / "S02"
        self.transcript = self.s02 / "semantic-transcript.json"
        self.draft = self.s02 / "semantic-blocks.json"
        self.approved = self.s02 / "semantic-blocks-approved.json"
        self.timeline.parent.mkdir(parents=True)
        write_json(
            self.timeline,
            {
                "schema_version": "2.0",
                "stage": "S01",
                "timebase": "INPUT_VIDEO_ABSOLUTE_SECONDS",
                "units": [
                    {
                        "unit_id": f"unit-{index:06d}",
                        "text": text,
                        "start": float(index - 1),
                        "end": float(index),
                    }
                    for index, text in enumerate("甲乙丙丁戊己", start=1)
                ],
            },
        )
        write_json(
            self.decisions,
            {
                "punctuation_decisions": [
                    {"after_unit_id": "unit-000003", "punctuation": "，", "paragraph_break_after": False},
                    {"after_unit_id": "unit-000006", "punctuation": "。", "paragraph_break_after": True},
                ],
                "block_decisions": [
                    {
                        "end_unit_id": "unit-000003",
                        "title": "提出问题",
                        "semantic_role": "问题",
                        "cognitive_goal": "观众理解问题",
                        "boundary_reason": "从问题转入解释",
                    },
                    {
                        "end_unit_id": "unit-000006",
                        "title": "给出解释",
                        "semantic_role": "解释",
                        "cognitive_goal": "观众理解答案",
                        "boundary_reason": "END_OF_TRANSCRIPT",
                    },
                ],
            },
        )
        build(self.timeline, self.decisions, self.s02)

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def submitted_blocks(self) -> list[dict[str, object]]:
        payload = review_payload(self.timeline, self.transcript, self.draft, self.approved)
        return payload["blocks"]

    def test_build_recomputes_derived_fields_after_boundary_change(self) -> None:
        blocks = self.submitted_blocks()
        blocks[0]["end_unit_id"] = "unit-000002"
        document = build_approved_document(
            self.timeline, self.transcript, self.draft, blocks, "边界后移"
        )
        self.assertEqual(document["blocks"][0]["verbatim_text"], "甲乙")
        self.assertEqual(document["blocks"][1]["semantic_text"], "丙，丁戊己。")
        self.assertEqual(document["approval"]["change_count"], 1)

    def test_save_writes_valid_approved_artifact(self) -> None:
        result = save_approved(
            self.timeline,
            self.transcript,
            self.draft,
            self.approved,
            {"blocks": self.submitted_blocks(), "reviewer_note": "通过"},
        )
        self.assertEqual(result["status"], "saved")
        self.assertEqual(validate_approved(self.timeline, self.transcript, self.draft, self.approved), [])
        self.assertEqual(read_json(self.approved)["approval"]["status"], "APPROVED")

    def test_per_block_confirmation_is_not_required(self) -> None:
        blocks = self.submitted_blocks()
        blocks[0]["confirmed"] = False
        document = build_approved_document(self.timeline, self.transcript, self.draft, blocks, "")
        self.assertEqual(document["approval"]["status"], "APPROVED")

    def test_review_always_starts_from_semantic_blocks_draft(self) -> None:
        changed = self.submitted_blocks()
        changed[0]["title"] = "批准文件中的旧标题"
        save_approved(
            self.timeline,
            self.transcript,
            self.draft,
            self.approved,
            {"blocks": changed, "reviewer_note": ""},
        )
        payload = review_payload(self.timeline, self.transcript, self.draft, self.approved)
        self.assertEqual(payload["source_kind"], "draft")
        self.assertEqual(payload["blocks"][0]["title"], "提出问题")

    def test_approved_output_name_is_fixed_and_cannot_overwrite_draft(self) -> None:
        with self.assertRaisesRegex(ValueError, "文件名必须固定"):
            review_payload(
                self.timeline, self.transcript, self.draft, self.s02 / "other.json"
            )
        with self.assertRaisesRegex(ValueError, "文件名必须固定|不得覆盖"):
            review_payload(self.timeline, self.transcript, self.draft, self.draft)

    def test_changed_draft_hash_invalidates_approval(self) -> None:
        save_approved(
            self.timeline,
            self.transcript,
            self.draft,
            self.approved,
            {"blocks": self.submitted_blocks(), "reviewer_note": ""},
        )
        draft = read_json(self.draft)
        draft["blocks"][0]["title"] = "新的机器草稿"
        write_json(self.draft, draft)
        issues = validate_approved(self.timeline, self.transcript, self.draft, self.approved)
        self.assertTrue(any("草稿来源哈希不匹配" in issue for issue in issues))

    def test_html_is_generic_and_has_native_project_save(self) -> None:
        html_path = Path(__file__).resolve().parent.parent / "assets" / "tools" / "s02-block-review.html"
        html = html_path.read_text(encoding="utf-8")
        self.assertNotIn("__S02_EMBEDDED_DATA__", html)
        self.assertIn("window.showDirectoryPicker", html)
        self.assertIn('getDirectoryHandle("S01", {create:false})', html)
        self.assertIn('getDirectoryHandle("S02", {create:false})', html)
        self.assertIn('readJsonFile(s01Directory, "text-unit-timeline.json")', html)
        self.assertIn('readJsonFile(s02Directory, "semantic-transcript.json")', html)
        self.assertIn('readJsonFile(s02Directory, "semantic-blocks.json")', html)
        self.assertIn('getFileHandle("semantic-blocks-approved.json", {create:true})', html)
        self.assertIn('semantic-blocks-approved.json 已存在。确认用当前审批结果覆盖它吗', html)
        self.assertNotIn("window.showSaveFilePicker", html)
        self.assertIn("scheduleBoundaryPreview()", html)
        self.assertIn("requestAnimationFrame(updateBoundaryPreview)", html)
        self.assertIn('id="reload-draft"', html)
        self.assertIn('id="import-json"', html)
        self.assertIn('id="import-file"', html)
        self.assertIn('$("#save").disabled = state.saving', html)
        self.assertNotIn('data-action="confirm"', html)
        self.assertNotIn('confirm("放弃当前修改', html)
        self.assertNotIn('state.modal.value = Number(event.target.value); renderModal();', html)
        self.assertNotIn('fetch("/api/', html)

    def test_generic_review_html_is_installed_inside_customer_s02(self) -> None:
        payload = review_payload(self.timeline, self.transcript, self.draft, self.approved)
        target = materialize_review_html(self.s02)
        self.assertEqual(target, self.s02 / "semantic-blocks-review.html")
        html = target.read_text(encoding="utf-8")
        self.assertNotIn("__S02_EMBEDDED_DATA__", html)
        self.assertEqual(
            target.read_bytes(),
            (Path(__file__).resolve().parent.parent / "assets" / "tools" / "s02-block-review.html").read_bytes(),
        )
        self.assertEqual(payload["review_html"], str(target))


if __name__ == "__main__":
    unittest.main()
