# DeepSeek Harness小白安装教程

[安装总入口](INSTALL.md) · [首页三版对照](../README.md)

目标Skill：`progressive-mastery-tutor`（递进式学习与母题研究助手）。**适配DeepSeek Harness，不等于普通DeepSeek网页聊天。** 先确认Harness本身已能正常使用；还没有应用时从[DeepSeek官方Harness页面](https://deepseek.com/en/harness/)查安装入口，不要安装同名第三方包冒充官方应用。

## 1. 下载并取出整个Skill文件夹

1. [下载DeepSeek专用分支ZIP](https://github.com/C-xudco/course-study-guide/archive/refs/heads/deepseek/progressive-mastery-tutor.zip)。
2. 找到下载的ZIP，右键解压。
3. 在解压目录依次打开 `platforms` → `deepseek`。
4. 找到并复制整个 `progressive-mastery-tutor` 文件夹；进入它应直接看到 `SKILL.md` 和 `references`。

包内9个文件：

```text
progressive-mastery-tutor/
  SKILL.md
  references/
    source-audit.md
    unit-design.md
    mother-problems.md
    assessment.md
    deliverables.md
    bilingual.md
    templates.md
    example-unit.md
```

## 2. 推荐：放到用户级Skill目录（Windows）

默认Harness配置根是 `~/.dsh`，其中的 `skills` 会由文件Skill provider扫描。若你的环境设置了 `DSH_HOME`，应使用它指向目录下的 `skills`，不要继续套默认位置。[官方目录说明](https://github.com/deepseek-ai/deepseek-harness/blob/master/packages/skill/skill-filesystem/README.md)

1. 打开资源管理器，在地址栏输入 `%USERPROFILE%` 后回车，这就是当前用户的个人文件夹。
2. 默认配置下，找到 `.dsh` 文件夹；没有可新建名为 `.dsh` 的文件夹，再在其中新建 `skills`。
3. 进入 `.dsh\skills`，粘贴刚才复制的整个 `progressive-mastery-tutor`。
4. 最终结构必须是 `.dsh\skills\progressive-mastery-tutor\SKILL.md`，不能多套一层。
5. 若已有同名包，先把旧包备份到扫描目录外，再放完整新包。macOS/Linux默认可放 `~/.dsh/skills/progressive-mastery-tutor`。

文件放好不等于当前profile一定启用了发现功能；下面还要检查Harness是否实际识别。

## 3. 另一种：只给当前项目使用

在Harness实际使用的项目根目录下建立 `.dsh/skills`，把整个Skill文件夹放进去。例：`项目根/.dsh/skills/progressive-mastery-tutor/SKILL.md`。如果有Git仓库，项目根按最近的 `.git` 所在目录判断；否则使用当前工作目录。[官方规则](https://github.com/deepseek-ai/deepseek-harness/blob/master/packages/skill/skill-filesystem/README.md)

**下载区、桌面普通文件夹、名为 `skill` 的源文件夹并不会自动变成发现目录。** 只有它本身已被配置为 `customSkillDirs` 等扫描根时，才可直接作为运行位置。不要同时在多处安装同名Skill而不清楚优先级。

## 4. 调用并确认真的加载

在Harness新会话输入：

```text
/progressive-mastery-tutor
```

官方Skill能力支持直接 `/name` 调用，但要求当前profile提供目录发现与Skill工具。[官方Skill能力说明](https://github.com/deepseek-ai/deepseek-harness/blob/master/packages/skill/README.md)

然后上传一段实际可读讲义并发送：

```text
使用递进式学习与母题研究助手，按我刚上传的资料做1个单元。
自学，常规场景，中文；2基础＋1母题＋每母题3变式，0套模拟卷。
先直觉、先修和定义，再示范、母题与变式；答案集中在题组后。
给五维教学预估与证据、关键词检索、掌握核对、术语表和续作记录。
资料足够就开始，不要只给提纲；先交付Markdown正文。
```

验证它使用的是当前 `progressive-mastery-tutor`，而不是只在普通对话里口头答应。再用[总教程的小题量测试](INSTALL.md)核对母题/变式数量、答案对应和0变式设置。

## 5. 三种日常用法

**教师备课**：“教师模式，四年级，40分钟，2道上传母题每题3个变式，学生无答案版＋教师详解/评价/教案，0模拟卷。”

**只出变式**：“仅母题变式，保留我上传的3道母题，每题2变式，含条件变化与辨错；逐题完整答案和评价，不写整套学案。”

**考试复习**：“自学＋考试复习，中英双语，母题总共3道，每题2变式，2套原创练习卷。题干、小问、关键步骤、完整答案与评分点双语对应。”

默认语言跟随用户，不会因为Skill用中文写就强迫英文用户读中文。模拟卷为原创训练，不预测考试。课时未指定时45分钟只是本版假设，可改。

## 6. 识别不到时按顺序排查

1. 文件是否叫 `SKILL.md`，不是 `.txt`，没有多套一层目录，8份参考文件都在。
2. 是否用了 `DSH_HOME` 自定义根，或把源文件放在普通目录而未加入扫描。
3. 当前profile是否启用文件Skill provider及Skill工具。定制部署由维护者按官方说明确认 `@deepseek-ai/dsh-skill`、`@deepseek-ai/dsh-skill-filesystem` 及相应Skill调用工具；不要盲目改配置或用插件安装命令安装这份文字Skill。
4. 官方默认provider会监视目录并在后续目录刷新中反映变化；若没看到，先检查目录，再用新会话验证，不能保证所有定制profile无需重新加载。

## 7. 普通DeepSeek聊天的备用方法

如果你只有DeepSeek网页/普通聊天，把 `SKILL.md` 正文与本次相关参考文件直接上传或粘贴到同一对话。母题用 `mother-problems.md`，评价用 `assessment.md`，学案用 `unit-design.md` 和 `deliverables.md`，双语再加 `bilingual.md`；这些文件名都在包的 `references` 中。

这是手动提供工作规范，不等于安装Harness Skill。不要只发送磁盘路径，也不要假装普通聊天能直接访问其他浏览器登录态、后台监控目录或跨会话保存资料。

## 8. 文件生成、额度与更新

本包只有指令和模板，没有执行脚本或账号/SSO连接器。生成PDF/Word依赖当前工具；没有导出能力时交付Markdown，再复制到Word/WPS检查后导出。长学习包消耗的模型额度由你的Harness提供方/账户决定，Skill不读取或推测真实余额。

每批保存续作记录，补充新资料后让它按差异更新稳定编号与索引。更新Skill按[总教程](INSTALL.md)先备份再替换完整包。此次发布已做静态与打包检查，没有在Harness重新进行模型端到端测试；[审核记录](https://github.com/C-xudco/course-study-guide/blob/deepseek/progressive-mastery-tutor/platforms/deepseek/REVIEW.md)如实说明范围。
