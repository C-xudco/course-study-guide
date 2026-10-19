# Codex小白安装教程

[安装总入口](INSTALL.md) · [首页三版对照](../README.md)

目标：安装名为 `course-study-guide` 的Codex Skill。先保证Codex已安装并能正常聊天；不用先安装Python，普通学案工作流不要求你运行脚本。

## 方法A：直接让Codex安装（最省事）

在Codex新对话粘贴：

```text
使用 $skill-installer，从GitHub仓库 C-xudco/course-study-guide 安装Skill。
ref=main，path=skills/course-study-guide。
如果已有同名Skill，请先告诉我实际位置并保留可恢复备份，再更新完整文件夹。
完成后核对Skill是否出现在可用列表里，不要只告诉我“已完成”。
```

等待实际下载和检查结果。安装需要可用网络和文件权限，按Codex实际提示处理。如果界面找不到内置安装器，使用下面的手动方法。

## 方法B：手动复制（Windows）

1. [下载Codex版ZIP](https://github.com/C-xudco/course-study-guide/archive/refs/heads/main.zip)，右键解压。
2. 打开解压目录，再打开 `skills`，找到 `course-study-guide` 文件夹。进入它应看到 `SKILL.md`、`references`、`assets`、`agents`、`scripts`。
3. 返回上一层，复制整个 `course-study-guide`。
4. 打开资源管理器，在地址栏粘贴 `%USERPROFILE%\.agents\skills` 后按回车。若这是你的Codex个人Skill目录但尚不存在，可在用户目录下依次创建 `.agents`、`skills`。
5. 将复制的文件夹粘贴进去。最终结构应是 `.agents\skills\course-study-guide\SKILL.md`，中间没有第二层 `course-study-guide`。
6. 新会话输入 `$course-study-guide`，看看是否能选到/调用目标Skill；未显示时重启Codex，再核对实际目录。

这采用当前[OpenAI官方用户级路径](https://learn.chatgpt.com/docs/build-skills)。某些已有环境由安装器管理在 `~/.codex/skills`；如果你的环境实际在那里加载，请沿用其安装器报告的位置，不要在两个扫描目录重复装同名包。macOS/Linux用户可使用 `~/.agents/skills/course-study-guide`。

## 第一次这样用

先上传或粘贴一段你有权使用的讲义，再发送：

```text
使用 $course-study-guide。按我刚上传的第一章，中文，自学。
只做1个单元：2基础题＋1母题＋每母题3个变式，0套模拟卷。
先讲直觉与条件，再给完整示范、题组和逐题详解。
给关键词索引、掌握核对、术语表；先输出可编辑正文。
```

不要只发一个你电脑上的路径就假定已授权可读；让Codex报告实际读取结果。需要双语可加“题干、小问、关键步骤和完整答案都中英对照”。

## 可选功能及排错

需要来源台账和本次搜索预算工具时，改为安装 `feature/authorized-online-research` 的同一路径；这是另一个发布分支，别把“默认main”当成已带该扩展。联网不等于可使用任何登录账户。

若要使用本地题库校验等Python辅助工具，再按根README的“Codex辅助工具”说明操作；它们只校验结构和显式数据，不自动证明学术答案正确。

识别不到时依次检查：分支是否main、文件夹内是否立即有 `SKILL.md`、后缀是否正确、当前Codex实际扫描位置、是否有同名重复包。[更新与备份](INSTALL.md)。
