# living-mirror for Claude Code

这个包是 Claude Code 版的见己镜（Living Mirror）Skill。

## 放置位置

推荐放在：

```text
C:\Users\hangi\.claude\skills\living-mirror
```

## 使用方式

在 Claude Code 中可以直接说：

- `使用 living-mirror 蒸馏我的聊天记录`
- `按 living-mirror 框架分析这些 jsonl`
- `帮我做月度自画像，先验证 sender`
- `读取 references/sender-verification.md，检查这几条 verbatim 归属`

## 入口文件

- `SKILL.md`：主流程和触发规则
- `references/`：证据分级、CONFLICT、Correction、sender 验证、模板
- `scripts/`：标准库脚本，适合 Claude Code 本地运行

## Claude Code 使用重点

1. 先读 `SKILL.md`。
2. 涉及原文引用或"谁说了什么"时，必须读 `references/sender-verification.md`。
3. 使用 `scripts/verify_sender.py` 验证关键 verbatim。
4. 不要仅凭关键词定性关系、情绪或人格。
5. 每个主题报告完成后等待用户复核，再进入下一主题。

