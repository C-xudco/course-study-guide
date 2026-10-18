import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPTS = Path(__file__).resolve().parents[1] / "skills/course-study-guide/scripts"
sys.path.insert(0, str(SCRIPTS))
from quota_guard import policy, run


class QuotaGuardTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.config = self.root / "config.json"
        self.ledger = self.root / "usage.json"
        self.value = {"online_research": {"enabled": True,
                                          "approved_domains": ["courses.example.invalid", "bank.example.invalid"]}}
        self.save()

    def tearDown(self):
        self.temporary.cleanup()

    def save(self):
        self.config.write_text(json.dumps(self.value), encoding="utf-8")

    def action(self, action, usage=None, credits=0, domain="courses.example.invalid", **kwargs):
        return run(action, self.config, self.ledger, domain, usage, credits, **kwargs)

    def test_preflight_is_read_only_record_is_explicit(self):
        planned = self.action("check", {"search_requests": 1})
        self.assertEqual(planned["decision"], "allow")
        self.assertFalse(planned["recorded"])
        self.assertFalse(self.ledger.exists())
        self.action("record", {"search_requests": 1})
        self.assertEqual(self.action("status")["used_or_projected"]["search_requests"], 1)

    def test_warn_at_eighty_percent_stop_before_exceeding(self):
        result = self.action("record", {"search_requests": 8})
        self.assertIn("search_requests", result["warnings"])
        self.assertEqual(result["local_remaining"]["search_requests"], 2)
        before = self.ledger.read_bytes()
        self.assertEqual(self.action("check", {"search_requests": 3})["decision"], "stop")
        self.assertEqual(self.ledger.read_bytes(), before)
        self.action("record", {"search_requests": 2})
        self.assertIn("search_requests", self.action("status")["exhausted"])
        self.assertEqual(self.action("check", {"search_requests": 1})["decision"], "stop")
        self.assertEqual(self.action("check", {"page_reads": 1})["decision"], "allow")

    def test_default_zero_cost_and_credits(self):
        self.assertEqual(self.action("check", {"downloads": 1})["decision"], "allow")
        self.assertEqual(self.action("check", {"downloads": 1}, credits=1)["decision"], "stop")
        self.assertEqual(self.action("check", {"cost": 0.1})["decision"], "stop")
        self.assertFalse(self.ledger.exists())

    def test_observed_overrun_is_recorded_not_discarded(self):
        result = self.action("record", {"downloads": 4})
        self.assertTrue(result["recorded"])
        self.assertEqual(result["decision"], "stop")
        self.assertEqual(result["local_remaining"]["downloads"], 0)
        self.assertEqual(self.action("status")["used_or_projected"]["downloads"], 4)

    def test_site_credits_are_separate(self):
        self.value["online_research"]["site_credit_limits"] = {
            "courses.example.invalid": 5, "bank.example.invalid": 2}
        self.save()
        self.action("record", {"downloads": 1}, credits=4)
        self.action("record", {"downloads": 1}, credits=1, domain="bank.example.invalid")
        status = self.action("status")
        self.assertEqual(status["site_credits"]["courses.example.invalid"]["used"], 4)
        self.assertEqual(status["site_credits"]["bank.example.invalid"]["used"], 1)
        self.assertEqual(self.action("check", credits=2)["decision"], "stop")

    def test_disabled_and_unapproved_domains_do_not_write(self):
        self.value["online_research"]["enabled"] = False
        self.save()
        with self.assertRaises(ValueError):
            self.action("record", {"search_requests": 1})
        self.assertEqual(self.action("status")["decision"], "disabled")
        self.value["online_research"]["enabled"] = True
        self.save()
        for domain in ("other.example.invalid", "sub.courses.example.invalid", "https://courses.example.invalid/?token=secret"):
            with self.assertRaises(ValueError):
                self.action("record", {"search_requests": 1}, domain=domain)
        self.assertFalse(self.ledger.exists())

    def test_no_credentials_or_nonfinite_values_in_configuration(self):
        with self.assertRaises(ValueError):
            policy({"online_research": {"password": "do-not-store"}})
        for value in (float("nan"), float("inf"), -1, True):
            with self.assertRaises(ValueError):
                policy({"online_research": {"max_cost": value}})
        with self.assertRaises(ValueError):
            policy({"online_research": {"max_search_requests": 1.5}})

    def test_currency_mismatch_preserves_ledger(self):
        self.action("record", {"search_requests": 1})
        before = self.ledger.read_bytes()
        self.value["online_research"]["currency"] = "USD"
        self.save()
        with self.assertRaises(ValueError):
            self.action("record", {"page_reads": 1})
        self.assertEqual(self.ledger.read_bytes(), before)

    def test_failed_attempt_counted_and_account_balance_unknown(self):
        self.action("record", {"search_requests": 1, "downloads": 1}, outcome="failed")
        state = json.loads(self.ledger.read_text(encoding="utf-8"))
        self.assertEqual(state["events"][0]["outcome"], "failed")
        self.assertEqual(state["used"]["downloads"], 1)
        status = self.action("status")
        self.assertTrue(status["account_remaining"].startswith("unknown"))
        self.assertFalse(status["model_tokens_reported"])
        self.action("record", {"model_tokens": 321})
        self.assertTrue(self.action("status")["model_tokens_reported"])
        self.assertIsNone(self.action("status")["local_remaining"]["model_tokens"])

    def test_cost_decimal_boundary_and_limits_do_not_reset_usage(self):
        self.value["online_research"]["max_cost"] = 0.3
        self.save()
        self.action("record", {"cost": 0.1})
        result = self.action("record", {"cost": 0.2})
        self.assertEqual(result["used_or_projected"]["cost"], 0.3)
        self.assertEqual(result["local_remaining"]["cost"], 0)
        self.assertEqual(self.action("check", {"cost": 0.01})["decision"], "stop")
        self.value["online_research"]["max_cost"] = 0.2
        self.save()
        self.assertEqual(self.action("status")["used_or_projected"]["cost"], 0.3)
        self.assertEqual(self.action("status")["decision"], "stop")

    def test_cli_stop_code_and_no_config_overwrite(self):
        result = subprocess.run([sys.executable, "-X", "utf8", str(SCRIPTS / "quota_guard.py"),
                                 "check", "--config", str(self.config), "--ledger", str(self.ledger),
                                 "--domain", "courses.example.invalid", "--search-requests", "11"],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertFalse(self.ledger.exists())
        before = self.config.read_bytes()
        with self.assertRaises(ValueError):
            run("record", self.config, self.config, "courses.example.invalid", {"search_requests": 1})
        self.assertEqual(self.config.read_bytes(), before)


if __name__ == "__main__":
    unittest.main()
