#!/usr/bin/env python3
"""Filter messages by time range."""

from __future__ import annotations

import argparse
from pathlib import Path

from common import configure_stdio, in_range, parse_time, read_jsonl, write_jsonl


def main() -> None:
    configure_stdio()
    parser = argparse.ArgumentParser(description="Filter JSONL messages by start/end time.")
    parser.add_argument("--input", required=True, type=Path, help="Merged message JSONL.")
    parser.add_argument("--output", required=True, type=Path, help="Filtered output JSONL.")
    parser.add_argument("--start", help="Start time, e.g. 2024-01-01 or 2024-01-01T00:00:00.")
    parser.add_argument("--end", help="End time, e.g. 2024-12-31.")
    args = parser.parse_args()

    start = parse_time(args.start)
    end = parse_time(args.end)
    if args.start and not start:
        raise SystemExit(f"invalid --start: {args.start}")
    if args.end and not end:
        raise SystemExit(f"invalid --end: {args.end}")

    count = write_jsonl(args.output, (msg for msg in read_jsonl(args.input) if in_range(msg, start, end)))
    print(f"wrote {count} messages to {args.output}")


if __name__ == "__main__":
    main()

