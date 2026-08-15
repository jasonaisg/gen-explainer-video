#!/usr/bin/env python3
"""Validate the minimum executable structure of a V2 motion script."""

from __future__ import annotations

import re
import sys
from pathlib import Path


GLOBAL_HEADINGS = ["项目边界", "输出规格", "场景索引", "脚本级 QA 状态"]
SCENE_FIELDS = [
    "对应口播与绝对时间",
    "认知任务",
    "屏幕文字",
    "画面与构图",
    "人物呈现",
    "元素级动画",
    "相邻转场",
    "三个审阅状态",
    "输出与事实引用",
]
PLACEHOLDERS = ("[填写]", "待填写", "[场景标题]")
TIME_RANGE = re.compile(r"(?P<start>\d+(?:\.\d+)?)\s*(?:-|—|–|至)\s*(?P<end>\d+(?:\.\d+)?)")
SCENE_HEADING = re.compile(r"(?m)^##\s+(A\d{2,})｜([^\n]+)$")


def scene_blocks(text: str) -> list[tuple[str, str]]:
    matches = list(SCENE_HEADING.finditer(text))
    blocks: list[tuple[str, str]] = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        blocks.append((match.group(1), text[match.start():end]))
    return blocks


def field_body(block: str, field: str) -> str | None:
    pattern = re.compile(
        rf"(?ms)^\*\*{re.escape(field)}\*\*\s*(.*?)(?=^\*\*[^\n]+\*\*|^##\s+|\Z)"
    )
    match = pattern.search(block)
    return match.group(1).strip() if match else None


def validate(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    issues: list[str] = []

    for heading in GLOBAL_HEADINGS:
        if not re.search(rf"(?m)^##\s+{re.escape(heading)}\s*$", text):
            issues.append(f"全局缺少二级标题：{heading}")

    blocks = scene_blocks(text)
    if not blocks:
        issues.append("没有找到格式为“## A01｜标题”的场景")
        return issues

    actual = [scene_id for scene_id, _ in blocks]
    expected = [f"A{i:02d}" for i in range(1, len(blocks) + 1)]
    if actual != expected:
        issues.append(f"场景编号不连续：实际 {actual}，预期 {expected}")

    for scene_id, block in blocks:
        for field in SCENE_FIELDS:
            body = field_body(block, field)
            if body is None:
                issues.append(f"{scene_id} 缺少字段：{field}")
            elif not body or any(marker in body for marker in PLACEHOLDERS):
                issues.append(f"{scene_id} 字段未完成：{field}")

        time_field = field_body(block, "对应口播与绝对时间") or ""
        match = TIME_RANGE.search(time_field)
        if not match:
            issues.append(f"{scene_id} 缺少可解析的绝对时间范围")
        elif float(match.group("end")) <= float(match.group("start")):
            issues.append(f"{scene_id} 绝对结束时间必须大于开始时间")

        fact_field = field_body(block, "输出与事实引用") or ""
        if not re.search(r"\bF\d{2,}\b", fact_field):
            issues.append(f"{scene_id} 缺少事实锁定项引用")

    for line_number, line in enumerate(text.splitlines(), start=1):
        if re.search(r"\d\s+(?:%|元|万|万元|岁|天|年)", line):
            issues.append(f"第 {line_number} 行：数字和单位之间存在异常空格")

    return issues


def main() -> int:
    if len(sys.argv) != 2:
        print("用法：validate_motion_script.py <逐场景动效脚本.md>")
        return 2

    path = Path(sys.argv[1])
    if not path.is_file():
        print(f"错误：文件不存在：{path}")
        return 2

    issues = validate(path)
    if issues:
        print(f"脚本检查未通过，共 {len(issues)} 项：")
        for issue in issues:
            print(f"- {issue}")
        return 1

    print(f"脚本结构检查通过：{path}")
    print("提示：仍需完成脚本级内容 QA 和真实渲染检查。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
