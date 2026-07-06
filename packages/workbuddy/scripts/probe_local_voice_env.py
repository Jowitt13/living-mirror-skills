from __future__ import annotations

import importlib.util
import json
import os
import platform
import shutil
import sys
from datetime import datetime


ASR_BACKEND_MODULE = "funasr"


def module_status(name: str) -> dict:
    spec = importlib.util.find_spec(name)
    status = {"available": spec is not None}
    if spec is None:
        return status
    try:
        module = __import__(name)
        status["version"] = getattr(module, "__version__", None)
    except Exception as exc:  # pragma: no cover - diagnostic path
        status["import_error"] = repr(exc)
    return status


def torch_status() -> dict:
    if importlib.util.find_spec("torch") is None:
        return {"available": False}
    try:
        import torch

        payload = {
            "available": True,
            "version": getattr(torch, "__version__", None),
            "cuda_available": bool(torch.cuda.is_available()),
            "cuda_device_count": int(torch.cuda.device_count()) if torch.cuda.is_available() else 0,
        }
        if torch.cuda.is_available():
            payload["cuda_device_name"] = torch.cuda.get_device_name(0)
        return payload
    except Exception as exc:  # pragma: no cover - diagnostic path
        return {"available": True, "import_error": repr(exc)}


def main() -> int:
    result = {
        "checked_at": datetime.now().isoformat(timespec="seconds"),
        "python": sys.executable,
        "python_version": sys.version,
        "platform": platform.platform(),
        "cwd": os.getcwd(),
        "adapter": {
            "type": "local_asr",
            "python_module": ASR_BACKEND_MODULE,
            "model_env": "LIVING_MIRROR_ASR_MODEL",
            "model_configured": bool(os.environ.get("LIVING_MIRROR_ASR_MODEL") or os.environ.get("FUNASR_MODEL")),
        },
        "modules": {
            ASR_BACKEND_MODULE: module_status(ASR_BACKEND_MODULE),
            "modelscope": module_status("modelscope"),
            "soundfile": module_status("soundfile"),
            "librosa": module_status("librosa"),
            "pydub": module_status("pydub"),
        },
        "torch": torch_status(),
        "binaries": {
            "ffmpeg": shutil.which("ffmpeg"),
            "ffprobe": shutil.which("ffprobe"),
        },
        "env": {
            "MODELSCOPE_CACHE": os.environ.get("MODELSCOPE_CACHE"),
            "HF_HOME": os.environ.get("HF_HOME"),
            "CUDA_VISIBLE_DEVICES": os.environ.get("CUDA_VISIBLE_DEVICES"),
            "LIVING_MIRROR_ASR_MODEL": os.environ.get("LIVING_MIRROR_ASR_MODEL"),
        },
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["modules"][ASR_BACKEND_MODULE]["available"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
