# gen-explainer-video

从剪辑完成的中文口播视频出发，建立忠实、可追溯的文字时间证据和全文语义结构，为后续视觉表达设计与视频合成提供可靠输入。

当前版本：`0.2.0`

## 当前能力

当前已正式定义并验证两个阶段：

```text
剪辑完成的中文口播视频 + 匹配参考文稿
→ S01 忠实转录、纠错追溯与文字单元时间轴
→ S02 全文语义理解、机器语义块与人工审批
→ 后续视觉设计与 HyperFrames 合成阶段（待建立）
```

### S01：转录与对齐

- 以剪辑完成的视频时间轴作为统一时间基准。
- 保留实际口述内容、顺序、语气词、重复和临场补充。
- 参考文稿只辅助纠正同一发音直接支持的错字、同音字和专有名词。
- 生成可追溯的 `KEEP/REPLACE` 纠错映射。
- 将中文字符、连续数字、百分比、英文及结构化英数表达组织为带时间证据的文字单元。
- 通过来源覆盖、文字一致性、时间区间和追溯完整性验证。

### S02：语义切割与审批

- 在不改变 S01 忠实文字的前提下建立句子、段落和语义块。
- 语义块围绕单一主要认知目标组织，并直接锚定 S01 文字单元边界。
- 保留机器草稿 `semantic-blocks.json`，不以人工结果覆盖它。
- 提供无需 Server、无需嵌入项目数据的通用本地审批页。
- 用户选择项目根目录后，审批页读取最新草稿并固定生成 `semantic-blocks-approved.json`。
- 后续阶段只允许读取通过独立验证的批准文件。

### 竖屏平台安全区模板

- 提供微信视频号、抖音和小红书 `1080×1920` 竖屏播放画面的机器可读 JSON 模板。
- 每个平台只定义一套关键内容安全边界，并在其内部标注独立的字幕功能框。
- 抖音与小红书采用非对称左右边距，显式避让右侧互动操作栏和底部信息层。
- 项目存在用户显式配置时，以项目配置为准并记录覆盖来源。

## 安装

将仓库克隆到 Codex Skill 目录：

```text
git clone https://github.com/jasonaisg/gen-explainer-video.git <Codex-Skill-目录>/gen-explainer-video
```

也可以克隆到其他 Agent 能够读取 Skill 的目录。确保 Agent 能发现根目录中的 `SKILL.md`。

## 使用示例

```text
请使用 $gen-explainer-video，从这个已经剪辑完成的中文口播视频和参考文稿开始，执行 S01 转录与对齐。
```

执行 S02：

```text
请使用 $gen-explainer-video，读取已经验证的 S01 文字单元时间轴，生成语义转录和待审批语义块。
```

## 正式产物

### S01

```text
S01/
├── audio/extracted-audio.mp3
├── audio/extraction-report.json
├── asr-raw/engine-output.json
├── raw-asr.json
├── correction-map.json
├── text-unit-timeline.json
└── s01-report.json
```

### S02

```text
S02/
├── semantic-transcript.json
├── semantic-blocks.json
├── semantic-blocks-review.html
└── semantic-blocks-approved.json
```

其中 `semantic-blocks.json` 是机器草稿，`semantic-blocks-approved.json` 是后续阶段唯一允许消费的最终语义块文件。

## 主要目录

```text
gen-explainer-video/
├── SKILL.md                    # Agent 核心执行指令
├── VERSION                     # 当前版本号
├── agents/openai.yaml          # Codex 界面元数据
├── references/                 # S01、S02 与视觉表达参考资料
├── scripts/                    # 构建、审批与验证工具
└── assets/                     # JSON 模板及通用审批页
```

## 环境原则

Skill 本身不内嵌虚拟环境、媒体文件或第三方二进制文件。执行时优先复用目标机器已有的 Python、FFmpeg、FFprobe、ASR 和浏览器能力；具体项目可以在自己的 `AGENTS.md` 中规定运行环境。

S02 的 Python 构建与验证脚本只依赖标准库。通用审批页使用支持 File System Access API 的 Chrome 或 Edge，通过用户明确授权读取和写入项目目录。

## 验证

从 `scripts` 目录运行回归测试：

```text
python -B -m unittest test_s01_text_units.py test_s02_semantic_pipeline.py test_s02_block_review.py
```

当前回归测试共 16 项。真实测试项目已验证 1,674 个文字单元完整进入 49 个句子、13 个段落和 19 个批准语义块。

## 版本规则

本项目采用[语义化版本](https://semver.org/lang/zh-CN/)：

- 主版本：工作流或项目数据结构发生不兼容变化。
- 次版本：增加向后兼容的能力、阶段机制或工具。
- 修订版本：修复缺陷、改进文档或进行兼容性调整。

`VERSION` 是版本号的权威来源。正式发布时同时创建同名 Git 标签，例如 `0.1.0` 对应 `v0.1.0`。

## 当前状态

`0.2.0` 在 `0.1.0` 的 S01、S02 能力基础上，新增微信视频号、抖音和小红书 `1080×1920` 竖屏安全区与字幕区的正式 JSON 匹配模板。视觉设计、视觉表达选择和 HyperFrames 最终合成仍按后续迭代逐步加入。

## 致谢

本 Skill 的设计与演进受到了许多优秀实践与思考的启发。

特别感谢云云创作的 `build-spoken-video-motion`。其中围绕口播内容理解、动效组织和阶段化视频制作的探索，为本项目提供了重要灵感，也促使我们进一步思考如何把动效设计融入可执行、可审查的完整制作流程。

同时感谢 Kong 分享的第一性原理思路。它启发本项目从观众的认知目标、信息障碍和最小充分视觉出发，重新审视每一个动效是否真正有助于理解与记忆，而不是把动画当作单纯的装饰。

本项目在这些启发的基础上，结合已经排定的真实时间轴、人物连续性、用户最终内容权威、多 Session 协作和可验证交付机制，形成了当前的工作流。衷心感谢云云和 Kong 的分享、创造与启发。

## License

本项目基于 [MIT License](LICENSE) 开源。任何人均可免费使用、复制、修改、合并、发布和分发本项目，也可以用于商业用途，但须保留原始版权声明和许可证文本。

本项目按“原样”提供，不附带任何明示或暗示的担保。仓库中引用或依赖的第三方项目、工具和素材仍分别适用其各自的许可证与使用条款。
