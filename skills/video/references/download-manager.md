---
name: download-manager
description: 下载管理模块规范
---

# 下载管理模块

负责管理待下载队列、调用 lux 进行下载、控制并发、以及文件的分类存储。

## 核心组件

### 1. 队列管理器 (QueueManager)

```python
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

class TaskStatus(Enum):
    PENDING = "pending"
    DOWNLOADING = "downloading"
    COMPLETED = "completed"
    FAILED = "failed"
    PAUSED = "paused"

@dataclass(order=True)
class DownloadTask:
    priority: int = field(compare=True, default=0)
    task_id: str = field(compare=False)
    url: str = field(compare=False)
    title: str = field(compare=False, default="")
    status: TaskStatus = field(compare=False, default=TaskStatus.PENDING)
    progress: float = field(compare=False, default=0.0)
```

### 2. Lux 下载器

```python
class LuxDownloader:
    def __init__(self, lux_path: str = "lux"):
        self.lux_path = lux_path

    def download(self, url: str, output_dir: Path,
                 quality: str = "best") -> Dict[str, Any]:
        """
        执行下载

        Args:
            url: 视频 URL
            output_dir: 输出目录
            quality: 视频质量 (best/worst/high/low)

        Returns:
            包含下载结果和信息的字典
        """
        cmd = [self.lux_path, "-c", str(output_dir), "-f", quality, url]
        # 执行下载逻辑
        pass
```

### 3. 并发控制器

```python
class ConcurrencyController:
    def __init__(self, max_workers: int = 3):
        self.max_workers = max_workers
        self._semaphore = Semaphore(max_workers)
        self._executor = ThreadPoolExecutor(max_workers=max_workers)

    def start(self):
        """启动下载控制器"""
        pass

    def stop(self, wait: bool = True):
        """停止下载控制器"""
        pass
```

## 主下载管理器

```python
class DownloadManager:
    def __init__(self, base_dir: Path = Path("./downloads"),
                 max_concurrent: int = 3):
        self.queue_manager = QueueManager()
        self.downloader = LuxDownloader()
        self.storage_manager = StorageManager(base_dir)
        self.concurrency_controller = ConcurrencyController(
            max_workers=max_concurrent
        )

    def add_urls(self, urls: List[str], priority: int = 0) -> List[str]:
        """添加下载 URL 列表"""
        pass

    def start_download(self):
        """开始下载"""
        pass

    def get_status(self) -> Dict[str, Any]:
        """获取下载状态"""
        pass
```
