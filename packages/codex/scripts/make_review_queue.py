#!/usr/bin/env python3
"""Create a review queue from a Living Mirror portrait or theme report."""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path

from common import configure_stdio


TRIGGERS = [
    ("low_confidence", re.compile(r"\b(low|低)\b|置信度[:：].*(低|low)", re.IGNORECASE)),
    ("pending", re.compile(r"待验证|pending_pattern|pending", re.IGNORECASE)),
    ("counter_evidence", re.compile(r"CE-\d{3,}|反证", re.IGNORECASE)),
    ("rename", re.compile(r"待用户命名|user language|用户语言|temporary_name", re.IGNORECASE)),
    ("correction", re.compile(r"Correction|CORR-\d{3,}|推翻|纠正", re.IGNORECASE)),
]


@dataclass
class QueueItem:
    heading: str
    code: str
    line: str


def current_heading(line: str, previous: str) -> str:
    match = re.match(r"^(#{1,4})\s+(.+)$", line)
    if match:
        return match.group(2).strip()
    return previous


def extract_items(text: str, limit: int) -> list[QueueItem]:
    items: list[QueueItem] = []
    heading = "Document"
    seen: set[tuple[str, str, str]] = set()
    for raw_line in text.splitlines():
        line = raw_line.strip()
        heading = current_heading(line, heading)
        if not line or line.startswith("|---"):
            continue
        for code, pattern in TRIGGERS:
            if pattern.search(line):
                key = (heading, code, line)
                if key not in seen:
                    seen.add(key)
                    items.append(QueueItem(heading, code, line[:220]))
                break
        if len(items) >= limit:
            break
    return items


def question_for(item: QueueItem) -> str:
    if item.code == "low_confidence":
        return "这条低置信度洞察更像事实、解释、还是暂时命名？需要保留、收窄，还是删除？"
    if item.code == "pending":
        return "这条待验证模式有没有反例、特殊时期影响，或更准确的用户语言？"
    if item.code == "counter_evidence":
        return "这个反证会削弱、收窄、推翻洞察，还是生成新的 CONFLICT？"
    if item.code == "rename":
        return "这个命名像你自己的话吗？如果不像，你会怎么叫它？"
    if item.code == "correction":
        return "这条 Correction 是否已经同步到自画像、conflicts 和 changelog？"
    return "这条需要用户确认、否定或补充什么？"


def render(items: list[QueueItem]) -> str:
    lines = [
        "# Living Mirror Review Queue",
        "",
        "> Use this queue with the user before promoting uncertain insights into the main portrait.",
        "",
    ]
    if not items:
        lines.append("No obvious review items found. Still ask the user to review the highest-impact insights.")
        lines.append("")
        return "\n".join(lines)
    for index, item in enumerate(items, 1):
        lines.extend(
            [
                f"## RQ-{index:03d}: {item.heading}",
                "",
                f"- Trigger: `{item.code}`",
                f"- Source line: {item.line}",
                f"- Question: {question_for(item)}",
                "- User response:",
                "- Update needed: none / Correction / rename / counter-evidence / conflict update / confidence change",
                "",
            ]
        )
    return "\n".join(lines)


def main() -> None:
    configure_stdio()
    parser = argparse.ArgumentParser(description="Create a Living Mirror user review queue.")
    parser.add_argument("--input", required=True, type=Path, help="Markdown portrait or theme report.")
    parser.add_argument("--output", type=Path, help="Output Markdown path.")
    parser.add_argument("--limit", type=int, default=40)
    args = parser.parse_args()

    text = args.input.read_text(encoding="utf-8")
    report = render(extract_items(text, args.limit))
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(report, encoding="utf-8")
    else:
        print(report)


if __name__ == "__main__":
    main()

