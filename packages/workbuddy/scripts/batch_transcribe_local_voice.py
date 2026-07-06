from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Iterable


DEFAULT_EXTENSIONS = {
    ".wav",
    ".mp3",
    ".m4a",
    ".flac",
    ".ogg",
    ".opus",
    ".aac",
    ".amr",
    ".wma",
    ".mp4",
    ".mov",
}


def now() -> str:
    return datetime.now().isoformat(timespec="seconds")


def load_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return default


def atomic_write_json(path: Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    os.replace(tmp, path)


def append_jsonl(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, ensure_ascii=False) + "\n")


def file_signature(path: Path) -> str:
    stat = path.stat()
    raw = f"{path.resolve()}|{stat.st_size}|{int(stat.st_mtime)}"
    return hashlib.sha1(raw.encode("utf-8", errors="replace")).hexdigest()


def iter_audio(inputs: Iterable[str], recursive: bool, extensions: set[str]) -> list[Path]:
    found: list[Path] = []
    for item in inputs:
        path = Path(item).expanduser()
        if path.is_file() and path.suffix.lower() in extensions:
            found.append(path)
        elif path.is_dir():
            iterator = path.rglob("*") if recursive else path.glob("*")
            found.extend(p for p in iterator if p.is_file() and p.suffix.lower() in extensions)
    return sorted(dict.fromkeys(p.resolve() for p in found), key=lambda p: str(p).lower())


def normalize_result(raw) -> str:
    if isinstance(raw, list):
        parts = []
        for item in raw:
            if isinstance(item, dict):
                text = item.get("text") or item.get("sentence") or ""
                if text:
                    parts.append(str(text))
            elif item:
                parts.append(str(item))
        return "\n".join(parts).strip()
    if isinstance(raw, dict):
        return str(raw.get("text") or raw.get("sentence") or "").strip()
    return str(raw or "").strip()


def build_model(args):
    from funasr import AutoModel

    model_name = args.model or os.environ.get("LIVING_MIRROR_ASR_MODEL") or os.environ.get("FUNASR_MODEL")
    if not model_name:
        raise SystemExit(
            "Local ASR model is not configured. Pass --model <name-or-local-path> "
            "or set LIVING_MIRROR_ASR_MODEL. This skill does not hardcode or bundle a model."
        )

    kwargs = {
        "model": model_name,
        "device": args.device,
    }
    if args.vad_model:
        kwargs["vad_model"] = args.vad_model
    if args.punc_model:
        kwargs["punc_model"] = args.punc_model
    if args.spk_model:
        kwargs["spk_model"] = args.spk_model
    return AutoModel(**kwargs)


def transcribe_one(model, path: Path, args) -> tuple[str, object]:
    generate_kwargs = {
        "input": str(path),
        "batch_size_s": args.batch_size_s,
    }
    if args.language:
        generate_kwargs["language"] = args.language
    if args.use_itn:
        generate_kwargs["use_itn"] = True
    raw = model.generate(**generate_kwargs)
    return normalize_result(raw), raw


def write_summary(path: Path, records: list[dict]) -> None:
    lines = ["# Local Voice Transcription Summary", ""]
    for index, record in enumerate(records, start=1):
        lines.append(f"## {index}. {record['name']}")
        lines.append("")
        lines.append(f"- Source: `{record['source']}`")
        lines.append(f"- Completed: {record['completed_at']}")
        lines.append("")
        lines.append(record.get("text") or "")
        lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Batch transcribe local audio with the Living Mirror local ASR adapter.")
    parser.add_argument("--input", nargs="+", required=True, help="Audio file(s) or folder(s).")
    parser.add_argument("--output", required=True, help="Output directory.")
    parser.add_argument("--model", default=None, help="Local ASR model name or local path. Can also be set with LIVING_MIRROR_ASR_MODEL.")
    parser.add_argument("--vad-model", default=None, help="Optional VAD model for the local ASR adapter.")
    parser.add_argument("--punc-model", default=None, help="Optional punctuation model for the local ASR adapter.")
    parser.add_argument("--spk-model", default=None, help="Optional speaker model for the local ASR adapter.")
    parser.add_argument("--device", default="cpu", help="ASR device, usually cpu or cuda.")
    parser.add_argument("--language", default=None, help="Optional language hint supported by the model.")
    parser.add_argument("--batch-size-s", type=int, default=60, help="ASR batch size in seconds.")
    parser.add_argument("--recursive", action="store_true", help="Scan input folders recursively.")
    parser.add_argument("--resume", action="store_true", help="Skip completed file signatures from manifest.json.")
    parser.add_argument("--limit", type=int, default=None, help="Transcribe at most N files for smoke tests.")
    parser.add_argument("--extensions", default=",".join(sorted(DEFAULT_EXTENSIONS)), help="Comma-separated extensions.")
    parser.add_argument("--use-itn", action="store_true", help="Enable inverse text normalization when supported.")
    return parser.parse_args()


