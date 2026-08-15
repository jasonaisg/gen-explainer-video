#!/usr/bin/env python3
"""Build auditable S01 text-unit artifacts from whisper.cpp JSON."""

from __future__ import annotations

import argparse
import difflib
import json
import os
import re
import unicodedata
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SPECIAL_TOKEN = re.compile(r"^\[_[A-Z0-9_]+\]$")
PERCENT_SUFFIXES = {"%", "‰", "‱"}
CURRENCY_PREFIXES = {"$", "¥", "￥", "€", "£"}
DEGREE_SYMBOLS = {"°", "℃", "℉"}
INLINE_CONNECTORS = {".", ",", ":", "/", "-", "−", "–", "—", "~", "～", "_", "&", "'", "’", "+", "=", "<", ">"}
SCHEMA_VERSION = "2.0"
MAX_CROSS_SEGMENT_JOIN_GAP = 0.12


def read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"JSON 顶层必须是对象：{path}")
    return value


def is_han(char: str) -> bool:
    codepoint = ord(char)
    return (
        0x3400 <= codepoint <= 0x4DBF
        or 0x4E00 <= codepoint <= 0x9FFF
        or 0xF900 <= codepoint <= 0xFAFF
        or 0x20000 <= codepoint <= 0x3134F
    )


def is_word_char(char: str) -> bool:
    category = unicodedata.category(char)
    return category.startswith("L") or category.startswith("N")


def is_ascii_word_char(char: str) -> bool:
    return char.isascii() and char.isalnum()


def token_visible_text(value: object) -> tuple[str, bool, bool]:
    raw = str(value or "")
    stripped = raw.strip()
    if SPECIAL_TOKEN.fullmatch(stripped):
        return "", False, False
    visible = "".join(char for char in raw if not char.isspace())
    return visible, bool(raw and raw[0].isspace()), bool(raw and raw[-1].isspace())


def _neighbor(atoms: list[dict[str, Any]], index: int, direction: int) -> str | None:
    other = index + direction
    if other < 0 or other >= len(atoms):
        return None
    if direction < 0 and atoms[index].get("hard_boundary_before"):
        return None
    if direction > 0 and atoms[other].get("hard_boundary_before"):
        return None
    return str(atoms[other]["text"])


def _content_symbol(atoms: list[dict[str, Any]], index: int) -> bool:
    char = str(atoms[index]["text"])
    previous = _neighbor(atoms, index, -1)
    following = _neighbor(atoms, index, 1)
    if char in PERCENT_SUFFIXES:
        return previous is not None and (previous.isdigit() or previous in {"%", "‰", "‱"})
    if char in CURRENCY_PREFIXES:
        return following is not None and (following.isdigit() or is_ascii_word_char(following))
    if char in DEGREE_SYMBOLS:
        return (previous is not None and previous.isdigit()) or (
            following is not None and is_ascii_word_char(following)
        )
    if char in INLINE_CONNECTORS:
        if previous is None or following is None:
            return False
        if not is_word_char(previous) or not is_word_char(following):
            return False
        return is_ascii_word_char(previous) or is_ascii_word_char(following)
    return False


def classify_unit(text: str) -> str:
    if len(text) == 1 and is_han(text):
        return "han"
    if text[-1:] in PERCENT_SUFFIXES and any(char.isdigit() for char in text):
        return "percentage"
    letters = any(unicodedata.category(char).startswith("L") for char in text)
    digits = any(unicodedata.category(char).startswith("N") for char in text)
    symbols = any(not is_word_char(char) for char in text)
    if letters and not digits and not symbols:
        return "english" if all(char.isascii() for char in text) else "word"
    if digits and not letters and all(char.isdigit() or char in {".", ","} for char in text):
        return "number"
    if letters or digits:
        return "alphanumeric"
    return "content_symbol"


