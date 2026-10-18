#!/usr/bin/env python3
"""Check local research budgets and record observed usage; no network or login."""
import argparse
from datetime import datetime, timezone
from decimal import Decimal
import json
import math
import os
from pathlib import Path
import re
import tempfile

METRICS = ("search_requests", "page_reads", "downloads", "cost", "model_tokens")
DEFAULTS = {"enabled": False, "approved_domains": [], "max_search_requests": 10,
            "max_page_reads": 20, "max_downloads": 3, "max_cost": 0,
            "max_model_tokens": None, "site_credit_limits": {}, "currency": "CNY",
            "warn_fraction": 0.8}


def amount(value, integer=False):
    if (type(value) not in (int, float) or not math.isfinite(value) or value < 0
            or (integer and type(value) is not int)):
        raise ValueError("Usage/limits must be finite nonnegative numbers; counts must be integers")
    return value


def host(value):
    if not isinstance(value, str):
        raise ValueError("An exact hostname is required")
    try:
        value = value.lower().encode("idna").decode("ascii")
    except UnicodeError as exc:
        raise ValueError("Invalid hostname") from exc
    if (len(value) > 253 or "." not in value or any(
            not re.fullmatch(r"[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?", label)
            for label in value.split("."))):
        raise ValueError("Use an exact hostname, without URLs, wildcards, ports or account data")
    return value


def policy(config):
    if not isinstance(config, dict):
        raise ValueError("Config must be an object")
    incoming = config.get("online_research", {})
    if not isinstance(incoming, dict) or set(incoming) - set(DEFAULTS):
        raise ValueError("Unsupported online_research fields; credentials are not accepted")
    result = {**DEFAULTS, **incoming}
    if type(result["enabled"]) is not bool:
        raise ValueError("enabled must be boolean")
    if not isinstance(result["approved_domains"], list):
        raise ValueError("approved_domains must be a list")
    result["approved_domains"] = list(dict.fromkeys(host(x) for x in result["approved_domains"]))
    for metric in METRICS:
        value = result["max_" + metric]
        if value is None and metric == "model_tokens":
            continue
        amount(value, metric not in ("cost",))
    if not isinstance(result["currency"], str) or not re.fullmatch(r"[A-Z]{3}", result["currency"]):
        raise ValueError("currency must be a three-letter uppercase code")
    if not isinstance(result["site_credit_limits"], dict):
        raise ValueError("site_credit_limits must be an object")
    result["site_credit_limits"] = {host(domain): amount(limit)
                                    for domain, limit in result["site_credit_limits"].items()}
    if any(domain not in result["approved_domains"] for domain in result["site_credit_limits"]):
        raise ValueError("Site-credit domains must be explicitly approved")
    threshold = amount(result["warn_fraction"])
    if not 0 < threshold <= 1:
        raise ValueError("warn_fraction must be greater than 0 and no greater than 1")
    return result


def blank(currency):
    return {"schema_version": 1, "currency": currency,
            "used": dict.fromkeys(METRICS, 0), "site_credits": {},
            "reported_metrics": [], "events": []}


def read_ledger(path, currency):
    if not path.exists():
        return blank(currency)
    state = json.loads(path.read_text(encoding="utf-8-sig"))
    if (not isinstance(state, dict) or set(state) != set(blank(currency))
            or state["schema_version"] != 1 or state["currency"] != currency):
        raise ValueError("Ledger format/currency mismatch; do not mix sessions or currencies")
    if not isinstance(state["used"], dict) or set(state["used"]) != set(METRICS):
        raise ValueError("Ledger counters are invalid")
    for metric, value in state["used"].items():
        amount(value, metric != "cost")
    if not isinstance(state["site_credits"], dict):
        raise ValueError("Ledger site credits are invalid")
    for domain, value in state["site_credits"].items():
        host(domain)
        amount(value)
    if (not isinstance(state["reported_metrics"], list)
            or any(x not in METRICS for x in state["reported_metrics"])):
        raise ValueError("Ledger reported metrics are invalid")
    if not isinstance(state["events"], list):
        raise ValueError("Ledger events are invalid")
    for event in state["events"]:
        if not isinstance(event, dict) or set(event) != {"at", "domain", "usage", "site_credits", "outcome"}:
            raise ValueError("Unsupported ledger event format")
    return state


def add(left, right):
    result = Decimal(str(left)) + Decimal(str(right))
    return int(result) if result == result.to_integral_value() else float(result)


