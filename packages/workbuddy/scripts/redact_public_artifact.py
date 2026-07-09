#!/usr/bin/env python3
"""Redact a Living Mirror artifact for shareable or public use."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

from common import configure_stdio


PATTERNS = [
    ("EMAIL", re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.IGNORECASE)),
    ("PHONE", re.compile(r"(?<!\d)(?:\+?\d[\d\s\-()]{7,}\d)(?!\d)")),
    ("ID", re.compile(r"(?<![A-Za-z0-9])\d{15,18}[0-9Xx]?(?![A-Za-z0-9])")),
    ("WINDOWS_PATH", re.compile(r"[A-Za-z]:\\(?:[^\\/:*?\"<>|\r\n]+\\)*[^\\/:*?\"<>|\r\n]*")),
    ("URL", re.compile(r"https?://[^\s)>\"]+")),
]


def load_names(values: list[str], name_file: Path | None) -> list[str]:
    names: list[str] = []
    for value in values:
        names.extend(part.strip() for part in value.split(",") if part.strip())
    if name_file and name_file.exists():
        names.extend(line.strip() for line in name_file.read_text(encoding="utf-8").splitlines() if line.strip())
    return sorted(set(names), key=len, reverse=True)


def redact_quotes(text: str, max_chars: int) -> str:
    text = re.sub(r'"([^"\n]{%d,})"' % max_chars, '"<REDACTED_QUOTE>"', text)
    text = re.sub(r"“([^”\n]{%d,})”" % max_chars, "“<REDACTED_QUOTE>”", text)
    text = re.sub(r"「([^」\n]{%d,})」" % max_chars, "「<REDACTED_QUOTE>」", text)
    return text


def redact(text: str, names: list[str], level: str, keep_quotes: bool, max_quote_chars: int) -> str:
    for label, pattern in PATTERNS:
        text = pattern.sub(f"<REDACTED_{label}>", text)
    for index, name in enumerate(names, 1):
        if not name:
            continue
        text = re.sub(re.escape(name), f"<PERSON_{index}>", text, flags=re.IGNORECASE)
    if level == "public" and not keep_quotes:
        text = redact_quotes(text, max_quote_chars)
    header = (
        f"<!-- Living Mirror redaction: level={level}; direct private identifiers removed; "
        "review manually before publishing. -->\n\n"
    )
    return header + text


def main() -> None:
    configure_stdio()
    parser = argparse.ArgumentParser(description="Redact a Living Mirror Markdown/text artifact.")
    parser.add_argument("--input", required=True, type=Path, help="Input Markdown/text artifact.")
    parser.add_argument("--output", required=True, type=Path, help="Redacted output path.")
    parser.add_argument("--level", choices=["shareable", "public"], default="public")
    parser.add_argument("--name", action="append", default=[], help="Name or comma-separated names to redact.")
    parser.add_argument("--name-file", type=Path, help="UTF-8 file with one name per line.")
    parser.add_argument("--keep-quotes", action="store_true", help="Keep long quotes even for public output.")
    parser.add_argument("--max-quote-chars", type=int, default=24, help="Redact quotes at or above this length.")
    args = parser.parse_args()

    names = load_names(args.name, args.name_file)
    source = args.input.read_text(encoding="utf-8")
    output = redact(source, names, args.level, args.keep_quotes, args.max_quote_chars)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(output, encoding="utf-8")
    print(f"Redacted {args.input} -> {args.output}")


if __name__ == "__main__":
    main()

