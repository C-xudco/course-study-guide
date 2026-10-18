"""Shared quantity semantics for configurable problem families."""
DEFAULT = {"foundation_count": 2, "mother_count": 1, "variants_per_mother": 3,
           "include_uploaded": "all", "order": "progressive"}


def resolve(global_plan=None, unit_plan=None):
    plan = dict(DEFAULT)
    for incoming in (global_plan, unit_plan):
        if incoming is not None:
            if not isinstance(incoming, dict):
                raise ValueError("question_plan must be an object")
            plan.update(incoming)
    for field in ("foundation_count", "mother_count", "variants_per_mother"):
        if type(plan[field]) is not int or plan[field] < 0:
            raise ValueError(f"question_plan.{field} must be a nonnegative integer")
    if plan["include_uploaded"] not in ("all", "selected"):
        raise ValueError("include_uploaded must be all or selected")
    if plan["order"] not in ("progressive", "family"):
        raise ValueError("order must be progressive or family")
    if "difficulty_targets" in plan:
        values = plan["difficulty_targets"]
        if not isinstance(values, list) or not values or any(type(x) is not int or x not in range(1, 6) for x in values):
            raise ValueError("difficulty_targets must be levels 1–5")
    return plan


def family_errors(questions, plan):
    errors = []
    valid = [q for q in questions if isinstance(q, dict)]
    for q in valid:
        if q.get("role") not in ("foundation", "mother", "variant"):
            errors.append(f"{q.get('id')}: role must be foundation/mother/variant")
    foundations = [q for q in valid if q.get("role") == "foundation"]
    mothers = [q for q in valid if q.get("role") == "mother"]
    if len(foundations) != plan["foundation_count"]:
        errors.append(f"foundation_count expected {plan['foundation_count']}, got {len(foundations)}")
    uploaded_count = sum(q.get("uploaded") is True for q in mothers)
    expected_mothers = max(plan["mother_count"], uploaded_count) if plan["include_uploaded"] == "all" else plan["mother_count"]
    if len(mothers) != expected_mothers:
        errors.append(f"mother_count expected {expected_mothers}, got {len(mothers)}")
    mother_ids = {q.get("id") for q in mothers if isinstance(q.get("id"), str)}
    for q in valid:
        parent = q.get("mother_id")
        if q.get("role") == "variant":
            if not isinstance(parent, str) or parent not in mother_ids:
                errors.append(f"{q.get('id')}: mother_id must reference a mother in this unit")
        elif parent is not None:
            errors.append(f"{q.get('id')}: only a variant may have mother_id")
        if "uploaded" in q and type(q["uploaded"]) is not bool:
            errors.append(f"{q.get('id')}: uploaded must be boolean")
    for mother in mothers:
        count = mother.get("variant_count", plan["variants_per_mother"])
        if type(count) is not int or count < 0:
            errors.append(f"{mother.get('id')}: variant_count must be a nonnegative integer")
            continue
        actual = sum(q.get("role") == "variant" and q.get("mother_id") == mother.get("id") for q in valid)
        if actual != count:
            errors.append(f"{mother.get('id')}: expected {count} variants, got {actual}")
    return errors
