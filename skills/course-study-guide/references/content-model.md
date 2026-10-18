# 可编辑内容模型与结构检查

为便于跨格式渲染和更新，推荐一个 UTF-8 `workbook.json` 保存内容。已有课程生成器可保留自己的结构；下列校验器只接受本模型，不要为凑校验结果丢弃已有信息。

## 版本2：公开版配置与题目家族

新生成内容使用顶层 `schema_version:2`；没有此字段时校验器保留旧版双语5–8题行为。下面字段结构仍适用，但版本2以本节的规则覆盖旧版默认数值。

- `settings` 使用 `assets/config.example.json` 的模式、语言、`question_plan`、模块和 `mock_count`。默认母题1、每母题变式3、基础题2；每个单元可以有自己的 `question_plan`。
- `questions_min/questions_max` 在版本2仅作为可选总量限制，不用于计算母题/变式数；不再强制题组覆盖全部五层。
- 每道单元题新增 `role:foundation|mother|variant`；母题可有 `uploaded:true` 与 `variant_count`，变式必须有 `mother_id`，指向同单元母题。上传题仍在 `origin.refs` 中记录出处，`origin.type` 用 quoted/adapted/reconstructed 等说明处理方式。
- 每个变式包含 `transformation:{type,invariants,changes,purpose}`，具体见母题与评价参考。`type` 支持 parameter/condition/representation/inverse/error_diagnosis/transfer。
- 每题（含模拟卷题）有 `assessment`：按 `mother-variants-and-assessment.md` 记录五维评分及证据、知识点与认知过程、受众、置信度和理由。等级由脚本从显式评分计算，区别于教学顺序标签 `level`。
- 母题实际数量须等于配置；`include_uploaded:all` 时以配置数和实际已上传母题数的较大者为准。每道母题的实际变式数须与自身覆盖或全局配置完全一致。
- `modules` 关闭 retrieval/glossary/mastery 时对应集合可为空；仅讲解模式可关闭 practice 并保留空 questions。模块开关控制成品输出，模型仍保留简明单元目标、先修和来源，便于追踪。
- 默认 `languages` 仍为 zh/en；配置解析阶段应按用户/模式填入实际语言列表。单语内容仅要求对应语言键。
- 教师/variants 模式默认 `mock_count:0`；learner 默认2。关闭的模拟卷保留 `mocks:[]`。

`python scripts/assess_questions.py workbook.json --output assessment.json` 汇总题目评价；`python scripts/sync_knowledge_base.py --root knowledge-base --manifest outputs/knowledge-base.json --workbook workbook.json --apply` 更新本地索引并报告依赖影响。三个脚本仅使用 Python 标准库。

## 通用字段约定

`双语文本` 为 `{"zh":"中文完整内容", "en":"Equivalent English content"}`。单语时只保留配置语言的键。共享公式可嵌在两段中或作为单独扩展字段。字段可扩展；校验器不负责渲染。若用户指定其他语言，修改 `settings.languages`，所有本地化文本字段使用相同语言键。

稳定 ID 为非空字符串，全局唯一。答案锚点自动约定为 `{题号}-ANS`，不要另外定义冲突 ID。数组顺序即教学/题目顺序。难度用整数 1–5，含义见教学参考。

`来源定位` 为 `{"source_id":"SRC01", "locator":"PDF p.12 / slide 10"}`；必须能回查具体位置，非 PDF 用节/题号等。`origin` 为 `{"type":"original|adapted|quoted|reconstructed", "refs":[来源定位]}`，非原创必须有来源。

## 顶层字段

| 字段 | 内容 |
|---|---|
| `course` | 双语课程名称 |
| `settings` | 可省略；默认 `languages:["zh","en"]`, `questions_min:5`, `questions_max:8`, `mock_count:2`。仅依用户要求调整 |
| `sources` | 来源数组：`id`, `file`（相对文件名）, `kind`（资料类型），可加版本、页数、读取状态等 |
| `coverage` | 覆盖数组：`topic` 双语，`status` 为 `covered/partial/missing/out_of_scope`，`unit_ids` 数组；可加来源及缺口说明 |
| `units` | 按先修顺序的完整单元数组，见下文 |
| `routes` | 关键词导航数组，见下文 |
| `mocks` | 模拟卷数组，见下文；用户不需要时 `mock_count:0` 且数组为空 |
| `glossary` | 每项 `term` 双语，`definition` 双语，`unit_ids` 非空，可加缩写与易混点 |
| `checklist` | 每项 `unit_id`, `criteria` 非空双语文本数组；每个单元至少有一项 |

## 单元

每项字段：

- `id`、`title` 双语、`scope`（`core/prerequisite/supplement`）。
- `prerequisites`：先修单元 ID 数组，可为空；先修必须在本单元之前。所有单元（包括补课单元）执行相同题量约定，避免用单元名规避练习；若仅为短回顾，放在正文而非单独建单元。
- `refs`：非空来源定位数组。
- `goal`、`intuition`、`principles`、`demonstration`：双语文本。`principles` 包含定义、公式、符号和条件；`demonstration` 给最小实例和解释，可与独立题目关联而不重复计数。
- `method`、`pitfalls`：非空双语文本数组。
- `questions`：默认 5–8 项；每题 `id`, `level`, `kind`, `origin`, `prompt` 双语, `answer`。`kind` 为 `recognition/application/canonical/variation/transfer`。

旧版默认题组至少包含 `recognition`, `canonical`, `variation`, `transfer` 并触及1、3、5层；版本2按配置与目标设计，可采用 `order:family` 家族分组，不强制全局递增。脚本不能判断变式是否仅换数字，该项必须人工审查。

## 答案

`answer` 为 `conclusion` 双语、`steps` 非空双语文本数组，可加 `check` 双语和 `rubric`。建议每题都有 `check`，难题有评分点。

`rubric` 为 `[{"criterion":双语文本, "marks":数值}, ...]`；模拟卷必须有，得分点之和等于对应题分值。多种合法答案的条件与接受标准写入答案，不能只列一个结果。

## 检索

`routes` 每项：`id`, `keywords:{"zh":["词"],"en":["term","abbreviation"]}`, `family` 双语, `distinguish` 双语, `first_step` 双语, `targets` 非空 ID 数组。

目标可以是单元、题号、`题号-ANS` 或模拟卷 ID；每条路由至少指向一个题目/答案，并补一个对应单元可方便学习。`distinguish` 解释如何排除相似题，避免关键词触发误用。PDF 页码由最终排版生成，不能在内容阶段猜测。

## 模拟卷

`mocks` 每项：`id`, `title` 双语, `basis` 双语（区分历史依据与作者设定）, `minutes` 正数, `total_marks` 正数, `questions` 非空。

每题同单元题字段，但 `level` 与 `kind` 可选，额外必需 `unit_ids` 非空及 `marks` 正数，`answer.rubric` 分值和必须等于本题分值。子问题及其分值完整写入 `prompt`，相应子问题评分写入 rubric；如增加结构化子题字段，自行扩展校验。当前脚本不解析题干字符串里的分值。

## 运行与限制

```text
python scripts/validate_workbook.py <课程输出目录>/workbook.json
```

退出码 0：通过结构检查；1：内容结构存在缺项/引用/计分问题；2：无法读取 JSON 或配置非法。只使用 Python 标准库，不联网、不修改输入。输出路径及 Python 的实际位置由当前环境决定。

该脚本不验证翻译质量、知识正确性、图文提取、难度真实性、版权或 PDF/HTML 排版与功能。不要把结构检查通过写成“所有内容均已验证正确”。
