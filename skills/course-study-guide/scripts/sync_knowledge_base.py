#!/usr/bin/env python3
"""Index local source changes and dependent workbook content; never edit sources."""
import argparse
from collections import defaultdict
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import stat
import tempfile

EXTENSIONS = {".pdf", ".ppt", ".pptx", ".doc", ".docx", ".txt", ".md", ".html", ".htm",
              ".png", ".jpg", ".jpeg", ".webp", ".csv", ".xlsx", ".json"}
EXCLUDE = {"output", "outputs", "tmp", "temp", "cache", "previous_version", "node_modules",
           "__pycache__", "dist", "build"}


def digest(path):
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def is_link(path):
    # is_junction is not available on every supported Python version.
    return path.is_symlink() or bool(getattr(path.lstat(), "st_file_attributes", 0)
                                    & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400))


def scan(root, omit):
    result = []

    def on_error(error):
        raise error

    for base, directories, files in os.walk(root, followlinks=False, onerror=on_error):
        directories[:] = sorted(d for d in directories
                                if not d.startswith(".") and d.lower() not in EXCLUDE
                                and not is_link(Path(base) / d))
        for name in sorted(files):
            path = Path(base) / name
            if name.startswith(".") or path.suffix.lower() not in EXTENSIONS or is_link(path):
                continue
            resolved = path.resolve()
            if not resolved.is_relative_to(root) or resolved in omit:
                continue
            before = path.stat()
            sha = digest(path)
            after = path.stat()
            if (before.st_size, before.st_mtime_ns) != (after.st_size, after.st_mtime_ns):
                raise ValueError(f"Source changed while reading: {path.relative_to(root)}; rescan")
            result.append({"path": path.relative_to(root).as_posix(), "sha256": sha, "bytes": after.st_size})
    return sorted(result, key=lambda row: row["path"])


def affected(workbook, changed_ids):
    units = workbook.get("units", [])
    unit_ids = {u["id"] for u in units
                if any(r.get("source_id") in changed_ids for r in u.get("refs", []))}
    question_ids = set()
    for group in ("units", "mocks"):
        for owner in workbook.get(group, []):
            for q in owner.get("questions", []):
                if any(r.get("source_id") in changed_ids for r in q.get("origin", {}).get("refs", [])):
                    question_ids.add(q["id"])
                    if group == "units":
                        unit_ids.add(owner["id"])
    expanded = True
    while expanded:
        before = len(unit_ids)
        unit_ids |= {u["id"] for u in units if set(u.get("prerequisites", [])) & unit_ids}
        expanded = before != len(unit_ids)
    mock_ids = set()
    all_questions = [(group, owner, q) for group in ("units", "mocks")
                     for owner in workbook.get(group, []) for q in owner.get("questions", [])]
    for group, owner, q in all_questions:
        if owner.get("id") in unit_ids or set(q.get("unit_ids", [])) & unit_ids:
            question_ids.add(q["id"])
    expanded = True
    while expanded:
        before = len(question_ids)
        question_ids |= {q["id"] for _, _, q in all_questions if q.get("mother_id") in question_ids}
        expanded = before != len(question_ids)
    for group, owner, q in all_questions:
        if group == "mocks" and q["id"] in question_ids:
            mock_ids.add(owner["id"])
    target_ids = unit_ids | question_ids | {x + "-ANS" for x in question_ids} | mock_ids
    routes = [r["id"] for r in workbook.get("routes", []) if set(r.get("targets", [])) & target_ids]
    return {"unit_ids": sorted(unit_ids), "question_ids": sorted(question_ids),
            "mock_ids": sorted(mock_ids), "route_ids": sorted(routes)}


def synchronize(root, manifest, workbook=None, apply=False):
    root, manifest = Path(root).resolve(), Path(manifest).resolve()
    if not root.is_dir():
        raise ValueError("Knowledge-base root must be an existing directory")
    old = json.loads(manifest.read_text(encoding="utf-8-sig")) if manifest.exists() else {}
    if old and (old.get("schema_version") != 1 or old.get("root") != str(root)):
        raise ValueError("Manifest version/root differs; use a separate manifest for each knowledge base")
    previous = old.get("sources", [])
    if not isinstance(previous, list) or any(not isinstance(r, dict) or not all(k in r for k in ("id", "path", "sha256")) for r in previous):
        raise ValueError("Invalid previous sources")
    if len({r["id"] for r in previous}) != len(previous) or len({r["path"] for r in previous}) != len(previous):
        raise ValueError("Duplicate source IDs/paths in manifest")
    omit = {manifest}
    workbook_data = None
    if workbook:
        workbook_path = Path(workbook).resolve()
        omit.add(workbook_path)
        workbook_data = json.loads(workbook_path.read_text(encoding="utf-8-sig"))
    current = scan(root, omit)
    by_path = {row["path"]: row for row in previous}
    current_paths = {row["path"] for row in current}
    rename_pool = defaultdict(list)
    for row in previous:
        if row["path"] not in current_paths and row.get("status") != "removed":
            rename_pool[row["sha256"]].append(row)
    used, rows, changes = set(), [], []
    known_ids = {row["id"] for row in previous}
    for row in current:
        prior = by_path.get(row["path"])
        if prior is None:
            candidates = [r for r in rename_pool[row["sha256"]] if r["id"] not in used]
            prior = candidates[0] if len(candidates) == 1 else None
        if prior:
            source_id = prior["id"]
            status = ("restored" if prior.get("status") == "removed" else "renamed"
                      if prior["path"] != row["path"] else "modified"
                      if prior["sha256"] != row["sha256"] else "unchanged")
        else:
            source_id = "SRC-" + hashlib.sha256(row["path"].encode("utf-8")).hexdigest()[:16]
            while source_id in known_ids or source_id in used:
                source_id += "x"
            status = "added"
        used.add(source_id)
        updated = {"id": source_id, **row, "status": status}
        rows.append(updated)
        if status != "unchanged":
            changes.append({**updated, "previous_path": prior["path"] if prior else None})
    for prior in previous:
        if prior["id"] not in used:
            rows.append({**prior, "status": "removed"})
            if prior.get("status") != "removed":
                changes.append({**prior, "status": "removed"})
    hashes = defaultdict(list)
    for row in rows:
        if row["status"] != "removed":
            hashes[row["sha256"]].append(row["path"])
    result = {"schema_version": 1, "root": str(root),
              "updated_at": datetime.now(timezone.utc).isoformat(),
              "sources": sorted(rows, key=lambda row: row["path"]), "changes": changes,
              "duplicates": [paths for paths in hashes.values() if len(paths) > 1]}
    if workbook_data is not None:
        result["affected"] = affected(workbook_data, {row["id"] for row in changes})
    if apply:
        manifest.parent.mkdir(parents=True, exist_ok=True)
        temp_name = None
        try:
            with tempfile.NamedTemporaryFile(mode="w", dir=manifest.parent, prefix=manifest.name + ".", suffix=".tmp", encoding="utf-8", delete=False) as stream:
                temp_name = stream.name
                json.dump(result, stream, ensure_ascii=False, indent=2)
                stream.write("\n")
            os.replace(temp_name, manifest)
        finally:
            if temp_name and Path(temp_name).exists():
                Path(temp_name).unlink()
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True, type=Path)
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--workbook", type=Path)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    try:
        result = synchronize(args.root, args.manifest, args.workbook, args.apply)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except (OSError, ValueError, TypeError, KeyError, AttributeError) as exc:
        print(f"ERROR: {exc}; manifest not updated.")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
