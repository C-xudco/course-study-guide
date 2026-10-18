# Course Study Guide

[中文](README.md) · [Skill](skills/course-study-guide/SKILL.md)

> Feature branch: `feature/authorized-online-research`. This adds optional public/authorized study-material research with local quota reminders. The pre-update `main` branch remains unchanged. This feature has not been merged into `main`.

An open, source-grounded workflow for anyone learning a new subject and for K–12 teachers preparing lessons: intuition → concepts → canonical problems → purposeful variants → transfer and self-assessment.

This repository contains an **AI assistant Skill**, templates and local helpers. It is not a standalone tutoring app. Skill instructions and most reference material are currently in Chinese; the assistant can produce materials in the requested language.

## Features

- Learner, teacher and uploaded-problem variant modes.
- Configurable foundation problems, mother problems per unit and variants per mother, with per-unit and per-mother overrides.
- Uploaded PDFs, images, documents or text: source verification, problem normalization, solution checks and stable lineage.
- Parameter, condition, representation, inverse, error-diagnosis and transfer variants, each with an independently checked solution and change rationale.
- Explainable **estimated** difficulty, evidence across five dimensions, knowledge dimensions, cognitive processes and confidence. No fabricated student success rates.
- Grade-appropriate lesson plans, pacing, differentiated tasks, exit tickets, separate student and teacher editions.
- Optional explanations, solutions, retrieval, mastery checks, glossary, answer scaffolds, assessments and mock exams.
- Single-language or bilingual output; PDF, offline HTML and editable Markdown as supported by the host assistant.
- Local knowledge-base change detection and dependency-aware revision on each invocation; no background daemon or automatic public uploads.
- Optional research on permitted course sites, school LMSs, question banks and community sources, with access/provenance checks and source-based question selection.
- Separate local budgets for searches, page reads, download attempts, site credits and costs; 80% reminders and stop-at-limit decisions. Unavailable account balances remain unknown.

## Install

Ask the built-in installer in a compatible Codex host:

```text
Use $skill-installer to install skills/course-study-guide
from C-xudco/course-study-guide with ref feature/authorized-online-research.
Use this feature branch rather than main.
```

Or copy that skill directory into your host's personal skills location. Current official Codex documentation lists `~/.agents/skills`; existing installations may expose `~/.codex/skills`. Follow your host's actual location. See [official Skills documentation](https://learn.chatgpt.com/docs/build-skills). Invoke `$course-study-guide` after installation; restart the host if discovery has not refreshed.

[Download this feature branch as ZIP](https://github.com/C-xudco/course-study-guide/archive/refs/heads/feature/authorized-online-research.zip), or select the branch on GitHub and choose **Code → Download ZIP**. Switch to `main` to obtain the original version. See [GitHub's archive documentation](https://docs.github.com/en/repositories/working-with-files/using-files/downloading-source-code-archives).

## Authorized online research

Read the [workflow](skills/course-study-guide/references/online-research.md), [configuration](skills/course-study-guide/assets/online-research.example.json) and [source catalog](skills/course-study-guide/assets/source-catalog-template.md). Online research is disabled by default.

1. Provide the course/grade, institution, scope, years, target count and permitted starting sites. Prefer verified official course resources and released past papers; community posts are supplementary leads until checked.
2. Approve exact domains and task budgets. Complete passwords, MFA, QR codes and campus SSO yourself in the site's normal login UI or an official connector. Do not send credentials, cookies or tokens to the assistant, config or repository.
3. The assistant uses only tools actually available in the host. A web search tool does not inherit your personal browser session. Without authorized browser/connector support, use public sources or upload documents you legitimately export yourself.
4. Distinguish full reading, partial preview, metadata-only and inaccessible leads. Classify sources, verify questions and solutions, respect permitted uses, and label originals/adaptations/new variants. Download access is not automatically redistribution permission.
5. Check before actions and record observed use afterwards, including failed attempts and retries. Defaults: 10 searches, 20 page reads, 3 download attempts, zero money and zero paid credits. Warn at 80%; stop exhausted operations. Report actual website balances only when explicitly available, with evidence; local remaining budget is not an account balance.

DeepSeek/Doubao users can paste the [research add-on prompt](skills/course-study-guide/assets/online-research-prompt.md) into their existing study role. This does not create browser permissions or account integrations. The module contains no private site API, crawler or universal SSO client, and has not been tested end to end using real campus/member accounts.

Local preflight demo; no network requests:

```text
python skills/course-study-guide/scripts/quota_guard.py check --config examples/research.config.json --ledger outputs/research-usage-demo.json --domain courses.example.invalid --search-requests 1
python skills/course-study-guide/scripts/quota_guard.py status --config examples/research.config.json --ledger outputs/research-usage-demo.json
```

After real actions the host must invoke `record` with observed use. Checks are read-only; records preserve unexpected overruns and return a stop decision. Credits are tracked per domain and costs in one explicit currency. The helper neither intercepts browser calls nor reads account balances; update each private ledger sequentially.

## Example prompts

```text
Use $course-study-guide in learner mode with my uploaded course folder.
Cover chapters 1–5. Use English; 2 foundation problems and 2 mother problems
per unit, each with 3 variants. Explain gradually, then provide solutions,
two original mock exams, retrieval and a glossary. Export PDF and offline HTML.
```

```text
Use $course-study-guide in teacher mode for a 40-minute primary-school
rectangle-perimeter lesson. Use the uploaded sources and two mother problems,
each with four variants. Create differentiated tasks, an exit ticket,
a student worksheet and teacher solutions with assessment evidence. No mocks.
```

```text
Use $course-study-guide in variants mode. Use all three uploaded mother
problems and make four variants each: condition change, inverse,
error diagnosis and transfer. Include solutions, lineage, knowledge dimensions
and estimated difficulty. Only output the question bank and assessment table.
```

Options are documented [here](skills/course-study-guide/references/options-and-modes.md), with an editable [configuration example](skills/course-study-guide/assets/config.example.json). Natural-language instructions override saved settings. Default practice count is 2 foundations + 1 mother + 3 variants = 6, with no fixed 5–8 limit.

## Helpers and tests

Python 3.10+, standard library only; no API key required for the helpers:

```text
python skills/course-study-guide/scripts/validate_workbook.py examples/primary-perimeter.workbook.json
python skills/course-study-guide/scripts/assess_questions.py examples/primary-perimeter.workbook.json
python skills/course-study-guide/scripts/sync_knowledge_base.py --root examples/knowledge-base --manifest outputs/knowledge-base.json --apply
python -m unittest discover -s tests -v
```

The validator checks structure, counts, lineage, references and marks. Assessment aggregates explicit model/teacher ratings; it does not understand questions. Knowledge-base synchronization hashes local sources; `--workbook` reports dependent content and omitting `--apply` previews changes. These tools do not generate lessons, solve questions or render files by themselves. The host assistant performs those tasks using the workflow and available tools.

The included primary-school example is original synthetic material, not a real textbook or a curriculum certification. Do not submit private course materials, copyrighted source collections or identifiable student records. Contribute templates and reproducible fixes via [CONTRIBUTING.md](CONTRIBUTING.md).

## License

[MIT](LICENSE) covers this project's code, instructions and original templates. Uploaded materials retain their own rights. Difficulty labels are teaching estimates, not standardized measurement. Check subject correctness, solutions and suitability for the intended learners.
