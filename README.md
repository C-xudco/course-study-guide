# Course Study Guide · 递进式学案与教师备课

**同一套循序渐进的学习方法，提供 Codex、豆包、DeepSeek Harness 三个适配版本。** 给自学者和大学生整理课程、复习与母题变式，也给中小学教师准备教案、分层任务和答案。

[English](README.en.md) · **[零基础安装总教程](docs/INSTALL.md)** · [使用与贡献](CONTRIBUTING.md) · [MIT许可证](LICENSE)

## 第一次来：只选你正在使用的应用

| 你使用的应用 | 下载与分支 | ZIP内要取出的文件夹 | 安装教程 |
|---|---|---|---|
| **Codex** | [main原版](https://github.com/C-xudco/course-study-guide/tree/main) · [下载ZIP](https://github.com/C-xudco/course-study-guide/archive/refs/heads/main.zip) | `skills/course-study-guide` | [Codex小白教程](docs/INSTALL-CODEX.md) |
| **豆包：有本地Skill功能的版本** | [豆包分支](https://github.com/C-xudco/course-study-guide/tree/doubao/progressive-study-guide) · [下载ZIP](https://github.com/C-xudco/course-study-guide/archive/refs/heads/doubao/progressive-study-guide.zip) | `platforms/doubao/progressive-study-guide` | [豆包小白教程](docs/INSTALL-DOUBAO.md) |
| **DeepSeek Harness** | [DeepSeek分支](https://github.com/C-xudco/course-study-guide/tree/deepseek/progressive-mastery-tutor) · [下载ZIP](https://github.com/C-xudco/course-study-guide/archive/refs/heads/deepseek/progressive-mastery-tutor.zip) | `platforms/deepseek/progressive-mastery-tutor` | [DeepSeek Harness小白教程](docs/INSTALL-DEEPSEEK.md) |

**不知道选哪个？** 看你平时打开的应用名称来选，不需要为了使用学案而同时安装三个应用。普通DeepSeek网页聊天与DeepSeek Harness不同；普通聊天的备用方式见各教程。Skill是给AI执行的指令包，双击 `SKILL.md` 只会打开文字，不会启动学习软件。

下载ZIP → 解压 → 取出表中那**整个Skill文件夹** → 放入对应应用识别的目录 → 新会话测试。不要只复制 `SKILL.md`，也不要把整个ZIP直接当作已安装。详细步骤、目录长什么样、首次测试、备份更新与常见问题都写在教程中。

## 三版分别有什么特点

| 对比项 | Codex版 | 豆包版 | DeepSeek Harness版 |
|---|---|---|---|
| Skill名称 | `course-study-guide` | `progressive-study-guide` | `progressive-mastery-tutor` |
| 重点 | 学案、备课、结构化题库与本地辅助工具 | 原生中文三模式、易用的参考文件组织 | 11步完整单元、7字段母题卡、方法白名单与细化评价 |
| 调用 | `$course-study-guide` | 用名称请求；以豆包实际Skill界面为准 | `/progressive-mastery-tutor`，需宿主启用Skill能力 |
| 母题/变式/题量可调 | 支持 | 支持 | 支持 |
| 中文、英文、中英对照 | 支持 | 支持 | 支持；默认跟随用户语言 |
| 难度与考查维度 | 五维证据＋教学预估 | 五维证据＋教学预估 | 五维证据、认知过程、置信度与四段式详解 |
| 教师与学生版本 | 支持 | 支持 | 支持 |
| 运行依赖 | 指令无需Python；辅助脚本需Python 3.10+ | 指令包，无执行脚本 | 指令包，无执行脚本 |

三版遵循共同流程，细节和预设有所不同，**不要把平台A的安装目录或调用符号套到平台B**。文件读取、联网、登录会话、PDF/Word生成均由宿主实际工具提供，安装Skill不自动增加这些工具。

## 从资料到学习包的共同流程

1. 提供讲义、教材、笔记、练习或母题，说明年级/基础、范围、语言和目标。
2. 核对实际可读资料、缺口和原答案，按先修关系安排单元。
3. 从直觉、定义和条件讲到完整示范，再给通用方法、母题与有目的的变式。
4. 每题对应详解、知识考查、认知过程和有证据的预估难度；双语时题干与解答对应。
5. 开头放关键词检索，末尾放掌握核对与术语；教师可要学生无答案版和教师版。
6. 用户补充资料后沿题目依赖更新，保留编号与已审核笔记，用续作记录衔接下一批。

默认完整单元为2基础＋1母题＋每母题3变式=6题；总母题数、逐单元/逐母题数量、0变式、0模拟卷均可指定。上传的适用母题默认保留，明确筛选时按用户选择。不同版本模拟卷默认值以各自配置为准，可直接说“要0套/2套”。

## 安装后，复制这段就能开始

```text
使用我刚安装的递进式学习Skill，根据我本次上传的讲义整理第一章。
自学模式，中文，先用直觉和小例子引入，再讲条件与方法。
先做1个单元：2道基础题、1道母题、每母题3个变式，不出模拟卷。
题组后给完整详解，标注考查维度、五维难度依据和教学预估。
开头给关键词检索，最后给掌握核对与术语表。
不要只给提纲；资料足够就开始。没有实际文件生成工具时先给可编辑正文。
```

教师可改为“教师备课，四年级，40分钟，学生无答案版＋教师详解版”；只出变式可说“仅母题变式，保留上传3道母题，每题2个变式，不出基础题”。三平台的准确调用示例在专用教程中。

## 联网、知识库更新与额度

Codex的[授权联网功能分支](https://github.com/C-xudco/course-study-guide/tree/feature/authorized-online-research)提供来源台账与本次预算工具；豆包发布包含可选联网规范。DeepSeek本次包以资料教学和题目评价为主；如需联网，可按宿主能力叠加[通用联网附加指令](https://github.com/C-xudco/course-study-guide/blob/feature/authorized-online-research/skills/course-study-guide/assets/online-research-prompt.md)。不能据此声称三版都内置网站连接器或自动计费监控。

账号登录/SSO由用户在正常界面完成，不把密码、Cookie或令牌放进聊天或仓库。任务预算与网站/模型真实余额分开，未报告余额就写未知。知识库更新发生在本次调用，不是后台常驻监控或跨对话永久记忆。公开仓库不包含教材、私人课程、学生数据或生成学案。

## 分支与初版保留

- `main`：Codex原版Skill与三版统一文档。此次主分支只更新介绍与安装文档，原Skill、脚本、测试和示例保持原实现。
- `doubao/progressive-study-guide`：豆包独立发布快照。
- `deepseek/progressive-mastery-tutor`：DeepSeek专用分支，同时保留三套包以便查阅；安装时只取目标应用的一套。
- `feature/authorized-online-research`：原有联网扩展分支。
- [初版实现快照](https://github.com/C-xudco/course-study-guide/tree/afb702f2822ea9649b23fd6104aa226b42efe787)：更新文档前的原版可随时查看。

## Codex辅助工具与示例

仅在需要结构化校验时使用；普通安装不需要运行。Python 3.10+，仅标准库：

```text
python skills/course-study-guide/scripts/validate_workbook.py examples/primary-perimeter.workbook.json
python skills/course-study-guide/scripts/assess_questions.py examples/primary-perimeter.workbook.json
python -m unittest discover -s tests -v
```

工具检查结构、显式评分及知识库变化，不能替代学术答案核验。[原创周长示例](examples/primary-perimeter.workbook.json)不对应真实学生或教材。欢迎按[贡献说明](CONTRIBUTING.md)补充模板与可复现问题。

## 许可与验证

[MIT](LICENSE)适用于项目代码、指令与原创模板；用户材料按各自许可处理。难度是教学预估，课程/课标对齐需有依据，生成答案须核查。公开说明只报告实际完成的静态/打包/脚本检查，不承诺每个应用版本与模型输出都已端到端验证。
