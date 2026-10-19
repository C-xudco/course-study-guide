# 豆包小白安装教程

[安装总入口](INSTALL.md) · [首页三版对照](../README.md)

目标Skill：`progressive-study-guide`，中文名“递进式学案与备课助手”。适用于已具备本地Skill发现功能的豆包版本。下面目录来自用户实际使用的Windows实例，不代表所有豆包版本或所有系统都相同。

## 1. 下载正确版本

1. [下载豆包分支ZIP](https://github.com/C-xudco/course-study-guide/archive/refs/heads/doubao/progressive-study-guide.zip)。
2. 右键解压，打开 `platforms` → `doubao`。
3. 找到 `progressive-study-guide`。进入后应看到 `SKILL.md`、`references`、`assets`。
4. 返回上一层，复制这整个 `progressive-study-guide` 文件夹。

## 2. 找到你的真实Skill目录

如果你这台豆包已经创建过Skill，优先找到它实际保存的位置。对用户提供的Windows安装实例，可在资源管理器地址栏输入：

```text
%LOCALAPPDATA%\Doubao\User Data\Default\.doubao\agent_mode\workspace\.user_skills
```

如果路径能打开，而且确实是当前豆包使用的Skill目录，就继续。若打不开，不要新建整条路径就宣称装好了：先在当前豆包版本中查实际Skill目录或正常创建一个简单Skill来确定位置。普通聊天版本可能根本没有此本地机制，此时用下方备用方式。

## 3. 粘贴与检查

1. 若已有同名Skill，将旧的完整文件夹备份到 `.user_skills` 外，避免同时识别两份。
2. 粘贴下载的整个文件夹。
3. 打开后，确认最终结构是 `.user_skills\progressive-study-guide\SKILL.md`，旁边有 `references` 和 `assets`。
4. 按当前应用实际提供的刷新/重载方式加载；若没有该入口，可重新打开豆包并在新会话测试。这里不假定存在某个“导入ZIP”按钮。

## 4. 第一次这样用

上传一小段讲义，发送：

```text
请使用“递进式学案与备课助手”（progressive-study-guide）。
根据我刚上传的讲义，中文自学，只做1个单元。
2道基础题、1道母题、每母题3个变式，0套模拟卷。
由直觉慢慢引入，先示范后练习，题组后给完整详解。
要关键词检索、知识点核对和术语表；先交付正文。
```

不是发送Codex的 `$skill-installer`。不同平台调用方式不同。验收方法见[总教程](INSTALL.md)，尤其检查题量与学生版是否泄漏答案。

## 5. 如果只有普通豆包聊天

打开 `SKILL.md`，把正文复制到同一对话；再上传/粘贴本次模式需要的参考文件：自学用 `mode-self-study.md`，教师用 `mode-teacher.md`，变式用 `mode-variant.md`；出题补 `question-evaluation.md`，双语/成品补 `bilingual-and-output.md`。让它按这些实际提供的内容处理资料。

这属于手动提供指令，不声称已经安装原生Skill；仅发路径不能让普通聊天访问硬盘。

## 6. 联网、PDF与更新

本包有可选联网规范，但必须豆包当前真的能联网/操作已授权网页。不要发送密码、验证码、Cookie或令牌。没有文件生成工具就先复制正文到Word/WPS，检查公式后导出PDF；没有实际导出文件时不应出现假下载链接。

更新前备份整个旧包，按以上步骤替换完整目录；资料与生成学案单独存放。更细说明见[豆包发布说明](https://github.com/C-xudco/course-study-guide/blob/doubao/progressive-study-guide/platforms/doubao/README.md)。
