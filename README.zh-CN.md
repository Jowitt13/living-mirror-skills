# Living Mirror Skills · 见己镜

> 一面可验证的自我之镜：把本地聊天记录、笔记和日记，蒸馏成一份有证据、可修正、可回滚的自画像。

语言：[English](README.md) | 简体中文

**Living Mirror，中文名「见己镜」**，是一套可复用的自我蒸馏技能包。它帮助 Codex、Claude Code 或 WorkBuddy 读取你的碎片记录，比如微信/聊天记录、flomo、日记、语音转录等，然后产出一份带证据、带置信度、允许矛盾、允许被用户推翻，并且可以持续迭代的自画像。

它不是把你克隆成一个 AI，也不是训练一个模仿你说话的人格。它更像是一面会迭代、会认错、能留下证据链的镜子：照见自己，也允许自己推翻它。

## 本地语音入口

Living Mirror 也可以在自我蒸馏前先处理语音材料。**本地语音入口**模块会把本地音频，包括微信语音导出、会议录音、语音备忘、听力练习音频等，转成后续可分析的文本产物。

这个模块不内置语音模型，也不写死某个模型名。请在运行时通过 `--model` 参数或 `LIVING_MIRROR_ASR_MODEL` 环境变量指定你自己的本地语音识别模型。

## 这是什么

很多个人记忆项目都在追求「让 AI 更像我」或者「让 AI 记住更多事实」。这个项目关注的是另一件事：

- 从真实记录里提取模式、价值观、变化、冲突和行为倾向。
- 每条重要洞察都必须有证据。
- 不确定的地方标注置信度，而不是假装已经知道。
- 矛盾先保留，不强行统一成漂亮结论。
- 用户可以随时推翻分析，系统必须写入 Correction。
- 每次更新都有版本，可以追踪，也可以回滚。
- 区分稳定特质、阶段状态、关系触发模式和特殊时期反应，不把一次性的状态写成永久人格。
- 把反证和例外显式列出来，不藏在一段顺滑的叙述里。

最终得到的不是一个固定标签，而是一份会成长的自画像。

## 它有什么用

你可以用它来：

- 从多年的聊天记录、笔记、日记中理解自己。
- 做月度、季度或年度自我复盘。
- 分析关系模式，但不依赖玄学式印象。
- 追踪价值观、目标、情绪、习惯、思维方式、生活偏好、说话风格和冲突处理方式的变化。
- 给每条重要判断留下证据链。
- 避免 AI 分析聊天记录时常见的错误：sender 归属搞反、关键词过度解读、特殊时期误判。
- 搭建一个本地优先的个人记忆工作流。

## 适合谁

这套技能尤其适合：

- 有大量聊天记录、flomo、日记、语音转录，并希望从中看见长期模式的人。
- 想给自己做「月度自画像」或「人生阶段复盘」的人。
- 正在搭建个人 AI 记忆系统的 AI 深度用户。
- 想用证据而不是感觉来分析关系、目标、情绪和行为模式的人。
- 教练、研究者、自我追踪爱好者，或者需要做定性材料整理的人。
- 想把本地 AI 工作流封装成 Codex / Claude Code / WorkBuddy Skill 的开发者。

它不是心理治疗、医疗建议、法律建议，也不适合替代危机干预。它是一套结构化自我理解工具。

## 核心方法

框架分三层：

```text
1. 数据采集层
   聊天记录 + 笔记 + 日记 -> 统一碎片格式

2. 蒸馏框架层
   Part A：自我记忆 11 维度
   Part B：人格五层
   证据分级 + CONFLICT 追踪 + Correction + 版本管理 + 动态镜像规则

3. 输出层
   自画像 + conflicts + corrections + changelog + manifest
```

### Part A：自我记忆 11 维度

1. 价值观与情绪
2. 行为与决策模式
3. 人际关系
4. 目标与方向
5. 个人经历与成长轨迹
6. 饮食偏好
7. 生活习惯
8. 思维方式
9. 世界观与人生观
10. 爱好系统
11. 亲密/性表达（可选敏感维度，必须获得用户明确同意）

### v0.4 / v0.5 框架扩展

v0.4 将纵向主题从 10 个扩展到 15 个，新增饮食偏好、生活习惯、思维方式、世界观与人生观、爱好系统。

v0.5 增加第 16 个可选敏感主题：亲密/性表达。该主题默认关闭，只有用户明确要求或授权时才分析；可以跳过，不影响主流程。启用时必须更严格地保护隐私、脱敏引用、验证 sender，并避免道德评判或病理化。

### 动态镜像规则

