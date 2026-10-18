#!/usr/bin/env python3
"""Aggregate explicit model/teacher ratings; does not infer difficulty from text."""
import argparse
import json
import math
from pathlib import Path

DIMENSIONS = ("prerequisites", "reasoning", "abstraction", "transfer", "representation")
PROCESSES = {"remember", "understand", "apply", "analyze", "evaluate", "create"}
ASPECTS = {"concept", "procedure", "reasoning", "representation", "application"}


def has_text(value):
    return (isinstance(value, str) and bool(value.strip())) or (
        isinstance(value, dict) and bool(value)
        and all(isinstance(v, str) and v.strip() for v in value.values()))


def assess(value):
    if not isinstance(value, dict) or value.get("status") != "estimated":
        raise ValueError("assessment.status must be estimated; empirical statistics belong in a separate field")
    ratings, evidence = value.get("ratings", {}), value.get("evidence", {})
    if not isinstance(ratings, dict) or not isinstance(evidence, dict):
        raise ValueError("ratings and evidence must be objects")
    for name in DIMENSIONS:
        if type(ratings.get(name)) is not int or not 1 <= ratings[name] <= 5:
            raise ValueError(f"ratings.{name} must be an integer 1–5")
        if not has_text(evidence.get(name)):
            raise ValueError(f"evidence.{name} is required")
    for name in ("audience", "rationale"):
        if not has_text(value.get(name)):
            raise ValueError(f"assessment.{name} is required")
    confidence = value.get("confidence")
    if type(confidence) not in (int, float) or not math.isfinite(confidence) or not 0 <= confidence <= 1:
        raise ValueError("assessment.confidence must be finite and within 0–1")
    processes = value.get("cognitive_processes")
    if not isinstance(processes, list) or not processes or any(not isinstance(x, str) or x not in PROCESSES for x in processes):
        raise ValueError("cognitive_processes must contain supported process labels")
    knowledge = value.get("knowledge_dimensions")
    if not isinstance(knowledge, list) or not knowledge:
        raise ValueError("knowledge_dimensions must not be empty")
    for item in knowledge:
        if (not isinstance(item, dict) or not isinstance(item.get("unit_id"), str) or not item["unit_id"].strip()
                or not isinstance(item.get("aspect"), str) or item["aspect"] not in ASPECTS or not has_text(item.get("evidence"))):
            raise ValueError("each knowledge dimension needs unit_id, aspect and evidence")
    mean = sum(ratings[name] for name in DIMENSIONS) / len(DIMENSIONS)
    level = min(5, max(1, math.floor(mean + 0.5)))
    return {**value, "mean_rating": round(mean, 2), "difficulty_level": level,
            "method": "equal-weight mean of five explicit 1–5 ratings; half-up level"}


def report(workbook):
    rows = []
    for group in ("units", "mocks"):
        for owner in workbook.get(group, []):
            for question in owner.get("questions", []):
                try:
                    result = assess(question.get("assessment"))
                except ValueError as exc:
                    raise ValueError(f"{question.get('id', '?')}: {exc}") from exc
                rows.append({"id": question["id"], "owner_id": owner["id"],
                             "mother_id": question.get("mother_id"),
                             "transformation": question.get("transformation"), **result})
    return {"note": "Teaching estimates, not measured success rates or content verification.", "questions": rows}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("workbook", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        data = json.loads(args.workbook.read_text(encoding="utf-8-sig"))
        result = json.dumps(report(data), ensure_ascii=False, indent=2)
        if args.output:
            args.output.write_text(result + "\n", encoding="utf-8")
        else:
            print(result)
    except (OSError, ValueError, TypeError, AttributeError, KeyError) as exc:
        print(f"ERROR: {exc}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
