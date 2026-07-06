#!/usr/bin/env python3
"""Find candidate verbatim messages and print sender/context for verification."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from common import (
    configure_stdio,
    in_range,
    message_conversation,
    message_sender,
    message_text,
    message_time,
    parse_time,
    read_jsonl,
    split_keywords,
)


def main() -> None:
    configure_stdio()
    parser = argparse.ArgumentParser(description="Verify sender for verbatim quotes in JSONL messages.")
    parser.add_argument("--input", required=True, type=Path, help="Merged message JSONL.")
    parser.add_argument("--keyword", action="append", required=True, help="Keyword or comma-separated keywords.")
    parser.add_argument("--start", help="Optional start time.")
    parser.add_argument("--end", help="Optional end time.")
    parser.add_argument("--context", type=int, default=2, help="Neighbor messages to show around each hit.")
    parser.add_argument("--jsonl", action="store_true", help="Emit machine-readable JSONL.")
    args = parser.parse_args()

    keywords = split_keywords(args.keyword)
    start = parse_time(args.start)
    end = parse_time(args.end)
    rows = list(read_jsonl(args.input))

    hits = []
    for index, msg in enumerate(rows):
        if not in_range(msg, start, end):
            continue
        text = message_text(msg)
        matched = [kw for kw in keywords if kw in text]
        if not matched:
            continue
        left = max(0, index - args.context)
        right = min(len(rows), index + args.context + 1)
        hits.append(
            {
                "index": index,
                "matched_keywords": matched,
                "message": msg,
                "context": rows[left:right],
            }
        )

    if args.jsonl:
        for hit in hits:
            print(json.dumps(hit, ensure_ascii=False))
        return

    for hit in hits:
        msg = hit["message"]
        ts = message_time(msg)
        print("=" * 80)
        print(f"hit_index={hit['index']} keywords={','.join(hit['matched_keywords'])}")
        print(f"time={ts} conversation={message_conversation(msg)} sender={message_sender(msg)}")
        print(message_text(msg))
        print("- context -")
        for ctx in hit["context"]:
            ctx_ts = message_time(ctx)
            print(f"[{ctx_ts}] {message_conversation(ctx)} | sender={message_sender(ctx)} | {message_text(ctx)}")
    print(f"\nmatched {len(hits)} messages")


if __name__ == "__main__":
    main()