Living Mirror 现在多了一层动态判断：不只问「这个人是什么样」，还要问「这个判断在什么情境下成立」。重要洞察需要写清楚：

- 使用哪一种人类理解维度：身体/能量、羞耻/防御、欲望与行动落差、审美秩序、关系角色切换、主体性、注意力节律、意义叙事、边界、修复。
- 它是稳定特质、阶段状态、特殊时期反应、关系触发模式，还是待验证模式。
- 哪些情境影响了证据：时间、关系、身体/能量状态、环境、事件、媒介。
- 三段置信度：证据置信度、解释置信度、稳定性置信度。
- 事实、解释和临时命名要分开，不让一个好听标签跑在证据前面。
- 什么新证据或用户纠正会推翻/削弱这条洞察。
- 哪些 `CE-XXX` 反证条目正在挑战这条洞察。
- 如果用户本来就有自己的说法，优先使用用户自己的语言。

这会让自画像更像一面会校准的镜子，而不是一台给人贴标签的机器。

### Part B：人格五层

1. 硬规则
2. 身份
3. 说话风格
4. 情感模式
5. 人际行为

## 安全机制

### 1. 证据分级

每条洞察都必须标注证据等级：

| 等级 | 含义 |
|---|---|
| `verbatim` | 原文直引，必须验证 sender。 |
| `artifact` | 统计数据、文件、时间分布、消息密度、行为痕迹。 |
| `impression` | 蒸馏器的解释或印象，等级最低，不能单独作为结论。 |

同时标注置信度：高 / 中 / 低。

### 2. CONFLICT 追踪

人本来就是矛盾的。不同时间、不同关系、不同情境中出现不一致，不要急着压成一个结论，而是写入 `conflicts.md`。

状态包括：

- `🟢 已解决`
- `🟡 待验证`
- `🔴 矛盾加剧`

### 3. Correction 纠正层

用户说「我不是这样」时，系统必须立即修正：

- 不删除原洞察。
- 标记原洞察已被推翻。
- 在 `corrections.md` 中记录推翻原因。
- 更新自画像中的新表述。

这能让自画像不是一次性判断，而是持续校准的结果。

### 4. 增量合并与版本管理

月度更新不覆盖旧版本。新增、修订、矛盾、纠正都写入：

- `self-portrait-YYYY-MM.md`
- `conflicts.md`
- `corrections.md`
- `changelog.md`
- `manifest.json`
- `archive/`

### 5. 状态/特质与可推翻条件

动态镜像规则会阻止过度判断：一句很有力量的原文可以让证据置信度很高，但稳定性置信度仍然可能很低。每条重要洞察都要说明它受什么情境影响，以及什么新证据或用户纠正会推翻它。

### 6. 反证索引

重要洞察可以维护 `CE-XXX` 反证条目。每条反证都链接到被挑战的洞察，记录例外、相反证据、用户纠正或替代解释，并标注它是削弱、收窄、推翻，还是生成新的 CONFLICT。

## 可选输出

除了完整自画像，这套 Skill 也可以输出：

- 短版自画像：5 到 9 条带证据的高密度要点。
- 关系地图：按关系类型，或经同意的具体关系，整理互动模式。
- 变化时间线：标记某个模式何时出现、增强、变弱或被 Correction 推翻。
- 验证问题清单：把低置信度但重要的洞察变成可供用户确认、否定或重命名的问题。
- 证据账本：并排展示支持证据、反证、当前置信度和状态。
- 情境权重概览：说明哪些情境正在塑造当前自画像。
- 修复地图：整理冲突、道歉、重新靠近和不修复的模式。
- 用户语言词典：优先保存用户自己的命名，再放外部理论标签。

## 三个版本怎么选

这个仓库包含三套可直接使用的版本：

| 版本 | 路径 | 适合场景 |
|---|---|---|
| WorkBuddy | `packages/workbuddy/` | 使用 WorkBuddy，想保留 `version`、`updated`、`platforms`、`triggers` 等元数据。 |
| Codex | `packages/codex/` | 安装到 Codex Skills。这个版本使用 Codex 兼容的最小 frontmatter。 |
| Claude Code | `packages/claude-code/` | 安装到 Claude Code Skills。包含 Claude Code 使用说明。 |

三套版本的方法论、references 和 scripts 是一致的，只是入口元数据适配不同平台；三套版本都包含本地语音入口工具。

## 安装方式

### Codex

把 Codex 版本复制到 Codex skills 目录：

```powershell
Copy-Item -Path .\packages\codex -Destination "$env:USERPROFILE\.codex\skills\living-mirror" -Recurse -Force
```

