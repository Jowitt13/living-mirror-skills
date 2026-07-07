#!/usr/bin/env python3
"""Batch-transcribe WeChat .silk voice messages with a local FunASR model.

Part of Living Mirror's Local Voice Ingestion module. This is the WeChat-SILK
specialization: SILK is WeChat's native voice codec and must be decoded before
any ASR model can read it.

Performance design (why this is fast):
1. SILK decode with `pilk` directly to 16 kHz PCM — no manual resampling step.
   `pilk.decode(silk, pcm, 16000)` yields correct 16k data in one call.
2. Multiprocess pre-decode: all SILK files are decoded to WAV on CPU cores in
   parallel, so the GPU never waits on the CPU decode stage.
3. Single-process batched FunASR inference: the main process feeds batches of
   WAV paths to `model.generate(input=[...])`, saturating the GPU.

Environment caveats (learned the hard way, Python 3.13 + Windows):
- FunASR depends on `editdistance`, which has no prebuilt wheel for py3.13 and
  fails to compile; pip then rolls back the whole install. Fix: install all
  other deps first, then `pip install funasr --no-deps` (editdistance is only
  used for WER scoring, not for transcription).
- FunASR also needs `torchaudio` at import time; install torch + torchaudio cu124.
- `pilk` is the SILK decoder; install via pip.

Usage:
    LIVING_MIRROR_ASR_MODEL="paraformer-zh" \
        python scripts/batch_transcribe_wechat_silk.py \
        --input "D:/wechat/voice" --output raw/voice-transcripts --resume

The script does NOT hardcode a model. Supply one with --model or
LIVING_MIRROR_ASR_MODEL.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import time
import wave
import tempfile
import glob
from datetime import datetime
from pathlib import Path
from multiprocessing import Pool

SILK_NAME_RE = re.compile(
    r'^(\d+)_(wxid_\w+)_(wxid_\w+)_(\d+)_(\d{10})_(\d+)\.silk$'
)


def now() -> str:
    return datetime.now().isoformat(timespec="seconds")


def atomic_write_json(path: Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    os.replace(tmp, path)


def append_jsonl(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as h:
        h.write(json.dumps(payload, ensure_ascii=False) + "\n")


def file_signature(path: Path) -> str:
    stat = path.stat()
    raw = f"{path.resolve()}|{stat.st_size}|{int(stat.st_mtime)}"
    return hashlib.sha1(raw.encode("utf-8", errors="replace")).hexdigest()


def _cuda_available() -> bool:
    try:
        import torch
        return torch.cuda.is_available()
    except Exception:
        return False


def decode_worker(args):
    """CPU stage: one SILK file -> 16k WAV. Returns wav path or None."""
    path_str, wav_dir = args
    import pilk
    src = Path(path_str)
    wav_path = os.path.join(wav_dir, src.name[:-5] + ".wav")
    try:
        data = src.read_bytes()
        silk_data = data[1:] if data[0] == 0x02 else data
        if not silk_data.startswith(b'#!SILK_V3'):
            return None
        tmp_silk = tempfile.mktemp(suffix=".silk")
        tmp_pcm = tempfile.mktemp(suffix=".pcm")
        with open(tmp_silk, 'wb') as f:
            f.write(silk_data)
        pilk.decode(tmp_silk, tmp_pcm, 16000)  # direct 16k, no resampling
        pcm = Path(tmp_pcm).read_bytes()
        try:
            os.unlink(tmp_silk); os.unlink(tmp_pcm)
        except Exception:
            pass
        if not pcm or len(pcm) < 44:
            return None
        with wave.open(wav_path, 'wb') as wf:
            wf.setnchannels(1); wf.setframerate(16000); wf.setsampwidth(2)
            wf.writeframes(pcm)
        return wav_path
    except Exception:
        return None


def normalize_result(raw) -> str:
    if isinstance(raw, list):
        parts = []
        for item in raw:
            if isinstance(item, dict):
                t = item.get("text") or item.get("sentence") or ""
                if t:
                    parts.append(str(t))
            elif item:
                parts.append(str(item))
        return "\n".join(parts).strip()
    if isinstance(raw, dict):
        return str(raw.get("text") or raw.get("sentence") or "").strip()
    return str(raw or "").strip()


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Batch transcribe WeChat SILK voice with local FunASR.")
    p.add_argument("--input", nargs="+", required=True, help="SILK file(s) or folder(s).")
    p.add_argument("--output", required=True, help="Output directory.")
    p.add_argument("--model", default=None, help="FunASR model name/path. Or set LIVING_MIRROR_ASR_MODEL.")
    p.add_argument("--vad-model", default="fsmn-vad")
    p.add_argument("--punc-model", default="ct-punc")
    p.add_argument("--device", default="cuda:0" if _cuda_available() else "cpu")
    p.add_argument("--recursive", action="store_true")
    p.add_argument("--resume", action="store_true", help="Skip completed voice_ids from manifest.")
    p.add_argument("--workers", type=int, default=max(1, (os.cpu_count() or 4) - 2),
                   help="CPU workers for SILK decode.")
    p.add_argument("--batch-size", type=int, default=32, help="FunASR inference batch size.")
    p.add_argument("--limit", type=int, default=None, help="Transcribe at most N files (smoke test).")
    p.add_argument("--me-wxid", default=None, help="Your wxid; if set, is_self inferred from filename.")
    return p.parse_args()


def main() -> int:
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    args = parse_args()
    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)
    manifest_path = out / "manifest.json"
    transcript_path = out / "transcripts.jsonl"
    summary_path = out / "summary.md"
    run_summary_path = out / "run_summary.json"

    # collect silk files
    exts = {".silk"}
    files = []
    for item in args.input:
        p = Path(item).expanduser()
        if p.is_file() and p.suffix.lower() in exts:
            files.append(p)
        elif p.is_dir():
            it = p.rglob("*") if args.recursive else p.glob("*")
            files.extend(q for q in it if q.is_file() and q.suffix.lower() in exts)
    files = sorted(dict.fromkeys(f.resolve() for f in files), key=lambda f: str(f).lower())
    if args.limit is not None:
        files = files[: args.limit]

    manifest = {}
    if manifest_path.exists():
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except Exception:
            manifest = {}
    completed = manifest.setdefault("completed", {})

    meta_map = {}
    todo = []
    for f in files:
        m = SILK_NAME_RE.match(f.name)
        vid = f.stem
        ts = int(m.group(5)) if m else int(f.stat().st_mtime)
        sender = m.group(2) if m else None
        is_self = (sender == args.me_wxid) if (m and args.me_wxid) else None
        meta_map[vid] = {
            "voice_id": vid,
            "timestamp": ts,
            "sender_wxid": sender,
            "is_self": is_self,
            "time": datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S"),
        }
        sig = file_signature(f)
        if args.resume and (vid in completed or sig in completed):
            continue
        todo.append(f)

    print(f"[{now()}] {len(todo)} SILK files to decode (of {len(files)} total)", flush=True)

    # stage 1: multiprocess pre-decode SILK -> WAV (CPU parallel, GPU idle)
    wav_dir = tempfile.mkdtemp(prefix="silk_wav_")
    t1 = time.time()
    with Pool(args.workers) as pool:
        wav_list = pool.map(decode_worker, [(str(f), wav_dir) for f in todo])
    wav_list = [w for w in wav_list if w]
    print(f"[{now()}] decoded {len(wav_list)} ok in {(time.time()-t1)/60:.1f}min", flush=True)

    # stage 2: single-process batched FunASR inference
    from funasr import AutoModel
    model_name = args.model or os.environ.get("LIVING_MIRROR_ASR_MODEL")
    if not model_name:
        raise SystemExit("No ASR model. Pass --model or set LIVING_MIRROR_ASR_MODEL.")
    model = AutoModel(
        model=model_name,
        vad_model=args.vad_model,
        punc_model=args.punc_model,
        device=args.device,
        ngpu=0 if args.device == "cpu" else 1,
    )

    succeeded = failed = 0
    start = time.time()
    for i in range(0, len(wav_list), args.batch_size):
        batch = wav_list[i:i + args.batch_size]
        try:
            res = model.generate(input=batch, batch_size_s=300)
            for wav, r in zip(batch, res):
                vid = Path(wav).stem
                text = normalize_result(r)
                rec = {**meta_map.get(vid, {"voice_id": vid}), "transcript": text,
                       "model": model_name, "device": args.device}
                append_jsonl(transcript_path, rec)
                completed[vid] = {"completed_at": now(), "text_length": len(text)}
                if text:
                    succeeded += 1
                else:
                    failed += 1
        except Exception:
            for wav in batch:
                try:
                    r = model.generate(input=wav, batch_size_s=300)
                    text = normalize_result(r)
                    vid = Path(wav).stem
                    rec = {**meta_map.get(vid, {"voice_id": vid}), "transcript": text,
                           "model": model_name, "device": args.device}
                    append_jsonl(transcript_path, rec)
                    completed[vid] = {"completed_at": now(), "text_length": len(text)}
                    if text:
                        succeeded += 1
                    else:
                        failed += 1
                except Exception as e2:
                    vid = Path(wav).stem
                    append_jsonl(transcript_path, {**meta_map.get(vid, {"voice_id": vid}),
                                  "transcript": "", "error": repr(e2)[:200]})
                    failed += 1
        atomic_write_json(manifest_path, manifest)

    for w in wav_list:
        try:
            os.unlink(w)
        except Exception:
            pass

    records = []
    if transcript_path.exists():
        for line in transcript_path.read_text(encoding="utf-8").splitlines():
            try:
                records.append(json.loads(line))
            except Exception:
                pass
    lines = ["# WeChat SILK Transcription Summary", ""]
    for i, r in enumerate(records, 1):
        lines.append(f"## {i}. {r.get('voice_id')}")
        lines.append("")
        lines.append(f"- Time: {r.get('time')}")
        lines.append(f"- Transcript: {r.get('transcript') or ''}")
        lines.append("")
    summary_path.write_text("\n".join(lines), encoding="utf-8")

    run_summary = {
        "finished_at": now(),
        "elapsed_seconds": round(time.time() - start, 2),
        "input_count": len(files),
        "decoded": len(wav_list),
        "succeeded": succeeded,
        "failed": failed,
        "model": model_name,
        "outputs": {
            "manifest": str(manifest_path),
            "transcripts": str(transcript_path),
            "summary": str(summary_path),
        },
    }
    atomic_write_json(run_summary_path, run_summary)
    print(json.dumps(run_summary, ensure_ascii=False, indent=2), flush=True)
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
