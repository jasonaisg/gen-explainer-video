# S01 — 音频提取、忠实转录与文字单元时间轴

## S01.1 — 接收并检查输入

接收两个必需输入：

1. 剪辑完成的口播视频；
2. 与该视频内容匹配的 UTF-8 参考文稿。

确认视频可解码且含音轨，记录视频时长、音频起点、采样率和声道。参考文稿只能辅助核对同一发音对应的写法，不能证明某段内容已在视频中说出。

| 事项 | 权威 |
|---|---|
| 是否实际出现、出现顺序、占用时间 | 视频音频 |
| 带时间的初始文字骨架和原生书写形式 | ASR |
| 同音错字、专名的局部核对 | 参考文稿辅助判断 |
| 数字、百分比、日期、金额等语义解释 | 后续语义阶段，不属于 S01 |

不得修改、裁剪、重排或变速输入视频。

S01 必须恰好产生并保留以下七类正式文件：

| 文件 | 必要性与使用方 |
|---|---|
| `audio/extracted-audio.mp3` | S01 用于 ASR；后续剪辑流程复用独立音轨 |
| `audio/extraction-report.json` | 证明 MP3 与输入视频音轨的起点和时长一致 |
| `asr-raw/engine-output.json` | 保留 ASR 引擎未经修改的原始证据 |
| `raw-asr.json` | 保存从原始 token 确定性生成的原始文字单元、时间和置信度 |
| `correction-map.json` | 证明每个原始文字单元只经过 `KEEP/REPLACE` |
| `text-unit-timeline.json` | 后续语义分析和动效流程使用的校对后文字单元时间底座 |
| `s01-report.json` | 记录输入、统计、待确认项和最终验证结论 |

废弃的 `character-timeline.json` 不得保留在正式 S01 目录中。

## S01.2 — 从视频提取 MP3

运行：

```text
<python> scripts/s01_extract_audio.py <输入视频> <项目目录>/S01/audio/extracted-audio.mp3
```

脚本调用本机已验证的 FFmpeg/FFprobe，完整提取视频音轨并验证：

- 输出起点与输入音轨一致；
- 输出时长与输入音轨在报告容差内；
- 不使用 `-ss`、`-t`、变速、降噪或静默裁剪；
- 输出 MP3 是正式产物；后续时间继续使用视频绝对时间。

若视频没有音轨、媒体不可解码或时长核对失败，停止 S01。

## S01.3 — 执行带 token 时间证据的 ASR

对 `extracted-audio.mp3` 执行本机可用的中文 ASR。将未经修改的引擎结果保存为 `<项目目录>/S01/asr-raw/engine-output.json`，不用参考文稿提示模型重写口述。

S01 只读取 ASR 原生可见 token 和它们的时间区间，不另做数字、百分比、金额、日期或缩写的二次语义识别。原始引擎已经输出 `20%`、`CRS` 或 `GPT-5` 时，保留这种表面形式。

将 ASR 输出规范化为 `<项目目录>/S01/raw-asr.json`：

```json
{
  "raw_unit_id": "raw-unit-000001",
  "text": "20%",
  "kind": "percentage",
  "start": 2.060,
  "end": 2.590,
  "confidence": 0.99,
  "source_token_ids": ["token-0001-0001", "token-0001-0002"],
  "timing_method": "SOURCE_TOKEN_ENVELOPE"
}
```

原始时间来自 whisper.cpp token：单 token 内多个汉字只能按 token 区间比例拆分，并明确标为 `TOKEN_PROPORTIONAL_SPLIT`；合并单元取第一来源 token 的开始和最后来源 token 的结束。不得覆盖或修改 `engine-output.json`。

## S01.4 — 生成文字单元

按以下确定性规则扫描连续可见文字：

| 输入形态 | 正式单元 | `kind` |
|---|---|---|
| `中 国`（相邻汉字） | `中`、`国` | `han` |
| `2026` | `2026` | `number` |
| `20%`、`3.5%` | 各自一个整体 | `percentage` |
| `CRS`、`OpenAI` | 各自一个整体 | `english` |
| `GPT-5`、`T+1`、`B2B`、`C919`、`v2.0` | 各自一个整体 | `alphanumeric` |
| `，`、`、`、`。`、`！` 等推断标点 | 排除 | 不进入有声时间轴 |

