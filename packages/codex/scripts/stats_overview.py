#!/usr/bin/env python3
"""Generate descriptive message statistics for a distillation dataset."""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean

from common import configure_stdio, message_conversation, message_sender, message_text, message_time, read_jsonl


def main() -> None:
    configure_stdio()
    parser = argparse.ArgumentParser(description="Create message statistics overview.")
    parser.add_argument("--input", required=True, type=Path, help="Merged message JSONL.")
    parser.add_argument("--output", type=Path, help="Optional Markdown output path.")
    parser.add_argument("--json", type=Path, help="Optional JSON output path.")
    args = parser.parse_args()

    total = 0
    by_conversation = Counter()
    by_sender = Counter()
    by_month = Counter()
    by_hour = Counter()
    lengths = []
    deep_night = 0
    conv_sender = defaultdict(Counter)

    for msg in read_jsonl(args.input):
        total += 1
        conv = message_conversation(msg)
        sender = message_sender(msg)
        text = message_text(msg)
        ts = message_time(msg)
        by_conversation[conv] += 1
        by_sender[sender] += 1
        conv_sender[conv][sender] += 1
        lengths.append(len(text))
        if ts:
            by_month[ts.strftime("%Y-%m")] += 1
            by_hour[f"{ts.hour:02d}"] += 1
            if ts.hour >= 23 or ts.hour < 5:
                deep_night += 1

    stats = {
        "total_messages": total,
        "by_conversation": dict(by_conversation.most_common()),
        "by_sender": dict(by_sender.most_common()),
        "by_month": dict(sorted(by_month.items())),
        "by_hour": dict(sorted(by_hour.items())),
        "deep_night_messages": deep_night,
        "deep_night_ratio": deep_night / total if total else 0,
        "text_length": {
            "avg": mean(lengths) if lengths else 0,
            "max": max(lengths) if lengths else 0,
        },
        "conversation_sender": {k: dict(v.most_common()) for k, v in conv_sender.items()},
    }

    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(json.dumps(stats, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        "# 数据概览",
        "",
        f"- 总消息数：{total}",
        f"- 深夜消息：{deep_night} ({stats['deep_night_ratio']:.1%})",
        f"- 平均文本长度：{stats['text_length']['avg']:.1f}",
        f"- 最长文本长度：{stats['text_length']['max']}",
        "",
        "## 会话分布",
        "",
        "| 会话 | 消息数 |",
        "|---|---:|",
    ]
    for conv, count in by_conversation.most_common(20):
        lines.append(f"| {conv} | {count} |")
    lines.extend(["", "## 月度趋势", "", "| 月份 | 消息数 |", "|---|---:|"])
    for month, count in sorted(by_month.items()):
        lines.append(f"| {month} | {count} |")

    output = "\n".join(lines) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(output, encoding="utf-8")
        print(f"wrote {args.output}")
    else:
        print(output)


if __name__ == "__main__":
    main()
