#!/usr/bin/env python3
"""Install the generic S02 review page and validate approved artifacts."""

from __future__ import annotations

import argparse
import json
import webbrowser
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from s02_semantic_pipeline import (
    SCHEMA_VERSION,
    load_units,
    read_json,
    semantic_span,
    sha256_file,
    source_range,
    unit_index,
    validate_artifacts,
    verbatim_span,
    write_json,
)


TOOL_VERSION = "1.1.0"
DEFAULT_OUTPUT_NAME = "semantic-blocks-approved.json"
PROJECT_HTML_NAME = "semantic-blocks-review.html"
HTML_PATH = Path(__file__).resolve().parent.parent / "assets" / "tools" / "s02-block-review.html"


def ensure_output_contract(draft_path: Path, approved_path: Path) -> None:
    if approved_path.name != DEFAULT_OUTPUT_NAME:
        raise ValueError(f"批准文件名必须固定为 {DEFAULT_OUTPUT_NAME}")
    if draft_path.resolve() == approved_path.resolve():
        raise ValueError("批准文件不得覆盖 semantic-blocks.json")


def punctuation_map(transcript: dict[str, Any], unit_count: int) -> dict[int, str]:
    result: dict[int, str] = {}
    sentences = transcript.get("sentences")
    if not isinstance(sentences, list):
        raise ValueError("semantic-transcript.json 缺少 sentences")
    for sentence in sentences:
        inserted = sentence.get("inserted_punctuation") if isinstance(sentence, dict) else None
        if not isinstance(inserted, list):
            raise ValueError("semantic-transcript.json 的 inserted_punctuation 非法")
        for item in inserted:
            if not isinstance(item, dict) or not isinstance(item.get("punctuation"), str):
                raise ValueError("semantic-transcript.json 包含非法标点记录")
            index = unit_index(item.get("after_unit_id"), unit_count)
            if index in result:
                raise ValueError(f"重复的标点锚点：{item.get('after_unit_id')}")
            result[index] = item["punctuation"]
    return result


def materialize_review_html(output_dir: Path) -> Path:
    """Install the generic review page without embedding project data."""
    if not HTML_PATH.exists():
        raise ValueError(f"找不到 Skill 审批页面母版：{HTML_PATH}")
    html_bytes = HTML_PATH.read_bytes()
    output_dir.mkdir(parents=True, exist_ok=True)
    target = output_dir / PROJECT_HTML_NAME
    if target.exists() and target.read_bytes() == html_bytes:
        return target
    temporary = output_dir / f"{PROJECT_HTML_NAME}.tmp"
    temporary.write_bytes(html_bytes)
    temporary.replace(target)
    return target


def editable_blocks(block_doc: dict[str, Any], units: list[dict[str, Any]]) -> list[dict[str, Any]]:
    blocks = block_doc.get("blocks")
    if not isinstance(blocks, list) or not blocks:
        raise ValueError("semantic-blocks.json 缺少 blocks")
    result: list[dict[str, Any]] = []
    for block in blocks:
        if not isinstance(block, dict):
            raise ValueError("semantic-blocks.json 包含非法 block")
        end_index = unit_index(
            block.get("source_unit_range", {}).get("end_unit_id")
            if isinstance(block.get("source_unit_range"), dict)
            else None,
            len(units),
        )
        result.append(
            {
                "title": block.get("title", ""),
                "semantic_role": block.get("semantic_role", ""),
                "cognitive_goal": block.get("cognitive_goal", ""),
                "boundary_reason": block.get("boundary_reason", ""),
                "end_unit_id": units[end_index]["unit_id"],
            }
        )
    return result


def review_payload(
    timeline_path: Path,
    transcript_path: Path,
    draft_path: Path,
    approved_path: Path,
) -> dict[str, Any]:
    ensure_output_contract(draft_path, approved_path)
    _, units = load_units(timeline_path)
    transcript = read_json(transcript_path)
    draft = read_json(draft_path)
    issues = validate_artifacts(timeline_path, transcript_path, draft_path)
    if issues:
        raise ValueError("S02 草稿未通过验证：\n- " + "\n- ".join(issues))

    punctuation = punctuation_map(transcript, len(units))
    return {
        "tool_version": TOOL_VERSION,
        "project_name": approved_path.parent.parent.name,
        "source_kind": "draft",
        "output_file": str(approved_path),
        "output_name": approved_path.name,
        "output_exists": approved_path.exists(),
        "review_html": str(approved_path.parent / PROJECT_HTML_NAME),
        "artifact_sources": {
            "text_unit_timeline": {
                "file": "../S01/text-unit-timeline.json",
                "schema_version": "2.0",
                "sha256": sha256_file(timeline_path),
                "unit_count": len(units),
            },
            "semantic_transcript": {
                "file": transcript_path.name,
                "schema_version": SCHEMA_VERSION,
                "sha256": sha256_file(transcript_path),
            },
            "semantic_blocks_draft": {
                "file": draft_path.name,
                "schema_version": SCHEMA_VERSION,
                "sha256": sha256_file(draft_path),
            },
        },
        "draft_sha256": sha256_file(draft_path),
        "units": [
            {
                "unit_id": unit["unit_id"],
                "text": unit["text"],
                "start": unit["start"],
                "end": unit["end"],
            }
            for unit in units
        ],
        "punctuation": {str(index): value for index, value in punctuation.items()},
        "blocks": editable_blocks(draft, units),
        "draft_blocks": editable_blocks(draft, units),
    }


