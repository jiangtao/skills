---
name: video
description: 视频链接收集和下载管理工具
metadata:
  author: Jiangtao
  version: "0.1.0"
---

> 基于 lux 的视频下载工具，支持多来源链接收集、去重、并发下载和分类存储。

## 概述

video 技能提供完整的视频下载解决方案：

- **链接收集：** 支持手动输入、书签导入、历史记录、剪贴板监控
- **下载管理：** 队列管理、并发控制、断点续传
- **分类存储：** 按来源和日期自动分类存储
- **多平台支持：** Bilibili、YouTube、直接链接

## 使用方法

```bash
/video [--collect] [--download] [--status]
```

**触发短语：**
- `/video`
- `download videos` / `视频下载`
- `collect links` / `收集链接`

## 核心参考

| 主题 | 描述 | 参考 |
|-------|-------------|-----------|
| 链接收集 | 链接来源、去重、存储接口 | [链接收集模块](references/link-collector.md) |
| 下载管理 | 队列管理、lux 封装、并发控制 | [下载管理模块](references/download-manager.md) |
| 存储策略 | 文件分类、目录结构、命名规则 | [存储管理](references/storage.md) |
| 使用示例 | 命令行用法和 API 示例 | [使用示例](references/usage.md) |

## 执行脚本

**位置：** `bin/`

| 脚本 | 功能 | 依赖 |
|------|------|------|
| `collect_links.sh` | 链接收集执行脚本 | Python 3.10+ |
| `download_manager.sh` | 下载管理执行脚本 | lux, Python 3.10+ |
