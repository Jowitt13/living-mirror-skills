#!/usr/bin/env python3
"""Merge text messages and voice transcriptions into one JSONL timeline."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, Iterable, Tuple

from common import configure_stdio, message_time, read_jsonl, write_jsonl


def load_voice_cache(path: Path) -> Dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, dict):
        return data
    if isinstance(data, list):
        cache: Dict[str, Any] = {}
        for item in data:
            if not isinstance(item, dict):
                continue
            for key in ("id", "msg_id", "local_id", "voice_id"):
                if item.get(key) is not None:
                    cache[str(item[key])] = item
        return cache
    raise SystemExit("voice file must be a JSON object or array")


def candidate_keys(msg: Dict[str, Any]) -> Iterable[str]:
    for fields in (("username", "local_id"), ("talker", "local_id"), ("conversation", "local_id")):
        if all(msg.get(field) is not None for field in fields):
            yield json.dumps([msg[field] for field in fields], ensure_ascii=False)
    for key in ("id", "msg_id", "local_id", "voice_id"):
        if msg.get(key) is not None:
            yield str(msg[key])


def is_voice(msg: Dict[str, Any]) -> bool:
    value = str(msg.get("type", "")).lower()
    if value in {"34", "voice", "audio"}:
        return True
    text = str(msg.get("text", msg.get("content", "")))
    return text in {"[语音]", "[voice]", "[audio]"}


def extract_voice_text(entry: Any) -> Tuple[str, str]:
    if isinstance(entry, dict):
        for key in ("text", "transcript", "content", "message"):
            if entry.get(key):
                return str(entry[key]), str(entry.get("backend", entry.get("source", "unknown")))
    elif isinstance(entry, str):
        return entry, "unknown"
    return "", "unknown"


def main() -> None:
    configure_stdio()
    parser = argparse.ArgumentParser(description="Merge messages JSONL and voice transcription JSON.")
    parser.add_argument("--messages", required=True, type=Path, help="Input message JSONL.")
    parser.add_argument("--voice", required=True, type=Path, help="Voice transcription JSON object or array.")
    parser.add_argument("--output", required=True, type=Path, help="Output merged JSONL.")
    parser.add_argument("--sort", action="store_true", help="Sort output by message timestamp.")
    args = parser.parse_args()

    voice_cache = load_voice_cache(args.voice)
    rows = []
    total = voice_total = merged = missing = 0

    for msg in read_jsonl(args.messages):
        total += 1
        if is_voice(msg):
            voice_total += 1
            entry = next((voice_cache[key] for key in candidate_keys(msg) if key in voice_cache), None)
            text, backend = extract_voice_text(entry)
            if text:
                msg["text"] = text
                msg["voice_transcribed"] = True
                msg["voice_backend"] = backend
                merged += 1
            else:
                msg["text"] = "[语音-未转录]"
                msg["voice_transcribed"] = False
                missing += 1
        rows.append(msg)

    if args.sort:
        rows.sort(key=lambda item: message_time(item) or "")

    write_jsonl(args.output, rows)
    print(f"messages={total} voice={voice_total} merged={merged} missing={missing} output={args.output}")


if __name__ == "__main__":
    main()
