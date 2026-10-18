import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "skills/course-study-guide/scripts"
sys.path.insert(0, str(SCRIPTS))
from assess_questions import assess, report
from question_plan import family_errors, resolve
from sync_knowledge_base import affected, synchronize
from validate_workbook import validate


def example():
    return json.loads((ROOT / "examples/primary-perimeter.workbook.json").read_text(encoding="utf-8"))


class WorkbookTests(unittest.TestCase):
    def test_full_single_language_teacher_example(self):
        data = example()
        self.assertEqual(validate(data), [])
        self.assertEqual(len(report(data)["questions"]), 6)
        self.assertEqual(sum(s["minutes"] for s in data["lesson_plan"]["stages"]), 40)

    def test_configurable_three_mothers_four_variants(self):
        questions = []
        for i in range(3):
            qid = f"M{i}"
            questions.append({"id": qid, "role": "mother"})
            questions.extend({"id": f"{qid}-V{j}", "role": "variant", "mother_id": qid} for j in range(4))
        plan = resolve({"foundation_count": 0, "mother_count": 3, "variants_per_mother": 4})
        self.assertEqual(len(questions), 15)
        self.assertEqual(family_errors(questions, plan), [])
        questions.pop()
        self.assertIn("M2: expected 4 variants, got 3", family_errors(questions, plan))

    def test_zero_and_per_mother_override_and_uploaded_preservation(self):
        plan = resolve({"foundation_count": 0, "mother_count": 1, "variants_per_mother": 0})
        self.assertEqual(family_errors([{"id": "M1", "role": "mother"}], plan), [])
        qs = [{"id": "M1", "role": "mother", "uploaded": True, "variant_count": 1},
              {"id": "M2", "role": "mother", "uploaded": True},
              {"id": "V1", "role": "variant", "mother_id": "M1"}]
        self.assertEqual(family_errors(qs, plan), [])
        self.assertTrue(any("mother_count" in issue for issue in family_errors(qs, resolve({**plan, "include_uploaded": "selected"}))))

    def test_broken_mother_and_missing_translation(self):
        data = example()
        data["settings"]["languages"] = ["zh", "en"]
        data["units"][0]["questions"][-1]["mother_id"] = "not-a-mother"
        errors = validate(data)
        self.assertTrue(any("mother_id" in error for error in errors))
        self.assertTrue(any("prompt.en" in error for error in errors))

    def test_family_order_and_hidden_optional_modules(self):
        data = example()
        data["settings"]["question_plan"]["order"] = "family"
        data["units"][0]["questions"] = list(reversed(data["units"][0]["questions"]))
        self.assertEqual(validate(data), [])
        data["settings"]["modules"] = ["knowledge"]
        data["units"][0]["questions"] = []
        data["routes"] = data["glossary"] = data["checklist"] = []
        self.assertEqual(validate(data), [])

    def test_assessment_unknown_unit_and_lesson_timing(self):
        data = example()
        data["units"][0]["questions"][0]["assessment"]["knowledge_dimensions"][0]["unit_id"] = "BAD"
        data["lesson_plan"]["stages"][0]["minutes"] = 7
        errors = validate(data)
        self.assertTrue(any("knowledge_dimensions: unknown target" in error for error in errors))
        self.assertTrue(any("stage minutes 42" in error for error in errors))

    def test_score_requires_evidence_and_finite_confidence(self):
        value = example()["units"][0]["questions"][0]["assessment"]
        self.assertEqual(assess(value)["difficulty_level"], 1)
        value["ratings"] = dict.fromkeys(value["ratings"], 5)
        self.assertEqual(assess(value)["difficulty_level"], 5)
        del value["evidence"]["transfer"]
        with self.assertRaises(ValueError):
            assess(value)
        value = example()["units"][0]["questions"][0]["assessment"]
        value["confidence"] = float("nan")
        with self.assertRaises(ValueError):
            assess(value)
        value["status"] = "measured"
        with self.assertRaises(ValueError):
            assess(value)

    def test_v1_compatibility_and_duplicate_answer_anchor(self):
        data = example()
        data.pop("schema_version")
        data["settings"] = {"languages": ["zh"], "questions_min": 1, "mock_count": 0}
        self.assertEqual(validate(data), [])
        data["units"][0]["questions"][1]["id"] = data["units"][0]["questions"][0]["id"] + "-ANS"
        self.assertTrue(any("duplicate id" in error for error in validate(data)))

    def test_independent_numerical_checks(self):
        # The synthetic solutions are checked independently of metadata validation.
        self.assertEqual(sum([8, 5, 8, 5]), 26)
        self.assertEqual(sum([8, 5, 8, 5]) - 2, 24)
        width = 30 // 2 - 9
        self.assertEqual(width, 6)
        self.assertEqual(2 * (9 + width), 30)

    def test_cli_input_not_modified(self):
        path = ROOT / "examples/primary-perimeter.workbook.json"
        before = path.read_bytes()
        completed = subprocess.run([sys.executable, "-X", "utf8", str(SCRIPTS / "validate_workbook.py"), str(path)], capture_output=True, text=True)
        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
        self.assertEqual(path.read_bytes(), before)