def _unit_from_atoms(group: list[dict[str, Any]]) -> dict[str, Any]:
    source_token_ids = list(dict.fromkeys(str(atom["token_id"]) for atom in group))
    token_counts = Counter(str(atom["token_id"]) for atom in group)
    token_visible_counts = {
        str(atom["token_id"]): int(atom["token_visible_count"])
        for atom in group
    }
    exact_envelope = all(
        token_counts[token_id] == token_visible_counts[token_id]
        for token_id in source_token_ids
    )
    if any(atom.get("token_timing_method") == "ZERO_LENGTH_TOKEN_INTERPOLATED" for atom in group):
        timing_method = "ZERO_LENGTH_TOKEN_INTERPOLATED"
    elif any(atom.get("token_timing_method") == "OVERLAPPING_TOKEN_INTERVAL_REPAIRED" for atom in group):
        timing_method = "OVERLAPPING_TOKEN_INTERVAL_REPAIRED"
    else:
        timing_method = "SOURCE_TOKEN_ENVELOPE" if exact_envelope else "TOKEN_PROPORTIONAL_SPLIT"
    text = "".join(str(atom["text"]) for atom in group)
    return {
        "text": text,
        "kind": classify_unit(text),
        "start": round(float(group[0]["start"]), 6),
        "end": round(float(group[-1]["end"]), 6),
        "confidence": round(min(float(atom["confidence"]) for atom in group), 6),
        "source_token_ids": source_token_ids,
        "segment_indices": list(dict.fromkeys(int(atom["segment_index"]) for atom in group)),
        "timing_method": timing_method,
    }


def atoms_to_units(atoms: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], int]:
    units: list[dict[str, Any]] = []
    current: list[dict[str, Any]] = []
    discarded = 0

    def flush() -> None:
        nonlocal current
        if current:
            units.append(_unit_from_atoms(current))
            current = []

    for index, atom in enumerate(atoms):
        char = str(atom["text"])
        if is_han(char):
            flush()
            units.append(_unit_from_atoms([atom]))
            continue
        if is_word_char(char) or _content_symbol(atoms, index):
            if current and atom.get("hard_boundary_before"):
                flush()
            current.append(atom)
            continue
        flush()
        discarded += 1
    flush()
    return units, discarded


def engine_atoms(entries: list[object]) -> list[dict[str, Any]]:
    atoms: list[dict[str, Any]] = []
    previous_segment = 0
    previous_end: float | None = None
    for segment_index, entry in enumerate(entries, start=1):
        if not isinstance(entry, dict):
            continue
        offsets = entry.get("offsets") or {}
        segment_start = max(0.0, float(offsets.get("from", 0)) / 1000.0)
        segment_end = max(segment_start, float(offsets.get("to", 0)) / 1000.0)
        visible_tokens: list[dict[str, Any]] = []
        for token in entry.get("tokens") or []:
            if not isinstance(token, dict):
                continue
            visible, leading_space, trailing_space = token_visible_text(token.get("text"))
            if not visible:
                continue
            token_offsets = token.get("offsets") or {}
            token_start = max(segment_start, float(token_offsets.get("from", 0)) / 1000.0)
            token_end = min(segment_end, max(token_start, float(token_offsets.get("to", 0)) / 1000.0))
            visible_tokens.append(
                {
                    "text": visible,
                    "leading_space": leading_space,
                    "trailing_space": trailing_space,
                    "start": token_start,
                    "end": token_end,
                    "confidence": float(token.get("p", 0.0)),
                    "token_timing_method": "SOURCE_TOKEN_EXACT",
                }
            )

        token_index = 0
        while token_index < len(visible_tokens):
            item = visible_tokens[token_index]
            if float(item["end"]) > float(item["start"]):
                token_index += 1
                continue
            run_end = token_index
            while run_end < len(visible_tokens) and float(visible_tokens[run_end]["end"]) <= float(visible_tokens[run_end]["start"]):
                run_end += 1
            left = segment_start if token_index == 0 else float(visible_tokens[token_index - 1]["end"])
            right = segment_end
            share_next_interval = False
            if run_end < len(visible_tokens):
                next_item = visible_tokens[run_end]
                next_start = float(next_item["start"])
                next_end = float(next_item["end"])
                if next_start > left:
                    right = next_start
                elif next_end > left:
                    right = next_end
                    share_next_interval = True
            if right <= left:
                raise ValueError(
                    f"第 {segment_index} 段第 {token_index + 1}–{run_end} 个可见 token 无法在相邻时间证据间插值"
                )
            invalid_count = run_end - token_index
            slot_count = invalid_count + (1 if share_next_interval else 0)
            slot_duration = (right - left) / slot_count
            for offset, invalid_item in enumerate(visible_tokens[token_index:run_end]):
                invalid_item["start"] = left + offset * slot_duration
                invalid_item["end"] = left + (offset + 1) * slot_duration
                invalid_item["token_timing_method"] = "ZERO_LENGTH_TOKEN_INTERPOLATED"
            if share_next_interval:
                visible_tokens[run_end]["start"] = left + invalid_count * slot_duration
                visible_tokens[run_end]["token_timing_method"] = "OVERLAPPING_TOKEN_INTERVAL_REPAIRED"
            token_index = run_end

        for token_number, item in enumerate(visible_tokens, start=1):
            visible = str(item["text"])
            leading_space = bool(item["leading_space"])
            trailing_space = bool(item["trailing_space"])
            token_start = float(item["start"])
            token_end = float(item["end"])
            token_id = f"token-{segment_index:04d}-{token_number:04d}"
            duration = token_end - token_start
            segment_changed = bool(atoms and segment_index != previous_segment)
            cross_segment_gap = token_start - previous_end if previous_end is not None else 0.0
            for char_index, char in enumerate(visible):
                hard_boundary = False
                if char_index == 0:
                    hard_boundary = leading_space or (
                        segment_changed and cross_segment_gap > MAX_CROSS_SEGMENT_JOIN_GAP
                    )
                atoms.append(
                    {
                        "text": char,
                        "start": token_start + char_index * duration / len(visible),
                        "end": token_start + (char_index + 1) * duration / len(visible),
                        "confidence": float(item["confidence"]),
                        "token_id": token_id,
                        "token_visible_count": len(visible),
                        "token_timing_method": item["token_timing_method"],
                        "segment_index": segment_index,
                        "hard_boundary_before": hard_boundary,
                    }
                )
            if trailing_space and atoms:
                atoms[-1]["hard_boundary_after"] = True
            previous_segment = segment_index
            previous_end = token_end
        if atoms and atoms[-1].get("hard_boundary_after"):
            previous_end = float(atoms[-1]["end"])
    for index in range(1, len(atoms)):
        if atoms[index - 1].get("hard_boundary_after"):
            atoms[index]["hard_boundary_before"] = True
    return atoms


