# 生成信息

- **类型：** Type 3 - 手动技能（手写）
- **来源：** 原创技能，从 baby-video 项目迁移
- **创建时间：** 2026-02-18
- **版本：** 0.1.0
- **原始项目：** https://github.com/jiangtao/baby-video

## 技能结构

```
skills/video/
├── skill.md              # 主技能索引，包含命令模式
├── GENERATION.md         # 本文件
├── bin/
│   ├── collect_links.sh  # 链接收集执行脚本
│   └── download_manager.sh # 下载管理执行脚本
└── references/
    ├── link-collector.md # 链接收集模块规范
    ├── download-manager.md # 下载管理模块规范
    ├── storage.md        # 存储管理规范
    └── usage.md          # 使用示例
```

## 依赖

- **命令类型：** 伪命令（对话模式，非可执行）
- **触发模式：** `/video` 带可选参数
- **外部依赖：**
  - lux (视频下载工具)
  - Python 3.10+
  - git (worktree 支持)
