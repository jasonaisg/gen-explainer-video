#!/usr/bin/env python3
"""Validate S01 ASR correction and text-unit provenance."""

from __future__ import annotations

import argparse
import json
import math
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


REQUIRED_FILES = (
    "audio/extracted-audio.mp3",
    "audio/extraction-report.json",
    "asr-raw/engine-output.json",
    "raw-asr.json",
    "correction-map.json",
    "text-unit-timeline.json",
    "s01-report.json",
)
ALLOWED_OPERATIONS = {"KEEP", "REPLACE"}
ALLOWED_KINDS = {"han", "number", "percentage", "english", "word", "alphanumeric", "content_symbol"}
SCHEMA_VERSION = "2.0"


def load_json(path: Path, issues: list[str]) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        issues.append(f"无法读取 JSON {path.name}：{exc}")
        return {}
    if not isinstance(value, dict):
        issues.append(f"{path.name} 顶层必须是对象")
        return {}
    return value


def finite_number(value: object) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(float(value))


def validate(transcript_dir: Path, video_duration: float) -> list[str]:
    issues: list[str] = []
    for name in REQUIRED_FILES:
        if not (transcript_dir / name).is_file():
            issues.append(f"缺少文件：{name}")
    if (transcript_dir / "character-timeline.json").exists():
        issues.append("发现遗留 character-timeline.json；S01 v2.0 只允许正式使用 text-unit-timeline.json")
    if issues:
        return issues

    raw = load_json(transcript_dir / "raw-asr.json", issues)
    corrections = load_json(transcript_dir / "correction-map.json", issues)
    timeline = load_json(transcript_dir / "text-unit-timeline.json", issues)
    if issues:
        return issues
    for name, value in (("raw-asr.json", raw), ("correction-map.json", corrections), ("text-unit-timeline.json", timeline)):
        if value.get("schema_version") != SCHEMA_VERSION:
            issues.append(f"{name} schema_version 必须为 {SCHEMA_VERSION}")

    raw_units = raw.get("units")
    mappings = corrections.get("mappings")
    final_units = timeline.get("units")
    for label, value in (
        ("raw-asr.units", raw_units),
        ("correction-map.mappings", mappings),
        ("text-unit-timeline.units", final_units),
    ):
        if not isinstance(value, list) or not value:
            issues.append(f"{label} 必须是非空数组")
    if issues:
        return issues

    raw_by_id: dict[str, dict[str, Any]] = {}
    previous_start = -math.inf
    for index, unit in enumerate(raw_units, start=1):
        if not isinstance(unit, dict):
            issues.append(f"raw-asr 第 {index} 项必须是对象")
            continue
        unit_id = unit.get("raw_unit_id")
        text = unit.get("text")
        start, end = unit.get("start"), unit.get("end")
        kind = unit.get("kind")
        source_token_ids = unit.get("source_token_ids")
        if not isinstance(unit_id, str) or not unit_id:
            issues.append(f"raw-asr 第 {index} 项缺少 raw_unit_id")
            continue
        if unit_id in raw_by_id:
            issues.append(f"raw-asr raw_unit_id 重复：{unit_id}")
        raw_by_id[unit_id] = unit
        if not isinstance(text, str) or not text:
            issues.append(f"{unit_id} 的 text 必须非空")
        if kind not in ALLOWED_KINDS:
            issues.append(f"{unit_id} 的 kind 非法：{kind}")
        if kind == "han" and (not isinstance(text, str) or len(text) != 1):
            issues.append(f"{unit_id} 的中文单元必须恰好包含一个汉字")
        if kind == "percentage" and (not isinstance(text, str) or not any(char.isdigit() for char in text) or text[-1:] not in {"%", "‰", "‱"}):
            issues.append(f"{unit_id} 的百分比单元格式不正确：{text}")
        if not isinstance(source_token_ids, list) or not source_token_ids or not all(isinstance(x, str) for x in source_token_ids):
            issues.append(f"{unit_id} 必须引用至少一个 source_token_id")
        if not finite_number(start) or not finite_number(end):
            issues.append(f"{unit_id} 的时间必须是有限数字")
            continue
        start_f, end_f = float(start), float(end)
        if start_f < 0 or end_f <= start_f or end_f > video_duration:
            issues.append(f"{unit_id} 时间越界、倒置或零时长：{start_f}–{end_f}")
        if start_f < previous_start:
            issues.append(f"{unit_id} 的开始时间逆序")
        previous_start = start_f

    mapping_by_id: dict[str, dict[str, Any]] = {}
    mapping_source_sequence: list[str] = []
    for index, mapping in enumerate(mappings, start=1):
        if not isinstance(mapping, dict):
            issues.append(f"correction-map 第 {index} 项必须是对象")
            continue
        mapping_id = mapping.get("mapping_id")
        operation = mapping.get("operation")
        source_ids = mapping.get("source_unit_ids")
        source_text = mapping.get("source_text")
        result_text = mapping.get("result_text")
        if not isinstance(mapping_id, str) or not mapping_id:
            issues.append(f"correction-map 第 {index} 项缺少 mapping_id")
            continue
        if mapping_id in mapping_by_id:
            issues.append(f"mapping_id 重复：{mapping_id}")
        mapping_by_id[mapping_id] = mapping
        if operation not in ALLOWED_OPERATIONS:
            issues.append(f"{mapping_id} 使用非法操作：{operation}")
        if not isinstance(source_ids, list) or not source_ids or not all(isinstance(x, str) for x in source_ids):
            issues.append(f"{mapping_id} 必须引用至少一个 source_unit_id")
            continue
        mapping_source_sequence.extend(source_ids)
        missing = [source_id for source_id in source_ids if source_id not in raw_by_id]
        if missing:
            issues.append(f"{mapping_id} 引用了不存在的原始文字单元：{missing}")
            continue
        expected_source_text = "".join(str(raw_by_id[source_id].get("text", "")) for source_id in source_ids)
        if source_text != expected_source_text:
            issues.append(f"{mapping_id} 的 source_text 与原始文字单元不一致")
        if not isinstance(result_text, str) or not result_text:
            issues.append(f"{mapping_id} 的 result_text 必须非空")
        if operation == "KEEP" and result_text != source_text:
            issues.append(f"{mapping_id} 为 KEEP，但 result_text 改变了文字")
        if mapping.get("decision_status", "RESOLVED") != "RESOLVED":
            issues.append(f"{mapping_id} 尚未解决")

    raw_ids = list(raw_by_id)
    counts = Counter(mapping_source_sequence)
    if mapping_source_sequence != raw_ids:
        issues.append("correction-map 必须按原始顺序完整覆盖所有 raw_unit_id")
    duplicated = [unit_id for unit_id, count in counts.items() if count != 1]
    if duplicated:
        issues.append(f"原始文字单元没有被唯一覆盖：{duplicated}")
    if corrections.get("pending_items") not in ([], None):
        issues.append("correction-map 仍有 pending_items")

    final_by_id: dict[str, dict[str, Any]] = {}
    final_groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    previous_start = -math.inf
    for index, unit in enumerate(final_units, start=1):
        if not isinstance(unit, dict):
            issues.append(f"text-unit-timeline 第 {index} 项必须是对象")
            continue
        unit_id = unit.get("unit_id")
        text = unit.get("text")
        kind = unit.get("kind")
        mapping_id = unit.get("mapping_id")
        source_ids = unit.get("source_unit_ids")
        operation = unit.get("operation")
        start, end = unit.get("start"), unit.get("end")
        if not isinstance(unit_id, str) or not unit_id:
            issues.append(f"text-unit-timeline 第 {index} 项缺少 unit_id")
            continue
        if unit_id in final_by_id:
            issues.append(f"最终 unit_id 重复：{unit_id}")
        final_by_id[unit_id] = unit
        if not isinstance(text, str) or not text:
            issues.append(f"{unit_id} 的 text 必须非空")
        if kind not in ALLOWED_KINDS:
            issues.append(f"{unit_id} 的 kind 非法：{kind}")
        if mapping_id not in mapping_by_id:
            issues.append(f"{unit_id} 引用了不存在的 mapping_id：{mapping_id}")
            continue
        final_groups[mapping_id].append(unit)
        mapping = mapping_by_id[mapping_id]
        if source_ids != mapping.get("source_unit_ids"):
            issues.append(f"{unit_id} 的 source_unit_ids 与映射不一致")
        if operation != mapping.get("operation") or operation not in ALLOWED_OPERATIONS:
            issues.append(f"{unit_id} 的 operation 与映射不一致")
        if not finite_number(start) or not finite_number(end):
            issues.append(f"{unit_id} 的时间必须是有限数字")
            continue
        start_f, end_f = float(start), float(end)
        source_units = [raw_by_id[x] for x in mapping.get("source_unit_ids", []) if x in raw_by_id]
        if source_units:
            source_start = min(float(x["start"]) for x in source_units)
            source_end = max(float(x["end"]) for x in source_units)
            if start_f < source_start - 1e-6 or end_f > source_end + 1e-6 or end_f <= start_f:
                issues.append(f"{unit_id} 的时间不在来源区间内或没有正时长")
        if start_f < previous_start:
            issues.append(f"{unit_id} 的开始时间逆序")
        previous_start = start_f

    for mapping_id, mapping in mapping_by_id.items():
        group = final_groups.get(mapping_id, [])
        if not group:
            issues.append(f"{mapping_id} 没有生成最终文字单元")
            continue
        if "".join(str(x.get("text", "")) for x in group) != mapping.get("result_text"):
            issues.append(f"{mapping_id} 的最终文字单元与 result_text 不一致")
        source_units = [raw_by_id[x] for x in mapping.get("source_unit_ids", []) if x in raw_by_id]
        if source_units:
            source_start = min(float(x["start"]) for x in source_units)
            source_end = max(float(x["end"]) for x in source_units)
            if abs(float(group[0]["start"]) - source_start) > 1e-6 or abs(float(group[-1]["end"]) - source_end) > 1e-6:
                issues.append(f"{mapping_id} 的最终文字单元没有完整继承来源时间包络")

    final_text = "".join(str(unit.get("text", "")) for unit in final_units if isinstance(unit, dict))
    expected_final_text = "".join(
        str(mapping.get("result_text", "")) for mapping in mappings if isinstance(mapping, dict)
    )
    if final_text != expected_final_text:
        issues.append("text-unit-timeline 全文与 correction-map 结果不一致")
    return issues


def main() -> int:
    parser = argparse.ArgumentParser(description="验证 S01 忠实转录、纠错映射和文字单元时间轴。")
    parser.add_argument("transcript_dir", type=Path)
    parser.add_argument("--video-duration", type=float, required=True)
    parser.add_argument("--update-report", action="store_true", help="将验证结论回写到 s01-report.json")
    args = parser.parse_args()
    if args.video_duration <= 0:
        print("错误：video-duration 必须大于 0")
        return 2
    issues = validate(args.transcript_dir, args.video_duration)
    if args.update_report:
        report_path = args.transcript_dir / "s01-report.json"
        if report_path.is_file():
            report = json.loads(report_path.read_text(encoding="utf-8"))
            report["validation"] = {
                "status": "FAILED" if issues else "PASSED",
                "command": (
                    "scripts/s01_validate_transcript_alignment.py S01 "
                    f"--video-duration {args.video_duration:.6f} --update-report"
                ),
                "issue_count": len(issues),
            }
            report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if issues:
        print(f"S01 验证未通过，共 {len(issues)} 项：")
        for issue in issues:
            print(f"- {issue}")
        return 1
    print(f"S01 验证通过：{args.transcript_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
