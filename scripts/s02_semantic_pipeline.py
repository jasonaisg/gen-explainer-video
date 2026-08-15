#!/usr/bin/env python3
"""Build and validate S02 semantic transcript and semantic blocks."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
from pathlib import Path
from typing import Any


SCHEMA_VERSION = "1.0"
TERMINAL_PUNCTUATION = {"。", "！", "？", "!", "?"}
ALLOWED_PUNCTUATION = {"，", "。", "！", "？", "；", "：", "、", ",", ".", "!", "?", ";", ":"}
UNIT_ID_PATTERN = re.compile(r"^unit-(\d{6})$")


def read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"JSON 顶层必须是对象：{path}")
    return value


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def finite_number(value: object) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(float(value))


def unit_index(unit_id: object, unit_count: int) -> int:
    if not isinstance(unit_id, str):
        raise ValueError(f"文字单元 ID 非法：{unit_id!r}")
    match = UNIT_ID_PATTERN.fullmatch(unit_id)
    if not match:
        raise ValueError(f"文字单元 ID 非法：{unit_id}")
    index = int(match.group(1)) - 1
    if index < 0 or index >= unit_count:
        raise ValueError(f"文字单元 ID 超出来源范围：{unit_id}")
    return index


def load_units(timeline_path: Path) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    timeline = read_json(timeline_path)
    units = timeline.get("units")
    if timeline.get("schema_version") != "2.0" or not isinstance(units, list) or not units:
        raise ValueError("输入必须是 S01 schema 2.0 的非空 text-unit-timeline.json")
    expected_ids = [f"unit-{index:06d}" for index in range(1, len(units) + 1)]
    actual_ids = [unit.get("unit_id") if isinstance(unit, dict) else None for unit in units]
    if actual_ids != expected_ids:
        raise ValueError("S01 unit_id 必须连续且按顺序排列")
    previous_start = -math.inf
    for unit in units:
        if not isinstance(unit.get("text"), str) or not unit["text"]:
            raise ValueError(f"{unit.get('unit_id')} 缺少非空文字")
        if not finite_number(unit.get("start")) or not finite_number(unit.get("end")):
            raise ValueError(f"{unit.get('unit_id')} 时间非法")
        start, end = float(unit["start"]), float(unit["end"])
        if start < previous_start or end <= start:
            raise ValueError(f"{unit['unit_id']} 时间倒置、零时长或逆序")
        previous_start = start
    return timeline, units


def source_range(units: list[dict[str, Any]], start: int, end: int) -> dict[str, Any]:
    return {
        "start_unit_id": units[start]["unit_id"],
        "end_unit_id": units[end]["unit_id"],
        "unit_count": end - start + 1,
    }


def verbatim_span(units: list[dict[str, Any]], start: int, end: int) -> str:
    return "".join(str(unit["text"]) for unit in units[start : end + 1])


def semantic_span(
    units: list[dict[str, Any]],
    start: int,
    end: int,
    punctuation_by_index: dict[int, str],
) -> str:
    pieces: list[str] = []
    for index in range(start, end + 1):
        pieces.append(str(units[index]["text"]))
        if index in punctuation_by_index:
            pieces.append(punctuation_by_index[index])
    return "".join(pieces)


def resolve_punctuation(
    units: list[dict[str, Any]], decisions: object
) -> list[dict[str, Any]]:
    if not isinstance(decisions, list) or not decisions:
        raise ValueError("punctuation_decisions 必须是非空数组")
    resolved: list[dict[str, Any]] = []
    previous_index = -1
    for number, decision in enumerate(decisions, start=1):
        if not isinstance(decision, dict):
            raise ValueError(f"第 {number} 个标点决定必须是对象")
        index = unit_index(decision.get("after_unit_id"), len(units))
        punctuation = decision.get("punctuation")
        if punctuation not in ALLOWED_PUNCTUATION:
            raise ValueError(f"第 {number} 个标点决定使用非法标点：{punctuation}")
        if index <= previous_index:
            raise ValueError("标点决定必须按 unit_id 严格递增")
        paragraph_break = bool(decision.get("paragraph_break_after", False))
        if paragraph_break and punctuation not in TERMINAL_PUNCTUATION:
            raise ValueError("段落只能结束在句末标点")
        resolved.append(
            {
                "unit_index": index,
                "after_unit_id": units[index]["unit_id"],
                "punctuation": punctuation,
                "paragraph_break_after": paragraph_break,
            }
        )
        previous_index = index
    if resolved[-1]["unit_index"] != len(units) - 1:
        raise ValueError("最后一个标点决定必须位于 S01 全文末尾")
    if resolved[-1]["punctuation"] not in TERMINAL_PUNCTUATION:
        raise ValueError("全文必须以句末标点结束")
    return resolved


def build_sentences(
    units: list[dict[str, Any]], decisions: list[dict[str, Any]]
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[int, str]]:
    punctuation_by_index = {
        int(decision["unit_index"]): str(decision["punctuation"]) for decision in decisions
    }
    sentences: list[dict[str, Any]] = []
    paragraphs: list[dict[str, Any]] = []
    sentence_start = 0
    paragraph_sentence_start = 0
    paragraph_number = 1

    for decision_index, decision in enumerate(decisions):
        if decision["punctuation"] not in TERMINAL_PUNCTUATION:
            continue
        sentence_end = int(decision["unit_index"])
        if sentence_end < sentence_start:
            raise ValueError("句子边界必须形成非空且连续的来源范围")
        sentence_id = f"sentence-{len(sentences) + 1:04d}"
        inserted = [
            {
                "after_unit_id": item["after_unit_id"],
                "punctuation": item["punctuation"],
            }
            for item in decisions[: decision_index + 1]
            if sentence_start <= int(item["unit_index"]) <= sentence_end
        ]
        sentences.append(
            {
                "sentence_id": sentence_id,
                "paragraph_id": f"paragraph-{paragraph_number:03d}",
                "verbatim_text": verbatim_span(units, sentence_start, sentence_end),
                "semantic_text": semantic_span(
                    units, sentence_start, sentence_end, punctuation_by_index
                ),
                "start": round(float(units[sentence_start]["start"]), 6),
                "end": round(float(units[sentence_end]["end"]), 6),
                "source_unit_range": source_range(units, sentence_start, sentence_end),
                "inserted_punctuation": inserted,
            }
        )
        sentence_start = sentence_end + 1
        if decision["paragraph_break_after"]:
            group = sentences[paragraph_sentence_start:]
            paragraphs.append(
                {
                    "paragraph_id": f"paragraph-{paragraph_number:03d}",
                    "start_sentence_id": group[0]["sentence_id"],
                    "end_sentence_id": group[-1]["sentence_id"],
                    "sentence_count": len(group),
                    "semantic_text": "".join(str(item["semantic_text"]) for item in group),
                }
            )
            paragraph_sentence_start = len(sentences)
            paragraph_number += 1

    if sentence_start != len(units):
        raise ValueError("句子没有完整覆盖 S01 全文")
    if paragraph_sentence_start < len(sentences):
        group = sentences[paragraph_sentence_start:]
        paragraphs.append(
            {
                "paragraph_id": f"paragraph-{paragraph_number:03d}",
                "start_sentence_id": group[0]["sentence_id"],
                "end_sentence_id": group[-1]["sentence_id"],
                "sentence_count": len(group),
                "semantic_text": "".join(str(item["semantic_text"]) for item in group),
            }
        )
    return sentences, paragraphs, punctuation_by_index


def build_blocks(
    units: list[dict[str, Any]],
    decisions: object,
    punctuation_by_index: dict[int, str],
) -> list[dict[str, Any]]:
    if not isinstance(decisions, list) or not decisions:
        raise ValueError("block_decisions 必须是非空数组")
    blocks: list[dict[str, Any]] = []
    block_start = 0
    for number, decision in enumerate(decisions, start=1):
        if not isinstance(decision, dict):
            raise ValueError(f"第 {number} 个语义块决定必须是对象")
        required = ("title", "semantic_role", "cognitive_goal", "boundary_reason")
        if any(not isinstance(decision.get(key), str) or not decision[key].strip() for key in required):
            raise ValueError(f"第 {number} 个语义块决定字段不完整")
        block_end = unit_index(decision.get("end_unit_id"), len(units))
        if block_end < block_start:
            raise ValueError("语义块边界必须按 unit_id 递增并形成非空范围")
        blocks.append(
            {
                "block_id": f"block-{number:03d}",
                "title": decision["title"].strip(),
                "semantic_role": decision["semantic_role"].strip(),
                "cognitive_goal": decision["cognitive_goal"].strip(),
                "boundary_reason": decision["boundary_reason"].strip(),
                "start": round(float(units[block_start]["start"]), 6),
                "end": round(float(units[block_end]["end"]), 6),
                "source_unit_range": source_range(units, block_start, block_end),
                "verbatim_text": verbatim_span(units, block_start, block_end),
                "semantic_text": semantic_span(
                    units, block_start, block_end, punctuation_by_index
                ),
            }
        )
        block_start = block_end + 1
    if block_start != len(units):
        raise ValueError("语义块没有完整覆盖 S01 全文")
    if blocks[-1]["boundary_reason"] != "END_OF_TRANSCRIPT":
        raise ValueError("最后一个语义块的 boundary_reason 必须是 END_OF_TRANSCRIPT")
    return blocks


def range_indices(value: object, unit_count: int) -> tuple[int, int]:
    if not isinstance(value, dict):
        raise ValueError("source_unit_range 必须是对象")
    start = unit_index(value.get("start_unit_id"), unit_count)
    end = unit_index(value.get("end_unit_id"), unit_count)
    if end < start or value.get("unit_count") != end - start + 1:
        raise ValueError("source_unit_range 的范围或数量不一致")
    return start, end


def validate_artifacts(
    timeline_path: Path,
    transcript_path: Path,
    blocks_path: Path,
    require_passed: bool = True,
) -> list[str]:
    issues: list[str] = []
    try:
        _, units = load_units(timeline_path)
        transcript = read_json(transcript_path)
        block_doc = read_json(blocks_path)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        return [str(error)]

    timeline_hash = sha256_file(timeline_path)
    if transcript.get("schema_version") != SCHEMA_VERSION or transcript.get("stage") != "S02":
        issues.append("semantic-transcript 的 schema_version 或 stage 不正确")
    source = transcript.get("source")
    if not isinstance(source, dict) or source.get("sha256") != timeline_hash:
        issues.append("semantic-transcript 的 S01 来源哈希不匹配")
    elif source.get("schema_version") != "2.0" or source.get("unit_count") != len(units):
        issues.append("semantic-transcript 的 S01 来源元数据不匹配")

    sentences = transcript.get("sentences")
    paragraphs = transcript.get("paragraphs")
    punctuation_by_index: dict[int, str] = {}
    if not isinstance(sentences, list) or not sentences:
        issues.append("sentences 必须是非空数组")
        sentences = []
    expected_unit_start = 0
    for number, sentence in enumerate(sentences, start=1):
        if not isinstance(sentence, dict):
            issues.append(f"第 {number} 个句子必须是对象")
            continue
        if sentence.get("sentence_id") != f"sentence-{number:04d}":
            issues.append(f"第 {number} 个 sentence_id 不连续")
        try:
            start, end = range_indices(sentence.get("source_unit_range"), len(units))
        except ValueError as error:
            issues.append(f"{sentence.get('sentence_id')}：{error}")
            continue
        if start != expected_unit_start:
            issues.append(f"{sentence.get('sentence_id')} 没有连续覆盖来源文字单元")
        expected_unit_start = end + 1
        if sentence.get("verbatim_text") != verbatim_span(units, start, end):
            issues.append(f"{sentence.get('sentence_id')} 忠实文字与来源不一致")
        if sentence.get("start") != round(float(units[start]["start"]), 6) or sentence.get("end") != round(float(units[end]["end"]), 6):
            issues.append(f"{sentence.get('sentence_id')} 时间不等于来源包络")
        inserted = sentence.get("inserted_punctuation")
        if not isinstance(inserted, list) or not inserted:
            issues.append(f"{sentence.get('sentence_id')} 缺少插入标点")
            continue
        local_indices: list[int] = []
        for item in inserted:
            try:
                index = unit_index(item.get("after_unit_id") if isinstance(item, dict) else None, len(units))
            except ValueError as error:
                issues.append(f"{sentence.get('sentence_id')}：{error}")
                continue
            punctuation = item.get("punctuation") if isinstance(item, dict) else None
            if index < start or index > end or punctuation not in ALLOWED_PUNCTUATION:
                issues.append(f"{sentence.get('sentence_id')} 插入标点不合法")
                continue
            if index in punctuation_by_index:
                issues.append(f"{sentence.get('sentence_id')} 重复使用标点边界")
            punctuation_by_index[index] = str(punctuation)
            local_indices.append(index)
        if local_indices != sorted(local_indices) or not local_indices or local_indices[-1] != end:
            issues.append(f"{sentence.get('sentence_id')} 标点顺序或句末边界不正确")
        elif punctuation_by_index.get(end) not in TERMINAL_PUNCTUATION:
            issues.append(f"{sentence.get('sentence_id')} 没有句末标点")
        if sentence.get("semantic_text") != semantic_span(units, start, end, punctuation_by_index):
            issues.append(f"{sentence.get('sentence_id')} 语义文字与插入标点不一致")
    if expected_unit_start != len(units):
        issues.append("句子没有完整覆盖全部 S01 文字单元")

    if not isinstance(paragraphs, list) or not paragraphs:
        issues.append("paragraphs 必须是非空数组")
        paragraphs = []
    expected_sentence_start = 0
    for number, paragraph in enumerate(paragraphs, start=1):
        if not isinstance(paragraph, dict):
            issues.append(f"第 {number} 个段落必须是对象")
            continue
        paragraph_id = f"paragraph-{number:03d}"
        if paragraph.get("paragraph_id") != paragraph_id:
            issues.append(f"第 {number} 个 paragraph_id 不连续")
        try:
            start = int(str(paragraph.get("start_sentence_id")).split("-")[-1]) - 1
            end = int(str(paragraph.get("end_sentence_id")).split("-")[-1]) - 1
        except ValueError:
            issues.append(f"{paragraph_id} 句子范围非法")
            continue
        if start != expected_sentence_start or end < start or end >= len(sentences):
            issues.append(f"{paragraph_id} 没有连续覆盖句子")
            continue
        group = sentences[start : end + 1]
        expected_sentence_start = end + 1
        if paragraph.get("sentence_count") != len(group):
            issues.append(f"{paragraph_id} sentence_count 不正确")
        if any(item.get("paragraph_id") != paragraph_id for item in group):
            issues.append(f"{paragraph_id} 与句子的 paragraph_id 不一致")
        if paragraph.get("semantic_text") != "".join(str(item.get("semantic_text", "")) for item in group):
            issues.append(f"{paragraph_id} 文字与所属句子不一致")
    if expected_sentence_start != len(sentences):
        issues.append("段落没有完整覆盖全部句子")

    full_verbatim = verbatim_span(units, 0, len(units) - 1)
    if transcript.get("full_verbatim_text") != full_verbatim:
        issues.append("full_verbatim_text 与 S01 全文不一致")
    expected_semantic = "\n\n".join(str(item.get("semantic_text", "")) for item in paragraphs)
    if transcript.get("full_semantic_text") != expected_semantic:
        issues.append("full_semantic_text 与段落文字不一致")

    if block_doc.get("schema_version") != SCHEMA_VERSION or block_doc.get("stage") != "S02":
        issues.append("semantic-blocks 的 schema_version 或 stage 不正确")
    sources = block_doc.get("sources")
    timeline_source = sources.get("text_unit_timeline") if isinstance(sources, dict) else None
    transcript_source = sources.get("semantic_transcript") if isinstance(sources, dict) else None
    if not isinstance(timeline_source, dict) or timeline_source.get("sha256") != timeline_hash:
        issues.append("semantic-blocks 的 S01 来源哈希不匹配")
    if not isinstance(transcript_source, dict) or transcript_source.get("sha256") != sha256_file(transcript_path):
        issues.append("semantic-blocks 的 semantic-transcript 来源哈希不匹配")

    blocks = block_doc.get("blocks")
    if not isinstance(blocks, list) or not blocks:
        issues.append("blocks 必须是非空数组")
        blocks = []
    expected_unit_start = 0
    for number, block in enumerate(blocks, start=1):
        if not isinstance(block, dict):
            issues.append(f"第 {number} 个语义块必须是对象")
            continue
        block_id = f"block-{number:03d}"
        if block.get("block_id") != block_id:
            issues.append(f"第 {number} 个 block_id 不连续")
        for key in ("title", "semantic_role", "cognitive_goal", "boundary_reason"):
            if not isinstance(block.get(key), str) or not block[key].strip():
                issues.append(f"{block_id} 缺少 {key}")
        try:
            start, end = range_indices(block.get("source_unit_range"), len(units))
        except ValueError as error:
            issues.append(f"{block_id}：{error}")
            continue
        if start != expected_unit_start:
            issues.append(f"{block_id} 没有连续覆盖来源文字单元")
        expected_unit_start = end + 1
        if block.get("verbatim_text") != verbatim_span(units, start, end):
            issues.append(f"{block_id} 忠实文字与来源不一致")
        if block.get("semantic_text") != semantic_span(units, start, end, punctuation_by_index):
            issues.append(f"{block_id} 语义文字与 semantic-transcript 不一致")
        if block.get("start") != round(float(units[start]["start"]), 6) or block.get("end") != round(float(units[end]["end"]), 6):
            issues.append(f"{block_id} 时间不等于来源包络")
    if expected_unit_start != len(units):
        issues.append("语义块没有完整覆盖全部 S01 文字单元")
    if blocks and blocks[-1].get("boundary_reason") != "END_OF_TRANSCRIPT":
        issues.append("最后一个语义块的 boundary_reason 必须是 END_OF_TRANSCRIPT")

    if require_passed:
        for name, document in (("semantic-transcript", transcript), ("semantic-blocks", block_doc)):
            validation = document.get("validation")
            if not isinstance(validation, dict) or validation.get("status") != "PASSED" or validation.get("issue_count") != 0:
                issues.append(f"{name} 最终验证状态不正确")
    return issues


def build(timeline_path: Path, decisions_path: Path, output_dir: Path) -> None:
    _, units = load_units(timeline_path)
    decisions = read_json(decisions_path)
    punctuation = resolve_punctuation(units, decisions.get("punctuation_decisions"))
    sentences, paragraphs, punctuation_by_index = build_sentences(units, punctuation)
    blocks = build_blocks(units, decisions.get("block_decisions"), punctuation_by_index)
    timeline_hash = sha256_file(timeline_path)
    full_verbatim = verbatim_span(units, 0, len(units) - 1)

    transcript = {
        "schema_version": SCHEMA_VERSION,
        "stage": "S02",
        "timebase": "INPUT_VIDEO_ABSOLUTE_SECONDS",
        "source": {
            "file": "../S01/text-unit-timeline.json",
            "schema_version": "2.0",
            "sha256": timeline_hash,
            "unit_count": len(units),
        },
        "full_verbatim_text": full_verbatim,
        "full_semantic_text": "\n\n".join(str(item["semantic_text"]) for item in paragraphs),
        "paragraphs": paragraphs,
        "sentences": sentences,
        "validation": {
            "status": "PENDING",
            "issue_count": None,
            "source_units_covered": len(units),
            "source_units_total": len(units),
        },
    }
    output_dir.mkdir(parents=True, exist_ok=True)
    transcript_path = output_dir / "semantic-transcript.json"
    blocks_path = output_dir / "semantic-blocks.json"
    write_json(transcript_path, transcript)

    block_doc = {
        "schema_version": SCHEMA_VERSION,
        "stage": "S02",
        "timebase": "INPUT_VIDEO_ABSOLUTE_SECONDS",
        "sources": {
            "text_unit_timeline": {
                "file": "../S01/text-unit-timeline.json",
                "schema_version": "2.0",
                "sha256": timeline_hash,
                "unit_count": len(units),
            },
            "semantic_transcript": {
                "file": "semantic-transcript.json",
                "schema_version": SCHEMA_VERSION,
                "sha256": sha256_file(transcript_path),
            },
        },
        "blocks": blocks,
        "validation": {
            "status": "PENDING",
            "issue_count": None,
            "source_units_covered": len(units),
            "source_units_total": len(units),
        },
    }
    write_json(blocks_path, block_doc)
    issues = validate_artifacts(
        timeline_path, transcript_path, blocks_path, require_passed=False
    )
    if issues:
        raise ValueError("S02 产物验证失败：\n- " + "\n- ".join(issues))

    transcript["validation"]["status"] = "PASSED"
    transcript["validation"]["issue_count"] = 0
    write_json(transcript_path, transcript)
    block_doc["sources"]["semantic_transcript"]["sha256"] = sha256_file(transcript_path)
    block_doc["validation"]["status"] = "PASSED"
    block_doc["validation"]["issue_count"] = 0
    write_json(blocks_path, block_doc)
    final_issues = validate_artifacts(timeline_path, transcript_path, blocks_path)
    if final_issues:
        raise ValueError("S02 最终验证失败：\n- " + "\n- ".join(final_issues))
    print(
        json.dumps(
            {
                "sentences": len(sentences),
                "paragraphs": len(paragraphs),
                "blocks": len(blocks),
                "source_units": len(units),
                "validation": "PASSED",
            },
            ensure_ascii=False,
        )
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="构建或验证 S02 语义转录与语义块。")
    subparsers = parser.add_subparsers(dest="command", required=True)
    build_parser = subparsers.add_parser("build")
    build_parser.add_argument("timeline", type=Path)
    build_parser.add_argument("decisions", type=Path)
    build_parser.add_argument("output_dir", type=Path)
    validate_parser = subparsers.add_parser("validate")
    validate_parser.add_argument("timeline", type=Path)
    validate_parser.add_argument("semantic_transcript", type=Path)
    validate_parser.add_argument("semantic_blocks", type=Path)
    args = parser.parse_args()
    try:
        if args.command == "build":
            build(args.timeline, args.decisions, args.output_dir)
            return 0
        issues = validate_artifacts(
            args.timeline, args.semantic_transcript, args.semantic_blocks
        )
        if issues:
            print("S02 验证失败：")
            for issue in issues:
                print(f"- {issue}")
            return 1
        print("S02 验证通过")
        return 0
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"错误：{error}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
