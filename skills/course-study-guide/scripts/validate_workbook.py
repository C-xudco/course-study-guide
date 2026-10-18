#!/usr/bin/env python3
"""Check the course-study-guide JSON model; no writes or third-party packages."""
import argparse
import json
import math
from pathlib import Path
from assess_questions import assess, has_text
from question_plan import resolve, family_errors


def validate(data):
    if not isinstance(data, dict):
        raise ValueError("Workbook must be a JSON object")
    settings = data.get("settings", {})
    if not isinstance(settings, dict):
        raise ValueError("settings must be an object")
    version = data.get("schema_version", 1)
    if type(version) is not int or version not in (1, 2):
        raise ValueError("schema_version must be 1 or 2")
    modern = version == 2
    modules = settings.get("modules", ["knowledge", "practice", "solutions", "retrieval", "mastery", "glossary"])
    if not isinstance(modules, list) or not all(isinstance(x, str) for x in modules):
        raise ValueError("modules must be a list of names")
    practice = not modern or "practice" in modules
    global_plan = resolve(settings.get("question_plan")) if modern else None
    languages = settings.get("languages", ["zh", "en"])
    low = settings.get("questions_min", 0 if modern else 5)
    high = settings.get("questions_max", 100000 if modern else 8)
    mock_count = settings.get("mock_count", 0 if modern and settings.get("mode") in ("teacher", "variants") else 2)
    if (not isinstance(languages, list) or not languages
            or not all(isinstance(x, str) and x for x in languages)
            or len(set(languages)) != len(languages)):
        raise ValueError("languages must be distinct nonempty strings")
    if (any(type(x) is not int for x in (low, high, mock_count))
            or low < (0 if modern else 1) or high < low or mock_count < 0):
        raise ValueError("Invalid question bounds or mock_count")
    errors, ids = [], set()

    def fail(path, message):
        errors.append(f"{path}: {message}")

    def text(value, path):
        if not isinstance(value, str) or not value.strip():
            fail(path, "expected nonempty text")

    def bi(value, path):
        value = value if isinstance(value, dict) else {}
        for lang in languages:
            text(value.get(lang), f"{path}.{lang}")

    def array(value, path, nonempty=False):
        if not isinstance(value, list):
            fail(path, "expected array")
            return []
        if nonempty and not value:
            fail(path, "must not be empty")
        return value

    def objects(key):
        result = []
        for i, value in enumerate(array(data.get(key), key)):
            if isinstance(value, dict):
                result.append(value)
            else:
                fail(f"{key}[{i}]", "expected object")
        return result

    def identify(value, path):
        text(value, path)
        if not isinstance(value, str) or not value.strip():
            return None
        if value in ids:
            fail(path, f"duplicate id {value}")
        ids.add(value)
        return value

    def named(rows, path):
        return {v for i, row in enumerate(rows)
                if (v := identify(row.get("id"), f"{path}[{i}].id"))}

    def links(values, allowed, path, nonempty=False):
        for value in array(values, path, nonempty):
            if not isinstance(value, str) or value not in allowed:
                fail(path, f"unknown target {value!r}")

    def bi_list(value, path):
        for i, item in enumerate(array(value, path, True)):
            bi(item, f"{path}[{i}]")

    def number(value, path, positive=True):
        valid = (type(value) in (int, float) and math.isfinite(value)
                 and (value > 0 if positive else value >= 0))
        if not valid:
            fail(path, "expected finite positive number" if positive else "expected nonnegative number")
        return value if valid else 0

    sources, units, mocks = objects("sources"), objects("units"), objects("mocks")
    routes, coverage = objects("routes"), objects("coverage")
    glossary, checklist = objects("glossary"), objects("checklist")
    for label, rows in (("sources", sources), ("units", units), ("routes", routes),
                        ("coverage", coverage), ("glossary", glossary)):
        enabled = not modern or label not in ("routes", "glossary") or ("retrieval" if label == "routes" else "glossary") in modules
        if not rows and enabled:
            fail(label, "must not be empty")
    source_ids, unit_ids = named(sources, "sources"), named(units, "units")
    mock_ids = named(mocks, "mocks")
    named(routes, "routes")
    questions = []
    for group, rows in (("units", units), ("mocks", mocks)):
        for i, row in enumerate(rows):
            path = f"{group}[{i}].questions"
            qs = array(row.get("questions"), path, group == "mocks" or not modern)
            for j, q in enumerate(qs):
                qp = f"{path}[{j}]"
                if not isinstance(q, dict):
                    fail(qp, "expected object")
                    continue
                qid = identify(q.get("id"), qp + ".id")
                if qid:
                    identify(qid + "-ANS", qp + ".answer_id")
                questions.append((q, qp, group == "mocks"))
    question_targets = {x for q, _, _ in questions
                        if isinstance((qid := q.get("id")), str) and qid.strip()
                        for x in (qid, qid + "-ANS")}

    def refs(values, path, nonempty=True):
        for i, ref in enumerate(array(values, path, nonempty)):
            if not isinstance(ref, dict):
                fail(f"{path}[{i}]", "expected source reference object")
                continue
            links([ref.get("source_id")], source_ids, path)
            text(ref.get("locator"), f"{path}[{i}].locator")

    bi(data.get("course"), "course")
    for i, source in enumerate(sources):
        for field in ("file", "kind"):
            text(source.get(field), f"sources[{i}].{field}")
    prior = set()
    for i, unit in enumerate(units):
        path = f"units[{i}]"
        for field in ("title", "goal", "intuition", "principles", "demonstration"):
            bi(unit.get(field), f"{path}.{field}")
        for field in ("method", "pitfalls"):
            bi_list(unit.get(field), f"{path}.{field}")
        if unit.get("scope") not in ("core", "prerequisite", "supplement"):
            fail(path + ".scope", "expected core/prerequisite/supplement")
        links(unit.get("prerequisites"), prior, path + ".prerequisites")
        if isinstance(unit.get("id"), str):
            prior.add(unit["id"])
        refs(unit.get("refs"), path + ".refs")
        qs = unit.get("questions") if isinstance(unit.get("questions"), list) else []
        if not low <= len(qs) <= high:
            fail(path + ".questions", f"expected {low}–{high} questions, got {len(qs)}")
        levels = [q.get("level") for q in qs if isinstance(q, dict)]
        if any(type(x) is not int or x not in range(1, 6) for x in levels):
            fail(path + ".questions", "levels must be integers 1–5")
        elif levels != sorted(levels) and (not modern or resolve(settings.get("question_plan"), unit.get("question_plan"))["order"] == "progressive"):
            fail(path + ".questions", "difficulty must not decrease")
        if modern and practice:
            plan = resolve(settings.get("question_plan"), unit.get("question_plan"))
            for issue in family_errors(qs, plan):
                fail(path + ".questions", issue)
        if low >= 5 and not modern:
            if not {1, 3, 5}.issubset(x for x in levels if type(x) is int):
                fail(path + ".questions", "missing foundation/canonical/transfer levels (1,3,5)")
            kinds = {q.get("kind") for q in qs if isinstance(q, dict) and isinstance(q.get("kind"), str)}
            if not {"recognition", "canonical", "variation", "transfer"}.issubset(kinds):
                fail(path + ".questions", "missing recognition/canonical/variation/transfer kinds")
    for q, path, is_mock in questions:
        bi(q.get("prompt"), path + ".prompt")
        if not is_mock and q.get("kind") not in ("recognition", "application", "canonical", "variation", "transfer"):
            fail(path + ".kind", "unknown practice kind")
        origin = q.get("origin") if isinstance(q.get("origin"), dict) else {}
        if origin.get("type") not in ("original", "adapted", "quoted", "reconstructed"):
            fail(path + ".origin", "unknown/missing provenance type")
        refs(origin.get("refs", []), path + ".origin.refs", origin.get("type") != "original")
        answer = q.get("answer") if isinstance(q.get("answer"), dict) else {}
        bi(answer.get("conclusion"), path + ".answer.conclusion")
        bi_list(answer.get("steps"), path + ".answer.steps")
        if "check" in answer:
            bi(answer["check"], path + ".answer.check")
        if modern:
            try:
                evaluation = assess(q.get("assessment"))
                for item in evaluation["knowledge_dimensions"]:
                    links([item["unit_id"]], unit_ids, path + ".assessment.knowledge_dimensions")
            except ValueError as exc:
                fail(path + ".assessment", str(exc))
            if q.get("role") == "variant":
                transform = q.get("transformation") if isinstance(q.get("transformation"), dict) else {}
                if transform.get("type") not in ("parameter", "condition", "representation", "inverse", "error_diagnosis", "transfer"):
                    fail(path + ".transformation.type", "unknown transformation type")
                for field in ("invariants", "changes", "purpose"):
                    if not has_text(transform.get(field)):
                        fail(path + ".transformation." + field, "required explanation")
        if is_mock:
            links(q.get("unit_ids"), unit_ids, path + ".unit_ids", True)
            marks = number(q.get("marks"), path + ".marks")
            subtotal = 0
            for i, item in enumerate(array(answer.get("rubric"), path + ".answer.rubric", True)):
                if not isinstance(item, dict):
                    fail(path + ".answer.rubric", "expected object")
                    continue
                bi(item.get("criterion"), f"{path}.answer.rubric[{i}].criterion")
                subtotal += number(item.get("marks"), f"{path}.answer.rubric[{i}].marks", False)
            if not math.isclose(subtotal, marks, abs_tol=1e-8):
                fail(path + ".answer.rubric", f"rubric total {subtotal} != marks {marks}")
    if len(mocks) != mock_count:
        fail("mocks", f"expected {mock_count} mock exams, got {len(mocks)}")
    for i, mock in enumerate(mocks):
        path = f"mocks[{i}]"
        bi(mock.get("title"), path + ".title")
        bi(mock.get("basis"), path + ".basis")
        number(mock.get("minutes"), path + ".minutes")
        total = number(mock.get("total_marks"), path + ".total_marks")
        qs = mock.get("questions") if isinstance(mock.get("questions"), list) else []
        subtotal = sum(q.get("marks", 0) for q in qs if isinstance(q, dict) and type(q.get("marks")) in (int, float) and math.isfinite(q["marks"]))
        if not math.isclose(total, subtotal, abs_tol=1e-8):
            fail(path, f"question marks {subtotal} != total_marks {total}")
    for i, route in enumerate(routes):
        path = f"routes[{i}]"
        keywords = route.get("keywords") if isinstance(route.get("keywords"), dict) else {}
        for lang in languages:
            for word in array(keywords.get(lang), path + ".keywords." + lang, True):
                text(word, path + ".keywords." + lang)
        for field in ("family", "distinguish", "first_step"):
            bi(route.get(field), path + "." + field)
        targets = route.get("targets")
        links(targets, unit_ids | mock_ids | question_targets, path + ".targets", True)
        if not isinstance(targets, list) or not any(isinstance(t, str) and t in question_targets for t in targets):
            fail(path + ".targets", "must link to a question or answer")
    for i, row in enumerate(coverage):
        path = f"coverage[{i}]"
        bi(row.get("topic"), path + ".topic")
        if row.get("status") not in ("covered", "partial", "missing", "out_of_scope"):
            fail(path + ".status", "unknown coverage state")
        links(row.get("unit_ids"), unit_ids, path + ".unit_ids", row.get("status") == "covered")
    for i, row in enumerate(glossary):
        for field in ("term", "definition"):
            bi(row.get(field), f"glossary[{i}].{field}")
        links(row.get("unit_ids"), unit_ids, f"glossary[{i}].unit_ids", True)
    checked = set()
    for i, row in enumerate(checklist):
        links([row.get("unit_id")], unit_ids, f"checklist[{i}].unit_id")
        if isinstance(row.get("unit_id"), str):
            checked.add(row["unit_id"])
        bi_list(row.get("criteria"), f"checklist[{i}].criteria")
    for uid in sorted(unit_ids - checked) if not modern or "mastery" in modules else []:
        fail("checklist", f"missing mastery check for {uid}")
    if "lesson_plan" in data:
        lesson = data["lesson_plan"] if isinstance(data["lesson_plan"], dict) else {}
        minutes = number(lesson.get("minutes"), "lesson_plan.minutes")
        subtotal = 0
        for i, stage in enumerate(array(lesson.get("stages"), "lesson_plan.stages", True)):
            if not isinstance(stage, dict):
                fail(f"lesson_plan.stages[{i}]", "expected object")
                continue
            subtotal += number(stage.get("minutes"), f"lesson_plan.stages[{i}].minutes")
        if not math.isclose(minutes, subtotal, abs_tol=1e-8):
            fail("lesson_plan", f"stage minutes {subtotal} != lesson minutes {minutes}")
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("workbook", type=Path)
    args = parser.parse_args()
    try:
        data = json.loads(args.workbook.read_text(encoding="utf-8-sig"))
        errors = validate(data)
    except (OSError, ValueError) as exc:
        print(f"INPUT ERROR: {exc}")
        return 2
    if errors:
        for issue in errors:
            print("ERROR:", issue)
        print(f"FAIL: {len(errors)} structural issue(s); input unchanged.")
        return 1
    print("PASS: structure only. Verify academic content, translations and rendered files separately.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
