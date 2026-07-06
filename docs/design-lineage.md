# Design Lineage / 设计谱系

Living Mirror is an original integration, but its architecture was shaped by several prior skill-design patterns. This page records those conceptual references clearly so readers can understand where the framework comes from and what Living Mirror adds.

Living Mirror does not claim these upstream ideas as isolated inventions. It combines them into a local-first, evidence-backed, correction-friendly self-distillation workflow for Codex, Claude Code, and WorkBuddy.

## Conceptual References

| Source | Referenced idea | How Living Mirror uses it |
|---|---|---|
| `yourself-skill` | Dual structure: **Self Memory + Persona** | Living Mirror keeps a two-part model: self-memory dimensions for values, relationships, goals, behavior, and history; plus persona layers for hard rules, identity, speaking style, emotional patterns, and interpersonal behavior. |
| `immortal-skill` | Contradictions should not be forcibly unified; unresolved contradictions should be archived separately. | Living Mirror keeps conflicts in `conflicts.md` and also surfaces a "pending verification" area in the self portrait instead of flattening conflicting evidence into one clean conclusion. |
| `yourself-skill` / `ex-skill` | Correction layer: when the user says "this is not me", the system should revise immediately. | Living Mirror treats the portrait as overturnable. Corrections are recorded in `corrections.md`, old claims remain traceable, and future versions must respect the user's correction. |
| `immortal-skill` | Evidence grading: `verbatim` / `artifact` / `impression`. | Living Mirror requires every important insight to carry an evidence grade and confidence level, with direct quotes requiring sender verification. |

## What Living Mirror Adds

Living Mirror combines those patterns into one practical workflow:

- A monthly and longitudinal self-distillation process.
- Sender verification before direct quotes or claims about who said what.
- Versioned self portraits with `manifest.json`, `changelog.md`, and `archive/`.
- Local voice ingestion for turning audio records into analyzable transcript artifacts.
- Platform-specific packages for Codex, Claude Code, and WorkBuddy.

## Attribution Scope

This attribution is for conceptual and architectural influence. No upstream code, private data, model weights, or proprietary assets are intentionally copied into this repository.

If future versions copy code, prompts, long text passages, templates, or assets from another project, preserve that project's license and NOTICE requirements in the relevant file and in this page.

---

# 中文说明

Living Mirror 是一个原创整合项目，但它的架构确实参考了几个既有 Skill 的设计模式。这里把这些方法论来源写清楚，方便读者理解这个框架从哪里来，也方便区分 Living Mirror 自己做了哪些整合。

Living Mirror 不把这些上游想法包装成自己的单点发明，而是把它们组合成一套本地优先、证据驱动、允许被修正的自我蒸馏工作流。

## 方法论参考

| 来源 | 参考点 | Living Mirror 中的用法 |
|---|---|---|
| `yourself-skill` | 双层结构：**Self Memory + Persona** | Living Mirror 保留两部分模型：自我记忆维度用于描述价值观、关系、目标、行为和经历；人格层用于描述硬规则、身份、说话风格、情绪模式和人际行为。 |
| `immortal-skill` | 矛盾不强行统一，未解决矛盾单独存档。 | Living Mirror 把冲突写入 `conflicts.md`，并在自画像中保留“矛盾待验证”区域，而不是把冲突证据压成一个漂亮但不可靠的结论。 |
| `yourself-skill` / `ex-skill` | Correction 层：用户说“我不是这样”时立即修正。 | Living Mirror 把自画像设计成可被推翻的结构。修正写入 `corrections.md`，旧判断保留可追溯痕迹，后续版本必须尊重用户修正。 |
| `immortal-skill` | 证据分级：`verbatim` / `artifact` / `impression`。 | Living Mirror 要求每条重要洞察附证据等级和置信度；直接引用原文时必须验证 sender。 |

## Living Mirror 的整合贡献

Living Mirror 把这些模式组合成一个可执行的工作流：

- 月度蒸馏 + 纵向主题蒸馏。
- 原文引用和“谁说了什么”之前必须验证 sender。
- 用 `manifest.json`、`changelog.md`、`archive/` 管理自画像版本。
- 本地语音入口，把音频记录转成可分析的转写材料。
- 同时适配 Codex、Claude Code 和 WorkBuddy。

## 引用边界

这里的标注是方法论和架构层面的引用。仓库没有刻意复制上游代码、私密数据、模型权重或专有资产。

如果未来版本复制了其他项目的代码、prompt、长段文本、模板或素材，需要在对应文件和本页中继续保留对方的 license / NOTICE 要求。
