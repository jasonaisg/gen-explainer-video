#!/usr/bin/env python3
"""Regression tests for S01 text-unit grouping."""

from __future__ import annotations

import unittest

from s01_build_outputs import atoms_to_units, engine_atoms, reference_plain_text, split_surface_text


def token(text: str, start_ms: int, end_ms: int, confidence: float = 0.99) -> dict[str, object]:
    return {"text": text, "offsets": {"from": start_ms, "to": end_ms}, "p": confidence}


def segment(tokens: list[dict[str, object]], start_ms: int = 0, end_ms: int = 3000) -> dict[str, object]:
    return {"offsets": {"from": start_ms, "to": end_ms}, "tokens": tokens}


class TextUnitTests(unittest.TestCase):
    def build(self, tokens: list[dict[str, object]]) -> tuple[list[dict[str, object]], int]:
        starts = [int(item["offsets"]["from"]) for item in tokens]  # type: ignore[index]
        ends = [int(item["offsets"]["to"]) for item in tokens]  # type: ignore[index]
        return atoms_to_units(engine_atoms([
            segment(tokens, start_ms=max(0, min(starts) - 100), end_ms=max(ends) + 100)
        ]))

    def test_percentage_spans_all_source_tokens(self) -> None:
        units, discarded = self.build([
            token("收", 1900, 2060),
            token("20", 2060, 2510),
            token("%", 2510, 2590),
            token("个", 2590, 2750),
        ])
        self.assertEqual([unit["text"] for unit in units], ["收", "20%", "个"])
        self.assertEqual(units[1]["kind"], "percentage")
        self.assertEqual((units[1]["start"], units[1]["end"]), (2.06, 2.59))
        self.assertEqual(len(units[1]["source_token_ids"]), 2)
        self.assertEqual(discarded, 0)

    def test_consecutive_english_is_one_unit(self) -> None:
        units, _ = self.build([
            token("随", 100, 200),
            token("着", 200, 300),
            token("CR", 300, 320),
            token("S", 320, 420),
            token("金", 420, 520),
        ])
        self.assertEqual([unit["text"] for unit in units], ["随", "着", "CRS", "金"])
        self.assertEqual(units[2]["kind"], "english")
        self.assertEqual((units[2]["start"], units[2]["end"]), (0.3, 0.42))

    def test_whitespace_separates_english_words(self) -> None:
        units, _ = self.build([
            token(" Common", 100, 300),
            token(" Reporting", 300, 500),
            token(" Standard", 500, 700),
        ])
        self.assertEqual([unit["text"] for unit in units], ["Common", "Reporting", "Standard"])

    def test_structured_ascii_groups(self) -> None:
        pieces = split_surface_text("GPT-5 T+1 B2B C919 v2.0 3.5%")
        self.assertEqual(
            [piece["text"] for piece in pieces],
            ["GPT-5", "T+1", "B2B", "C919", "v2.0", "3.5%"],
        )
        self.assertEqual(pieces[-1]["kind"], "percentage")

    def test_inferred_punctuation_is_removed_but_content_symbols_remain(self) -> None:
        self.assertEqual(reference_plain_text("你好，20%！CRS。"), "你好20%CRS")

    def test_zero_length_visible_token_is_interpolated_in_neighbor_gap(self) -> None:
        units, _ = self.build([
            token("键", 9920, 10230),
            token("要", 10330, 10330),
            token("看", 10400, 10430),
        ])
        self.assertEqual([unit["text"] for unit in units], ["键", "要", "看"])
        self.assertEqual(units[1]["timing_method"], "ZERO_LENGTH_TOKEN_INTERPOLATED")
        self.assertGreater(units[1]["end"], units[1]["start"])
        self.assertGreaterEqual(units[1]["start"], units[0]["end"])
        self.assertLessEqual(units[1]["end"], units[2]["start"])


if __name__ == "__main__":
    unittest.main()
