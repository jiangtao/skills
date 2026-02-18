---
name: usage
description: 使用示例和命令行接口
---

# 使用示例

## 基本使用

### Python API

```python
from pathlib import Path
from download_manager import DownloadManager

# 创建下载管理器
manager = DownloadManager(
    base_dir=Path("./videos"),
    max_concurrent=3
)

# 添加下载链接
urls = [
    "https://www.youtube.com/watch?v=example1",
    "https://www.bilibili.com/video/BV1xx411c7mD",
]
task_ids = manager.add_urls(urls)

# 开始下载
manager.start_download()

# 查看状态
status = manager.get_status()
print(f"Status: {status}")
```

### 命令行使用

```bash
# 下载单个视频
lux -o "./videos" "https://www.bilibili.com/video/BVxxx"

# 批量下载
lux -o "./videos" -F video_list.txt

# 仅获取信息
lux -i "https://www.youtube.com/watch?v=xxx"
```

## 依赖安装

```bash
# 安装 lux
brew install lux

# 安装 ffmpeg
brew install ffmpeg

# 验证安装
lux --version
ffmpeg --version
```
