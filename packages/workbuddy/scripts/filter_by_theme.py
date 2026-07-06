#!/usr/bin/env python3
"""Filter messages by self-distillation theme keywords, with optional context."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Dict, List

from common import configure_stdio, in_range, message_text, parse_time, read_jsonl, split_keywords, write_jsonl


DEFAULT_THEMES: Dict[str, List[str]] = {
    "价值观与情绪": ["自由", "生活", "爱", "生命", "羡慕", "开心", "难过", "焦虑", "害怕", "愤怒", "热爱", "喜欢"],
    "行为与决策模式": ["应该", "决定", "选择", "计划", "怎么办", "要不要", "原因", "解决方案", "总结", "复盘"],
    "与伴侣关系": ["老婆", "宝宝", "想你", "见面", "分手", "吵架", "异地", "礼物", "纪念日", "陪"],
    "与家人关系": ["妈妈", "妈", "爸爸", "爸", "家里", "阿公", "阿婆", "医保", "生活费", "报备"],
    "与朋友关系": ["朋友", "同学", "老师", "毕业", "麻烦", "请你", "群", "兄弟", "闺蜜"],
    "目标与方向": ["目标", "方向", "上班", "工作", "创业", "建筑", "AI", "编程", "投资", "考研", "考公"],
    "个人经历时间线": ["高考", "复读", "大学", "转专业", "专升本", "录取", "实习", "毕业", "第一次"],
    "说话风格演变": ["哈哈", "真的服了", "我觉得", "超级", "好吧", "妈咪", "老婆大人", "老师"],
    "冲突处理进化": ["吵架", "道歉", "错了", "复盘", "解决", "沟通", "情绪价值", "哄", "冷暴力"],
    "消费观演变": ["买", "钱", "贵", "便宜", "花", "转账", "预算", "省钱", "投资", "消费"],
}


def main() -> None:
    configure_stdio()
    parser = argparse.ArgumentParser(description="Filter JSONL messages by theme keywords.")
    parser.add_argument("--input", required=True, type=Path, help="Merged message JSONL.")
    parser.add_argument("--output", required=True, type=Path, help="Filtered output JSONL.")
    parser.add_argument("--theme", required=True, help="Theme name. Use --list-themes to inspect defaults.")
    parser.add_argument("--keywords", action="append", help="Extra comma-separated keywords. Can repeat.")
    parser.add_argument("--context", type=int, default=0, help="Number of neighbor messages to include around each hit.")
    parser.add_argument("--start", help="Optional start time.")
    parser.add_argument("--end", help="Optional end time.")
    parser.add_argument("--list-themes", action="store_true", help="Print default theme names and exit.")
    args = parser.parse_args()

    if args.list_themes:
        for name, keywords in DEFAULT_THEMES.items():
            print(f"{name}: {', '.join(keywords)}")
        return

    keywords = list(DEFAULT_THEMES.get(args.theme, [])) + split_keywords(args.keywords)
    if not keywords:
        raise SystemExit("No keywords found. Choose a known theme or pass --keywords.")

    start = parse_time(args.start)
    end = parse_time(args.end)
    rows = list(read_jsonl(args.input))
    selected = set()
    for index, msg in enumerate(rows):
        if not in_range(msg, start, end):
            continue
        text = message_text(msg)
        hit = [kw for kw in keywords if kw in text]
        if hit:
            left = max(0, index - args.context)
            right = min(len(rows), index + args.context + 1)
            for ctx_index in range(left, right):
                rows[ctx_index]["_theme"] = args.theme
                rows[ctx_index]["_matched_keywords"] = hit if ctx_index == index else []
                rows[ctx_index]["_is_context"] = ctx_index != index
                selected.add(ctx_index)

    count = write_jsonl(args.output, (rows[i] for i in sorted(selected)))
    print(f"theme={args.theme} keywords={len(keywords)} wrote={count} output={args.output}")


if __name__ == "__main__":
    main()
