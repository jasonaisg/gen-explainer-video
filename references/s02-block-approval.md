# S02 语义块审批工具

## 目的与文件角色

审批器位于机器语义切割和后续视觉设计之间，用于让用户检查并修正机器分块。

- `semantic-blocks.json`：机器草稿，必须保留，用于审批溯源和差异统计；
- `semantic-blocks-review.html`：安装到客户项目 S02 输出目录的通用审批页面，不包含项目数据，是用户直接双击打开的审批入口；
- `semantic-blocks-approved.json`：用户批准后的最终语义块，是后续流程唯一允许读取的语义块文件；
- `assets/tools/s02-block-review.html`：Skill 内置审批页母版，不作为客户项目入口直接使用；
- `scripts/s02_block_review.py`：安装通用审批页并独立验证最终批准 JSON 的确定性工具。

## 启动

确保 S02 机器草稿已通过 `s02_semantic_pipeline.py validate`，再运行：

```text
<python> scripts/s02_block_review.py prepare <项目目录>/S01/text-unit-timeline.json <项目目录>/S02/semantic-transcript.json <项目目录>/S02/semantic-blocks.json <项目目录>/S02/semantic-blocks-approved.json --open-browser
```

`prepare` 必须先验证上游，再把通用 Skill 母版原子安装为 `<项目目录>/S02/semantic-blocks-review.html`。页面不包含项目数据；未使用 `--open-browser` 时直接双击该 HTML，随后选择包含 S01 和 S02 的项目根目录。页面不请求 API、不启动端口，也不依赖常驻进程。

Skill 母版与项目内页面使用相同通用逻辑。客户入口通常是项目 S02 目录中由 `prepare` 安装的页面；同一页面也可打开其他符合正式目录契约的项目。

## 审批操作

1. 打开页面后选择包含 `S01` 和 `S02` 的项目根目录；页面验证并读取三个正式输入；
2. 从左侧导航通览所有语义块及持续时间；
3. 在连续文稿中核对每块内容、语义角色、认知目标与结束理由；
4. 通过块间分界线移动边界；需要时拆分当前块或合并下一块；
5. “存档”按钮始终可用；不设置逐块确认；
6. 补全所有字段，最后一块的结束理由必须为 `END_OF_TRANSCRIPT`；
7. 可填写审批备注，点击“存档”；页面直接在已授权项目的 S02 目录写入固定文件名 `semantic-blocks-approved.json`。

页面始终以用户所选项目中的最新 `semantic-blocks.json` 为编辑起点，即使已有批准文件也不得自动载入它。页面提供撤销、重做、搜索、`Ctrl+S` 存档、“重新加载草稿”和 Import JSON。“重新加载草稿”重新读取磁盘上的 S01 时间轴、语义转录和机器草稿；机器草稿重新生成后无需更新 HTML。Import 接受 `semantic-blocks.json`、`semantic-blocks-approved.json` 或同结构分块 JSON，导入标题、角色、认知目标、结束理由和边界；时间、来源范围与文字仍从当前项目重新计算。拆分或导入产生的块必须包含真实语义字段。

## 保存契约

页面只把每块的 `end_unit_id`、`title`、`semantic_role`、`cognitive_goal`、`boundary_reason` 及可选审批备注视为用户决定，并完成以下工作：

- 检查全部字段、边界递增和全文覆盖；
- 从 S01 重新生成 `block_id`、绝对时间、`source_unit_range` 和 `verbatim_text`；
- 从 `semantic-transcript.json` 的标点锚点重新生成 `semantic_text`；
- 写入 S01、语义转录和机器草稿的 SHA-256；
- 写入 `approval.status=APPROVED`、审批时间、块数、相对机器草稿的变更数和审批备注；
- 通过浏览器目录选择器授权项目根目录，并直接创建或覆盖该项目 S02 目录中的 `semantic-blocks-approved.json`。

工具必须拒绝其他批准文件名，也必须拒绝让批准文件路径等于 `semantic-blocks.json`。允许覆盖旧的 `semantic-blocks-approved.json`，但绝不覆盖机器草稿。

必须使用支持 File System Access API 的最新版 Chrome 或 Edge。每次打开通用页面时由用户选择待审批项目，页面自动确定输出目录和文件名，不要求选择文件名。只有页面成功关闭 writable 并明确提示写入完成，且 Python 验证器重新读取 S02 中的实际文件并通过后，保存才算完成。

## 独立验证

```text
<python> scripts/s02_block_review.py validate <项目目录>/S01/text-unit-timeline.json <项目目录>/S02/semantic-transcript.json <项目目录>/S02/semantic-blocks.json <项目目录>/S02/semantic-blocks-approved.json
```

验证失败时不得继续下游。机器草稿、语义转录或 S01 时间轴发生变化后，旧批准文件会因来源哈希不匹配而自动失效，必须重新审批。