def text_atoms(text: str) -> list[dict[str, Any]]:
    atoms: list[dict[str, Any]] = []
    boundary = False
    for index, char in enumerate(text):
        if char.isspace():
            boundary = True
            continue
        atoms.append(
            {
                "text": char,
                "start": float(index),
                "end": float(index + 1),
                "confidence": 1.0,
                "token_id": f"text-{index:06d}",
                "token_visible_count": 1,
                "segment_index": 0,
                "hard_boundary_before": boundary,
            }
        )
        boundary = False
    return atoms


def split_surface_text(text: str) -> list[dict[str, str]]:
    units, _ = atoms_to_units(text_atoms(text))
    return [{"text": str(unit["text"]), "kind": str(unit["kind"])} for unit in units]


def reference_plain_text(text: str) -> str:
    """Remove layout/inferred punctuation while preserving content-bearing written units."""
    return "".join(unit["text"] for unit in split_surface_text(text))


def parse_replacement(value: str) -> tuple[str, str]:
    if "=" not in value:
        raise argparse.ArgumentTypeError("替换必须使用 原识别片段=纠正片段")
    source, result = value.split("=", 1)
    if not source or not result or source == result:
        raise argparse.ArgumentTypeError("替换两端必须非空且内容不同")
    return source, result


def replacement_spans(
    raw_units: list[dict[str, Any]], replacements: list[tuple[str, str]], reference: str
) -> dict[int, tuple[int, str]]:
    raw_text = "".join(str(unit["text"]) for unit in raw_units)
    offsets: list[tuple[int, int]] = []
    cursor = 0
    for unit in raw_units:
        end = cursor + len(str(unit["text"]))
        offsets.append((cursor, end))
        cursor = end
    start_to_unit = {start: index for index, (start, _) in enumerate(offsets)}
    end_to_unit = {end: index + 1 for index, (_, end) in enumerate(offsets)}
    spans: dict[int, tuple[int, str]] = {}
    occupied: set[int] = set()
    for source_raw, result_raw in replacements:
        source = reference_plain_text(source_raw)
        result = reference_plain_text(result_raw)
        if not source or not result or source == result:
            raise ValueError(f"纠正项规范化后无效：{source_raw}={result_raw}")
        if result not in reference:
            raise ValueError(f"纠正结果未在参考文稿中出现：{result}")
        matches = list(re.finditer(re.escape(source), raw_text))
        if not matches:
            raise ValueError(f"原始识别中找不到待纠正片段：{source}")
        available: list[tuple[int, int]] = []
        for match in matches:
            if match.start() not in start_to_unit or match.end() not in end_to_unit:
                continue
            unit_start = start_to_unit[match.start()]
            unit_end = end_to_unit[match.end()]
            if not any(index in occupied for index in range(unit_start, unit_end)):
                available.append((unit_start, unit_end))
        if not available:
            raise ValueError(f"待纠正片段未落在完整文字单元边界或没有未占用匹配：{source}")
        for unit_start, unit_end in available:
            occupied.update(range(unit_start, unit_end))
            spans[unit_start] = (unit_end - unit_start, result)
    return spans


