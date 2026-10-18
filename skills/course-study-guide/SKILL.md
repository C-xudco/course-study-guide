---
name: course-study-guide
description: "Create progressive study guides and teacher lesson plans from a knowledge base, or generate assessed variants from uploaded mother problems. Use for 学案、备课、分层练习、母题变式 and course revision with configurable counts, language, templates and knowledge-base updates. Supports self-learners, university and K–12 teaching; not a generic document summary."
---

# 递进式学案与教师备课 / Progressive Study Guides

为自学者、大学课程及中小学教师，把资料转化为逐步引入知识的学案、教案与题库。也可仅上传母题生成变式。课程资料是事实来源，学案按先修关系组织；不要把逐页摘要当成教学设计。资料和学生信息默认留在用户工作目录。

## 默认成品与可调整项

先读 [references/options-and-modes.md](references/options-and-modes.md)。从自然语言或保存的配置选择 `learner`、`teacher`、`variants` 模式，沿用本次明确参数；不再把原作者的个人偏好强加给其他使用者。

- 语言可选中文、英文、双语或跟随资料；选择双语时，术语、全部题干与答案及关键步骤均须对照。
- 母题数、每母题变式数、基础题数分别可调，支持单元/母题覆盖；默认每单元 2 基础题＋1 母题＋3 变式。不要把每个术语拆成单元。
- 学习者复习预设两套原创模拟卷，教师和仅出变式预设不生成；可指定任意非负数量。时长/分值无依据时标明练习设定。
- 学案开头提供“题干关键词 → 题型 → 判断条件/第一步 → 单元/例题/答案”的检索导航。
- 末尾提供可操作的知识点掌握核对表及中英学术术语表。
- 模块可选：知识讲解、习题、答案、检索、掌握表、术语表、教案、答题模板与题目评价表。提供可选 PDF、离线 HTML、可编辑 Markdown。
- 教师模式按年级、学科、已学知识和课时输出教案、分层任务、学生版与教师版；使用 [assets/lesson-plan-template.md](assets/lesson-plan-template.md)。

用户只要部分模块或格式时缩减相应产出。答题模板使用 [assets/answer-templates.md](assets/answer-templates.md)，按学科改写并说明适用条件。不要强制低年级使用外语、大学符号或超纲方法。

## 执行流程

### 1. 建立资料与范围台账

先读取 [references/source-workflow.md](references/source-workflow.md)。检查指定文件夹、用户新补充的文件和已有学案，排除生成输出与缓存，形成资料清单及覆盖映射。开启自主更新时按 [references/knowledge-base-updates.md](references/knowledge-base-updates.md) 扫描变化、维护来源 ID 与索引；这发生于每次调用，不是后台常驻服务。

从用户消息、课程安排、考试说明中确定学习范围；区分考试核心、先修补充和范围外拓展。范围不明确时按已提供课程资料继续编写，标注“待确认”，不把所有文件都宣称为必考。只问会实质影响结果且无法推断的必要信息；不要等用户批准目录才开始工作。

### 2. 规划教学路径

按“能完成什么任务”切分知识单元，保留课程章节对应关系。确定先修知识、符号、术语和依赖顺序，再排由基础到综合的学习路径。跨章先修知识用短补课单元引入，不在解答里突然使用未解释的方法。

使用 [assets/unit-template.md](assets/unit-template.md) 编写每个单元；读 [references/pedagogy-and-assessment.md](references/pedagogy-and-assessment.md) 设计题目、解答和模拟卷。计算、证明、编程、阅读、实验、案例论述按实际能力目标调整题型。低年级从直观图示、操作和适龄情境引入；课标或教材版本不明时标为待确认。

### 3. 编写学案与习题

按所选模块完成：目标与先修 → 直觉 → 术语与定义 → 原理/条件 → 示范与通法 → 易错辨析 → 按配置出题 → 对应详解 → 掌握检验。题量按配置计算，不再硬限制为5–8题。

涉及上传母题、变式或题目评价时读 [references/mother-variants-and-assessment.md](references/mother-variants-and-assessment.md)。先核对原题与答案、提炼母题骨架，再按指定类型和数量出变式；保留 `mother_id` 关系和修改目的，每题独立求解核验。题组覆盖能力以学习目标和配置为准，不为满足固定五层加入超出范围的难题。

逐题给出知识点/考查维度、认知过程、难度证据和置信度。没有实测学生数据时标为“预估难度”，不能编造正确率或区分度。`scripts/assess_questions.py` 仅按模型明确给出的量表评分汇总等级；不是能自行理解题目的算法。答案写出方法理由、步骤、结果及核验，双语模式不能只翻译结论。

### 4. 建立检索与模拟卷

关键词必须来自真实题干表达，同时包含中文、英文、缩写和易混表达。每条导航写清适用判据及第一步，避免看到某个词就机械套公式。链接到实际单元、母题和答案；模拟卷题目反向标注知识单元。

开启模拟卷时，从历史练习提炼考查能力、问法和常见失误，按指定数量生成可独立完成的新试卷。标明“原创模拟”，分清历史事实和练习设定，不声称预测真实考试。先呈现完整题目，再集中呈现答案及评分点。教师模式将答案与教学评价留在教师版，学生版默认不含答案。

### 5. 生成并核验成品

按 [references/delivery-and-update.md](references/delivery-and-update.md) 生成文件、实际检验检索和排版。编写 PDF 时，若当前环境提供 PDF 技能，使用它的生成与视觉检查流程；不依赖另一门课的脚本、私有路径或联网资源。所需环境能力缺失时保留完整可编辑内容并如实说明，不将未生成的 PDF 说成已完成。

内容数据可使用 [references/content-model.md](references/content-model.md) 及内置 `scripts/validate_workbook.py` 检查语言缺项、配置题量、母题关联、评价字段、重复编号、无效跳转、先修顺序和模拟卷计分。结构检查不证明学术答案正确；仍须独立核算计算题并检查论证、案例、年级适宜性与来源。

交付前核对：实际覆盖了哪些资料；哪些内容缺失/有争议；题干与答案是否对应；关键符号和条件是否保留；检索是否真能到答案；公式、代码、表格是否可读。报告真实数量和限制，不沿用其他课程的统计数字。

### 6. 补充资料时更新

比较新增/变更资料与现有内容，修补遗漏、纠正冲突、合并重复，保留稳定来源、单元和题目 ID。沿依赖更新知识点、母题、变式、答案、检索、术语、模拟卷和页码，不仅追加到文末。保留一版可恢复成品及用户已审核笔记；详细规则见知识库更新参考。

## 交付说明

用用户的语言简要说明产出链接、覆盖范围、重要缺口和本次新增内容。HTML 发给朋友时须发送实际文件；本机 `file:///...` 地址不能让对方访问。只有实测后的功能才写成已实现。
