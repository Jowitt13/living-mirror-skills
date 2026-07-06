# 数据合并与版本管理指南

## 目录结构

```text
distillation/
├── raw/
│   ├── messages.jsonl
│   ├── voice_transcriptions.json
│   └── merged.jsonl
├── v2/
│   ├── 00-conflict-tracker.md
│   ├── 01-values-emotions.md
│   └── ...
├── archive/
├── self-portrait-YYYY-MM.md
├── conflicts.md
├── corrections.md
├── changelog.md
└── manifest.json
```

## 消息合并

使用 `scripts/merge_messages.py` 合并文本消息和语音转录：

```bash
python scripts/merge_messages.py --messages raw/messages.jsonl --voice raw/voice_transcriptions.json --output raw/merged.jsonl
```

要求：

- 不硬编码路径。
- 原消息字段尽量保留。
- 语音转录写入 `text`，并保留 `voice_transcribed`、`voice_backend` 等字段。
- 输出按时间排序。

## 洞察 merge

- 新增洞察：标 `[新增 YYYY-MM]`。
- 修订洞察：标 `[修订 YYYY-MM]`，旧表述写入 changelog。
- 证据增强：提高置信度，但保留原证据链。
- 新证据冲突：不要覆盖，写入 CONFLICT。
- 用户推翻：写入 Correction，再同步自画像。

## manifest.json 建议字段

```json
{
  "current_version": "v1.0",
  "current_version_file": "self-portrait-YYYY-MM.md",
  "framework_version": "v2.0",
  "updated_at": "YYYY-MM-DDTHH:mm:ss",
  "data_sources": {
    "wechat": {"status": "active", "merged_file": "raw/merged.jsonl"},
    "flomo": {"status": "optional"}
  },
  "versions": [
    {
      "version": "v1.0",
      "date": "YYYY-MM-DD",
      "file": "self-portrait-YYYY-MM.md",
      "data_window": "YYYY-MM-DD ~ YYYY-MM-DD",
      "insights_new": 0,
      "insights_revised": 0,
      "conflicts_new": 0,
      "conflicts_closed": 0,
      "corrections": 0,
      "pending_review": true
    }
  ]
}
```

## changelog.md 模板

```markdown
# 变更日志

## YYYY-MM-DD vX.X
- 数据范围：
- 新增洞察：
- 修订洞察：
- 新增 CONFLICT：
- 关闭 CONFLICT：
- Correction：
- 用户复核状态：
```

## 回滚

回滚时从 `archive/` 恢复旧版自画像，并更新 `manifest.json` 的 `current_version`。不要删除被回滚的版本。

