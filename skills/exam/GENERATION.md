# 生成信息

- **类型：** Type 3 - 手动技能（手写）
- **来源：** 为本集合创建的原创技能
- **创建时间：** 2026-01-30
- **版本：** 0.2.0

## 技能结构

这是一个遵循 AGENTS.md 规范的手动 Type 3 技能：

```
skills/exam/
├── skill.md              # 主技能索引，包含命令模式
├── GENERATION.md         # 本文件
├── bin/
│   └── generate_pdfkit.js # PDF 生成脚本 (Node.js + PDFKit)
├── fonts/
│   └── SourceHanSansCN-Normal.ttf # 思源黑体中文字体
└── references/
    ├── question-types.md # 题型详细规范
    ├── parameters.md     # 命令参数和验证
    ├── examples.md       # 使用示例和输出样例
    └── error-handling.md # 错误场景和恢复
```

## 实现说明

- **命令类型：** 伪命令（对话模式，非可执行）
- **触发模式：** `/edu:exam` 带可选参数
- **输出：** PDF 文件生成（使用内置的 Node.js + PDFKit 脚本）
- **依赖：** Node.js + npm install pdfkit
- **语言：** 中文题目内容，中文文档

## PDF 生成脚本

**技术栈：** Node.js + PDFKit + 思源黑体

**特性：**
- A4 纸张格式 (210mm × 297mm)
- 中文字体嵌入 (Source Han Sans CN)
- 符合打印规范的布局
- 总分 100 分：根据题目数量调整和均分
  - 口算题：2 分/题
  - 计算题：4 分/题
  - 应用题：10 分/题

## 测试清单

- [ ] 目录结构符合 AGENTS.md Type 3 规范
- [ ] skill.md 有有效的 frontmatter（name、description、metadata）
- [ ] 所有参考文件都有 frontmatter
- [ ] skill.md 中存在核心参考表
- [ ] 已在 meta.ts 的 manual 数组中注册
- [ ] 无 TypeScript linting 错误
- [ ] 所有提交消息遵循格式："feat: ..."