边界规则：

- token 内部和相邻 token 之间没有空白或硬边界时，可以合并；
- ASR 原始 token 的空白必须被保留为分组边界，`Common Reporting Standard` 是三个英文单元，不得合并成一个；
- 相邻 segment 间只有在无空白且 token 间隔不超过 `0.12s` 时才允许继续合并，以处理被切断的连续表达；
- `%/‰/‱` 只在紧随数字时作为后缀并入；小数点、千位逗号、连接号、斜线、加号等只在表达内部两侧都有字母或数字时并入；
- 任何合并都必须保留全部 `source_token_ids`，时间是这些来源的完整包络，不把总时间平均压缩到单个字符。

`20%` 的时间必须覆盖原始 `20` token 开始到 `%` token 结束；`CR` 与 `S` 连续时生成一个 `CRS`，其时间覆盖两个 token 的完整区间。

## S01.5 — 比对并只执行 KEEP/REPLACE

先审核需要纠正的局部片段，再运行：

```text
<python> scripts/s01_build_outputs.py <项目目录>/S01/asr-raw/engine-output.json <参考文稿> <输入视频> <项目目录>/S01 \
  --replace <原识别片段>=<纠正片段>
```

可以重复传入 `--replace`。脚本会纠正该原片段的全部已审核匹配；未列出的文字单元全部生成 `KEEP`。纠正结果必须能在参考文稿中找到，并且替换来源必须落在完整文字单元边界。

允许 `REPLACE` 的范围是同一发音能直接支持的错字、同音字和专有名词。禁止在 S01 把“百分之二十”与 `20%`、中文数字与阿拉伯数字、缩写与全称互相转换；这些属于后续语义层。

在 `correction-map.json` 中：

- 每个原始 `raw_unit_id` 必须被一个且仅一个 `source_unit_ids` 引用；
- `KEEP` 必须保持表面文字不变；
- `REPLACE` 可以覆盖连续的多个原始文字单元，但结果只能继承同一来源时间包络；
- 禁止 `INSERT` 和 `DELETE`；参考稿独有内容不得补入，ASR 独有内容使用 `KEEP`。

## S01.6 — 生成正式文字单元时间轴

按映射顺序连接 `KEEP/REPLACE` 结果，使用 [文字单元时间轴模板](../assets/templates/s01/text-unit-timeline-template.json) 生成 `<项目目录>/S01/text-unit-timeline.json`。

每个最终单元至少包含：

- 连续的 `unit_id`；
- `text` 和 `kind`；
- `start/end` 视频绝对时间；
- 一个或多个 `source_unit_ids`；
- `mapping_id`、`KEEP/REPLACE`、`source_asr_text` 和 `timing_method`。

按顺序连接全部 `text`，就是 S01 唯一的校对后无标点全文。S01 不另造一份显示层文字稿。语气词、助词、重复、口头连接词和参考稿外的临场补充全部保留。

## S01.7 — 验证并完成 S01

运行：

```text
<python> scripts/s01_validate_transcript_alignment.py <项目目录>/S01 --video-duration <秒> --update-report
```

验证器必须确认：

- v2.0 三个 JSON schema 和七类正式产物存在，遗留 `character-timeline.json` 不存在；
- 原始文字单元 ID 唯一，种类、来源 token、时间合法且单调；
- 映射操作只有 `KEEP/REPLACE`，并完整且唯一覆盖全部原始文字单元；
- 最终文字单元全部可追溯，时间不超出来源包络且完整继承包络；
- `text-unit-timeline.json` 全文等于 `correction-map.json` 的全部结果；
- 没有未解决的纠错决定。

将输入、提取结果、ASR 引擎、各类单元数量、各时间生成方法数量、排除的推断标点数量、纠错数量和验证结论写入 `s01-report.json`。验证通过且待确认项为零时，S01 才完成。
