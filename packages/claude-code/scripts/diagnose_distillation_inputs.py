#!/usr/bin/env python3
"""Diagnose local inputs before running Living Mirror distillation."""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any

from common import configure_stdio, message_conversation, message_sender, message_text, message_time, read_jsonl


TEXT_EXTENSIONS = {".jsonl", ".json", ".csv", ".txt", ".md"}
AUDIO_EXTENSIONS = {".mp3", ".wav", ".m4a", ".flac", ".ogg", ".amr", ".silk", ".aac", ".wma"}
TIME_KEYS = {"timestamp", "time", "datetime", "create_time", "created_at", "date"}
SENDER_KEYS = {"sender", "from", "from_user", "speaker", "name", "nickname", "is_self"}
TEXT_KEYS = {"text", "content", "message", "body", "caption"}
CONVERSATION_KEYS = {"conversation", "talker", "room_name", "chat", "session", "username"}


@dataclass
class FileFinding:
    path: str
    kind: str
    records_checked: int = 0
    usable_text_records: int = 0
    sender_records: int = 0
    conversation_records: int = 0
    earliest: str | None = None
    latest: str | None = None
    fields: list[str] | None = None
    note: str = ""


def iter_files(root: Path) -> list[Path]:
    if root.is_file():
        return [root]
    return [path for path in root.rglob("*") if path.is_file()]