def normalize_decision(block: dict[str, Any]) -> tuple[str, str, str, str, str]:
    return tuple(
        str(block.get(key, "")).strip()
        for key in (
            "title",
            "semantic_role",
            "cognitive_goal",
            "boundary_reason",
            "end_unit_id",
        )
    )  # type: ignore[return-value]


def build_approved_document(
    timeline_path: Path,
    transcript_path: Path,
    draft_path: Path,
    submitted: object,
    reviewer_note: object,
) -> dict[str, Any]:
    _, units = load_units(timeline_path)
    transcript = read_json(transcript_path)
    draft = read_json(draft_path)
    draft_issues = validate_artifacts(timeline_path, transcript_path, draft_path)
    if draft_issues:
        raise ValueError("S02 草稿未通过验证：\n- " + "\n- ".join(draft_issues))
    if not isinstance(submitted, list) or not submitted:
        raise ValueError("审批结果必须包含至少一个语义块")

    punctuation = punctuation_map(transcript, len(units))
    approved_blocks: list[dict[str, Any]] = []
    decisions: list[dict[str, Any]] = []
    block_start = 0
    for number, item in enumerate(submitted, start=1):
        if not isinstance(item, dict):
            raise ValueError(f"第 {number} 个审批块必须是对象")
        clean: dict[str, Any] = {}
        for key in ("title", "semantic_role", "cognitive_goal", "boundary_reason"):
            value = item.get(key)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"第 {number} 个语义块缺少 {key}")
            clean[key] = value.strip()
        block_end = unit_index(item.get("end_unit_id"), len(units))
        if block_end < block_start:
            raise ValueError("语义块边界必须递增且每块至少包含一个文字单元")
        clean["end_unit_id"] = units[block_end]["unit_id"]
        decisions.append(clean)
        approved_blocks.append(
            {
                "block_id": f"block-{number:03d}",
                "title": clean["title"],
                "semantic_role": clean["semantic_role"],
                "cognitive_goal": clean["cognitive_goal"],
                "boundary_reason": clean["boundary_reason"],
                "start": round(float(units[block_start]["start"]), 6),
                "end": round(float(units[block_end]["end"]), 6),
                "source_unit_range": source_range(units, block_start, block_end),
                "verbatim_text": verbatim_span(units, block_start, block_end),
                "semantic_text": semantic_span(units, block_start, block_end, punctuation),
            }
        )
        block_start = block_end + 1

    if block_start != len(units):
        raise ValueError("审批后的语义块没有完整覆盖 S01 全文")
    if approved_blocks[-1]["boundary_reason"] != "END_OF_TRANSCRIPT":
        raise ValueError("最后一个语义块的 boundary_reason 必须是 END_OF_TRANSCRIPT")

    original = editable_blocks(draft, units)
    original_signatures = [normalize_decision(item) for item in original]
    approved_signatures = [normalize_decision(item) for item in decisions]
    change_count = sum(
        1
        for index in range(max(len(original_signatures), len(approved_signatures)))
        if index >= len(original_signatures)
        or index >= len(approved_signatures)
        or original_signatures[index] != approved_signatures[index]
    )
    note = reviewer_note.strip() if isinstance(reviewer_note, str) else ""
    return {
        "schema_version": SCHEMA_VERSION,
        "stage": "S02",
        "timebase": "INPUT_VIDEO_ABSOLUTE_SECONDS",
        "sources": {
            "text_unit_timeline": {
                "file": "../S01/text-unit-timeline.json",
                "schema_version": "2.0",
                "sha256": sha256_file(timeline_path),
                "unit_count": len(units),
            },
            "semantic_transcript": {
                "file": "semantic-transcript.json",
                "schema_version": SCHEMA_VERSION,
                "sha256": sha256_file(transcript_path),
            },
            "semantic_blocks_draft": {
                "file": draft_path.name,
                "schema_version": SCHEMA_VERSION,
                "sha256": sha256_file(draft_path),
            },
        },
        "approval": {
            "status": "APPROVED",
            "approved_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            "tool": "s02_block_review.py",
            "tool_version": TOOL_VERSION,
            "reviewed_block_count": len(approved_blocks),
            "change_count": change_count,
            "reviewer_note": note,
        },
        "blocks": approved_blocks,
        "validation": {
            "status": "PENDING",
            "issue_count": None,
            "source_units_covered": len(units),
            "source_units_total": len(units),
        },
    }


