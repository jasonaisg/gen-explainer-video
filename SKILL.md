---
name: gen-explainer-video
description: 从剪辑完成的中文口播视频和匹配参考文稿出发，生成带可追溯文字单元时间戳的忠实转录，并在全文理解基础上建立语义转录和语义块。用于开发或执行 gen-explainer-video 科普讲解视频生成流程；当前已定义 S01 转录与对齐、S02 语义切割阶段，后续阶段按用户要求增量加入。
---

# 科普讲解视频生成器

将剪辑完成的口播视频逐步转化为与真实口述同步的完整科普讲解视频。当前已定义 `S01` 和 `S02`。

## 全局契约

- 所有时间相关流程以剪辑完成的视频时间轴为统一时间基准。
- 每个流程只产生并保留本流程执行或下游流程消费所必需的文件。
- 各流程读取已经验证通过的上游正式产物作为输入。
- 视频合成与动画使用 HyperFrames。

## S01 — 音频提取、忠实转录与文字单元时间轴

从输入视频完整提取并保留 MP3，对 MP3 执行带 token 时间证据的语音识别，以参考文稿辅助局部错字核对，并生成可追溯的纠错映射和全篇文字单元时间轴。

### S01 输入与边界

- 接收两个必需输入：剪辑完成的口播视频、与其匹配的参考文稿。
- 将视频中的实际音频视为内容是否出现、出现顺序和占用时间的权威。
- 将 ASR 原生文字作为最终文字骨架；参考文稿只辅助纠正能够由同一发音直接确认的错字、同音字和专有名词。
- 保留全部实际口述，包括参考稿没有的语气词、助词、重复和临场补充；参考稿独有内容不得补入。
- 保留 ASR 原生书写形式；数字、日期、金额、单位及缩写的语义归一化属于后续阶段。

执行 S01 前必须完整读取 [S01 详细规范](references/s01-transcription-and-alignment.md)，并严格按 `S01.1` 至 `S01.7` 的顺序执行。

必须产生并保留的产物：

- `<项目目录>/S01/audio/extracted-audio.mp3`
- `<项目目录>/S01/audio/extraction-report.json`
- `<项目目录>/S01/asr-raw/engine-output.json`
- `<项目目录>/S01/raw-asr.json`
- `<项目目录>/S01/correction-map.json`
- `<项目目录>/S01/text-unit-timeline.json`
- `<项目目录>/S01/s01-report.json`

确定性工具：

- 使用 `scripts/s01_extract_audio.py` 提取并核对 MP3。
- 使用 `scripts/s01_build_outputs.py` 从保留的 whisper.cpp 原始 JSON 和人工确认的局部替换生成审计产物。
- 使用 `scripts/s01_validate_transcript_alignment.py --update-report` 验证必需产物、纠错覆盖、文字单元追溯、时间单调和最终全文，并回写验证结论。

只有验证器通过且没有待确认的文字纠错时，才能宣布 S01 完成。

## S02 — 语义转录与语义切割

从已经验证的 S01 文字单元时间轴恢复忠实全文，在理解全文后补充标点、句子和段落，并按认知任务将全部口述切分为可追溯的语义块。

### S02 输入与边界

- 只读取 `<项目目录>/S01/text-unit-timeline.json` 作为内容、顺序、追溯和时间输入。
- `semantic-transcript.json` 只在 S01 忠实全文中增加标点和段落，不改变原始文字。
- 语义块直接锚定 S01 文字单元边界，由认知任务和必要依赖决定，不要求与句子或段落一一对应。
- S02 只建立语义结构，不生成视觉表达候选或动画意图。

执行 S02 前必须完整读取 [S02 详细规范](references/s02-semantic-segmentation.md)，并严格按 `S02.1` 至 `S02.6` 的顺序执行。

必须产生并保留的产物：

- `<项目目录>/S02/semantic-transcript.json`
- `<项目目录>/S02/semantic-blocks.json`
- `<项目目录>/S02/semantic-blocks-review.html`
- `<项目目录>/S02/semantic-blocks-approved.json`

使用 `scripts/s02_semantic_pipeline.py` 确定性生成并验证语义转录与机器分块草稿；随后使用 `scripts/s02_block_review.py prepare` 在项目 S02 目录安装通用 `semantic-blocks-review.html`。该 HTML 不嵌入项目数据；用户打开后选择包含 S01 和 S02 的项目根目录，页面实时读取并验证 `text-unit-timeline.json`、`semantic-transcript.json` 和最新 `semantic-blocks.json`。页面始终以机器草稿为编辑起点，不要求逐块确认；“存档”始终可用，并使用已授权项目中的 S02 目录直接创建或覆盖固定文件名 `semantic-blocks-approved.json`，且不得覆盖 `semantic-blocks.json`。页面允许 Import 同结构分块 JSON，但必须以当前项目文字单元重新生成派生字段。批准文件是后续流程唯一允许读取的语义块文件。只有其来源哈希匹配且独立验证通过时，才能宣布 S02 完成。

## 按需参考资料

需要选择或校验视觉表达类型、设计动效方案或维护视觉表达词典时，读取 [科普视频视觉表达 Taxonomy](references/visual-expression-taxonomy.md)。

需要为 `1080×1920` 竖屏项目配置或校验安全区和字幕区时，按目标平台读取并复用对应模板：[微信视频号](assets/templates/platforms/wechat-channels-vertical-safe-area.json)、[抖音](assets/templates/platforms/douyin-vertical-safe-area.json)或[小红书](assets/templates/platforms/xiaohongshu-vertical-safe-area.json)，同时遵守 [生产与安全区规范](references/production-spec.md)。
