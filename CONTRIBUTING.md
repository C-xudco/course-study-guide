# Contributing / 贡献

欢迎改进学科模板、母题变式策略、年级适宜性、语言表达与辅助工具。

提交问题时提供预期行为、实际行为、模式/选项和最小可复现的原创或有权分享的示例。不上传私人课程资料、教师内部试卷、可识别学生记录或密钥。

修改工具后运行 `python -m unittest discover -s tests -v`，并运行 README 中的示例校验。新增变式应有解答、来源/原创标记、母题关联、变化目的与难度估计证据。不要仅通过换数字宣称增加认知层级。

保持 Skill 的主入口简明，将模式细节放入有链接的参考文件。区分模型完成的工作、确定性脚本的功能和未来设想；贡献文档不要宣称尚未实现的 UI、后台服务或验证能力。

Pull requests should include the behavior change and relevant validation. Please use synthetic or shareable examples, keep model estimates separate from observed student results, and preserve backward compatibility or document migrations.
