#!/usr/bin/env python3
"""Shared helpers for self-distillation scripts."""

from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Iterable, Iterator, List, Optional


def configure_stdio() -> None:
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")


def read_jsonl(path: Path) -> Iterator[Dict[str, Any]]:
    with path.open("r", encoding="utf-8") as handle:
        for line_no, line in enumerate(handle, 1):
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError as exc:
                raise SystemExit(f"{path}:{line_no}: invalid JSON: {exc}") from exc
            if isinstance(obj, dict):
                yield obj


def write_jsonl(path: Path, rows: Iterable[Dict[str, Any]]) -> int:
    count = 0
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
            count += 1
    return count


def parse_time(value: Any) -> Optional[datetime]:
    if value is None:
        return None
    text = str(value).strip()
    if not text:
        return None
    if text.isdigit():
        number = int(text)
        if number > 10_000_000_000:
            number = number / 1000
        return datetime.fromtimestamp(number)
    text = text.replace("Z", "+00:00")
    for fmt in (
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d %H:%M",
        "%Y/%m/%d %H:%M:%S",
        "%Y/%m/%d %H:%M",
        "%Y-%m-%d",
    ):
        try:
            return datetime.strptime(text, fmt)
        except ValueError:
            pass
    try:
        return datetime.fromisoformat(text)
    except ValueError:
        return None


def message_time(msg: Dict[str, Any]) -> Optional[datetime]:
    for key in ("timestamp", "time", "datetime", "create_time", "created_at", "date"):
        parsed = parse_time(msg.get(key))
        if parsed:
            return parsed
    return None


def message_text(msg: Dict[str, Any]) -> str:
    for key in ("text", "content", "message", "body", "caption"):
        value = msg.get(key)
        if value is not None:
            return str(value)
    return ""


def message_sender(msg: Dict[str, Any]) -> str:
    for key in ("sender", "from", "from_user", "speaker", "name", "nickname"):
        value = msg.get(key)
        if value:
            return str(value)
    if msg.get("is_self") is True:
        return "me"
    if msg.get("is_self") is False:
        return "other"
    return "unknown"


def message_conversation(msg: Dict[str, Any]) -> str:
    for key in ("conversation", "talker", "room_name", "chat", "session", "username"):
        value = msg.get(key)
        if value:
            return str(value)
    return "unknown"


def split_keywords(values: Optional[List[str]]) -> List[str]:
    result: List[str] = []
    for value in values or []:
        for part in str(value).split(","):
            part = part.strip()
            if part:
                result.append(part)
    return result


def in_range(msg: Dict[str, Any], start: Optional[datetime], end: Optional[datetime]) -> bool:
    ts = message_time(msg)
    if ts is None:
        return start is None and end is None
    if start and ts < start:
        return False
    if end and ts > end:
        return False
    return True

