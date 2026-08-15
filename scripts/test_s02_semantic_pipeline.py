from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from s02_semantic_pipeline import build, read_json, validate_artifacts, write_json


class S02SemanticPipelineTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        self.timeline_path = self.root / "text-unit-timeline.json"
        self.decisions_path = self.root / "decisions.json"
        self.output_dir = self.root / "S02"
        timeline = {
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
                for index, text in enumerate("甲乙丙丁戊", start=1)
            ],
        }
        decisions = {
            "punctuation_decisions": [
                {
                    "after_unit_id": "unit-000003",
                    "punctuation": "，",
                    "paragraph_break_after": False,
                },
                {
                    "after_unit_id": "unit-000005",
                    "punctuation": "。",
                    "paragraph_break_after": True,
                },
            ],
            "block_decisions": [
                {
                    "end_unit_id": "unit-000002",
                    "title": "前半认知任务",
                    "semantic_role": "铺垫",
                    "cognitive_goal": "观众理解前半部分",
                    "boundary_reason": "主要认知任务发生变化",
                },
                {
                    "end_unit_id": "unit-000005",
                    "title": "后半认知任务",
                    "semantic_role": "结论",
                    "cognitive_goal": "观众理解后半部分",
                    "boundary_reason": "END_OF_TRANSCRIPT",
                },
            ],
        }
        write_json(self.timeline_path, timeline)
        write_json(self.decisions_path, decisions)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_block_can_end_inside_sentence(self) -> None:
        build(self.timeline_path, self.decisions_path, self.output_dir)
        transcript = read_json(self.output_dir / "semantic-transcript.json")
        blocks = read_json(self.output_dir / "semantic-blocks.json")
        self.assertEqual(len(transcript["sentences"]), 1)
        self.assertEqual(len(blocks["blocks"]), 2)
        self.assertEqual(blocks["blocks"][0]["verbatim_text"], "甲乙")
        self.assertEqual(blocks["blocks"][1]["semantic_text"], "丙，丁戊。")
        self.assertEqual(
            validate_artifacts(
                self.timeline_path,
                self.output_dir / "semantic-transcript.json",
                self.output_dir / "semantic-blocks.json",
            ),
            [],
        )

    def test_validator_detects_changed_block_text(self) -> None:
        build(self.timeline_path, self.decisions_path, self.output_dir)
        blocks_path = self.output_dir / "semantic-blocks.json"
        blocks = json.loads(blocks_path.read_text(encoding="utf-8"))
        blocks["blocks"][0]["verbatim_text"] = "被修改"
        write_json(blocks_path, blocks)
        issues = validate_artifacts(
            self.timeline_path,
            self.output_dir / "semantic-transcript.json",
            blocks_path,
        )
        self.assertTrue(any("忠实文字与来源不一致" in issue for issue in issues))


if __name__ == "__main__":
    unittest.main()
