---
name: link-collector
description: 链接收集模块规范
---

# 链接收集模块

负责从多种来源收集视频下载链接，进行去重处理后，传递给下载模块。

## 支持的链接来源

### 1. 手动输入 URL

用户直接通过命令行或配置文件提供链接。

```bash
# 命令行参数
python collector.py --url "https://www.youtube.com/watch?v=xxx"

# 多个链接
python collector.py --url "url1" --url "url2"
```

### 2. 浏览器书签导入

支持从 Chrome/Safari/Firefox 导出书签文件中提取视频链接。

**书签文件路径：**
- Chrome: `~/Library/Application Support/Google/Chrome/Default/Bookmarks`
- Safari: `~/Library/Safari/Bookmarks.plist`
- Firefox: `~/Library/Application Support/Firefox/Profiles/*/places.sqlite`

**支持的域名模式：**
```python
VIDEO_DOMAIN_PATTERNS = [
    r'youtube\.com',
    r'youtu\.be',
    r'bilibili\.com',
    r'b23\.tv',
    r'vimeo\.com',
]
```

### 3. 剪贴板监控（可选）

自动监控剪贴板内容，识别视频链接。

## 本地存储格式

### 存储路径
```
~/.video-downloader/links.json
```

### JSON 数据结构

```json
{
  "version": "1.0",
  "last_updated": "2026-02-16T10:30:00Z",
  "links": [
    {
      "id": "uuid-1",
      "url": "https://www.youtube.com/watch?v=example",
      "source": "manual",
      "added_time": "2026-02-16T10:00:00Z",
      "title": "示例视频标题",
      "status": "pending"
    }
  ]
}
```

## 链接去重逻辑

### URL 规范化

```python
def normalize_url(url: str) -> str:
    from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

    # 移除追踪参数
    TRACKING_PARAMS = {'utm_source', 'utm_medium', 'utm_campaign', 'fbclid'}

    parsed = urlparse(url)
    query_params = parse_qs(parsed.query)

    for param in TRACKING_PARAMS:
        query_params.pop(param, None)

    return urlunparse((
        parsed.scheme,
        parsed.netloc.lower(),
        parsed.path,
        parsed.params,
        urlencode(query_params, doseq=True),
        ''
    ))
```

## 接口设计

```python
from dataclasses import dataclass
from enum import Enum
from typing import Optional

class LinkSource(Enum):
    MANUAL = "manual"
    BOOKMARK = "bookmark"
    HISTORY = "history"
    CLIPBOARD = "clipboard"

class LinkStatus(Enum):
    PENDING = "pending"
    DOWNLOADING = "downloading"
    COMPLETED = "completed"
    FAILED = "failed"

@dataclass
class VideoLink:
    id: str
    url: str
    source: LinkSource
    added_time: str
    title: Optional[str] = None
    status: LinkStatus = LinkStatus.PENDING

class LinkCollector:
    def __init__(self, storage_path: str):
        self.storage_path = storage_path

    def add_link(self, url: str, source: LinkSource) -> Optional[VideoLink]:
        """添加链接，返回新链接或None（如果是重复）"""
        pass

    def get_pending_links(self) -> list[VideoLink]:
        """获取待下载链接"""
        pass
```
