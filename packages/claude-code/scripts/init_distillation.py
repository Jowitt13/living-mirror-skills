#!/usr/bin/env python3
"""Initialize a reusable self-distillation workspace."""

from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path

from common import configure_stdio


def write_if_missing(path: Path, content: str) -> None:
    if not path.exists():
        path.write_text(content, encoding="utf-8")


def main() -> None:
    configure_stdio()
    parser = argparse.ArgumentParser(description="Initialize distillation directory structure.")
    parser.add_argument("workspace", type=Path, help="Workspace path where distillation/ will be created.")
    parser.add_argument("--version", default="v0.9", help="Initial portrait version.")
    args = parser.parse_args()

    root = args.workspace / "distillation"
    for name in ("raw", "v2", "reviews", "actions", "exports", "archive"):
        (root / name).mkdir(parents=True, exist_ok=True)

    today = datetime.now().strftime("%Y-%m-%d")
    portrait_name = f"self-portrait-{today[:7]}.md"

    write_if_missing(root / "conflicts.md", "# 矛盾待验证区\n\n> 状态：🟢 已解决 / 🟡 待验证 / 🔴 矛盾加剧\n\n")
    write_if_missing(root / "corrections.md", "# 纠正记录\n\n> 用户说\"我不是这样\"时立即修正。\n\n")
    write_if_missing(root / "changelog.md", f"# 变更日志\n\n## {today} {args.version}\n- 初始化 distillation 目录。\n")
    write_if_missing(root / portrait_name, f"# 自画像 · {today[:7]}\n\n> 待蒸馏。\n")

    manifest = root / "manifest.json"
    if not manifest.exists():
        manifest.write_text(
            json.dumps(
                {
                    "current_version": args.version,
                    "current_version_file": portrait_name,
                    "framework_version": "Living Mirror v0.9",
                    "updated_at": datetime.now().isoformat(timespec="seconds"),
                    "versions": [],
                    "data_sources": {},
                    "consent_scope": {
                        "source_scope": "unset",
                        "time_scope": "unset",
                        "relationship_scope": "unset",
                        "theme_scope": "unset",
                        "output_scope": "private",
                    },
                },
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

    print(f"Initialized: {root}")


if __name__ == "__main__":
    main()