def rel(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def update_time_bounds(value: Any, earliest: Any, latest: Any) -> tuple[Any, Any]:
    if value is None:
        return earliest, latest
    if earliest is None or value < earliest:
        earliest = value
    if latest is None or value > latest:
        latest = value
    return earliest, latest


def diagnose_jsonl(path: Path, root: Path, limit: int) -> FileFinding:
    fields: Counter[str] = Counter()
    records = usable = senders = conversations = 0
    earliest = latest = None
    try:
        for row in read_jsonl(path):
            records += 1
            fields.update(row.keys())
            if message_text(row).strip():
                usable += 1
            if message_sender(row) != "unknown":
                senders += 1
            if message_conversation(row) != "unknown":
                conversations += 1
            earliest, latest = update_time_bounds(message_time(row), earliest, latest)
            if records >= limit:
                break
    except SystemExit as exc:
        return FileFinding(rel(path, root), "jsonl", note=str(exc))
    return FileFinding(
        rel(path, root),
        "jsonl",
        records,
        usable,
        senders,
        conversations,
        earliest.isoformat(sep=" ") if earliest else None,
        latest.isoformat(sep=" ") if latest else None,
        sorted(fields),
    )


def diagnose_json(path: Path, root: Path, limit: int) -> FileFinding:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001 - diagnosis should not crash on one file.
        return FileFinding(rel(path, root), "json", note=f"unreadable json: {exc}")
    rows = data.get("messages") if isinstance(data, dict) else data
    if not isinstance(rows, list):
        return FileFinding(rel(path, root), "json", note="not a list or object.messages")
    fields: Counter[str] = Counter()
    records = usable = senders = conversations = 0
    earliest = latest = None
    for item in rows[:limit]:
        if not isinstance(item, dict):
            continue
        records += 1
        fields.update(item.keys())
        if message_text(item).strip():
            usable += 1
        if message_sender(item) != "unknown":
            senders += 1
        if message_conversation(item) != "unknown":
            conversations += 1
        earliest, latest = update_time_bounds(message_time(item), earliest, latest)
    return FileFinding(
        rel(path, root),
        "json",
        records,
        usable,
        senders,
        conversations,
        earliest.isoformat(sep=" ") if earliest else None,
        latest.isoformat(sep=" ") if latest else None,
        sorted(fields),
    )


def diagnose_csv(path: Path, root: Path, limit: int) -> FileFinding:
    try:
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            fields = list(reader.fieldnames or [])
            records = usable = senders = conversations = 0
            earliest = latest = None
            for row in reader:
                records += 1
                if any(str(row.get(key, "")).strip() for key in TEXT_KEYS):
                    usable += 1
                if any(str(row.get(key, "")).strip() for key in SENDER_KEYS):
                    senders += 1
                if any(str(row.get(key, "")).strip() for key in CONVERSATION_KEYS):
                    conversations += 1
                earliest, latest = update_time_bounds(message_time(row), earliest, latest)
                if records >= limit:
                    break
    except Exception as exc:  # noqa: BLE001
        return FileFinding(rel(path, root), "csv", note=f"unreadable csv: {exc}")
    return FileFinding(
        rel(path, root),
        "csv",
        records,
        usable,
        senders,
        conversations,
        earliest.isoformat(sep=" ") if earliest else None,
        latest.isoformat(sep=" ") if latest else None,
        fields,
    )


def diagnose_plain_text(path: Path, root: Path) -> FileFinding:
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except Exception as exc:  # noqa: BLE001
        return FileFinding(rel(path, root), path.suffix.lower().lstrip("."), note=f"unreadable text: {exc}")
    non_empty = sum(1 for line in text.splitlines() if line.strip())
    return FileFinding(rel(path, root), path.suffix.lower().lstrip("."), non_empty, non_empty, note="plain text; sender/date unknown")


def diagnose_file(path: Path, root: Path, limit: int) -> FileFinding | None:
    suffix = path.suffix.lower()
    if suffix == ".jsonl":
        return diagnose_jsonl(path, root, limit)
    if suffix == ".json":
        return diagnose_json(path, root, limit)
    if suffix == ".csv":
        return diagnose_csv(path, root, limit)
    if suffix in {".txt", ".md"}:
        return diagnose_plain_text(path, root)
    if suffix in AUDIO_EXTENSIONS:
        return FileFinding(rel(path, root), "audio", note="needs local voice ingestion before text distillation")
    return None


def score_quality(total_usable: int, sender_ratio: float, audio_count: int) -> str:
    if total_usable < 50 and audio_count == 0:
        return "light_start"
    if total_usable < 5000:
        return "standard"
    if sender_ratio < 0.6:
        return "standard"
    return "deep"


def render_markdown(root: Path, findings: list[FileFinding]) -> str:
    text_files = [item for item in findings if item.kind != "audio"]
    audio_files = [item for item in findings if item.kind == "audio"]
    usable = sum(item.usable_text_records for item in text_files)
    checked = sum(item.records_checked for item in text_files)
    sender_records = sum(item.sender_records for item in text_files)
    conversation_records = sum(item.conversation_records for item in text_files)
    sender_ratio = sender_records / checked if checked else 0
    conversation_ratio = conversation_records / checked if checked else 0
    earliest_values = [item.earliest for item in text_files if item.earliest]
    latest_values = [item.latest for item in text_files if item.latest]
    mode = score_quality(usable, sender_ratio, len(audio_files))
    risks: list[str] = []
    if sender_ratio < 0.6 and checked:
        risks.append("sender fields are partial or missing")
    if conversation_ratio < 0.4 and checked:
        risks.append("conversation fields are partial or missing")
    if audio_files and usable == 0:
        risks.append("audio needs local voice ingestion before distillation")
    if not earliest_values:
        risks.append("timestamps are missing or unreadable")
    if not risks:
        risks.append("no major structural risk detected")

    lines = [
        "# Living Mirror Data Diagnosis",
        "",
        f"- Root: `{root}`",
        f"- Recommended mode: `{mode}`",
        f"- Usable text records checked: {usable}",
        f"- Audio files needing transcription: {len(audio_files)}",
        f"- Sender coverage: {sender_records}/{checked} ({sender_ratio:.0%})" if checked else "- Sender coverage: unknown",
        f"- Conversation coverage: {conversation_records}/{checked} ({conversation_ratio:.0%})" if checked else "- Conversation coverage: unknown",
        f"- Time span: {min(earliest_values) if earliest_values else 'unknown'} to {max(latest_values) if latest_values else 'unknown'}",
        f"- Main risks: {', '.join(risks)}",
        "",
        "## Files",
        "",
        "| File | Kind | Checked | Usable text | Sender rows | Conversation rows | Time span | Note |",
        "|---|---|---:|---:|---:|---:|---|---|",
    ]
    for item in findings:
        span = f"{item.earliest or '?'} to {item.latest or '?'}" if item.earliest or item.latest else ""
        lines.append(
            f"| `{item.path}` | {item.kind} | {item.records_checked} | {item.usable_text_records} | "
            f"{item.sender_records} | {item.conversation_records} | {span} | {item.note.replace('|', '/')} |"
        )
    lines.extend(
        [
            "",
            "## Next Step",
            "",
        ]
    )
    if audio_files and usable == 0:
        lines.append("1. Run local voice ingestion for the audio files, then merge transcripts.")
    elif mode == "light_start":
        lines.append("1. Start with the cold-start interview in `references/onboarding-and-data-diagnosis.md`.")
    else:
        lines.append("1. Run a small pilot distillation before processing every source.")
    lines.append("2. Confirm consent scope and privacy level before writing quotes into outputs.")
    lines.append("3. Run `quality_check_distillation.py` after the first portrait or theme report.")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    configure_stdio()
    parser = argparse.ArgumentParser(description="Diagnose Living Mirror input files.")
    parser.add_argument("root", type=Path, help="File, raw folder, or workspace to inspect.")
    parser.add_argument("--output", type=Path, help="Markdown report path.")
    parser.add_argument("--json", type=Path, help="Optional JSON report path.")
    parser.add_argument("--sample", type=int, default=2000, help="Rows to inspect per structured file.")
    args = parser.parse_args()

    root = args.root
    search_root = root / "distillation" / "raw" if (root / "distillation" / "raw").exists() else root
    findings = [item for path in iter_files(search_root) if (item := diagnose_file(path, search_root, args.sample))]

    report = render_markdown(search_root, findings)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(report, encoding="utf-8")
    else:
        print(report)

    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(json.dumps([asdict(item) for item in findings], ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()

