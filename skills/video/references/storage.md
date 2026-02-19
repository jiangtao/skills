---
name: storage
description: 文件分类存储管理规范
---

# 存储管理

按来源和日期分类存储视频文件。

## 目录结构

```
downloads/
├── youtube/
│   ├── 2024/
│   │   ├── 02/
│   │   │   └── baby_video_1708089600.mp4
│   │   └── 03/
│   └── 2025/
│       └── 01/
├── bilibili/
│   └── 2024/
│       └── 02/
│           └── anime_episode_1708089800.mp4
└── direct/
    └── 2024/
        └── 02/
            └── recording_1708089900.avi
```

## 存储管理器

```python
from pathlib import Path
from datetime import datetime

class StorageManager:
    def __init__(self, base_dir: Path,
                 date_format: str = "%Y/%m"):
        self.base_dir = Path(base_dir)
        self.date_format = date_format
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def get_output_dir(self, source: str, date: datetime) -> Path:
        """
        获取输出目录

        目录结构: base_dir/{source}/{date}/
        例如: downloads/youtube/2024/02/
        """
        source_dir = self.base_dir / source
        date_dir = source_dir / date.strftime(self.date_format)
        date_dir.mkdir(parents=True, exist_ok=True)
        return date_dir
```

## 文件命名规则

默认格式: `{title}_{timestamp}`

```python
def get_filename(task: DownloadTask) -> str:
    safe_title = sanitize_filename(task.title or "video")
    timestamp = int(task.created_at.timestamp())
    return f"{safe_title}_{timestamp}"
```

## 下载提速

### 并发下载

默认并发数为 10，可根据网络情况调整：

```bash
# 增加并发数到 16
skills/video/bin/download_manager.sh --pending -c 16

# 降低并发数（网络较差时）
skills/video/bin/download_manager.sh --pending -c 5
```

### 速度调优建议

| 网络环境 | 并发数 | 说明 |
|---------|--------|------|
| 家庭宽带 | 8-12 | 默认配置 |
| 千兆网络 | 16-20 | 可增加并发数 |
| 企业网络 | 5-8 | 避免占用过多带宽 |
| 海外网络 | 5-8 | 减少超时风险 |

**注意**: 如果已设置系统代理，程序会自动使用。