def validate_approved(
    timeline_path: Path,
    transcript_path: Path,
    draft_path: Path,
    approved_path: Path,
    require_passed: bool = True,
) -> list[str]:
    issues = validate_artifacts(
        timeline_path, transcript_path, approved_path, require_passed=require_passed
    )
    try:
        approved = read_json(approved_path)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        return issues + [str(error)]
    source = approved.get("sources", {}).get("semantic_blocks_draft")
    if not isinstance(source, dict) or source.get("sha256") != sha256_file(draft_path):
        issues.append("批准文件的 semantic-blocks 草稿来源哈希不匹配")
    approval = approved.get("approval")
    if not isinstance(approval, dict) or approval.get("status") != "APPROVED":
        issues.append("批准文件缺少 APPROVED 审批状态")
    elif approval.get("reviewed_block_count") != len(approved.get("blocks", [])):
        issues.append("批准文件的审批块数量不一致")
    return issues


def save_approved(
    timeline_path: Path,
    transcript_path: Path,
    draft_path: Path,
    approved_path: Path,
    request: dict[str, Any],
) -> dict[str, Any]:
    ensure_output_contract(draft_path, approved_path)
    if approved_path.exists() and request.get("allow_overwrite") is not True:
        raise FileExistsError(f"目标已存在，需要明确确认覆盖：{approved_path}")
    document = build_approved_document(
        timeline_path,
        transcript_path,
        draft_path,
        request.get("blocks"),
        request.get("reviewer_note"),
    )
    approved_path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = approved_path.with_name(approved_path.name + ".tmp")
    write_json(temporary_path, document)
    issues = validate_approved(
        timeline_path,
        transcript_path,
        draft_path,
        temporary_path,
        require_passed=False,
    )
    if issues:
        temporary_path.unlink(missing_ok=True)
        raise ValueError("批准文件验证失败：\n- " + "\n- ".join(issues))
    document["validation"]["status"] = "PASSED"
    document["validation"]["issue_count"] = 0
    write_json(temporary_path, document)
    final_issues = validate_approved(
        timeline_path, transcript_path, draft_path, temporary_path
    )
    if final_issues:
        temporary_path.unlink(missing_ok=True)
        raise ValueError("批准文件最终验证失败：\n- " + "\n- ".join(final_issues))
    temporary_path.replace(approved_path)
    return {
        "status": "saved",
        "file": str(approved_path),
        "sha256": sha256_file(approved_path),
        "block_count": len(document["blocks"]),
        "change_count": document["approval"]["change_count"],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="S02 通用语义块 HTML 审批工具。")
    subparsers = parser.add_subparsers(dest="command", required=True)
    prepare_parser = subparsers.add_parser("prepare", help="安装可直接打开的通用审批页面")
    validate_parser = subparsers.add_parser("validate", help="验证批准后的最终文件")
    for child in (prepare_parser, validate_parser):
        child.add_argument("timeline", type=Path)
        child.add_argument("semantic_transcript", type=Path)
        child.add_argument("semantic_blocks_draft", type=Path)
        child.add_argument("semantic_blocks_approved", type=Path)
    prepare_parser.add_argument("--open-browser", action="store_true")
    args = parser.parse_args()
    try:
        ensure_output_contract(args.semantic_blocks_draft, args.semantic_blocks_approved)
        if args.command == "prepare":
            payload = review_payload(
                args.timeline,
                args.semantic_transcript,
                args.semantic_blocks_draft,
                args.semantic_blocks_approved,
            )
            target = materialize_review_html(args.semantic_blocks_approved.parent)
            print(
                json.dumps(
                    {
                        "review_html": str(target),
                        "output": str(args.semantic_blocks_approved),
                        "blocks": len(payload["blocks"]),
                    },
                    ensure_ascii=False,
                )
            )
            if args.open_browser:
                webbrowser.open(target.resolve().as_uri())
            return 0
        issues = validate_approved(
            args.timeline,
            args.semantic_transcript,
            args.semantic_blocks_draft,
            args.semantic_blocks_approved,
        )
        if issues:
            print("S02 批准文件验证失败：")
            for issue in issues:
                print(f"- {issue}")
            return 1
        print("S02 批准文件验证通过")
        return 0
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"错误：{error}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
