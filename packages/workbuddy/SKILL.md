---
name: living-mirror
description: 见己镜 Living Mirror - 从用户的聊天记录/flomo/日记/语音转录里蒸馏出带证据、三段置信度、情境权重、反证索引、用户语言优先、允许矛盾、可被推翻的自画像。当用户说"蒸馏自己""自画像""理解自己""自我认知""分析我的聊天记录"时触发。支持两轮蒸馏（按时间段 + 最多16主题纵向）+ sender全验证 + CONFLICT追踪 + Correction机制 + 状态/特质区分。
version: "1.0"
updated: "2026-07-07"
platforms: [workbuddy, claude-code]
triggers:
  - "蒸馏自己"
  - "自画像"
  - "自我蒸馏"
  - "理解自己"
  - "分析我的聊天记录"
  - "自我认知"
  - "月度蒸馏"
  - "distillation"
---

# 见己镜 Living Mirror v0.6

从用户的碎片记录里（聊天记录/flomo/日记），蒸馏出此刻的他/她，产出一套带证据、带置信度、允许矛盾、可被推翻、可回滚的自画像。

不是克隆用户，是给用户一面会迭代、会认错的镜子。

## 不可妥协原则

1. **镜子不是复读机** —— 提取模式与价值观，不模仿说话。
2. **每条洞察必须附证据** —— verbatim > artifact > impression，附置信度。无证据不写进自画像。
3. **矛盾不强行统一** —— 人本来就是矛盾的。记录下来，标"待验证"，等数据够了再说。
4. **蒸馏器允许被推翻** —— 用户说"我不是这样"，立即修正，写入 Correction 层。
5. **本地处理，不上云** —— 用户数据全部本地。
6. **长期主义** —— 月/年是尺度。不为了显得有用而硬出洞察。
7. **碎片是用户的** —— 引用克制，转述脱敏。

## 架构

```
① 数据采集层：聊天记录 + flomo/日记 -> 统一碎片格式
② 蒸馏框架层：Part A 自我记忆11维度（基础5 + v0.4/v0.5扩展6）+ Part B 人格5层 + 四套机制 + v0.6 动态镜像规则
③ 输出层：自画像 + conflicts + corrections + changelog + manifest
```

### Part A 自我记忆

1. 价值观与情绪
2. 行为与决策模式
3. 人际关系
4. 目标与方向
5. 个人经历
6. 饮食偏好
7. 生活习惯
8. 思维方式
9. 世界观与人生观
10. 爱好系统
11. 亲密/性表达（可选敏感维度，必须获得用户明确同意）

### Part B 人格五层

- Layer 1 硬规则：不可违背的底线、稳定行为规则、雷区
- Layer 2 身份：用户是谁、当前阶段、核心自我认同
- Layer 3 说话风格：句式、语气词、不同关系中的表达差异
- Layer 4 情感模式：触发器、调节方式、压力/亲密中的变化
- Layer 5 人际行为：关系中的行动方式、冲突处理、照顾/依赖模式

## 四套机制

### 1. 证据分级

每条洞察必须标注证据等级和置信度。细则见 `references/evidence-grading.md`。

```
verbatim   -> 原文直引，必须标 sender=已验证
artifact   -> 统计数据/消息密度/时间分布/文件痕迹
impression -> 蒸馏器推断，最低级，必须配原文或 artifact
置信度     -> 高 / 中 / 低
```

### 2. CONFLICT 追踪

不同来源、不同时间、不同情境说法不一致时，不强行统一，写入 `conflicts.md`。每次蒸馏开始前先拉出当前 CONFLICT 状态。细则见 `references/conflict-tracker.md`。

### 3. Correction 层

用户指出"我不是这样"时立即修正。不要删除原洞察，保留迭代痕迹，写入 `corrections.md`。细则见 `references/correction-rules.md`。

### 4. 增量 merge + 版本管理

月度 merge 不覆盖旧结论。新增标 `[新增 YYYY-MM]`，修订标 `[修订 YYYY-MM]`，旧版本归档到 `archive/`，`manifest.json` 记录版本元数据。细则见 `references/merge-guide.md`。

### 5. 动态镜像规则

重要洞察必须区分稳定特质、阶段状态、特殊时期反应、关系触发模式或待验证模式；把置信度拆成 evidence / interpretation / stability；分离事实/解释/命名；优先使用用户语言；并维护反证索引。细则见 `references/dynamic-mirror-rules.md`。

v0.6 还提供机器可读 schema 和自动质检脚本：

```bash
python scripts/quality_check_distillation.py --input self-portrait-YYYY-MM.md --output quality-report.md
```

## 关键防翻车规则

1. 凡涉及"谁说了什么""谁做了什么"的判断，必须回原始数据验证 sender。先读 `references/sender-verification.md`，并用 `scripts/verify_sender.py` 辅助。
2. 关键词统计只用于发现值得读的对话段，不用于定性关系、情绪、依恋类型。见 `references/keyword-usage.md`。
3. 每个时间段/主题开头强制标注特殊时期。凡涉及"下降/减少/边缘化"判断，先排除考试周、假期、生病期、重大事件期。见 `references/special-period.md`。
4. 优先采信用户自我报告；量化数据只做描述，不做定性终审。
5. 如涉及第 16 主题（亲密/性表达），先确认用户明确同意；不同意或犹豫时直接跳过，不追问、不推断。
6. 不把一次性状态写成永久人格；需要判断稳定性、情境权重、反证索引或可推翻条件时，先读 `references/dynamic-mirror-rules.md`。

