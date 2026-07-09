# 见己镜 Living Mirror Skills v0.9

> 自我蒸馏核心框架 v0.6 的 Skill Pack v0.9。它可以从杂乱记录开始，也可以从零数据访谈开始，把碎片整理成自画像、复核问题、行动实验、关系地图和可公开分享的脱敏模板。

语言：[English](README.md) | 简体中文

**Living Mirror，中文名「见己镜」**，是一套可复用的自我蒸馏技能包，适配 Codex、Claude Code 和 WorkBuddy。它帮助 AI Agent 读取本地碎片记录，例如微信聊天记录、flomo、日记、语音转录等，然后生成一份带证据、带置信度、允许矛盾、允许被用户推翻、可版本化、重视隐私的自画像。

它不是人格克隆，也不是训练一个“像你一样说话”的 AI。它更像一面会迭代、会认错、会保留反证、会等待你复核的镜子。

当前**自我蒸馏核心框架**：**v0.6**。  
当前 **Skill Pack / 产品化操作层**：**v0.9**。

## Skill Pack v0.9 新增了什么

自我蒸馏系统本身的统一框架版本仍然是 v0.6。Skill Pack v0.9 只是在 v0.6 核心框架外围增加入门、隐私、复核、行动、关系和社区模板能力；它不改写 manifest、自画像或操作层权威文件里的框架版本号。

| 版本 | 重点 | 解决什么痛点 |
|---|---|---|
| v0.7 | 入门与信任 | 冷启动访谈、数据体检、同意范围、隐私等级、公开稿脱敏、遗忘/删除规则。 |
| v0.8 | 行动与关系 | 7 天行动实验、沟通/边界/修复脚本、关系地图、复核队列。 |
| v0.9 | 产品化与社区模板 | 可复用模板、Obsidian/Notion/PDF/社交平台导出形态、公开案例结构、社区贡献检查表。 |

## 它能做什么

- 从多年的聊天记录、笔记、日记、语音转录里理解自己。
- 即使没有整理好的数据，也能通过冷启动访谈先生成第一版“待验证自画像”。
- 先体检本地数据，判断适合轻量、标准还是深度蒸馏。
- 做月度、季度、年度或人生阶段自我复盘。
- 在有同意和隐私边界的前提下，分析关系模式。
- 追踪价值观、目标、习惯、思维方式、生活方式、说话风格、冲突处理方式的变化。
- 给重要洞察保留证据链、反证索引和可推翻条件。
- 生成用户复核问题，让用户确认、否定、重命名或补充反证。
- 把洞察转成 7 天行动实验、沟通脚本、决策镜头和关系修复地图。
- 生成可发 GitHub、博客、Slides、小红书的脱敏公开版本。

## 适合谁

- 有聊天记录、笔记、日记、语音转录，想从中看见长期模式的人。
- 还没有整理数据，但想用结构化方式开始理解自己的人。
- 正在搭建本地 AI 记忆系统的深度用户。
- 教练、研究者、自我追踪爱好者，或需要整理定性材料的人。
- 想在同意和隐私边界内分析沟通模式的伴侣、朋友或协作者。
- 想把个人 AI 工作流封装成 Codex / Claude Code / WorkBuddy Skill 的开发者。

它不是心理治疗、医疗建议、法律建议，也不适合替代危机干预。它是一套结构化自我理解工具。

## 核心方法

```text
1. 入门层
   冷启动访谈 + 数据体检 + 同意范围

2. 数据层
   聊天记录 + 笔记 + 日记 + 本地语音转录 -> 统一碎片格式

3. 蒸馏层
   核心框架 v0.6：16 主题纵向蒸馏
   证据分级 + sender 验证 + CONFLICT + Correction
   动态镜像规则：情境、状态/特质、三段置信度、反证索引

4. 复核与行动层
   复核队列 + 7 天行动实验 + 关系地图 + 沟通脚本

5. 导出层
   私人自画像 + 可分享摘要 + 公开脱敏模板
```

## 16 个纵向主题

