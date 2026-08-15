# S02 — 语义转录与语义切割

## S02.1 — 接收上游产物

读取已经通过验证的 `<项目目录>/S01/text-unit-timeline.json`。S02 以其中按顺序排列的文字单元、来源追溯和视频绝对时间为唯一内容与时间输入。

连接全部文字单元的 `text` 得到忠实全文。先完整理解全文的主题、核心问题、论证路径和叙事推进，再作局部判断。

## S02.2 — 建立语义转录

在文字单元边界插入必要标点，据此组织句子和段落。标点、句子和段落由全文语义决定；原始文字单元的内容、顺序和书写形式保持不变。

生成 `<项目目录>/S02/semantic-transcript.json`：

- `full_verbatim_text` 是 S01 全部文字单元的直接连接；
- `full_semantic_text` 只增加标点和段落；
- 每个句子使用连续 `sentence_id`，记录段落、文字、时间、来源文字单元范围和插入标点；
- 每个段落使用连续 `paragraph_id`，记录连续句子范围及段落文字；
- 句子时间完整继承其首尾来源文字单元的时间包络。

## S02.3 — 划分语义块

完整读取 [视频语义切割第一性原理](semantic-segmentation-principles.md)，根据主要认知任务及必要依赖划分语义块。

语义块边界直接锚定在 S01 文字单元之间，不受句子和段落边界限制。每个语义块记录：

- 连续 `block_id`；
- 便于识别内容的 `title`；
- 当前内容在全文中的 `semantic_role`；
- 观众在该块完成后新增的唯一主要理解 `cognitive_goal`；
- 该块结束边界成立的 `boundary_reason`；
- 视频绝对时间、来源文字单元范围、忠实文字和带标点语义文字。

最后一个语义块的 `boundary_reason` 使用 `END_OF_TRANSCRIPT`。S02 只判断语义结构，不生成视觉表达候选或动画意图。

生成机器草稿 `<项目目录>/S02/semantic-blocks.json`。该文件必须进入人工审批，不得直接作为后续流程输入。

## S02.4 — 确定性构建

大模型在理解全文后只提供两类语义决定：

1. 在哪些 `unit_id` 后插入什么标点，以及是否结束段落；
2. 每个语义块结束于哪个 `unit_id`，以及该块的标题、语义角色、认知目标和边界理由。

将决定写入临时 JSON：

```json
{
  "punctuation_decisions": [
    {
      "after_unit_id": "unit-000010",
      "punctuation": "。",
      "paragraph_break_after": true
    }
  ],
  "block_decisions": [
    {
      "end_unit_id": "unit-000010",
      "title": "开场问题",
      "semantic_role": "提出核心问题",
      "cognitive_goal": "观众明确本段要回答的问题",
      "boundary_reason": "END_OF_TRANSCRIPT"
    }
  ]
}
```

运行：

```text
<python> scripts/s02_semantic_pipeline.py build <项目目录>/S01/text-unit-timeline.json <临时决定.json> <项目目录>/S02
```

脚本负责生成连续 ID、来源范围、时间、忠实文字、带标点文字、来源哈希和两个可验证 JSON。其中 `semantic-transcript.json` 是正式语义转录，`semantic-blocks.json` 是待审批的机器分块草稿。

## S02.5 — 人工审批语义块

机器草稿验证通过后，完整读取 [S02 语义块审批工具](s02-block-approval.md)，在项目 S02 目录安装不含项目数据的通用审批页。以下命令会自动创建或更新 `<项目目录>/S02/semantic-blocks-review.html`：

```text
<python> scripts/s02_block_review.py prepare <项目目录>/S01/text-unit-timeline.json <项目目录>/S02/semantic-transcript.json <项目目录>/S02/semantic-blocks.json <项目目录>/S02/semantic-blocks-approved.json --open-browser
```

用户直接打开项目内 `semantic-blocks-review.html`，选择包含 S01 和 S02 的项目根目录。页面实时读取并验证当前项目的 `S01/text-unit-timeline.json`、`S02/semantic-transcript.json` 和最新 `S02/semantic-blocks.json`，不自动载入已有批准文件。用户检查全文分块，按需修改标题、语义角色、认知目标和结束理由，也可调整边界、拆分或合并语义块；“存档”始终可用，无需逐块确认。页面使用已经授权的项目目录直接覆盖固定文件 `<项目目录>/S02/semantic-blocks-approved.json`，不得覆盖 `semantic-blocks.json`。“重新加载草稿”重新读取磁盘上的三个正式输入；机器草稿变化后不需要重新运行 `prepare`。Import 可选择同结构分块 JSON，导入前必须验证边界完整覆盖当前项目，并在来源哈希存在时核对当前 S01。

审批页是不包含项目内容的通用本地 HTML，不依赖 HTTP 服务。页面从用户授权的项目目录读取 S01 文字单元、语义标点、机器草稿和来源哈希，按用户决定重新计算连续 ID、时间、来源范围、忠实文字与带标点文字并生成批准 JSON；随后必须由 Python 验证器重新读取实际落盘文件，独立确认全部派生字段和来源哈希。

`semantic-blocks.json` 保留为机器草稿和审批来源；`semantic-blocks-approved.json` 是后续流程唯一允许读取的语义块文件。

## S02.6 — 验证并完成 S02

运行：

```text
<python> scripts/s02_semantic_pipeline.py validate <项目目录>/S01/text-unit-timeline.json <项目目录>/S02/semantic-transcript.json <项目目录>/S02/semantic-blocks.json
<python> scripts/s02_block_review.py validate <项目目录>/S01/text-unit-timeline.json <项目目录>/S02/semantic-transcript.json <项目目录>/S02/semantic-blocks.json <项目目录>/S02/semantic-blocks-approved.json
```

验证器必须确认：

- 语义转录、机器草稿和批准文件的来源文件与 SHA-256 匹配；
- 句子按顺序完整且唯一覆盖全部 S01 文字单元；
- 语义块独立按顺序完整且唯一覆盖全部 S01 文字单元；
- 忠实文字与来源单元逐字一致，语义文字只增加已记录的标点；
- 句子、段落和语义块 ID 连续，来源范围与时间包络一致；
- 每个语义块都有标题、语义角色、认知目标和边界理由；
- 机器草稿与批准文件的语义块都满足上述结构约束；
- 批准文件引用的机器草稿 SHA-256 匹配，`approval.status=APPROVED`；
- 三个产物的最终验证状态均为 `PASSED`，且 `issue_count=0`。

两个验证器都通过时 S02 完成。后续阶段读取 `semantic-transcript.json` 与 `semantic-blocks-approved.json`，不得读取 `semantic-blocks.json` 作为正式语义块。