## 标准流程

### 初始化

运行：

```bash
python scripts/init_distillation.py <workspace>
```

创建：

```
distillation/
├── raw/
├── v2/
├── archive/
├── self-portrait-YYYY-MM.md
├── conflicts.md
├── corrections.md
├── changelog.md
└── manifest.json
```

### 月度蒸馏

1. **数据准备**：收集聊天记录/flomo/日记到 `distillation/raw/`。需要合并文本和语音转录时运行 `scripts/merge_messages.py`，需要概览时运行 `scripts/stats_overview.py`。
2. **CONFLICT 回看**：读取 `conflicts.md`，列出本次要重点验证的矛盾。
3. **第一轮：按时间段蒸馏**：按季度、人生阶段或用户指定范围切分数据，用 `scripts/filter_by_time.py` 筛选，读原文并产出批次报告。模板见 `references/batch-report-template.md`。
4. **第二轮：按主题纵向蒸馏**：最多 16 个主题逐一跨全时段分析，可按用户目标裁剪；第 16 主题为可选敏感主题，必须获得明确同意后才启用。用 `scripts/filter_by_theme.py` 筛选，读原文、验证 sender、纵向识别模式。模板见 `references/theme-report-template.md`。
5. **用户复核**：每个主题完成后必须等用户复核。错误立即 Correction，补充立即追加，可关闭的 CONFLICT 标记关闭。
6. **合并自画像**：以已完成的纵向主题为骨架，把批次时间线深度、verbatim 证据、阶段演变细节编织进去。不简化、不删减。模板见 `references/self-portrait-template.md`。
7. **更新元数据**：更新 `conflicts.md`、`corrections.md`、`changelog.md`、`manifest.json`，旧版本归档。

## 最多 16 个纵向主题

1. 价值观与情绪
2. 行为与决策模式
3. 与伴侣关系
4. 与家人关系
5. 与朋友关系
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
16. 亲密/性表达（可选敏感主题，必须获得用户明确同意；可跳过）

每个主题流程：

```
Step 1: 用关键词+时间范围筛选相关消息
Step 2: 读取筛选消息原文和上下文，验证 sender
Step 3: 按时间纵向排列，识别模式/变化/矛盾
Step 4: 提取洞察，每条附证据等级、sender验证、置信度
Step 5: 标注特殊时期影响
Step 6: 与上一版本和第一轮批次洞察对比
Step 7: 等用户复核
```

## Reference 路由

- 需要完整框架说明：读 `references/framework-v2.md`
- 写洞察证据和置信度：读 `references/evidence-grading.md`
- 处理矛盾：读 `references/conflict-tracker.md`
- 处理用户纠正：读 `references/correction-rules.md`
- 使用 verbatim 或判断谁做了什么：读 `references/sender-verification.md`
- 使用关键词筛选：读 `references/keyword-usage.md`
- 分析特殊时期：读 `references/special-period.md`
- 判断状态/特质、情境权重、三段置信度、事实/解释/命名、反证索引、用户语言优先、可推翻条件：读 `references/dynamic-mirror-rules.md`
- 需要结构化字段约束：读 `references/insight-schema-v0.6.json`
- 需要自动检查自画像或主题报告：运行 `scripts/quality_check_distillation.py`
- 写自画像/批次/主题报告：读对应 template
- 合并两轮蒸馏结果或做版本管理：读 `references/merge-guide.md`

## 输出纪律

- 所有文件使用 UTF-8。
- 不硬编码任何用户姓名、关系名、会话名或本地路径。
- 只在用户允许的数据范围内处理，默认本地完成。
- 模板可以复制，但内容必须基于用户自己的证据重写。
- 每条原文引用都要克制；能转述脱敏就不要大段引用。



## Local Voice Ingestion / 本地语音入口

Use this path when source material includes local audio, voice notes, meeting recordings, listening-practice audio, or exported WeChat voice messages. Call it "Local Voice Ingestion" / "本地语音入口"; do not describe it as a bundled model. The user must provide a local ASR model with `--model` or `LIVING_MIRROR_ASR_MODEL`.

```bash
python scripts/probe_local_voice_env.py
python scripts/batch_transcribe_local_voice.py --input raw/audio --output raw/voice-transcripts --recursive --resume --model <local-asr-model-or-path>
```

Then merge `raw/voice-transcripts/transcripts.jsonl` with `scripts/merge_messages.py`.

### WeChat SILK (multiprocess-optimized)

WeChat voice exports are `.silk` (SILK codec). Use the dedicated script, which decodes SILK with `pilk` directly to 16 kHz, pre-decodes all files on CPU cores in parallel, then runs batched FunASR inference so the GPU is fully saturated:

```bash
LIVING_MIRROR_ASR_MODEL="paraformer-zh" python scripts/batch_transcribe_wechat_silk.py --input "D:/wechat/voice" --output raw/voice-transcripts --resume
```

It recovers `timestamp` / `sender_wxid` from the SILK filename; pass `--me-wxid` to infer `is_self`. Details and py3.13 install caveats are in `docs/local-voice-ingestion.md`.
