#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
from typing import Any

FORBIDDEN_PROMPT_TERMS = (
    "eval",
    "test",
    "judge",
    "experiment",
    "rubric",
    "score",
    "compare",
    "benchmark",
    "candidate",
    "arena",
)
PLAN_KEYS = frozenset(
    {"schema_version", "variant", "candidate_prompt", "criteria", "labels"}
)
CRITERION_KEYS = frozenset({"id", "description", "weight", "hard_gate"})
ID_PATTERN = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
LABEL_PATTERN = re.compile(r"^[a-z][a-z0-9-]{2,31}$")


class PlanError(ValueError):
    pass


def _closed_keys(value: dict[str, Any], expected: frozenset[str], field: str) -> None:
    actual = set(value)
    if actual != expected:
        missing = sorted(expected - actual)
        unknown = sorted(actual - expected)
        details: list[str] = []
        if missing:
            details.append("missing " + ", ".join(missing))
        if unknown:
            details.append("unknown " + ", ".join(unknown))
        raise PlanError(f"{field} has invalid fields: {'; '.join(details)}")


def _bounded_text(value: object, field: str, maximum: int) -> str:
    if not isinstance(value, str) or not value.strip() or value != value.strip():
        raise PlanError(f"{field} must be a non-empty trimmed string")
    if len(value) > maximum:
        raise PlanError(f"{field} exceeds {maximum} characters")
    return value


def _contains_forbidden_prompt_term(prompt: str) -> str | None:
    for term in FORBIDDEN_PROMPT_TERMS:
        if re.search(rf"(?<![a-z0-9]){re.escape(term)}[a-z]*(?![a-z0-9])", prompt.casefold()):
            return term
    return None

def _normalized_text(value: str) -> str:
    return " ".join(re.findall(r"[a-z0-9]+", value.casefold()))



def validate_plan(value: object) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise PlanError("plan must be an object")
    _closed_keys(value, PLAN_KEYS, "plan")
    if value.get("schema_version") != 1:
        raise PlanError("schema_version must be 1")
    _bounded_text(value.get("variant"), "variant", 200)
    prompt = _bounded_text(value.get("candidate_prompt"), "candidate_prompt", 4000)
    forbidden = _contains_forbidden_prompt_term(prompt)
    if forbidden is not None:
        raise PlanError(f"candidate_prompt leaks forbidden control term: {forbidden}")

    criteria = value.get("criteria")
    if not isinstance(criteria, list) or not 3 <= len(criteria) <= 6:
        raise PlanError("criteria must contain 3 to 6 entries")
    criterion_ids: set[str] = set()
    for index, criterion in enumerate(criteria):
        if not isinstance(criterion, dict):
            raise PlanError(f"criteria.{index} must be an object")
        _closed_keys(criterion, CRITERION_KEYS, f"criteria.{index}")
        criterion_id = criterion.get("id")
        if not isinstance(criterion_id, str) or not ID_PATTERN.fullmatch(criterion_id):
            raise PlanError(f"criteria.{index}.id is invalid")
        if criterion_id in criterion_ids:
            raise PlanError(f"duplicate criterion id: {criterion_id}")
        criterion_ids.add(criterion_id)
        description = _bounded_text(
            criterion.get("description"),
            f"criteria.{index}.description",
            300,
        )
        if _normalized_text(description) in _normalized_text(prompt):
            raise PlanError(
                f"candidate_prompt leaks criteria.{index}.description"
            )
        weight = criterion.get("weight")
        if type(weight) is not int or not 1 <= weight <= 5:
            raise PlanError(f"criteria.{index}.weight must be an integer from 1 to 5")
        if type(criterion.get("hard_gate")) is not bool:
            raise PlanError(f"criteria.{index}.hard_gate must be a boolean")

    labels = value.get("labels")
    if not isinstance(labels, list) or not 2 <= len(labels) <= 8:
        raise PlanError("labels must contain 2 to 8 entries")
    for index, label in enumerate(labels):
        if not isinstance(label, str) or not LABEL_PATTERN.fullmatch(label):
            raise PlanError(f"labels.{index} is invalid")
        if any(term in label.casefold() for term in FORBIDDEN_PROMPT_TERMS):
            raise PlanError(f"labels.{index} leaks a control term")
    if len(labels) != len(set(labels)):
        raise PlanError("labels must be unique")
    return value


def load_plan(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise PlanError("plan must be readable UTF-8 JSON") from exc
    return validate_plan(value)


def plan_fingerprint(plan: dict[str, Any]) -> str:
    canonical = json.dumps(plan, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(
        description="Validate a coordinator-only blinded assessment plan."
    )
    result.add_argument("plan", type=Path)
    return result


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        plan = load_plan(args.plan)
    except PlanError as exc:
        print(f"ASSESSMENT PLAN INVALID: {exc}")
        return 2
    output = {
        "criteria_count": len(plan["criteria"]),
        "labels_count": len(plan["labels"]),
        "plan_sha256": plan_fingerprint(plan),
        "schema_version": plan["schema_version"],
        "status": "valid",
    }
    print(json.dumps(output, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
