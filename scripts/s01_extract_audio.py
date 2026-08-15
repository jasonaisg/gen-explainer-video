#!/usr/bin/env python3
"""Extract the complete first audio stream from a spoken video as MP3."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


def run(command: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, check=False, text=True, capture_output=True, encoding="utf-8")


def probe(ffprobe: str, path: Path) -> dict:
    result = run([
        ffprobe,
        "-v", "error",
        "-show_entries", "format=duration,start_time:stream=index,codec_type,codec_name,start_time,duration,sample_rate,channels",
        "-of", "json",
        str(path),
    ])
    if result.returncode != 0:
        raise RuntimeError(f"FFprobe 失败：{result.stderr.strip()}")
    return json.loads(result.stdout)


def first_audio_stream(data: dict) -> dict | None:
    return next((stream for stream in data.get("streams", []) if stream.get("codec_type") == "audio"), None)


def number(value: object, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def main() -> int:
    parser = argparse.ArgumentParser(description="从剪辑完成的视频完整提取第一条音轨为 MP3。")
    parser.add_argument("input_video", type=Path)
    parser.add_argument("output_mp3", type=Path)
    parser.add_argument("--ffmpeg", default="ffmpeg", help="FFmpeg 命令或完整路径")
    parser.add_argument("--ffprobe", default="ffprobe", help="FFprobe 命令或完整路径")
    parser.add_argument("--duration-tolerance", type=float, default=0.15, help="允许的音轨时长差，单位秒")
    parser.add_argument("--report", type=Path, help="报告路径；默认在 MP3 旁生成 .report.json")
    args = parser.parse_args()

    if not args.input_video.is_file():
        print(f"错误：输入视频不存在：{args.input_video}")
        return 2
    if args.duration_tolerance < 0:
        print("错误：时长容差不能为负数")
        return 2
    for executable in (args.ffmpeg, args.ffprobe):
        if Path(executable).is_file() or shutil.which(executable):
            continue
        print(f"错误：找不到命令：{executable}")
        return 2

    try:
        input_probe = probe(args.ffprobe, args.input_video)
    except (RuntimeError, json.JSONDecodeError) as exc:
        print(f"错误：{exc}")
        return 1
    input_audio = first_audio_stream(input_probe)
    if input_audio is None:
        print("错误：输入视频没有音轨")
        return 1

    args.output_mp3.parent.mkdir(parents=True, exist_ok=True)
    command = [
        args.ffmpeg,
        "-hide_banner", "-loglevel", "error", "-y",
        "-i", str(args.input_video),
        "-map", "0:a:0", "-vn", "-sn", "-dn",
        "-c:a", "libmp3lame", "-q:a", "2",
        "-map_metadata", "-1",
        str(args.output_mp3),
    ]
    result = run(command)
    if result.returncode != 0:
        print(f"错误：FFmpeg 提取失败：{result.stderr.strip()}")
        return 1

    try:
        output_probe = probe(args.ffprobe, args.output_mp3)
    except (RuntimeError, json.JSONDecodeError) as exc:
        print(f"错误：{exc}")
        return 1
    output_audio = first_audio_stream(output_probe)
    if output_audio is None:
        print("错误：输出 MP3 没有可识别音轨")
        return 1

    input_duration = number(input_audio.get("duration"), number(input_probe.get("format", {}).get("duration")))
    output_duration = number(output_audio.get("duration"), number(output_probe.get("format", {}).get("duration")))
    duration_delta = abs(output_duration - input_duration)
    passed = duration_delta <= args.duration_tolerance
    report_path = args.report or args.output_mp3.parent / "extraction-report.json"
    report = {
        "schema_version": "1.0",
        "stage": "S01",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "input_video": str(args.input_video.resolve()),
        "output_mp3": str(args.output_mp3.resolve()),
        "time_contract": {
            "canonical_timebase": "INPUT_VIDEO_ABSOLUTE_SECONDS",
            "source_audio_start_seconds": number(input_audio.get("start_time")),
            "mp3_container_start_seconds": number(output_audio.get("start_time")),
            "note": "MP3 编码器延迟不改变后续时间权威；ASR 时间必须映射回输入视频绝对时间。",
        },
        "input_audio": input_audio,
        "output_audio": output_audio,
        "input_duration_seconds": input_duration,
        "output_duration_seconds": output_duration,
        "duration_delta_seconds": duration_delta,
        "duration_tolerance_seconds": args.duration_tolerance,
        "status": "PASS" if passed else "FAIL",
    }
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    if not passed:
        print(f"音频提取核对失败：时长差 {duration_delta:.6f}s，报告：{report_path}")
        return 1
    print(f"音频提取通过：{args.output_mp3}")
    print(f"时长差：{duration_delta:.6f}s；报告：{report_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