然后可以这样调用：

```text
Use $living-mirror to analyze my local chat records and build a monthly self portrait.
```

### Claude Code

把 Claude Code 版本复制到 Claude skills 目录：

```powershell
Copy-Item -Path .\packages\claude-code -Destination "$env:USERPROFILE\.claude\skills\living-mirror" -Recurse -Force
```

然后可以说：

```text
使用 living-mirror 蒸馏这些聊天记录。引用原文前先验证 sender。
```

### WorkBuddy

把 WorkBuddy 版本复制到 WorkBuddy skills 目录：

```powershell
Copy-Item -Path .\packages\workbuddy -Destination "$env:USERPROFILE\.workbuddy\skills\living-mirror" -Recurse -Force
```

可以用这些触发词：

- `蒸馏自己`
- `自画像`
- `自我蒸馏`
- `理解自己`
- `分析我的聊天记录`
- `月度蒸馏`
- `distillation`

## 基础用法

初始化蒸馏工作区：

```bash
python scripts/init_distillation.py <workspace>
```

用用户配置的本地语音识别模型转写音频：

```bash
LIVING_MIRROR_ASR_MODEL="<你的模型名或本地路径>" python scripts/batch_transcribe_local_voice.py --input raw/audio --output raw/voice-transcripts --recursive --resume
```

合并文本消息和语音转录：

```bash
python scripts/merge_messages.py --messages raw/messages.jsonl --voice raw/voice-transcripts/transcripts.jsonl --output raw/merged.jsonl --sort
```

生成数据概览：

```bash
python scripts/stats_overview.py --input raw/merged.jsonl --output stats.md --json stats.json
```

按时间段筛选：

```bash
python scripts/filter_by_time.py --input raw/merged.jsonl --output batch-2025.jsonl --start 2025-01-01 --end 2025-12-31
```

按主题筛选：

```bash
python scripts/filter_by_theme.py --input raw/merged.jsonl --output values.jsonl --theme "价值观与情绪" --context 3
```

验证 sender：

```bash
python scripts/verify_sender.py --input raw/merged.jsonl --keyword "自由" --start 2024-01-01 --context 2
```

## 推荐工作流

1. 把原始数据放进 `distillation/raw/`。
2. 合并文本消息和语音转录。
3. 生成数据概览。
4. 读取已有的 `conflicts.md` 和 `corrections.md`。
5. 第一轮：按时间段蒸馏。
6. 第二轮：按最多 16 个主题纵向蒸馏；第 16 主题为可选敏感主题，必须获得明确同意后才启用。
7. 对每条关键原文引用验证 sender。
8. 应用动态镜像规则：人类理解维度、状态/特质、情境权重、三段置信度、事实/解释/命名、反证索引、用户语言优先、可推翻条件。
9. 每个主题报告完成后让用户复核。
10. 合并成 `self-portrait-YYYY-MM.md`。
11. 更新 `manifest.json`、`changelog.md`、`conflicts.md`、`corrections.md`。

## 仓库结构

```text
.
├── packages/
│   ├── workbuddy/
│   ├── codex/
│   └── claude-code/
├── docs/
│   ├── examples.md
│   ├── local-voice-ingestion.md
│   ├── privacy-and-safety.md
│   └── platform-notes.md
├── LICENSE
├── README.md
└── README.zh-CN.md
```

每个 package 内部都有：

```text
SKILL.md
agents/openai.yaml
references/
scripts/
```

## 隐私原则

这套技能默认本地优先：

- 原始聊天记录不要上传。
- 不要把私密数据提交到 GitHub。
- 引用要克制。
- 能脱敏转述就不要贴大段原文。
- 涉及「谁说了什么」「谁做了什么」时，必须回原始数据验证 sender。

更多说明见 [Privacy and Safety](docs/privacy-and-safety.md)。

## 为什么 sender 验证这么重要

AI 分析聊天记录时最容易犯的严重错误之一，就是把一句话或一个行为归到错误的人身上。

所以本框架把 sender 验证作为硬规则：

```text
凡涉及「谁说了什么」「谁做了什么」的判断，必须回原始数据验证。
```

相关文件：

```text
references/sender-verification.md
scripts/verify_sender.py
```

## 设计谱系

Living Mirror 的架构是原创整合，但方法论上参考了 `yourself-skill`、`immortal-skill` 和 `ex-skill`。双层 Self Memory + Persona 结构、矛盾追踪、Correction 层和证据分级，已经在 [设计谱系](docs/design-lineage.md) 中标注清楚。

## License

MIT License. See [LICENSE](LICENSE).


