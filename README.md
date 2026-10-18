# Course Study Guide · 递进式学案与教师备课

[English](README.en.md) · [Skill 规范](skills/course-study-guide/SKILL.md) · [配置选项](skills/course-study-guide/references/options-and-modes.md)

> 当前为 `feature/authorized-online-research` 功能分支：新增可选联网检索与授权资料组题。`main` 保留更新前状态；本分支尚未合并。原有本地学案/备课流程仍可独立使用。

给任何想系统学习新知识的人，也给需要备课的中小学教师：提供课程资料或一道母题，按“建立直觉 → 理解概念 → 掌握母题 → 练习变式 → 迁移与自查”生成学习材料。

这是 **AI 助手使用的 Skill**：指令、模板与本地辅助工具，不是独立网站或无需模型的自动出题程序。公开项目不包含原作者的课程讲义、考试文件或私人笔记。

## 能做什么

- **三种模式**：`learner` 自学与课程复习、`teacher` 教师备课、`variants` 上传母题生成变式。
- **题量可调**：基础题数、母题数、每母题变式数分别设置，可细化到单元和单道母题。
- **母题上传**：PDF、图片、文档或文本；核对原题和答案，提炼骨架，保留来源与母题关联。
- **变式有目的**：参数、条件、表征、逆向、辨错、迁移；附独立解答及相对母题的变化说明。
- **可解释评价**：预估难度、五维证据、考查知识、认知过程和置信度；无实测数据时不冒充真实难度系数。
- **适龄备课**：教学目标、课时安排、活动与追问、分层任务、出口检测、学生版与教师答案版。
- **模块可选**：知识讲解、题库、答案、关键词检索、掌握核对、术语表、教案、答题模板、评价表及模拟卷。
- **语言可选**：中文、英文、中英双语或跟随资料。选择双语时题干和解答全过程对应。
- **知识库更新**：每次调用可扫描本地新增/修改/重命名/移除资料，沿知识点和题目依赖修订内容，保留稳定编号与已审核笔记。
- **交付格式**：PDF、单文件离线 HTML、可编辑 Markdown，按任务选择；具体排版生成由宿主助手及其可用工具完成。
- **可选联网模块**：按课程/年级检索公开或用户获准访问的学科网、校园课程站点及社区资料，核验后分类、组题并追溯来源。账号会话需宿主提供正规授权能力。
- **额度提醒**：本次搜索、页面读取、下载尝试、每站点数及费用分别计量，80%提醒、触顶停止；网站真实余量不可见时明确标为未知。

## 安装与调用

在支持 Skills 的 Codex 中，让内置安装器从本仓库安装：

```text
使用 $skill-installer，从 C-xudco/course-study-guide 安装 Skill。
指定 ref 为 feature/authorized-online-research，路径为 skills/course-study-guide。
请使用该功能分支，不要安装 main 分支。
```