1. 价值观与情绪
2. 行为与决策模式
3. 伴侣/亲密关系
4. 家庭关系
5. 朋友关系
6. 目标与方向
7. 个人经历时间线
8. 说话风格演变
9. 冲突处理进化
10. 消费观演变
11. 饮食偏好
12. 生活习惯
13. 思维方式
14. 世界观与人生观
15. 爱好系统
16. 亲密/性表达，可选敏感主题，默认关闭，必须获得明确同意

## 安全机制

- **证据分级**：`verbatim`、`artifact`、`impression`。
- **sender 验证**：凡涉及“谁说了什么”“谁做了什么”，必须回原始数据验证。
- **三段置信度**：证据置信度、解释置信度、稳定性置信度。
- **情境权重**：时间、关系、身体、环境、事件、媒介。
- **状态/特质区分**：不把一次性状态写成永久人格。
- **反证索引**：用 `CE-XXX` 显式记录例外、反向证据和替代解释。
- **Correction 层**：用户说“我不是这样”时立即修正并留痕。
- **同意范围**：数据源、时间、关系、主题、输出范围都要明确。
- **隐私等级**：private / shareable / public。
- **公开稿脱敏**：不把原始私密记录或可识别第三方信息放进公开示例。

## 本地语音入口

Living Mirror 可以在自我蒸馏前先处理语音材料。**本地语音入口**会把本地音频，包括微信语音导出、会议录音、语音备忘、听力练习音频等，转成后续可分析的文本产物。

这个模块不内置语音模型，也不写死某个模型名。请在运行时通过 `--model` 参数或 `LIVING_MIRROR_ASR_MODEL` 环境变量指定你自己的本地语音识别模型。

```bash
python scripts/batch_transcribe_local_voice.py --input raw/audio --output raw/voice-transcripts --recursive --resume --model <local-asr-model-or-path>
```

## 三个版本怎么选

| 版本 | 路径 | 适合场景 |
|---|---|---|
| WorkBuddy | `packages/workbuddy/` | WorkBuddy 用户，需要中文触发词和平台元数据。 |
| Codex | `packages/codex/` | 安装到 Codex Skills，使用最小 frontmatter。 |
| Claude Code | `packages/claude-code/` | Claude Code 用户，保留相同框架、脚本和模板。 |

三套版本的方法论、references、scripts 和 templates 是一致的。

## 快速开始

复制 Codex 版本到 Codex skills 目录：

```powershell
Copy-Item -Path .\packages\codex -Destination "$env:USERPROFILE\.codex\skills\living-mirror" -Recurse -Force
```

初始化蒸馏工作区：

```bash
python scripts/init_distillation.py <workspace>
```

体检本地数据：

```bash
python scripts/diagnose_distillation_inputs.py <workspace-or-raw-folder> --output data-diagnosis.md
```

合并文本消息和语音转录：

```bash
python scripts/merge_messages.py --messages raw/messages.jsonl --voice raw/voice-transcripts/transcripts.jsonl --output raw/merged.jsonl --sort
```

质检自画像：

```bash
python scripts/quality_check_distillation.py --input self-portrait-YYYY-MM.md --product --output quality-report.md
```

生成复核队列：

```bash
python scripts/make_review_queue.py --input self-portrait-YYYY-MM.md --output review-queue.md
```

生成公开脱敏稿：

```bash
python scripts/redact_public_artifact.py --input self-portrait-YYYY-MM.md --output public-case-study.md --level public
```

## 仓库结构

```text
.
├── packages/
│   ├── workbuddy/
│   ├── codex/
│   └── claude-code/
├── docs/
│   ├── design-lineage.md
│   ├── privacy-and-safety.md
│   ├── local-voice-ingestion.md
│   ├── productization-and-community.md
│   └── visual-templates.md
├── CHANGELOG.md
├── README.md
└── README.zh-CN.md
```

每个 package 内部都有：

```text
SKILL.md
agents/openai.yaml
references/
scripts/
assets/templates/
```

## 设计谱系

Living Mirror 的架构是原创整合，但方法论上参考了 `yourself-skill`、`immortal-skill` 和 `ex-skill`。双层 Self Memory + Persona 结构、矛盾追踪、Correction 层和证据分级，已经在 [设计谱系](docs/design-lineage.md) 中标注清楚。

## License

MIT License. See [LICENSE](LICENSE).
