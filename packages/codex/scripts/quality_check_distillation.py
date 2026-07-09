#!/usr/bin/env python3
"""Check Living Mirror v0.9 self-distillation artifacts."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from common import configure_stdio


REQUIRED_INSIGHT_FIELDS = [
    "id",
    "fact",
    "interpretation",
    "temporary_name",
    "human_dimension",
    "pattern_type",
    "context_weight",
    "evidence",
    "confidence",
    "falsifiability",
    "counter_evidence_index",
    "user_language",
    "status",
]
PRODUCT_FIELDS = ["review_state", "privacy_level", "consent_scope", "action_translation"]

CONFIDENCE_VALUES = {"high", "medium", "low"}
PATTERN_TYPES = {
    "stable_trait",
    "stage_state",
    "special_period_response",
    "relationship_triggered",
    "pending_pattern",
}
HUMAN_DIMENSIONS = {
    "body_energy",
    "shame_defense",
    "desire_action_gap",
    "aesthetic_order",
    "relationship_role_switching",
    "agency_control",
    "attention_learning_rhythm",
    "meaning_narrative",
    "boundary_consent",
    "repair_reconciliation",
    "other",
}


@dataclass
class Finding:
    level: str
    code: str
    message: str


def add(findings: list[Finding], level: str, code: str, message: str) -> None:
    findings.append(Finding(level, code, message))


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"{path}: invalid JSON: {exc}") from exc


def validate_insight_json(insight: dict[str, Any], index: int, findings: list[Finding]) -> None:
    label = str(insight.get("id") or f"insight[{index}]")
    for field in REQUIRED_INSIGHT_FIELDS:
        if field not in insight:
            add(findings, "error", "missing_field", f"{label}: missing `{field}`")

    if insight.get("pattern_type") not in PATTERN_TYPES:
        add(findings, "error", "pattern_type", f"{label}: invalid or missing pattern_type")

    if insight.get("human_dimension") not in HUMAN_DIMENSIONS:
        add(findings, "warning", "human_dimension", f"{label}: human_dimension is missing or not Living Mirror-compatible")

    confidence = insight.get("confidence")
    if not isinstance(confidence, dict):
        add(findings, "error", "confidence", f"{label}: confidence must be an object")
    else:
        for key in ("evidence", "interpretation", "stability"):
            if confidence.get(key) not in CONFIDENCE_VALUES:
                add(findings, "error", "confidence", f"{label}: confidence.{key} must be high/medium/low")

    context = insight.get("context_weight")
    if not isinstance(context, dict):
        add(findings, "error", "context_weight", f"{label}: context_weight must be an object")
    else:
        for key in ("time", "relationship", "body", "environment", "event", "medium"):
            if key not in context:
                add(findings, "warning", "context_weight", f"{label}: context_weight.{key} is missing")

    evidence = insight.get("evidence")
    if not isinstance(evidence, list) or not evidence:
        add(findings, "error", "evidence", f"{label}: evidence must be a non-empty list")
    elif not any(isinstance(item, dict) and item.get("level") in {"verbatim", "artifact"} for item in evidence):
        add(findings, "warning", "evidence", f"{label}: no verbatim/artifact evidence found")

    counter = insight.get("counter_evidence_index")
    if not isinstance(counter, list):
        add(findings, "error", "counter_evidence", f"{label}: counter_evidence_index must be a list")
    else:
        for item in counter:
            if not isinstance(item, dict) or not str(item.get("id", "")).startswith("CE-"):
                add(findings, "warning", "counter_evidence", f"{label}: counter-evidence entry without CE-XXX id")

    user_language = insight.get("user_language")
    if not isinstance(user_language, dict) or "preferred_phrase" not in user_language:
        add(findings, "warning", "user_language", f"{label}: user_language.preferred_phrase is missing")


def validate_product_fields(insight: dict[str, Any], index: int, findings: list[Finding]) -> None:
    label = str(insight.get("id") or f"insight[{index}]")
    for field in PRODUCT_FIELDS:
        if field not in insight:
            add(findings, "warning", "product_field", f"{label}: Living Mirror v0.9 framework field `{field}` is missing")
    if insight.get("privacy_level") not in {None, "private", "shareable", "public"}:
        add(findings, "error", "privacy_level", f"{label}: privacy_level must be private/shareable/public")
    if insight.get("review_state") not in {None, "unreviewed", "confirmed", "corrected", "rejected", "needs_more_evidence"}:
        add(findings, "error", "review_state", f"{label}: review_state is not Living Mirror v0.9-compatible")


def validate_json_artifact(path: Path, product: bool = False) -> list[Finding]:
    data = load_json(path)
    findings: list[Finding] = []
    insights = data.get("insights") if isinstance(data, dict) else data
    if not isinstance(insights, list):
        add(findings, "error", "json_shape", "JSON artifact must be a list of insights or an object with `insights`")
        return findings
    for index, insight in enumerate(insights, 1):
        if isinstance(insight, dict):
            validate_insight_json(insight, index, findings)
            if product:
                validate_product_fields(insight, index, findings)
        else:
            add(findings, "error", "json_shape", f"insight[{index}] is not an object")
    return findings


def has_any(text: str, patterns: list[str]) -> bool:
    return any(re.search(pattern, text, flags=re.IGNORECASE) for pattern in patterns)


def validate_markdown_artifact(path: Path, product: bool = False) -> list[Finding]:
    text = path.read_text(encoding="utf-8")
    findings: list[Finding] = []
    checks = [
        ("evidence", [r"证据[:：]", r"Evidence:?", r"\[verbatim\]", r"\[artifact\]"]),
        ("tri_confidence", [r"evidence\s*=", r"interpretation\s*=", r"stability\s*=", r"三段置信度"]),
        ("context_weight", [r"情境权重", r"Context weight"]),
        ("fact_interpretation_name", [r"事实/解释/命名", r"Fact:", r"fact=.*interpretation=.*temporary_name="]),
        ("counter_evidence", [r"反证索引", r"Counter-evidence", r"CE-\d{3,}"]),
        ("user_language", [r"用户语言", r"User language", r"用户语言词典"]),
        ("pattern_type", [r"模式类型", r"Pattern type", r"stable_trait|stage_state|pending_pattern"]),
        ("falsifiability", [r"可推翻条件", r"Falsifiability"]),
    ]
    if product:
        checks.extend(
            [
                ("privacy_level", [r"Privacy level", r"隐私等级", r"private|shareable|public"]),
                ("review_queue", [r"Review Queue", r"复核队列", r"待用户复核"]),
                ("action_translation", [r"7-Day Experiment", r"行动实验", r"Action Translation"]),
            ]
        )
    for code, patterns in checks:
        if not has_any(text, patterns):
            add(findings, "warning", code, f"{path.name}: missing Living Mirror marker `{code}`")

    insight_like = len(re.findall(r"^(#{2,4}\s+INSIGHT-|#{3,4}\s+|####\s+[A-Z]?\d+)", text, flags=re.MULTILINE))
    if insight_like == 0:
        add(findings, "info", "insight_count", f"{path.name}: no insight heading detected; checked as whole document")

    if "sender" in text.lower() and "已验证" not in text and "verified" not in text.lower():
        add(findings, "warning", "sender_verification", f"{path.name}: sender is mentioned but verification marker is not obvious")

    return findings


def render_markdown(findings: list[Finding]) -> str:
    counts = {level: sum(1 for item in findings if item.level == level) for level in ("error", "warning", "info")}
    lines = [
        "# Living Mirror v0.9 Quality Check",
        "",
        f"- Errors: {counts['error']}",
        f"- Warnings: {counts['warning']}",
        f"- Info: {counts['info']}",
        "",
        "| Level | Code | Message |",
        "|---|---|---|",
    ]
    for item in findings:
        lines.append(f"| {item.level} | {item.code} | {item.message.replace('|', '/')} |")
    if not findings:
        lines.append("| ok | clean | No findings. |")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    configure_stdio()
    parser = argparse.ArgumentParser(description="Check Living Mirror v0.6 artifacts and optional Living Mirror v0.9 framework fields.")
    parser.add_argument("--input", required=True, type=Path, help="Markdown or JSON artifact to check.")
    parser.add_argument("--output", type=Path, help="Optional Markdown report path.")
    parser.add_argument("--json", type=Path, help="Optional JSON findings path.")
    parser.add_argument("--fail-on", choices=["error", "warning", "never"], default="error")
    parser.add_argument("--product", action="store_true", help="Also check v0.9 productization/public workflow fields.")
    args = parser.parse_args()

    if args.input.suffix.lower() == ".json":
        findings = validate_json_artifact(args.input, product=args.product)
    else:
        findings = validate_markdown_artifact(args.input, product=args.product)

    report = render_markdown(findings)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(report, encoding="utf-8")
    else:
        print(report)

    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(
            json.dumps([item.__dict__ for item in findings], ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    has_error = any(item.level == "error" for item in findings)
    has_warning = any(item.level == "warning" for item in findings)
    if args.fail_on == "error" and has_error:
        raise SystemExit(1)
    if args.fail_on == "warning" and (has_error or has_warning):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