也可下载仓库，将 `skills/course-study-guide` 整个文件夹复制到宿主的个人 Skills 目录。当前 Codex 官方文档列出的用户目录为 `~/.agents/skills`；某些已有环境使用 `~/.codex/skills`，以宿主显示的实际技能位置为准。安装后调用 `$course-study-guide`，若未显示可重启宿主。参见 [官方 Skills 文档](https://learn.chatgpt.com/docs/build-skills)。

本功能分支可[直接下载ZIP](https://github.com/C-xudco/course-study-guide/archive/refs/heads/feature/authorized-online-research.zip)，或在仓库页面先选择该分支，再点击 **Code → Download ZIP**。完整下载流程见 [GitHub 官方说明](https://docs.github.com/en/repositories/working-with-files/using-files/downloading-source-code-archives)。下载原版请切换回 `main`；不要将资料网站下载的课程文件放入公开仓库。

## 联网找题、校园SSO与额度教程

完整流程见 [联网模块规范](skills/course-study-guide/references/online-research.md)，配置见 [联网配置示例](skills/course-study-guide/assets/online-research.example.json)，来源归类使用 [来源台账模板](skills/course-study-guide/assets/source-catalog-template.md)。

1. 告诉助手学校/年级、科目或课程代码、章节、年份、题量和允许访问的网站起始链接。大学课程优先官方课程/LMS，其他平台用于补充；“知乎/CSDN/GitHub上写着真题”不代表已经核实。
2. 开启 `online_research.enabled` 并设置允许的精确域名和预算。已有授权范围内的正常查询继续执行；新的授权范围、付费/扣点或额度变化按宿主规则处理。
3. 需要个人账号、校园网或SSO时，在网站正常登录界面**自行输入密码、验证码或扫码**。助手仅使用正规授权会话完成指定任务。不要把密码、Cookie或令牌发进聊天、配置或GitHub。
4. 助手区分“已实际读取、部分预览、只有元数据、无法访问”，按来源类别、年份、知识点、题型、难度和答案状态分类。核验题目与使用范围后组题，保留原题/改编/原创标记和出处；权限不明时给链接及原创同技能题。
5. 每次动作前检查预算，之后记录实际用量，失败与重试也计数。默认10次搜索、20次页面读取、3次下载尝试；金额和付费点数为0。80%提醒，达到上限或即将超限时停止相应操作并交付已有结果。
6. 网站余额只报告当前授权界面/官方工具或用户明确提供的真实信息，附依据；不可见时标未知。本地预算剩余不等于会员账户、API或模型订阅剩余额度。

示例：

```text
使用 $course-study-guide，教师模式，检索初中二次函数复习题。
允许在我指定的学科网/组卷网站查询；登录由我在网站完成。
先核验可用权限，按知识点和难度分类，选2道母题，每道生成3个原创变式。
本次最多10次搜索、20次页面读取、3次免费且不扣点的下载尝试；不付费。
80%时提醒，触顶先停止检索并整理已获得内容。输出学生版、教师答案和来源表。
```

```text
使用 $course-study-guide，查找我学校指定课程的已发布历年卷和复习资料。
我会提供学校官网课程起始链接，并自行完成校园SSO认证。
范围以本学期讲义为准；学校正式资料优先，知乎/GitHub/CSDN只作补充线索。
请区分已核验和待核验，按章节、年份、题型分类，附双语解答与用量摘要。
```

**DeepSeek / 豆包等普通聊天**：可将 [联网附加提示词](skills/course-study-guide/assets/online-research-prompt.md) 正文复制进你已创建的学案角色。只有搜索能力时查公开内容；若平台没有可交互浏览器/官方连接器，不能使用其他浏览器的校园登录态，此时由用户正常下载/导出后上传材料。不会因为粘贴提示词而自动获得账号访问权限。

本分支提供的是工作规范、模板和本地计量工具，未内置学科网/学校/知乎/CSDN的私有接口或通用SSO登录器。没有使用任何真实校园或会员账号进行端到端测试。网站权限、价格和额度以实际页面为准。

## 直接这样说

**自学 / 双语复习**

```text
使用 $course-study-guide。资料在我提供的课程文件夹，范围第1–5章。
中英双语；每单元2道基础题、2道母题，每道母题3个变式。
知识点从直觉逐步引入，答案放在题组后；要两套模拟卷、关键词检索和术语表。
输出PDF与离线HTML。以后补资料时更新同一知识库。
```

**小学教师备课**

```text
使用 $course-study-guide，teacher模式，为小学四年级“长方形周长”备课。
中文，40分钟，使用我上传的教材和2道母题；每道母题4个变式。
分支持、核心、拓展三层，方法不超出已学范围。
输出教案、学生练习版、教师答案与难度/考查维度表，不生成模拟卷。
```

**只从母题出变式**

```text
使用 $course-study-guide，variants模式。使用上传的3道母题，
每题生成4个变式，包含条件变化、逆向、辨错和迁移。
给母题关联、变化目的、完整答案、预估难度及考查知识；只输出题库和评价表。
```

也可复制 [配置示例](skills/course-study-guide/assets/config.example.json)。自然语言要求优先，无须先学会 JSON。默认题量为 2基础＋1母题＋3变式=6题；可以改成任意合理数量，模拟卷也可设为0。

## 本地辅助工具

需要 Python **3.10+**；仅标准库，无 API 密钥或第三方运行依赖。在仓库根目录运行：

```text
python skills/course-study-guide/scripts/validate_workbook.py examples/primary-perimeter.workbook.json
python skills/course-study-guide/scripts/assess_questions.py examples/primary-perimeter.workbook.json
python skills/course-study-guide/scripts/sync_knowledge_base.py --root examples/knowledge-base --manifest outputs/knowledge-base.json --apply
python -m unittest discover -s tests -v
```

联网预算工具只做本地演示，不发出网络请求：

```text
python skills/course-study-guide/scripts/quota_guard.py check --config examples/research.config.json --ledger outputs/research-usage-demo.json --domain courses.example.invalid --search-requests 1
python skills/course-study-guide/scripts/quota_guard.py status --config examples/research.config.json --ledger outputs/research-usage-demo.json
```

宿主真正完成操作后，用 `record` 记录实际用量（将示例配置和域名换成用户授权的配置）。`--page-reads`、`--downloads`、`--site-credits`、`--cost`、`--model-tokens` 可组合；点数按域名单独计量，金额按同一币种记录。`check`不写入台账；`record`会记录意外超额并返回停止状态。工具不自动拦截浏览器调用、不读取真实账户余额；台账须顺序更新，并与资料一样留在本地。

校验器检查内容结构、配置数量、母题关联、语言字段、跳转和计分；评价工具汇总模型/教师给出的显式评分；知识库工具计算哈希和依赖变化。**它们不自动理解题目、验证学术正确性或完成排版。** 解题、教学判断与生成由调用 Skill 的助手完成，仍需按流程核验。

“自主更新”在每次调用时运行，不是常驻监控。首次索引后，复用同一 manifest 可识别变化；`--workbook` 可额外输出受影响的单元、母题/变式、模拟题与检索入口。不加 `--apply` 只预览。

## 示例与贡献

[小学周长知识库](examples/knowledge-base/perimeter.md) 和 [完整可校验题库](examples/primary-perimeter.workbook.json) 均为本项目原创合成示例；非实际教材、课标认证或真实学生数据。

欢迎补充学科模板、适龄变式和可复现问题，见 [贡献说明](CONTRIBUTING.md)。不要提交未获授权的教材全文、试卷、个人课程文件、学生姓名或成绩。公开代码不等于使用过程中产生的知识库也应公开。

## 许可证与边界

[MIT](LICENSE)，可使用、修改和再分发本项目的代码、指令与原创模板。用户上传的材料仍按其各自权利与许可处理。预估难度不是标准化测评结论；课程/课标对齐需有实际来源，不凭年级名称自动声称认证。生成内容需核查知识、答案和教学适用性。