def summary(config, state, domain=None, usage=None, credits=0):
    usage = usage or {}
    projected = {name: add(value, usage.get(name, 0)) for name, value in state["used"].items()}
    local_remaining, warnings, exceeded, exhausted = {}, [], [], []
    for name, value in projected.items():
        limit = config["max_" + name]
        local_remaining[name] = None if limit is None else max(0, float(Decimal(str(limit)) - Decimal(str(value))))
        if limit is not None:
            if value > limit:
                exceeded.append(name)
            if limit > 0 and value >= limit:
                exhausted.append(name)
            if limit > 0 and Decimal(str(value)) >= Decimal(str(limit)) * Decimal(str(config["warn_fraction"])):
                warnings.append(name)
    sites = dict(state["site_credits"])
    if domain:
        sites[domain] = add(sites.get(domain, 0), credits)
    site_summary = {}
    for site in sorted(set(sites) | set(config["site_credit_limits"])):
        value, limit = sites.get(site, 0), config["site_credit_limits"].get(site, 0)
        site_summary[site] = {"used": value, "limit": limit, "local_remaining": max(0, add(limit, -value))}
        label = "site_credits:" + site
        if value > limit:
            exceeded.append(label)
        if limit > 0 and value >= limit:
            exhausted.append(label)
        if limit > 0 and Decimal(str(value)) >= Decimal(str(limit)) * Decimal(str(config["warn_fraction"])):
            warnings.append(label)
    return {"decision": "disabled" if not config["enabled"] else "stop" if exceeded else "allow",
            "used_or_projected": projected, "local_remaining": local_remaining,
            "currency": config["currency"], "site_credits": site_summary,
            "warnings": sorted(warnings), "exceeded": sorted(exceeded), "exhausted": sorted(exhausted),
            "model_tokens_reported": "model_tokens" in state["reported_metrics"] or "model_tokens" in usage,
            "account_remaining": "unknown: local counters are not website or model-account balances"}


def run(action, config_path, ledger_path, domain=None, usage=None, credits=0, outcome="unknown"):
    if outcome not in ("success", "failed", "unknown"):
        raise ValueError("outcome must be success, failed or unknown")
    config_path, ledger_path = Path(config_path).resolve(), Path(ledger_path).resolve()
    if config_path == ledger_path:
        raise ValueError("Ledger must not overwrite the configuration")
    config = policy(json.loads(config_path.read_text(encoding="utf-8-sig")))
    state = read_ledger(ledger_path, config["currency"])
    usage = {} if usage is None else dict(usage)
    if set(usage) - set(METRICS):
        raise ValueError("Unknown usage metric")
    for name, value in usage.items():
        amount(value, name != "cost")
    amount(credits)
    if action == "status":
        return summary(config, state)
    if action not in ("check", "record"):
        raise ValueError("action must be check, record or status")
    if not config["enabled"]:
        raise ValueError("Online research is disabled; enable it only for the user's authorized task")
    domain = host(domain)
    if domain not in config["approved_domains"]:
        raise ValueError("Domain is outside the explicitly approved list")
    if not any(usage.values()) and not credits:
        raise ValueError("Provide a nonzero planned or observed usage amount")
    result = summary(config, state, domain, usage, credits)
    if action == "record":
        # Observed overruns must be recorded truthfully, then stop further use.
        state["used"] = result["used_or_projected"]
        state["site_credits"][domain] = add(state["site_credits"].get(domain, 0), credits)
        state["reported_metrics"] = sorted(set(state["reported_metrics"]) | set(usage))
        state["events"].append({"at": datetime.now(timezone.utc).isoformat(), "domain": domain,
                                "usage": usage, "site_credits": credits, "outcome": outcome})
        ledger_path.parent.mkdir(parents=True, exist_ok=True)
        temporary = None
        try:
            with tempfile.NamedTemporaryFile(mode="w", dir=ledger_path.parent, prefix=ledger_path.name + ".", suffix=".tmp", delete=False, encoding="utf-8") as stream:
                temporary = stream.name
                json.dump(state, stream, ensure_ascii=False, indent=2)
                stream.write("\n")
            os.replace(temporary, ledger_path)
        finally:
            if temporary and Path(temporary).exists():
                Path(temporary).unlink()
        result["recorded"] = True
    else:
        result["recorded"] = False
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("check", "record", "status"))
    parser.add_argument("--config", required=True, type=Path)
    parser.add_argument("--ledger", required=True, type=Path)
    parser.add_argument("--domain")
    for metric in METRICS:
        parser.add_argument("--" + metric.replace("_", "-"), type=float if metric == "cost" else int)
    parser.add_argument("--site-credits", type=float, default=0)
    parser.add_argument("--outcome", choices=("success", "failed", "unknown"), default="unknown")
    args = parser.parse_args()
    usage = {name: getattr(args, name) for name in METRICS if getattr(args, name) is not None}
    try:
        result = run(args.action, args.config, args.ledger, args.domain, usage, args.site_credits, args.outcome)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except (OSError, ValueError, TypeError, KeyError) as exc:
        print(f"ERROR: {exc}")
        return 1
    return 2 if result["decision"] == "stop" else 0


if __name__ == "__main__":
    raise SystemExit(main())