def allocate_result_units(start: float, end: float, text: str) -> list[dict[str, Any]]:
    pieces = split_surface_text(text)
    normalized = "".join(piece["text"] for piece in pieces)
    if not pieces or normalized != text:
        raise ValueError(f"纠正结果包含不能进入有声时间轴的字符：{text!r}")
    weights = [max(1, len(piece["text"])) for piece in pieces]
    total = sum(weights)
    cursor = start
    result = []
    consumed = 0
    for index, (piece, weight) in enumerate(zip(pieces, weights)):
        consumed += weight
        piece_end = end if index == len(pieces) - 1 else start + (end - start) * consumed / total
        result.append({**piece, "start": round(cursor, 6), "end": round(piece_end, 6)})
        cursor = piece_end
    return result


def project_relative(path: Path, project_root: Path) -> str:
    try:
        return Path(os.path.relpath(path.resolve(), project_root.resolve())).as_posix()
    except ValueError:
        return str(path.resolve())


def main() -> int:
    parser = argparse.ArgumentParser(description="从 whisper.cpp JSON 生成可审计的 S01 文字单元产物。")
    parser.add_argument("engine_json", type=Path)
    parser.add_argument("reference_script", type=Path)
    parser.add_argument("video", type=Path)
    parser.add_argument("output_dir", type=Path)
    parser.add_argument("--replace", action="append", default=[], type=parse_replacement, metavar="FROM=TO")
    parser.add_argument("--model", default="ggml-large-v3.bin")
    args = parser.parse_args()

    engine = read_json(args.engine_json)
    entries = engine.get("transcription")
    if not isinstance(entries, list) or not entries:
        raise ValueError("whisper.cpp JSON 缺少非空 transcription")
    reference = reference_plain_text(args.reference_script.read_text(encoding="utf-8"))

    raw_units, discarded_punctuation = atoms_to_units(engine_atoms(entries))
    if not raw_units:
        raise ValueError("没有获得可用的识别文字单元")
    for index, unit in enumerate(raw_units, start=1):
        unit["raw_unit_id"] = f"raw-unit-{index:06d}"

    raw_text = "".join(str(unit["text"]) for unit in raw_units)
    spans = replacement_spans(raw_units, args.replace, reference)
    mappings: list[dict[str, Any]] = []
    final_units: list[dict[str, Any]] = []
    raw_index = 0
    while raw_index < len(raw_units):
        replacement = spans.get(raw_index)
        source_count, result_text = replacement if replacement else (1, str(raw_units[raw_index]["text"]))
        source_group = raw_units[raw_index : raw_index + source_count]
        source_ids = [str(unit["raw_unit_id"]) for unit in source_group]
        source_text = "".join(str(unit["text"]) for unit in source_group)
        operation = "REPLACE" if replacement else "KEEP"
        mapping_id = f"map-{len(mappings) + 1:06d}"
        mapping: dict[str, Any] = {
            "mapping_id": mapping_id,
            "operation": operation,
            "source_unit_ids": source_ids,
            "source_text": source_text,
            "result_text": result_text,
            "reason": "REFERENCE_CONFIRMED_TYPO_OR_TERM" if replacement else "ASR_PRESERVED",
            "decision_status": "RESOLVED",
        }
        if replacement:
            mapping["reference_evidence"] = f"参考文稿包含：{result_text}"
        mappings.append(mapping)
        envelope_start = float(source_group[0]["start"])
        envelope_end = float(source_group[-1]["end"])
        if operation == "KEEP":
            result_units = [{
                "text": source_text,
                "kind": str(source_group[0]["kind"]),
                "start": round(envelope_start, 6),
                "end": round(envelope_end, 6),
            }]
        else:
            result_units = allocate_result_units(envelope_start, envelope_end, result_text)
        for result_unit in result_units:
            final_units.append(
                {
                    "unit_id": f"unit-{len(final_units) + 1:06d}",
                    "mapping_id": mapping_id,
                    **result_unit,
                    "source_unit_ids": source_ids,
                    "source_asr_text": source_text,
                    "operation": operation,
                    "timing_method": "SOURCE_UNIT_ENVELOPE" if operation == "KEEP" else "SOURCE_ENVELOPE_PROPORTIONAL",
                }
            )
        raw_index += source_count

    args.output_dir.mkdir(parents=True, exist_ok=True)
    relative_engine = (
        args.engine_json.relative_to(args.output_dir).as_posix()
        if args.engine_json.is_relative_to(args.output_dir)
        else str(args.engine_json)
    )
    raw_output = {
        "schema_version": SCHEMA_VERSION,
        "stage": "S01",
        "timebase": "INPUT_VIDEO_ABSOLUTE_SECONDS",
        "engine": {"name": "whisper.cpp", "version": "1.9.2", "model": args.model},
        "unitization_policy": {
            "han": "ONE_CHARACTER_PER_UNIT",
            "numbers": "CONSECUTIVE_GROUP",
            "percentages": "NUMBER_AND_SUFFIX_GROUP",
            "english": "CONSECUTIVE_GROUP",
            "structured_alphanumeric": "CONSECUTIVE_GROUP",
            "inferred_punctuation": "EXCLUDED",
        },
        "units": [
            {key: value for key, value in unit.items() if key != "segment_indices"}
            for unit in raw_units
        ],
        "original_engine_output": relative_engine,
    }
    correction_output = {
        "schema_version": SCHEMA_VERSION,
        "stage": "S01",
        "allowed_operations": ["KEEP", "REPLACE"],
        "mappings": mappings,
        "pending_items": [],
    }
    timeline_output = {
        "schema_version": SCHEMA_VERSION,
        "stage": "S01",
        "timebase": "INPUT_VIDEO_ABSOLUTE_SECONDS",
        "unitization_policy": raw_output["unitization_policy"],
        "units": final_units,
    }
    matcher = difflib.SequenceMatcher(a=raw_text, b=reference, autojunk=False)
    inserted_reference_codepoints = sum(j2 - j1 for tag, _, _, j1, j2 in matcher.get_opcodes() if tag == "insert")
    preserved_asr_only_codepoints = sum(i2 - i1 for tag, i1, i2, _, _ in matcher.get_opcodes() if tag == "delete")
    raw_kind_counts = Counter(str(unit["kind"]) for unit in raw_units)
    raw_timing_method_counts = Counter(str(unit["timing_method"]) for unit in raw_units)
    final_kind_counts = Counter(str(unit["kind"]) for unit in final_units)
    report_output = {
        "schema_version": SCHEMA_VERSION,
        "stage": "S01",
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "inputs": {
            "video": project_relative(args.video, args.output_dir),
            "reference_script": project_relative(args.reference_script, args.output_dir),
        },
        "audio_extraction_report": "audio/extraction-report.json",
        "asr_engine": raw_output["engine"],
        "counts": {
            "raw_units": len(raw_units),
            "raw_units_by_kind": dict(sorted(raw_kind_counts.items())),
            "raw_units_by_timing_method": dict(sorted(raw_timing_method_counts.items())),
            "keep_mappings": sum(mapping["operation"] == "KEEP" for mapping in mappings),
            "replace_mappings": sum(mapping["operation"] == "REPLACE" for mapping in mappings),
            "final_units": len(final_units),
            "final_units_by_kind": dict(sorted(final_kind_counts.items())),
            "discarded_inferred_punctuation": discarded_punctuation,
            "reference_only_codepoints_ignored": inserted_reference_codepoints,
            "asr_only_codepoints_preserved": preserved_asr_only_codepoints,
        },
        "pending_items": [],
        "validation": {"status": "NOT_RUN", "command": ""},
    }

    outputs = {
        "raw-asr.json": raw_output,
        "correction-map.json": correction_output,
        "text-unit-timeline.json": timeline_output,
        "s01-report.json": report_output,
    }
    for name, value in outputs.items():
        (args.output_dir / name).write_text(
            json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
    print(json.dumps(report_output["counts"], ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
