---
name: video
description: 视频链接收集和下载管理工具
metadata:
  author: Jiangtao
  version: "0.2.0"
---

> 基于 yt-dlp 的视频下载工具，支持多来源链接收集、去重、并发下载、自动合并和分类存储。

## 概述

video 技能提供完整的视频下载解决方案：

- **链接收集：** 支持手动输入、书签导入、历史记录、剪贴板监控
- **下载管理：** 队列管理、并发控制、断点续传
- **自动合并：** 使用 ffmpeg 自动合并分离的视频和音频轨道
- **分类存储：** 按来源和日期自动分类存储
- **多平台支持：** Bilibili、YouTube、直接链接

## 使用方法

### 命令模式

```bash
# 收集视频链接
/video --collect --url "https://www.youtube.com/watch?v=xxx"

# 下载已收集的视频
/video --download

# 查看下载状态
/video --status

# 合并分离的视频和音频文件
/video --merge --directory "./videos"
```

### 触发短语

- `/video`
- `download videos` / `视频下载`
- `collect links` / `收集链接`
- `merge videos` / `合并视频`

## Integration with CLAUDE.md

video skill 与项目的 CLAUDE.md 配合使用：
- `/video --collect` 触发链接收集队员
- `/video --download` 触发下载管理队员
- 支持 Agent Team 协作模式进行任务分配

## 核心参考

| 主题 | 描述 | 参考 |
|-------|-------------|-----------|
| 链接收集 | 链接来源、去重、存储接口 | [link-collector](references/link-collector.md) |
| 下载管理 | 队列管理、yt-dlp 封装、并发控制 | [download-manager](references/download-manager.md) |
| 存储策略 | 文件分类、目录结构、命名规则 | [storage](references/storage.md) |
| 视频合并 | 自动合并分离的视频和音频文件 | [video-merger](references/video-merger.md) |
| 使用示例 | 命令行用法和 API 示例 | [usage](references/usage.md) |

## 执行脚本

**位置：** `bin/`

| 脚本 | 功能 | 依赖 |
|------|------|------|
| `collect_links.sh` | 链接收集执行脚本 | Python 3.10+ |
| `download_manager.sh` | 下载管理执行脚本 | yt-dlp, Python 3.10+ |
| `video_merger.py` | 自动合并视频和音频文件 | Python 3.10+, ffmpeg |

## Agent Team

本项目使用 Agent Team 协作模式：

- **链接收集队员 (link-collector)** - 负责链接收集、去重、本地存储
- **下载管理队员 (download-manager)** - 负责队列管理、yt-dlp 调用、并发控制、分类存储
- **视频合并队员 (video-merger)** - 负责自动合并分离的视频和音频文件

### 工作流

1. 用户请求下载视频
2. link-collector 收集和验证链接
3. download-manager 执行下载任务
4. 报告结果和状态