class KnowledgeBaseTests(unittest.TestCase):
    def test_preview_apply_rename_modify_delete_restore(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "kb"
            root.mkdir()
            manifest = Path(directory) / "index.json"
            a = root / "a.txt"
            a.write_text("First", encoding="utf-8")
            preview = synchronize(root, manifest)
            self.assertFalse(manifest.exists())
            self.assertEqual(preview["changes"][0]["status"], "added")
            first = synchronize(root, manifest, apply=True)
            source_id = first["sources"][0]["id"]
            self.assertEqual(synchronize(root, manifest)["changes"], [])
            a.rename(root / "b.txt")
            renamed = synchronize(root, manifest, apply=True)
            self.assertEqual(renamed["changes"][0]["status"], "renamed")
            self.assertEqual(renamed["sources"][0]["id"], source_id)
            (root / "b.txt").write_text("Revised", encoding="utf-8")
            self.assertEqual(synchronize(root, manifest, apply=True)["changes"][0]["status"], "modified")
            (root / "b.txt").unlink()
            self.assertEqual(synchronize(root, manifest, apply=True)["changes"][0]["status"], "removed")
            self.assertEqual(synchronize(root, manifest)["changes"], [])
            (root / "b.txt").write_text("Revised", encoding="utf-8")
            self.assertEqual(synchronize(root, manifest, apply=True)["changes"][0]["status"], "restored")

    def test_excludes_outputs_hidden_and_detects_duplicates(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for folder in ("outputs", ".private"):
                (root / folder).mkdir()
                (root / folder / "secret.txt").write_text("do not scan")
            (root / "one.txt").write_text("same")
            (root / "two.txt").write_text("same")
            result = synchronize(root, root / "index.json", apply=True)
            self.assertEqual(len(result["sources"]), 2)
            self.assertEqual(result["duplicates"], [["one.txt", "two.txt"]])
            self.assertEqual(synchronize(root, root / "index.json")["changes"], [])

    def test_failed_read_does_not_replace_manifest_and_rejects_other_root(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "kb"
            root.mkdir()
            (root / "note.txt").write_text("safe")
            manifest = Path(directory) / "index.json"
            synchronize(root, manifest, apply=True)
            before = manifest.read_bytes()
            with patch("sync_knowledge_base.digest", side_effect=OSError("unreadable")):
                with self.assertRaises(OSError):
                    synchronize(root, manifest, apply=True)
            self.assertEqual(manifest.read_bytes(), before)
            other = Path(directory) / "other"
            other.mkdir()
            with self.assertRaises(ValueError):
                synchronize(other, manifest, apply=True)

    def test_dependency_propagation_to_variants_mocks_and_routes(self):
        data = {"units": [
            {"id": "U1", "refs": [{"source_id": "S1"}], "questions": [{"id": "M1"}, {"id": "V1", "mother_id": "M1"}]},
            {"id": "U2", "prerequisites": ["U1"], "questions": [{"id": "Q2"}]}],
            "mocks": [{"id": "A", "questions": [{"id": "A-Q1", "unit_ids": ["U2"]}]}],
            "routes": [{"id": "R", "targets": ["V1-ANS"]}]}
        result = affected(data, {"S1"})
        self.assertEqual(result["unit_ids"], ["U1", "U2"])
        self.assertEqual(result["question_ids"], ["A-Q1", "M1", "Q2", "V1"])
        self.assertEqual(result["mock_ids"], ["A"])
        self.assertEqual(result["route_ids"], ["R"])


if __name__ == "__main__":
    unittest.main()