def main() -> int:
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")

    args = parse_args()
    out_dir = Path(args.output)
    out_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = out_dir / "manifest.json"
    transcript_path = out_dir / "transcripts.jsonl"
    errors_path = out_dir / "errors.jsonl"
    summary_path = out_dir / "summary.md"
    run_summary_path = out_dir / "run_summary.json"

    extensions = {ext.strip().lower() if ext.strip().startswith(".") else "." + ext.strip().lower() for ext in args.extensions.split(",") if ext.strip()}
    audio_files = iter_audio(args.input, args.recursive, extensions)
    if args.limit is not None:
        audio_files = audio_files[: args.limit]

    manifest = load_json(manifest_path, {"completed": {}})
    completed = manifest.setdefault("completed", {})
    records: list[dict] = []
    start = time.time()

    print(f"[{now()}] Found {len(audio_files)} audio file(s).", flush=True)
    model = build_model(args)

    succeeded = 0
    failed = 0
    skipped = 0

    for idx, path in enumerate(audio_files, start=1):
        sig = file_signature(path)
        if args.resume and sig in completed:
            skipped += 1
            continue
        print(f"[{now()}] [{idx}/{len(audio_files)}] {path}", flush=True)
        try:
            text, raw = transcribe_one(model, path, args)
            record = {
                "id": sig,
                "source": str(path),
                "name": path.name,
                "size": path.stat().st_size,
                "completed_at": now(),
                "model": args.model or os.environ.get("LIVING_MIRROR_ASR_MODEL") or os.environ.get("FUNASR_MODEL"),
                "device": args.device,
                "text": text,
                "raw": raw,
            }
            append_jsonl(transcript_path, record)
            completed[sig] = {
                "source": str(path),
                "completed_at": record["completed_at"],
                "text_length": len(text),
            }
            records.append(record)
            succeeded += 1
            atomic_write_json(manifest_path, manifest)
        except Exception as exc:  # pragma: no cover - depends on local audio/model
            failed += 1
            append_jsonl(errors_path, {"source": str(path), "time": now(), "error": repr(exc)})

    existing_records = []
    if transcript_path.exists():
        for line in transcript_path.read_text(encoding="utf-8").splitlines():
            try:
                existing_records.append(json.loads(line))
            except json.JSONDecodeError:
                pass
    write_summary(summary_path, existing_records)

    run_summary = {
        "finished_at": now(),
        "elapsed_seconds": round(time.time() - start, 2),
        "input_count": len(audio_files),
        "succeeded": succeeded,
        "failed": failed,
        "skipped": skipped,
        "model": args.model or os.environ.get("LIVING_MIRROR_ASR_MODEL") or os.environ.get("FUNASR_MODEL"),
        "device": args.device,
        "outputs": {
            "manifest": str(manifest_path),
            "transcripts": str(transcript_path),
            "errors": str(errors_path),
            "summary": str(summary_path),
        },
    }
    atomic_write_json(run_summary_path, run_summary)
    print(json.dumps(run_summary, ensure_ascii=False, indent=2), flush=True)
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
