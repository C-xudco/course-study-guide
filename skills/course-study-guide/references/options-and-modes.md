# 运行选项与模式

先解析用户自然语言和已保存的 `study-guide.config.json`，自然语言的本次明确要求优先于已有配置。缺项使用预设并在成品说明中列出关键设定；不要问完所有字段才工作。

## 模式预设

| 选项 | learner 自学/课程复习 | teacher 教师备课 | variants 上传母题出变式 |
|---|---|---|---|
| 默认语言 | 资料主要语言；中英混合课程用双语 | 授课语言，默认中文 | 跟随上传题目 |
| 每单元基础题 | 2 | 2 | 0 |
| 每单元母题 | 1 | 1 | 所有上传且被选中的母题 |
| 每母题变式 | 3 | 3 | 3 |
| 模拟卷 | 2；非考试学习可关 | 0，可打开 | 0 |
| 默认模块 | 讲解、题目、详解、检索、掌握表、术语表 | 前述模块＋教案、分层任务、学生版/教师版 | 母题解析、变式、详解、评价表 |

所有预设可覆盖。配置语言用 `languages:["zh"]`、`["en"]`、`["zh","en"]` 或其他用户指定语言代码。用户明确需要中英对照时，讲解中的术语、全部题干/子题、关键步骤和答案均中英对应。

## 题量计数

`question_plan`：

```json
{
  "foundation_count": 2,
  "mother_count": 1,
  "variants_per_mother": 3,
  "include_uploaded": "all",
  "difficulty_targets": [1, 2, 3],
  "order": "progressive"
}
```

默认 `mother_count` 指每单元母题总数，不是每章总数；`variants_per_mother` 指每一道母题的变式数量。总题数 = 基础题数 + 实际母题数 + 各母题变式数之和。默认 2+1+3=6，不再硬限制 5–8；用户选 3 母题×4 变式就是 15 道母题/变式，再加自选基础题。

- `include_uploaded:all`：保留所有上传且适用于当前范围的母题，若超过母题预设数量，采用实际数量并说明，不静默丢弃；不足时可补原创母题并标明。
- `include_uploaded:selected`：只使用用户选定的母题 ID；原始题目仍保留在知识库。
- 单元可用自身 `question_plan` 覆盖全局数量；每道母题可用 `variant_count` 覆盖全局变式数。自然语言中“母题共3道”应理解为总量分配，而非每单元3道，并将分配写入各单元。
- 0 是有效值：0 变式、0 模拟卷、仅母题解析都可。模式 `variants` 若未提供题目且知识库也没有可用母题，先索取母题文本/附件，不虚构“已上传题目”。
- `order:progressive` 把基础、母题、变式按难度排序并保留母题关联；`order:family` 按母题分组，每组内部递进。教师课堂可用分组顺序；难度相近的题无需强制分成1–5所有档。

## 可选模块与输出

`modules` 可选：`knowledge`, `practice`, `solutions`, `retrieval`, `mastery`, `glossary`, `lesson_plan`, `answer_templates`, `assessment_table`。模拟卷数量由 `mock_count` 单独控制。不要生成被明确关闭的模块，避免“仅出变式”仍输出整本学案。

用户可指定 `formats:["pdf","html","markdown"]` 的子集。没有专门要求时 learner 默认 PDF＋离线 HTML；teacher 默认 PDF 学生版＋教师版及可编辑 Markdown 教案；variants 默认可编辑 Markdown 题库及评价表，可追加 PDF。

教师参数包括 `grade`、`subject`、`curriculum`、`lesson_minutes`、已学先修、学习目标、班级共性困难和差异化需求。缺少具体课标版本时标记待确认，不声称“符合某版课标”。小学模式优先直观图示/操作/口头解释，按年级限制数字范围、术语、阅读负担和方法；挑战题不得默认使用尚未学习的方法。

答题模板只在有帮助时开启：计算、证明、阅读理解、实验分析、案例论述等分别使用合适的推理骨架，并解释适用条件、可变部分和一个填写示范；不能用通用套话代替正确知识。

可复制 [../assets/config.example.json](../assets/config.example.json) 并按自然语言需求修改。该配置是选项示例，不强制用户手动编辑 JSON。

## 可选外部资料输入

`online_research` 不是第四种教学模式，可与 learner/teacher/variants 任一模式组合。默认 `enabled:false`；用户明确要求联网时，根据其授权填写允许的精确站点域名、课程范围与预算。使用 [../assets/online-research.example.json](../assets/online-research.example.json) 的结构，不填写账号、密码或SSO令牌。登录授权、组题和额度流程见 [online-research.md](online-research.md)。
