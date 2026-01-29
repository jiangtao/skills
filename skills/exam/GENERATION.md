# 生成信息

- **类型：** Type 3 - 手动技能（手写）
- **来源：** 为本集合创建的原创技能
- **创建时间：** 2026-01-30
- **版本：** 0.1.0

## 技能结构

这是一个遵循 AGENTS.md 规范的手动 Type 3 技能：

```
skills/exam/
├── skill.md              # 主技能索引，包含命令模式
├── GENERATION.md         # 本文件
└── references/
    ├── question-types.md # 题型详细规范
    ├── parameters.md     # 命令参数和验证
    ├── examples.md       # 使用示例和输出样例
    └── error-handling.md # 错误场景和恢复
```

## 实现说明

- **命令类型：** 伪命令（对话模式，非可执行）
- **触发模式：** `/edu:exam` 带可选参数
- **输出：** PDF 文件生成（由 Claude Code 助手处理）
- **依赖：** 无（纯 markdown 技能）
- **语言：** 中文题目内容，中文文档

## 测试清单

- [ ] 目录结构符合 AGENTS.md Type 3 规范
- [ ] skill.md 有有效的 frontmatter（name、description、metadata）
- [ ] 所有参考文件都有 frontmatter
- [ ] skill.md 中存在核心参考表
- [ ] 已在 meta.ts 的 manual 数组中注册
- [ ] 无 TypeScript linting 错误
- [ ] 所有提交消息遵循格式："feat: ..."
